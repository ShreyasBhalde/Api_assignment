from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Invoice, InvoiceDetail
from .myserializer import InvoiceSerializer, InvoiceDetailSerializer
from datetime import datetime

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def create_invoice(self, data):
        response = self.client.post('/invoices/', data, format='json')
        return response

    def create_invoice_with_details(self, data):
        response = self.client.post('/invoices/', data, format='json')
        return response

    def test_create_invoice(self):
        data = {
            "date": "2024-01-20",
            "customer_name": "test_customer"
        }
        response = self.create_invoice(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)

    def test_create_invoice_with_invalid_data(self):
        data = {
            # Invalid data without required fields
        }
        response = self.create_invoice(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_invoice_details(self):
        invoice = Invoice.objects.create(date="2024-01-20", customer_name="test_customer")
        response = self.client.get(f'/invoices/{invoice.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_nonexistent_invoice_details(self):
        response = self.client.get('/invoices/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_invoice(self):
        invoice = Invoice.objects.create(date="2024-01-20", customer_name="test_customer")
        data = {"date": "2024-01-21", "customer_name": "updated_customer"}
        response = self.client.put(f'/invoices/{invoice.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_invoice = Invoice.objects.get(id=invoice.id)
        # Convert date to string for comparison
        updated_date_str = datetime.strftime(updated_invoice.date, '%Y-%m-%d')
        self.assertEqual(updated_date_str, "2024-01-21")
        self.assertEqual(updated_invoice.customer_name, "updated_customer")

    def test_delete_invoice(self):
        invoice = Invoice.objects.create(date="2024-01-20", customer_name="test_customer")
        response = self.client.delete(f'/invoices/{invoice.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invoice.objects.count(), 0)

def test_create_invoice_with_details(self):
    data = {
        "date": "2024-01-20",
        "customer_name": "test_customer",
        "details": [
            {"description": "Product 1", "quantity": 2, "unit_price": 10.0, "price": 20.0},
            {"description": "Product 2", "quantity": 3, "unit_price": 15.0, "price": 45.0}
        ]
    }
    response = self.create_invoice_with_details(data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Invoice.objects.count(), 1)

    # Check the actual number of InvoiceDetail objects created
    created_invoice_details_count = InvoiceDetail.objects.count()
    self.assertEqual(created_invoice_details_count, 2, f"Expected 2 InvoiceDetail objects, but found {created_invoice_details_count}")


    def test_create_invoice_with_invalid_details(self):
        data = {
            "date": "2024-01-20",
            "customer_name": "test_customer",
            "details": [
                # Invalid details without required fields
            ]
        }
        response = self.create_invoice_with_details(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
