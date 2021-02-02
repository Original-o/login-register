import datetime
import hashlib
from django.conf import settings
from . import models


def md5(data):
    data = data if isinstance(data, str) else str(data)

    return hashlib.md5(data.encode()).hexdigest()


def createRegisterCode(user):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    registerCode = md5(f'{user.userName}{now}')
    models.Confirm.objects.create(registerCode=registerCode, user=user)

    return registerCode


def sendMail(email, registerCode):
    from django.core.mail import EmailMultiAlternatives
    subject = '来自user.899988.xyz的注册确认邮件'
    content = f'''
            <p>感谢注册<a href="http://{settings.DOMAIN}/confirm?registerCode={registerCode}" target=blank>user.899988.xyz</a>，
            这里是Original的用户中心。
            <p>请点击站点链接完成注册确认！</p>
            <p>此链接有效期为{settings.CONFIRM_DAYS}天！</p>
    '''
    msg = EmailMultiAlternatives(subject, content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(content, 'text/html')
    msg.send()