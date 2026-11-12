"""
URL configuration for vitrineoff_exmaple project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import store.views as store_views


urlpatterns = [
  path('admin/', admin.site.urls),
  path('', store_views.render_index),
  path('customers', store_views.query_clients, name='query_clients'),
  path('products', store_views.query_products, name='query_products'),
  path('sales', store_views.query_sales, name='query_sales'),
  path('customer/new', store_views.put_client, name='put_client'),
  path('user/new', store_views.put_user, name='put_user'),
  path('product/new', store_views.put_product, name='put_product'),
  path('sale/new', store_views.put_sale, name='put_sale'),
]
