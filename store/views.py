from django.shortcuts import render
from django.contrib import messages
from store import forms
from store import models

# Create your views here.

def render_index(req):
  return render(req, "index.html")

def put_user(req):
  if req.method == "POST":
    form = forms.UserForm(req.POST, req.FILES)

    if form.is_valid():
      ins = form.save()

      messages.success(req, "User was sucessful registered")
      form = forms.UserForm()
    else:
      messages.error(req, "Failed to validate user data")

  else:
      form = forms.UserForm()

  return render(req, "newuser.html", context={ "form": form })

def put_client(req):
  if req.method == "POST":
    form = forms.CustomerForm(req.POST, req.FILES)

    if form.is_valid():
      form.save()
      messages.success(req, "Customer was sucessful registered")

      form = forms.CustomerForm()
    else:
      messages.error(req, "Failed to validate customer data")

  else:
      form = forms.CustomerForm()

  return render(req, "newclient.html", context={ "form": form })

def put_product(req):
  if req.method == "POST":
    form = forms.ProductForm(req.POST, req.FILES)

    if form.is_valid():
      form.save()
      messages.success(req, "Product was sucessful registered")

      form = forms.ProductForm()
    else:
      messages.error(req, "Failed to validate product data")

  else:
      form = forms.ProductForm()

  return render(req, "newproduct.html", context={ "form": form })

def put_sale(req):
  if req.method == "POST":
    form = forms.SaleForm(req.POST, req.FILES)

    if form.is_valid():
      form.save()
      messages.success(req, "Sale was sucessful registered")

      form = forms.SaleForm()
    else:
      messages.error(req, "Failed to validate sale data")

  else:
      form = forms.SaleForm()

  return render(req, "newsale.html", context={ "form": form })


def query_clients(req):
  return render(req, "customers.html", context={ 'customers': models.Customer.objects.filter(gender="F")  })

def query_products(req):
  return render(req, "products.html", context={ 'products': models.Product.objects.all() })

def query_sales(req):
  return render(req, "sales.html", context={ 'sales': models.Sale.objects.all() })
