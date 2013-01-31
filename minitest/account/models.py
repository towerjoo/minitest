from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from datetime import datetime

class AccountManager(models.Manager):
    def verify_and_login(self, acct, answer):
        if acct is None:
            return False
        if acct.answer == answer:
            acct.token = ""
            acct.user.last_login = datetime.utcnow()
            acct.save()
            return True
        return False

    def update_token(self, user):
        try:
            acct = Account.objects.get(user=user)
            # FIXME: token may be conflict if we have a big user table
            # But 30 length random string can avoid the conflict at most time
            # And after login successfully, the token will be reset to blank
            acct.token = get_random_string(30) 
            acct.save()
            return acct.token
        except:
            return None

    def get_acct_from_token(self, token):
        try:
            acct = Account.objects.get(token=token)
            # FIXME: token may be conflict if we have a big user table
            return acct
        except:
            return None
        
        
        

class Account(models.Model):
    user = models.ForeignKey(User, related_name="AccountUser")
    question = models.CharField(max_length=100, blank=False, null=False)
    answer = models.CharField(max_length=100, blank=False, null=False)
    token = models.CharField(max_length=100, blank=True, null=True)

    objects = AccountManager()

    def __unicode__(self):
        return "%s" % self.user

