from django import forms

from .models import Post, Comment, Category

from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm

from django.contrib.auth import get_user_model

from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'image', 'category') #image追加でファイル添付ボタン出る

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text')

class ContentImageForm(forms.Form):
    image = forms.ImageField

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)

#"""パスワード変更フォーム"""
class MyPasswordChangeForm(PasswordChangeForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

 #"""パスワード忘れたときのフォーム"""
class MyPasswordResetForm(PasswordResetForm):
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


#"""パスワード再設定用フォーム(パスワード忘れて再設定)"""
class MySetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'