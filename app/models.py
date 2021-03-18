from django.db import models
from datetime import datetime, timedelta

class UserManager(models.Manager):
	def basic_validator(self, postData):
		errors = {}
		if not postData['name']:
		    errors["name_empty"] = "Name not empty"
		if len(postData['name']) < 3:
		    errors["name_len"] = "Name should be at least 3 characters"
		if not postData['email']:
		    errors["email_empty"] = "Email not empty"
		if not postData['pwd']:
		    errors["password_empty"] = "Password not empty"
		if len(postData['pwd']) < 8:
		    errors["pwd_len"] = "Password should be at least 8 characters"
		if postData['confirm_pwd'] != postData['pwd']:
			errors["pwd_equal"] = "Not Equal Password"
		return errors

class User(models.Model):
	name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()
	def __repr__(self):
		return f"<User object: {self.name} ({self.id})>"
