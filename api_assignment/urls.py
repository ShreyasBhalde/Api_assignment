from django.contrib import admin
from django.urls import path
from invoices import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('invoices/', views.InvoiceList.as_view()),
    path('invoices/<int:pk>/', views.InvoiceDetails.as_view()),
]
