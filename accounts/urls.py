from django.urls import path, include

from .views import signup_view, dashboard_view, home_view

app_name = 'accounts'

urlpatterns = [
	path('', home_view, name='home'),
	path('dashboard/', dashboard_view, name='dashboard'),
	path('register/', signup_view, name='register'),
]
