from django.urls import path
from . import views
urlpatterns = [
	path('',views.index),
	path('home',views.home),
	path('sign-up',views.sign_up),
	path('sign-in',views.sign_in),
	path('logout',views.logout),
	path('thought/add',views.add),
	path('thought/delete/<thought_id>',views.delete),
	path('details/<thought_id>',views.details),
	path('like/<thought_id>',views.like),
	path('unlike/<thought_id>',views.unlike),
]
