from django.shortcuts import render, redirect
from . import models, forms, funcs
import datetime
from django.conf import settings


def index(request):
    if not request.session.get('loginState', None):
        return redirect('/login/')

    return render(request, 'login/index.html')


def login(request):
    msg = None

    if request.session.get('loginState', None):
        return redirect('/index/')

    if request.method == 'POST':
        loginForm = forms.UserForm(request.POST)

        if loginForm.is_valid():
            userName = loginForm.cleaned_data.get('userName')
            userPwd = loginForm.cleaned_data.get('userPwd')

            try:
                user = models.User.objects.get(userName=userName)

            except:
                msg = '用户名不存在'

            else:
                userPwd = funcs.md5(userPwd)

                if user.userPwd == userPwd:
                    userState = user.getState()
                    if userState[0]:
                        request.session['loginState'] = True
                        request.session['userId'] = user.id
                        request.session['userName'] = user.userName
                        return redirect('/index/')

                    else:
                        msg = userState[1]
                else:
                    msg = '密码错误'
        else:
            msg = '未输入用户名或密码'
    else:
        loginForm = forms.UserForm()

    return render(request, 'login/login.html', locals())


def register(request):
    msg = None

    if request.session.get('loginState', None):
        return redirect('/index/')

    if request.method == 'POST':
        registerForm = forms.RegisterForm(request.POST)

        if registerForm.is_valid():
            userName = registerForm.cleaned_data.get('userName')
            userPwd = registerForm.cleaned_data.get('userPwd')
            userPwdAgain = registerForm.cleaned_data.get('userPwdAgain')

            email = registerForm.cleaned_data.get('email')
            sex = registerForm.cleaned_data.get('sex')

            if userPwdAgain == userPwd:
                sameUserName = models.User.objects.filter(userName=userName)

                if not sameUserName:
                    sameUserEmail = models.User.objects.filter(email=email)

                    if not sameUserEmail:
                        newUser = models.User()

                        newUser.userName = userName
                        newUser.userPwd = funcs.md5(userPwd)
                        newUser.email = email
                        newUser.sex = sex
                        newUser.save()

                        # 注册邮件相关
                        registerCode = funcs.createRegisterCode(newUser)
                        funcs.sendMail(email, registerCode)
                        msg = '请前往邮箱进行确认！'

                        return render(request, 'login/confirm.html', locals())

                    else:
                        msg = '邮箱已被注册'
                else:
                    msg = '用户名已被注册'
            else:
                msg = '两次输入的密码不一致'
        else:
            msg = '内容输入不完整'
    else:
        registerForm = forms.RegisterForm()

    return render(request, 'login/register.html', locals())


def logout(request):
    if request.session.get('loginState', None):
        request.session.flush()

    return redirect('/login/')


def userConfirm(request):
    registerCode = request.GET.get('registerCode', None)
    msg = None

    try:
        confirm = models.Confirm.objects.get(registerCode=registerCode)

    except:
        msg = '无效的请求'

    else:
        confirmTime = confirm.confirmTime
        now = datetime.datetime.now()

        if now > confirmTime + datetime.timedelta(settings.CONFIRM_DAYS):
            msg = '您的注册邮件已超过有效期，请重新注册！'
            # 注册确认过期，删除这个未成功注册的用户
            confirm.user.delete()

        else:
            msg = '注册确认成功，现在此账号可以正常使用了。'
            # 注册确认验证通过，将用户状态置为正常，删除注册码
            confirm.delete()
            confirm.user.userState = 0
            confirm.user.tipInfo = '正常'
            confirm.user.save()

    return render(request, 'login/confirm.html', locals())