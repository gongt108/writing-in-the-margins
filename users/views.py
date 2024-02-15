from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect("/signup")
    else:
        form = UserCreationForm()
        return render(request, "users/register.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data["username"]
            p = form.cleaned_data["password"]
            user = authenticate(username=u, password=p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(f"/user/{u}")
                else:
                    print(f"{u} - account has been disabled")
                    return HttpResponseRedirect("/login")
            else:
                print("The username and/or password is incorrect")
                return HttpResponseRedirect("/login")
        else:
            return HttpResponseRedirect("/login")
    else:
        form = AuthenticationForm()
        return render(request, "users/login.html", {"form": form})


@login_required
def profile(request):
    return render(request, "users/profile.html")


def card(request):
    return render(
        request,
        "practice/card.html",
    )
