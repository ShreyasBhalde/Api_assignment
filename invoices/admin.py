from django.contrib import admin
from .models import Invoice, InvoiceDetail

class InvoiceDetailInline(admin.TabularInline):
    model = InvoiceDetail
    extra = 1

class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceDetailInline]
    list_display = ('id', 'date', 'customer_name')
    search_fields = ['customer_name']

class InvoiceDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice', 'description', 'quantity', 'unit_price', 'price')
    list_filter = ('invoice__customer_name',)

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceDetail, InvoiceDetailAdmin)
