from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.
def signup_view(request):
    if request.user.is_authenticated:
        print(request.user)
        return HttpResponseRedirect("/")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print("form is valid")
            user = form.save()
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return render(request, "users/register.html", {"form": form})

    else:
        form = UserCreationForm()
        return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data["username"]
            p = form.cleaned_data["password"]
            user = authenticate(username=u, password=p)

            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                error_message = "Your account is inactive."
                return render(
                    request,
                    "users/login.html",
                    {"form": form, "error_message": error_message},
                )

        else:
            return render(request, "users/login.html", {"form": form})
    else:
        form = AuthenticationForm()
        return render(request, "users/login.html", {"form": form})


@login_required
def profile_view(request):
    user = request.user
    return render(request, "users/profile.html", {"user": user})


@login_required
def profile_edit_view(request):
    user = request.user
    # Update fields
    user.first_name = "New First Name"
    user.last_name = "New Last Name"
    user.email = "new_email@example.com"

    # Save changes
    user.save()
    return render(request, "users/profile.html", {"user": user})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


def card(request):
    return render(
        request,
        "practice/card.html",
    )
