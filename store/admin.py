from typing import Any, Callable, Never

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http.request import HttpRequest
from store.models import *

# Register your models here.


@admin.register(User)
class UserAdm(admin.ModelAdmin):
  def get_list_display(self, request: HttpRequest) -> list[str | Callable[[Any], str | bool]] | tuple[str | Callable[[Any], str | bool], ...] | tuple[Never]:
      return [field.name for field in self.model._meta.fields]

@admin.register(Customer)
class CustomerAdm(admin.ModelAdmin):
  def get_list_display(self, request: HttpRequest) -> list[str | Callable[[Any], str | bool]] | tuple[str | Callable[[Any], str | bool], ...] | tuple[Never]:
    return [field.name for field in self.model._meta.fields]

@admin.register(Product)
class ProductAdm(admin.ModelAdmin):
  def get_list_display(self, request: HttpRequest) -> list[str | Callable[[Any], str | bool]] | tuple[str | Callable[[Any], str | bool], ...] | tuple[Never]:
    return [field.name for field in self.model._meta.fields]


@admin.register(Sale)
class SaleAdm(admin.ModelAdmin):
  def get_list_display(self, request: HttpRequest) -> list[str | Callable[[Any], str | bool]] | tuple[str | Callable[[Any], str | bool], ...] | tuple[Never]:
      return [field.name for field in self.model._meta.fields]
