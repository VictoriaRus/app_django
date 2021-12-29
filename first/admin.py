from django import forms
from django.contrib import admin
from .models import Article
from .models import Comment
from .models import Post
from .models import Profile

from ckeditor.widgets import CKEditorWidget


class ArticleAdminForm(forms.ModelForm):
    content = forms.CharField(label="Описание", widget=CKEditorWidget())
    class Meta:
        model = Article
        fields = '__all__'

class ArticlAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    form = ArticleAdminForm

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')


admin.site.register(Article, ArticlAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Post)
admin.site.register(Profile)