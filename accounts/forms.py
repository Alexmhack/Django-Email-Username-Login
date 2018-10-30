from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import User

class SignUpForm(UserCreationForm):
	email = forms.EmailField(
		label='',
		max_length=254,
		widget=forms.EmailInput(
			attrs={
				"placeholder": "Email",
				"class": "form-control"
			}
		)
	)

	username = forms.CharField(
		label='',
		max_length=30,
		min_length=5,
		required=True,
		widget=forms.TextInput(
			attrs={
				"placeholder": "Username",
				"class": "form-control"
			}
		)
	)

	password1 = forms.CharField(
		label='',
		max_length=30,
		min_length=8,
		required=True,
		widget=forms.PasswordInput(
			attrs={
				"placeholder": "Password",
				"class": "form-control"
			}
		)
	)

	password2 = forms.CharField(
		label='',
		max_length=30,
		min_length=8,
		required=True,
		widget=forms.PasswordInput(
			attrs={
				"placeholder": "Confirm Password",
				"class": "form-control"
			}
		)
	)
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')


class RegisterForm(forms.ModelForm):
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'email')

	def clean_username(self):
		username = self.cleaned_data.get('username')
		qs = User.objects.filter(username=username)
		if qs.exists():
			raise ValidationError('username already exists')
		return username

	def clean_email(self):
		"""check if the email already exists"""
		email = self.cleaned_data.get('email')
		qs = User.objects.filter(email=email)
		if qs.exists():
			raise ValidationError('email already exists')
		return email

	def clean_password2(self):
		"""check if the both passwords match"""
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError('passwords don\'t match')
		return password2


class AdminUserCreationForm(forms.ModelForm):
	"""form for creating new admin users with all fields and repeated password field"""
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'email')

	def clean_username(self):
		username = self.cleaned_data.get('username')
		qs = User.objects.filter(username=username)
		if qs.exists():
			raise ValidationError('username already exists')
		return username

	def clean_email(self):
		"""check if the email already exists"""
		email = self.cleaned_data.get('email')
		qs = User.objects.filter(email=email)
		if qs.exists():
			raise ValidationError('email already exists')
		return email

	def clean_password2(self):
		"""check if the both passwords match"""
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError('passwords don\'t match')
		return password2

	def save(self, commit=False):
		"""save the password in hashed format"""
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user


class UserAdminChangeForm(forms.ModelForm):
	"""a form for updating users including all the fields but hashed password field"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = ('username', 'email', 'password', 'active', 'admin')

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]
