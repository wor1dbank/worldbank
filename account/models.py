from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
# model  for superadmin
class MyAccountManager(BaseUserManager):

		def create_user(self, first_name, last_name, username, email, password=None):
			if not email:
				raise ValueError('User must have Email Address')
			if not username:
				raise ValueError('User must have Username')
				# normalize email
			user= self.model(
				email = self.normalize_email(email),
				username= username,
				first_name=first_name,
				last_name= last_name,

				)
			user.set_password(password)
			user.save(using=self._db)
			return user

		def create_superuser(self, first_name, last_name, email, username, password):
			user= self.create_user(
				email= self.normalize_email(email),
				username=username,
				password=password,
				first_name=first_name, 
				last_name=last_name,
				)
			# set permissions
			user.is_admin=True
			user.is_staff= True
			user.is_active=True
			user.is_superadmin= True

			user.save(using=self._db)
			return user

# tell it ur using  custom user
# objects = MyAccountManager()
# # settings after wsgi
# AUTH_USER_MODEL=accounts.Account

class Account(AbstractBaseUser):
	first_name= models.CharField(max_length=50)
	last_name= models.CharField(max_length=50)
	username= models.CharField(max_length=50, unique=True)
	email=models.EmailField(max_length=255, unique=True)
	
	

	# required
	date_joined= models.DateTimeField(auto_now_add=True)
	last_login= models.DateTimeField(auto_now_add=True)
	is_admin= models.BooleanField(default=False)
	is_staff= models.BooleanField(default=False)
	is_active= models.BooleanField(default=True)
	is_superadmin= models.BooleanField(default=False)

	# login with email
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS= ['username', 'first_name', 'last_name' ]

	objects = MyAccountManager()

	def __str__(self):
		return self.email
	# return manadatory records

	def has_perm(self, perm, obj=None):
		return self.is_admin
	def has_module_perms(self, add_label):
		return True
	




class Profile(models.Model):
	user = models.OneToOneField(Account, on_delete=models.CASCADE)
	email = models.EmailField(max_length=100, blank=True, null=True)
	first_name = models.CharField(max_length=100, blank=True, null=True)
	last_name = models.CharField(max_length=100, blank=True, null=True)
	phone = models.CharField(max_length=50, blank=True)
	education = models.CharField(max_length=100, blank=True, null=True)
	age = models.CharField(max_length=100, blank=True, null=True)
	gender = models.CharField(max_length=100, blank=True, null=True)
	address = models.CharField(max_length=100, blank=True, null=True)
	city = models.CharField(max_length=100, blank=True, null=True)
	zip = models.CharField(max_length=100, blank=True, null=True)
	country = models.CharField(max_length=100, blank=True, null=True)

	def is_profile_complete(self):
		# Check if all required fields are filled
		required_fields = [
			self.first_name, self.last_name, self.phone,
			self.education, self.age, self.gender,
			self.address, self.city, self.zip, self.country
		]

		return all(field for field in required_fields)

	def __str__(self):
		return self.country


class  Card(models.Model):
	account = models.OneToOneField(Account, on_delete=models.CASCADE)
	owner=models.CharField(max_length=255)
	cvv=models.CharField(max_length=255)
	number=models.CharField(max_length=255)
	month=models.IntegerField(choices=[(i,i) for i  in range(1,13)])
	year=models.IntegerField(choices=[(i,i) for i  in range(2023,2039)])
	bal=models.CharField(max_length=255)


	def __str__(self) -> str:
		return self.owner