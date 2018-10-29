from django.db import models
from django.contrib.auth.models import (
	BaseUserManager, AbstractUser
)

class UserManager(BaseUserManager):
	def create_user(self, username, email, password=None):
		"""
		creates a user with given email and password
		"""
		if not username:
			raise ValueError('user must have a username')

		if not email:
			raise ValueError('user must have a email address')

		user = self.model(
			username=self.normalize_email(username),
			email=self.normalize_email(email),
		)

		user.set_password(password)
		user.save(self._db)
		return user

	def create_staffuser(self, username, email, password):
		"""
		creates a user with staff permissions
		"""
		user = self.create_user(
			username=username,
			email=email,
			password=password
		)
		user.staff = True
		user.save(using=self._db)
		return user

	def create_superuser(self, username, email, password):
		"""
		creates a superuser with email and password
		"""
		user = self.create_user(
			username=username,
			email=email,
			password=password
		)
		user.staff = True
		user.admin = True
		user.save(using=self._db)
		return user


class User(AbstractUser):
	pass
