from django.db import models
from django.db.models import fields
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, request

from django.shortcuts import  render, redirect
from django.urls.base import reverse
from django.views import generic
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages #import messages
from django.contrib.auth import login, authenticate #add this
from django.contrib.auth.forms import AuthenticationForm #add this
from .forms import UserForm

from first.models import Article, Post, Profile
from .forms import CommentForm, ProfilePageForm
from .models import Comment


def about(request):
	posts = Article.objects.all() 
	# all() -все записи; 
	# order_by('-id') -сортировка по id в обратном порядке (или title, content...)
	# order_by('id')[:1] -  вывод только одной записи из таблицы , [:3]- 3 записи из таблицы
	print(posts)
	return render(request,'firstapp/about.html',{'posts':posts})

def create(request):
	error = ''
	coments = Comment.objects.order_by('-id')  # Коментарии на этой же страницы
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('coment')
		else:
			error = 'Форма была неверной'
	form = CommentForm()
	
	context = {
		"form":form,
		"error":error,
		'coments':coments # Коментарии на этой же страницы
	}
	return render(request, "firstapp/create.html", context)


# Коментарии на новой страницы
def coment(request):
	coments = Comment.objects.order_by('-id') 
	print(coments)
	return render(request,'firstapp/coment.html',{'coments':coments}) 

 
def index(request):
    form = '<tr><th><label for="id_name">Name:</label></th><td><input type="text" name="name" required id="id_name" /></td></tr><tr><th><label for="id_age">Age:</label></th><td><input type="number" name="age" required id="id_age" /></td></tr>'
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")     # получение значения поля age
        return HttpResponse("<h2>Привет, {0} возраст: {1}</h2>".format(name,age))
    else:
        userform = UserForm()
        return render(request, "index.html", {"form": userform})



def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="firstapp/register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("homepage")
			else:
				messages.error(request,"Неверное имя пользователя или пароль.")
		else:
			messages.error(request,"Неверное имя пользователя или пароль.")
	form = AuthenticationForm()
	return render(request=request, template_name="firstapp/login.html", context={"login_form":form})



from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm, EditForm
from django.urls  import reverse_lazy

class HomeView(ListView):
	model = Post
	template_name = 'firstapp/post.html'
	#ordering = ['-id']
	ordering = ['-post_date']

class PostHomeView(DetailView):
	model = Post
	template_name = 'firstapp/post_details.html'

	def get_context_data(self, **kwargs):
		context = super(PostHomeView, self).get_context_data(**kwargs)
		stuff = get_object_or_404(Post, id=self.kwargs['pk'])
		total_likes = stuff.total_likes()
		liked = False
		if stuff.likes.filter(id=self.request.user.id).exists():
			liked = True
		context['total_likes']= total_likes
		context['liked']= liked
		return context

class AddPostView(CreateView):
	model = Post
	form_class = PostForm
	template_name = 'firstapp/add_post.html'
	success_url = reverse_lazy('posts')
	#fields = '__all__'
	#fields = ('title','author','body')

class UpdatePostView(UpdateView):
	model = Post
	form_class = EditForm
	template_name = 'firstapp/update_post.html'
	#fields = ['title','body']
	success_url = reverse_lazy('posts')

class DeletePostView(DeleteView):
	model = Post
	template_name = 'firstapp/delete_post.html'
	success_url = reverse_lazy('posts')


from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .forms import EditProfileForm

class UserEditView(generic.UpdateView):
	form_class = EditProfileForm
	template_name = 'firstapp/edit_profile.html'
	success_url = reverse_lazy('posts')

	def get_object(self):
		return self.request.user


from django.contrib.auth.views import PasswordChangeView
from .forms import PasswordChangingForm

class PasswordsChangeView(PasswordChangeView):
	form_class = PasswordChangingForm
	success_url = reverse_lazy('password_success')

def password_success(request):
	return render(request, 'firstapp/password_success.html', {})


def likeView(request, pk):
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	liked = False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		liked = False
	else:
		post.likes.add(request.user)
		liked = True
	return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


class ShowProfilePageView(DetailView):
	model = Profile
	template_name = 'firstapp/user_profile.html'

	def get_context_data(self, *args, **kwargs):
		#users = Profile.objects.all() 
		context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
		
		page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
		context["page_user"] = page_user
		return context


class CreateProfilePageView(CreateView):
	model = Profile
	form_class = ProfilePageForm
	template_name = 'firstapp/create_user_profile.html'
	#fields ='__all__'
	
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)


class EditProfilePageView(UpdateView):
	model = Profile
	template_name = 'firstapp/edit_user_profile.html'
	fields = ['bio','profile_pic','website_url','facebook_url','instagram_url']
	
	success_url = reverse_lazy('posts')

