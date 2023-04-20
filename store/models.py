from django.db import models

# Create your models here.
class Address(models.Model):
    address = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)

class Product(models.Model):
    product_name = models.CharField(max_length=20)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    guid = models.CharField(primary_key=True, max_length=40)
    quantity = models.DecimalField(decimal_places=2, max_digits=10)
    rating = models.IntegerField()

# from the perspective of a product type bought
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    item_number = models.IntegerField()
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    def save(self, *args, **kwargs):
        price = self.product.price*self.item_number
        self.cost = price
        super(OrderItem, self).save(*args, **kwargs)


class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    address = models.OneToOneField(Address, on_delete= models.CASCADE)
    order_items = models.ForeignKey(OrderItem, on_delete= models.CASCADE)

class Categories(models.Model):
    category_name = models.CharField(max_length=20)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)

class Order(models.Model):
    items = models.ForeignKey(OrderItem, on_delete= models.CASCADE)
    order_total = models.DecimalField(decimal_places=2, max_digits=10)
    def save(self, *args, **kwargs):
        for item in self.items:
            self.order_total += item.cost
        super(Order, self).save(*args, **kwargs)

