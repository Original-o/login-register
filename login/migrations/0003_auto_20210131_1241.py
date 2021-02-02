# Generated by Django 3.1.5 on 2021-01-31 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20210129_1121'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-registerTime'], 'verbose_name': '用户名', 'verbose_name_plural': '用户'},
        ),
        migrations.CreateModel(
            name='Confirm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32)),
                ('confirmTime', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='login.user')),
            ],
            options={
                'verbose_name': '注册码',
                'verbose_name_plural': '注册码',
                'ordering': ['-confirmTime'],
            },
        ),
    ]
