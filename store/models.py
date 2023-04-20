from django.db import models

# Create your models here.
class Address(models.Model):
    address = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)

class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    address = models.OneToOneField(Address)

class Product(models.Model):
    product_name = models.CharField(max_length=20)
    price = models.DecimalField()
    guid = models.CharField(primary_key=True, max_length=40)
    quantity = models.DecimalField()
    rating = models.IntegerField(validators=[min(1), max(5)])

class Categories(models.Model):
    category_name = models.CharField(20)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)

# from the perspective of a product type bought
class OrderItem(models.Model):
    product = models.ForeignKey(Product)
    item_number = models.IntegerField()
    cost = models.DecimalField()
    buyer = models.OneToOneField(User)
    def save(self, *args, **kwargs):
        price = self.product.price*self.item_number
        self.cost = price
        super(OrderItem, self).save(*args, **kwargs)

class Order(models.Model):
    items = models.ForeignKey(OrderItem, on_delete= models.CASCADE)
