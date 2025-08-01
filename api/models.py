from django.db import models
import uuid

    
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=40, unique=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_barcode = models.CharField(max_length=50, null=True, blank=True)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)  

    def __str__(self):
        return self.product_name
    
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=40, unique=True)
    customer_address = models.CharField(max_length=100, null=True, blank=True)
    customer_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.customer_name
    

class Transactions(models.Model):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through='Order', related_name='orders')


    def __str__(self):
        return f'Order {self.transaction_id} by {self.customer}'
    
class Order(models.Model):
    transaction = models.ForeignKey(Transactions, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.product.product_price * self.quantity
    




