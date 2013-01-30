from django.db import models
from django.contrib.auth.models import User

class AccountManager(models.Manager):
    def verfiy_secret_question(self):
        pass

class Account(User):
    user = models.ForeignKey(User, related_name="AccountUser")
    question = models.CharField(max_length=100, required=True)
    answer = models.CharField(max_length=100, required=True)

    objects = AccountManager()

    def __unicode__(self):
        return user

