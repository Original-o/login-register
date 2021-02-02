from django.db import models
from django.conf import settings


class User(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )
    # 用户名，用户名不能重复
    userName = models.CharField(max_length=10, unique=True)
    # 密码
    userPwd = models.CharField(max_length=32)
    # 注册时间
    registerTime = models.DateTimeField(auto_now_add=True)
    # 邮箱
    email = models.EmailField(unique=True)
    # 性别
    sex = models.CharField(max_length=10, choices=gender, default='男')
    # 用户状态
    userState = models.IntegerField(default=-1)
    # 异常提示信息
    tipInfo = models.CharField(max_length=255, default='未激活')

    def getState(self):
        result = [
            True if self.userState >= 0 else False, settings.USERSTATE[self.userState]
        ]

        return result

    def __str__(self):
        return self.userName

    class Meta:
        ordering = ['-registerTime']
        verbose_name = '用户名'
        verbose_name_plural = '用户'


class Confirm(models.Model):
    registerCode = models.CharField(max_length=32)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    confirmTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.userName}: {self.registerCode}'

    class Meta:
        ordering = ['-confirmTime']
        verbose_name = '注册码'
        verbose_name_plural = '注册码'