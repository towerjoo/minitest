# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout as UserLogout
from django.contrib.auth import login as UserLogin, authenticate
from django.core.urlresolvers import reverse
from account.form import LoginForm, SecretForm
from account.models import Account

def login(request, template="account/login.html"):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    error = request.GET.get("e", None)
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    request.session["password"] = password
                    token = Account.objects.update_token(user)
                    if token:
                        return HttpResponseRedirect(reverse("secret")+"?token=" + token)
            else:
                error = "username and password don't match"
    else:
        form = LoginForm()
    return render_to_response(template, {"form" : form, "error" : error, "title" : "login"}, context_instance=RequestContext(request))

def secret(request, template="account/secret.html"):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login') + "?e=Please login at first")

    token = request.GET.get("token", request.POST.get("token", None))
    if token is None:
        return HttpResponseRedirect(reverse('login') + "?e=You need a token to continue, login again")
    acct = Account.objects.get_acct_from_token(token)
    if acct is None:
        return HttpResponseRedirect(reverse('login') + "?e=You got an invalid token, login again")
    form = SecretForm()
    error = request.GET.get("e")

    if request.method == "POST":
        error = None
        form = SecretForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data.get("answer")
            succ = Account.objects.verify_and_login(acct, answer)
            if succ:
                user = authenticate(username=acct.user.username, password=request.session.get("password", ""))
                if user:
                    UserLogin(request, user)
                    request.session["password"] = ""
                    return HttpResponseRedirect(reverse("home"))
                else:
                    error = "You need to enable your cookie"
            else:
                error = "An incorrect answer, try again."
    return render_to_response(template, {"form" : form, "error" : error, "question" : acct.question, "token" : token, "title" : "secret question"}, context_instance=RequestContext(request))

@login_required
def home(request, template="account/home.html"):
    return render_to_response(template, {"title" : "home"}, context_instance=RequestContext(request))

@login_required
def logout(request):
    return UserLogout(request, next_page=reverse("home"))
