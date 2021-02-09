from django.db import models


class UserModel(models.Model):
    login = models.CharField('login', max_length=50)
    password = models.CharField('password', max_length=50)


class AdminModel(models.Model):
    login = models.CharField('login', max_length=50)
    password = models.CharField('password', max_length=50)