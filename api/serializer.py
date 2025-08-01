from .models import *
from rest_framework import serializers

    
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_id', 'customer_name', 'customer_address', 'customer_number']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','category_name']

class ProductSerializer(serializers.ModelSerializer):
    product_category = serializers.SlugRelatedField(
                queryset = Category.objects.all(),
                slug_field = 'category_name'
    )
    product_barcode = serializers.CharField(max_length=13, required=False) 
    class Meta:
        model = Product
        fields = ['product_id', 
                  'product_name', 
                  'product_price', 
                  'product_category', 
                  'product_barcode']

class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name')
    product_price = serializers.DecimalField(max_digits=10, 
                                             decimal_places=2,
                                             source='product.product_price')
    class Meta:
        model = Order
        fields = ['id','product_name', 'product_price', 'quantity', 'item_subtotal']
        
class OrderWriteSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        queryset = Product.objects.all(),
        slug_field='product_name'
    )
    class Meta:
        model = Order
        fields = ['product', 'quantity']

class TransactionSerializer(serializers.ModelSerializer):
    transaction_id = serializers.UUIDField(read_only=True) 

    customer = serializers.SlugRelatedField(
        queryset=Customer.objects.all(),
        slug_field='customer_name'
    )
    
    order_items = OrderWriteSerializer(many=True, write_only=True)
    order_items_read = OrderSerializer(many=True, read_only=True, source='order_items')

    total_price = serializers.SerializerMethodField(method_name='total')

    def total(self, obj):
        return sum(order.item_subtotal for order in obj.order_items.all())

    class Meta:
        model = Transactions
        fields = ['transaction_id', 'customer', 'create_at', 'order_items', 'order_items_read', 'total_price']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        transaction = Transactions.objects.create(**validated_data)
        for item_data in order_items_data:
            Order.objects.create(transaction=transaction, **item_data)
        return transaction

        
# Serializer below if for Charts_display in dashboard
class TopCustomerSerializer(serializers.Serializer):
    transaction__customer__customer_name = serializers.CharField()
    total_spent = serializers.DecimalField(max_digits=10, decimal_places=2)

    def to_representation(self, instance):
        return {
            "customer": instance["transaction__customer__customer_name"],
            "total_spent": instance["total_spent"]
        }

class MostBoughtProductSerializer(serializers.Serializer):
    product__product_name = serializers.CharField()
    total_quantity = serializers.IntegerField()

    def to_representation(self, instance):
        return {
            "product": instance["product__product_name"],
            "total_quantity": instance["total_quantity"]
        }
              