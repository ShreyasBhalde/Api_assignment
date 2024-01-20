# views.py
from rest_framework import viewsets
from .models import Invoice
from .myserializer import InvoiceSerializer , InvoiceDetailSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response    

class InvoiceDetails(APIView):    
    def get(self, request, pk):
        try:
            invoice = Invoice.objects.get(pk=pk)
            serializer = InvoiceSerializer(invoice)
            return Response(serializer.data)
        except Invoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            invoice = Invoice.objects.get(pk=pk)
            invoice.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Invoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            invoice = Invoice.objects.get(pk=pk)
            serializer = InvoiceSerializer(invoice, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        except Invoice.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            invoice = serializer.save()

            # If you have details data in the request, create associated details
            details_data = request.data.get('details', [])
            if details_data:
                for detail_data in details_data:
                    detail_data['invoice'] = invoice.id  # Assign the invoice ID to each detail

                details_serializer = InvoiceDetailSerializer(data=details_data, many=True)
                if details_serializer.is_valid():
                    details_serializer.save()
                else:
                    # If details validation fails, delete the created invoice
                    invoice.delete()
                    return Response(details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceList(APIView):      
    def get(self, request):
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)

    def post(self, request):        
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

