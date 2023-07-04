from django.db import models, transaction
from django.core.validators import MaxValueValidator, MinValueValidator
# from ..store.models import Address, OrderItem
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=20)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    guid = models.CharField(primary_key= True, max_length=40)
    image = models.ImageField(null=True, upload_to="media")
    quantity = models.DecimalField(decimal_places=2, max_digits=10)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

class UserManager(BaseUserManager):
# standard for creating all types of users
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Please provide Email")
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using = self.db)
                return user
        except:
            raise
    # create normal user method
    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    # create superuser
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password=password, **extra_fields)

# Abstract class implementing feature model for admin compliant permisions
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=40, unique=True)
    password = models.CharField(max_length=20)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()
    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self
class Order(models.Model):
    order_total = models.DecimalField(decimal_places=2, max_digits=10)
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True)
    paid = models.BooleanField(default=False)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete= models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete= models.CASCADE, null=True)
    item_number = models.IntegerField()
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    paid = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        price = self.product.price*self.item_number
        self.cost = price
        super(OrderItem, self).save(*args, **kwargs)

class Address(models.Model):
    address = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    resident = models.OneToOneField(User, on_delete=models.CASCADE, default= None)

# from the perspective of a product type bought
class Categories(models.Model):
    category_name = models.CharField(max_length=20)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)


