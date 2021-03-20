from django.db import models
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class UserManager(models.Manager):
	def basic_validator(self, postData):
		errors = {}
		if not postData['first_name']:
		    errors["first_name_empty"] = "First_name not empty"
		if len(postData['first_name']) < 2:
		    errors["first_name_len"] = "First_name should be at least 2 characters"
		if not postData['last_name']:
		    errors["last_name_empty"] = "Last_name not empty"
		if len(postData['last_name']) < 2:
		    errors["last_name_len"] = "Last_name should be at least 2 characters"
		if not postData['email']:
		    errors["email_empty"] = "Email not empty"
		else:
			try:
				validate_email(postData['email'])
			except ValidationError as e:
				errors["email_correct"] = "Email incorrect format"
		if not postData['pwd']:
		    errors["password_empty"] = "Password not empty"
		if len(postData['pwd']) < 8:
		    errors["pwd_len"] = "Password should be at least 8 characters"
		if postData['confirm_pwd'] != postData['pwd']:
			errors["pwd_equal"] = "Not Equal Password"
		return errors

class ThoughtManager(models.Manager):
	def basic_validator(self, postData):
		errors = {}
		if not postData['thought']:
			errors["first_name_empty"] = "Thought not empty"
		elif len(postData['thought']) < 5:
			    errors["thought_len"] = "Thought should be at least 5 characters"
		return errors

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()
	def __repr__(self):
		return f"<User object: {self.first_name} ({self.id})>"

class Thought(models.Model):
	thought = models.CharField(max_length=255)
	user = models.ForeignKey(User, related_name="thoughts", on_delete = models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = ThoughtManager()
	def __repr__(self):
		return f"<Thought object: {self.thought} ({self.id})>"

class Like(models.Model):
	user = models.ForeignKey(User, related_name="likes", on_delete = models.CASCADE)
	thought = models.ForeignKey(Thought, related_name="likes", on_delete = models.SET_NULL, null= True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __repr__(self):
		return f"<Comment object: {self.user} {self.thought} ({self.id})>"
