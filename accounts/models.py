from django.db import models
from django.contrib.auth.models import User
from django.utils import tree

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank = True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	
	# profile model
	profile_pic = models.ImageField(default = "profile1.png" ,null=True, blank = True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		# email = self.user.email
		# print(self.user.email)
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name


# category
class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class Product(models.Model):
	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
	description = models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag)
	# null = True and blank = True

	def __str__(self):
		return self.name

class Order(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
			)
	# following relationships "backwards". For that _set is used.
	customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)

	# Next way could be passing 'related_name'
	# customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL, related_name="customer")

	product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	note = models.CharField(max_length=500, null=True)

	def __str__(self):
		return self.product.name

