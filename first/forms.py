from django import forms
from django.contrib.auth import models
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
#from django.contrib.auth.views import PasswordChangeView
#from django.db.models import fields

from .models import Comment
from django.forms import ModelForm, TextInput, 	Textarea, FileInput, Select, widgets

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ["title","content"]
		widgets = {
			"title":TextInput(attrs={
				'class':'form-control',
				'placeholder':'Введите тему'
			}),
			"content":Textarea(attrs={
				'class':'form-control',
				'placeholder':'Введите ваш коментарий'
			}),
		}



class UserForm(forms.Form):
    name = forms.CharField(label="Имя")
    age = forms.IntegerField(label="Возраст")

# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

from .models import Post

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ["title", "title_tag", "author", "body"]

		widgets = {
			"title":forms.TextInput(attrs={
				'class':'form-control',
				'placeholder':'Введите тему',
			}),
			"title_tag":forms.TextInput(attrs={
				'class':'form-control',
			}),
			"author":forms.TextInput(attrs={
				'class':'form-control',
				'value':'',
				'id':'elder',
				'type':'hidden',
			}),
			"body":forms.Textarea(attrs={
				'class':'form-control',
			}),
		}

class EditForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ("title", "title_tag", "body")

		widgets = {
			"title":forms.TextInput(attrs={
				'class':'form-control',
				'placeholder':'Введите тему'
			}),
			"title_tag":forms.TextInput(attrs={
				'class':'form-control',
			}),
			"body":forms.Textarea(attrs={
				'class':'form-control',
			}),
		}

from django import forms

class EditProfileForm(UserChangeForm):
		email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
		first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
		last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
		username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
		last_login = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
		#is_superuser = forms.CharField(widget=forms.CheckboxInput(attrs={'class':'form-check'}))
		#is_staff = forms.CharField(widget=forms.CheckboxInput(attrs={'class':'form-check'}))
		#is_active = forms.CharField(widget=forms.CheckboxInput(attrs={'class':'form-check'}))
		#data_joined = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
	
		class Meta:
			model = User
			fields = ('username','first_name', 'last_name', 'email','password','last_login')


class PasswordChangingForm(PasswordChangeForm):
	old_password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
	new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
	new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))

	class Meta:
			model = User
			fields = ('old_password','new_password1','new_password2')


from .models import Profile
class ProfilePageForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('bio','profile_pic','website_url','facebook_url','instagram_url')
		widgets = {
			"bio":forms.Textarea(attrs={
				'class':'form-control',
				'placeholder':'Кратко о себе'
			}),
			"profile_pic":forms.FileInput(attrs={
				'class':'form-control',
			}),
			"website_url":forms.TextInput(attrs={
				'class':'form-control',
			}),
			"instagram_url":forms.TextInput(attrs={
				'class':'form-control',
			}),
			"facebook_url":forms.TextInput(attrs={
				'class':'form-control',
			}),
		}

