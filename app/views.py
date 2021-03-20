from django.shortcuts import render, HttpResponse, redirect
from app.models import *
from django.db.models import Count
from django.contrib import messages
import bcrypt

def index(request):
	content = {
		'title' : 'Welcome'
	}
	if 'id' in request.session:
		return redirect('/home')

	return render(request,'app/index.html',content)

def home(request):
	content = {
		'title' : 'Home'
	}
	if 'id' in request.session:
		user = User.objects.filter(id = request.session['id'])[0]
		name = user.first_name+" "+user.last_name
		content.update({'name': name })
		# content.update({'thoughts': Thought.objects.all().aggregate('count_likes'=).order_by('-created_at') })
		content.update({'thoughts': Thought.objects.annotate(count=Count('likes')).order_by('-count') })

		return render(request,'app/home.html',content)
	else:
		return redirect('/')

def sign_up(request):
	if 'id' in request.session:
		return redirect('/home')
	if request.method == "POST":
		errors = User.objects.basic_validator(request.POST)
		if len(errors) > 0:
			for key, value in errors.items():
				messages.error(request, value)
			return redirect('/')
		else:
			this_user = User.objects.create(
				first_name = request.POST["first_name"],
				last_name = request.POST["last_name"],
				email = request.POST["email"],
				password = bcrypt.hashpw(request.POST["pwd"].encode(), bcrypt.gensalt()).decode()
				)
			request.session['id'] = this_user.id
			return redirect('/home')
	else :
		return redirect('/')

def sign_in(request):
	if 'id' in request.session:
		return redirect('/home')
	if  request.method == "POST":
		if not request.POST['email']:
			messages.error(request, 'Email not empty')
			return redirect('/')
		else:
			try:
				validate_email(request.POST['email'])
			except ValidationError as e:
				messages.error(request, 'Email incorrect format')
				return redirect('/')

		this_user = User.objects.filter(email=request.POST['email'])
		if not this_user:
			messages.error(request, 'Incorrect email or password')
			return redirect('/')
		if this_user:
			this_user = this_user[0]
			if bcrypt.checkpw(request.POST['pwd'].encode(), this_user.password.encode()):
				request.session['id'] = this_user.id
				return redirect('/home')
			messages.error(request, 'Incorrect email or password')
			return redirect('/')
	else :
		return redirect('/')

def logout(request):
	request.session.delete()
	return redirect('/')

def details(request,thought_id):
	content = {
		'title' : 'Details'
	}
	if 'id' in request.session:
		thought = Thought.objects.get(id = thought_id)
		content.update({'thought': thought })
		content.update({'users': thought.likes.exclude(user = thought.user.id) })
		liked = thought.likes.filter(
			thought = Thought.objects.get(id = thought_id),
			user = User.objects.get(id = request.session['id'])
			)
		if len(liked) > 0:
			content.update({'liked': False })
		else :
			content.update({'liked': True })

		liked_by_user = thought.likes.filter(
			thought = Thought.objects.get(id = thought_id),
			user = User.objects.get(id = thought.user.id)
			)
		if len(liked_by_user) > 0:
			content.update({'owner': User.objects.get(id = thought.user.id) })
		else :
			content.update({'owner': [] })
		return render(request,'app/details.html',content)
	else:
		return redirect('/')

def add(request):
	if 'id' in request.session:
		if request.method == "POST":
			errors = Thought.objects.basic_validator(request.POST)
			if len(errors) > 0:
				for key, value in errors.items():
					messages.error(request, value)
				return redirect('/home')
			else:
				this_thought = Thought.objects.create(
					thought = request.POST["thought"],
					user = User.objects.filter(id = request.session['id'])[0],
					)
				return redirect('/home')
	else:
		return redirect('/')

def delete(request,thought_id):
	if 'id' in request.session:
		thought = Thought.objects.filter(id = thought_id, user = User.objects.get(id = request.session['id']))
		thought.delete()
		return redirect('/home')
	else:
		return redirect('/')

def like(request,thought_id):
	if 'id' in request.session:
		like = Like.objects.filter(
			thought = Thought.objects.get(id = thought_id),
			user = User.objects.get(id = request.session['id'])
			)
		if len(like) < 1:
			Like.objects.create(
				thought = Thought.objects.get(id = thought_id,),
				user = User.objects.get(id = request.session['id'])
			)
		return redirect(f'/details/{thought_id}')
	else:
		return redirect('/')

def unlike(request,thought_id):
	if 'id' in request.session:
		like = Like.objects.filter(
			thought = Thought.objects.get(id = thought_id),
			user = User.objects.get(id = request.session['id'])
			)
		like.delete()
		return redirect(f'/details/{thought_id}')
	else:
		return redirect('/')
