from django.urls import path
from . import views
urlpatterns = [
	path('',views.index),
	path('sign-up',views.sign_up),
	path('sign-in',views.sign_in),
	path('logout',views.logout),
	path('other',views.logout),
]
