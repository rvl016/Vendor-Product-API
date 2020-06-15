"""VendorProduct URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include

from django.urls import path

from apps.vendors.views import VendorsList, VendorDetails
from apps.products.views import AllProductsList,  VendorProductsList
from apps.products.views import ProductDetails


urlpatterns = [
    path( 'api/vendors/', VendorsList.as_view(), name = 'vendors'),
    path( 'api/vendors/<int:primary_key>/', VendorDetails.as_view(), 
        name = 'vendor-details'),

    path( 'api/vendors/<int:vendor_id>/products', 
        VendorProductsList.as_view(), name = 'vendor-products'),

    path( 'api/products', AllProductsList.as_view(), name = 'all-products'),
    path( 'api/products/<int:primary_key>/', 
        ProductDetails.as_view(), name = 'product-details')
]
