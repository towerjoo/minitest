"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from account.models import Account
from django.core.urlresolvers import reverse


class ModelTest(TestCase):
    fixtures = ["user.json", "acct.json"]
    def setUp(self):
        self.users = User.objects.all()

    def test_users(self):
        self.assertEqual(len(self.users), 2)

    def test_account_succ(self):
        user = User.objects.get(pk=2)
        self.assertNotEqual(user, None)

        token = Account.objects.update_token(user)
        self.assertNotEqual(token, None)

        acct = Account.objects.get_acct_from_token(token)
        self.assertEqual(acct.user, user)

        can_login = Account.objects.verify_and_login(acct, "Zhu")
        self.assertTrue(can_login)

        
    def test_account_fail(self):
        user = User.objects.get(pk=1)
        self.assertNotEqual(user, None)

        token = Account.objects.update_token(user)
        self.assertEqual(token, None)

        acct = Account.objects.get_acct_from_token(token)
        self.assertEqual(acct, None)

        can_login = Account.objects.verify_and_login(acct, "Zhu")
        self.assertFalse(can_login)

class ViewTest(TestCase):
    fixtures = ["user.json", "acct.json"]
    def setUp(self):
        self.users = User.objects.all()
        self.home_url = reverse("home")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.secret_url = reverse("secret")

        self.username = "tower"
        self.password = "zhutao"
        self.answer = "Zhu"

    def test_login_succ(self):
        # get
        resp = self.client.get(self.login_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "account/login.html")

        # post
        resp = self.client.post(self.login_url, data={"username" : self.username, "password" : self.password})
        self.assertEqual(resp.status_code, 302)
        acct = Account.objects.get(pk=1)
        self.assertRedirects(resp, self.secret_url+"?token=" + acct.token)

    def test_login_fail(self):
        # post
        resp = self.client.post(self.login_url, data={"username" : self.username, "password" : self.password + "error"})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "account/login.html")

    def test_secret_succ(self):
        # without auth
        resp = self.client.get(self.secret_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.login_url+"?e=You%20need%20a%20token%20to%20continue,%20login%20again")

        # with auth
        resp = self.client.post(self.login_url, data={"username" : self.username, "password" : self.password})
        self.assertEqual(resp.status_code, 302)

        acct = Account.objects.get(pk=1)
        next_url = self.secret_url+"?token=" + acct.token
        resp = self.client.get(next_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "account/secret.html")

        # post to verify answer
        resp = self.client.post(next_url, data={"answer" : self.answer})
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.home_url)


    def test_secret_fail(self):
        # with auth
        resp = self.client.post(self.login_url, data={"username" : self.username, "password" : self.password})
        self.assertEqual(resp.status_code, 302)

        acct = Account.objects.get(pk=1)
        next_url = self.secret_url+"?token=" + acct.token
        resp = self.client.get(next_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "account/secret.html")

        # post to verify answer
        resp = self.client.post(next_url, data={"answer" : self.answer + "error"})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "account/secret.html")

    def test_home(self):
        resp = self.client.get(self.home_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.login_url+"?next=/")


