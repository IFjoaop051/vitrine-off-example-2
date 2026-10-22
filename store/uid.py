"""RFC 9562 UUIDv7 generation using only the Python standard library.

Public API:
    uuid7()                         -> uuid.UUID
    UUID7Generator().new()          -> uuid.UUID

The generator is thread-safe and monotonic within a generator instance: UUID
integer values increase in generation order, including when multiple values are
generated in one millisecond or the wall clock moves backwards. On platforms
supporting os.register_at_fork, generator state is reset in a child process.

Requires Python 3.7+.
"""
from __future__ import annotations

import os
import secrets
import threading
import time
import uuid
import weakref

_TIMESTAMP_BITS = 48
_TIMESTAMP_MAX = (1 << _TIMESTAMP_BITS) - 1
_TAIL_BITS = 74  # rand_a (12 bits) + rand_b (62 bits)
_TAIL_MAX = (1 << _TAIL_BITS) - 1
_RAND_B_BITS = 62
_RAND_B_MASK = (1 << _RAND_B_BITS) - 1
_VERSION = 7
_VARIANT_RFC = 0b10
_INCREMENT_BITS = 32

# Track live generators so their locks/state can be safely reinitialized after
# fork. Weak references avoid keeping short-lived generator instances alive.
_GENERATORS = weakref.WeakSet()


class UUID7Generator:
    """Thread-safe RFC 9562 UUIDv7 generator.

    Use one long-lived instance per process for monotonic generation order:

        generator = UUID7Generator()
        value = generator.new()

    Separate instances/processes remain unique with overwhelming probability,
    but do not share a single global monotonic ordering.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._last_timestamp_ms = -1
        self._tail = 0
        _GENERATORS.add(self)

    def new(self) -> uuid.UUID:
        """Return a UUIDv7.

        The 48-bit timestamp contains Unix milliseconds. The remaining 74 bits
        are a randomly seeded tail; while the timestamp is unchanged or moves
        backward, the tail advances by a positive cryptographically random
        increment. If that tail overflows, the logical timestamp advances by
        one millisecond and the tail is reseeded rather than wrapping.
        """
        with self._lock:
            now_ms = time.time_ns() // 1_000_000
            if not 0 <= now_ms <= _TIMESTAMP_MAX:
                raise OverflowError(
                    "Current Unix timestamp does not fit UUIDv7's 48-bit field"
                )

            if now_ms > self._last_timestamp_ms:
                # Acquire randomness before mutating state, so a random-source
                # failure leaves the generator's prior state intact.
                next_tail = secrets.randbits(_TAIL_BITS)
                self._last_timestamp_ms = now_ms
                self._tail = next_tail
            else:
                # A positive random increment gives monotonicity while avoiding
                # the predictability of a fixed +1 counter increment.
                increment = secrets.randbits(_INCREMENT_BITS) + 1
                next_tail = self._tail + increment

                if next_tail <= _TAIL_MAX:
                    self._tail = next_tail
                else:
                    # RFC 9562 says not to knowingly duplicate on counter
                    # rollover. Move logical time forward and reseed instead.
                    if self._last_timestamp_ms >= _TIMESTAMP_MAX:
                        raise OverflowError("UUIDv7 timestamp field is exhausted")
                    next_tail = secrets.randbits(_TAIL_BITS)
                    self._last_timestamp_ms += 1
                    self._tail = next_tail

            timestamp_ms = self._last_timestamp_ms
            tail = self._tail

            rand_a = tail >> _RAND_B_BITS
            rand_b = tail & _RAND_B_MASK
            value = (
                (timestamp_ms << 80)
                | (_VERSION << 76)
                | (rand_a << 64)
                | (_VARIANT_RFC << 62)
                | rand_b
            )
            # Do not pass version= here: UUID(int=...) must preserve the bits
            # explicitly composed above.
            return uuid.UUID(int=value)

    def _reset_after_fork(self) -> None:
        """Reset inherited synchronization/state in a forked child process."""
        self._lock = threading.Lock()
        self._last_timestamp_ms = -1
        self._tail = 0


def _reset_generators_after_fork() -> None:
    # In the child process, do not acquire an inherited lock: it may have been
    # held by a thread that did not survive fork().
    for generator in tuple(_GENERATORS):
        generator._reset_after_fork()


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_reset_generators_after_fork) # pyright: ignore[reportAttributeAccessIssue]

_DEFAULT_GENERATOR = UUID7Generator()


def uuid7() -> uuid.UUID:
    """Return a UUIDv7 from a process-wide, thread-safe generator."""
    return _DEFAULT_GENERATOR.new()


__all__ = ["UUID7Generator", "uuid7"]
