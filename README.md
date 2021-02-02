## 这是一个用户登录和注册的学习项目
## 这是一个可重用的APP
## 这个项目参照 https://www.liujiangblog.com/course/django/102 教程开发，但部分逻辑有改动

## 简单的使用方法
创建虚拟环境
使用pip安装第三方依赖
修改settings.example.py文件为settings.py
运行migrate命令，创建数据库和数据表
运行python manage.py runserver启动服务器


路由设置：

```
from django.contrib import admin
from django.urls import path, include
from login import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index/', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('confirm/', views.user_confirm),
    path('captcha/', include('captcha.urls'))   # 增加这一行
]
```
