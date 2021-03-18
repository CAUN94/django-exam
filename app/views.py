from django.shortcuts import render, HttpResponse, redirect
from app.models import *
from django.contrib import messages
import bcrypt

def index(request):
	content = {
		'title' : 'Index'
	}
	if 'id' in request.session:

		content.update({'name':User.objects.filter(id = request.session['id'])[0].name})

	return render(request,'app/index.html',content)

def sign_up(request):
	if 'id' in request.session:
		return redirect('/')
	content = {
		'title' : 'Sign Up'
	}
	if request.method == "POST":
		errors = User.objects.basic_validator(request.POST)
		if len(errors) > 0:
			for key, value in errors.items():
				messages.error(request, value)
			return redirect('/sign-up')
		else:
			this_user = User.objects.create(
				name = request.POST["name"],
				email = request.POST["email"],
				password = bcrypt.hashpw(request.POST["pwd"].encode(), bcrypt.gensalt()).decode()
				)
			request.session['id'] = this_user.id
			return redirect('/')
	else :
		return render(request,'app/sign-up.html',content)

def sign_in(request):
	if 'id' in request.session:
		return redirect('/')
	content = {
		'title' : 'Sign In'
	}
	if  request.method == "POST":
		if not request.POST['email']:
			messages.error(request, 'No Mail')
			return redirect('/sign-in')
		this_user = User.objects.filter(email=request.POST['email'])
		if this_user:
			this_user = this_user[0]
			if bcrypt.checkpw(request.POST['pwd'].encode(), this_user.password.encode()):
				request.session['id'] = this_user.id
				return redirect('/')
			messages.error(request, 'Incorrect email or password')
			return redirect('/sign-in')

	else :
		return render(request,'app/sign-in.html',content)

def logout(request):
	request.session.delete()
	return redirect('/')
