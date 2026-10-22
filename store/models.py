from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
  USER_ROLES = [
    ('CUSTOMER', 'Cliente'),
    ('MANAGER', 'Gerente'),
  ]

  user_role = models.CharField(
    max_length=12,
    choices=USER_ROLES,
    null=False,
    blank=False,
    default="CUSTOMER"
  )


class Client(models.Model):
  GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
  ]

  user = models.OneToOneField(User, on_delete=models.CASCADE)

  full_name = models.CharField(max_length=120, null=False, blank=False)
  gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=False, blank=False)
  phone_no = models.TextField(null=False, blank=False)
  notes = models.TextField(null=True, blank=False)


class Sale(models.Model):
  client = models.ForeignKey(Client, on_delete=models.RESTRICT)

  seq_id = models.BigAutoField(primary_key=True) # Sequential Identifier for DA
  crypt_id = models.UUIDField(editable=False, unique=True) # Shareable ID (avoids IDOR attacks)
  when_sold = models.DateTimeField(null=False)
  payment_way = models.CharField(max_length=16)
  total_discount = models.DecimalField(decimal_places=3, max_digits=7)


class Product(models.Model):
  PRODUCT_CATEGORIES = [
    ('SHIRTS', 'Shirts & T-Shirts'),
    ('PANTS', 'Pants & Chinos'),
    ('JEANS', 'Jeans'),
    ('SKIRTS', 'Skirts'),
  ]

  product_id = models.UUIDField(primary_key=True, editable=False)
  available_items = models.PositiveSmallIntegerField()
  price = models.DecimalField(decimal_places=3, max_digits=7)
  product_name = models.TextField(max_length=120)
  image_url = models.ImageField(upload_to="products/")
  product_category = models.CharField(choices=PRODUCT_CATEGORIES, blank=False, null=False, max_length=8)


class SaleItem(models.Model):
  sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.RESTRICT)

  quantity = models.PositiveSmallIntegerField()
  unity_price = models.DecimalField(decimal_places=3, max_digits=7)
