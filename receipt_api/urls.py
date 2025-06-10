
"""
URL patterns for the receipt_api app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('scrape-receipt/', views.scrape_receipt, name='scrape_receipt'),
]