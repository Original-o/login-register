from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    userName = forms.CharField(label='用户名', max_length=10, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '用户名',
        'autofocus': '',
        'required': ''
    }))
    userPwd = forms.CharField(label='密码', max_length=16, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '密码',
        'required': ''
    }))
    captcha = CaptchaField(label='验证码')


class RegisterForm(forms.Form):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )
    userName = forms.CharField(label='用户名', max_length=10, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    userPwd = forms.CharField(label='密码', max_length=16, widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    userPwdAgain = forms.CharField(label='再次输入密码', max_length=16, widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    sex = forms.ChoiceField(label='性别', choices=gender)
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    captcha = CaptchaField(label='验证码')