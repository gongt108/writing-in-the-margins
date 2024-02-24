from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator

from .forms import ProfileUpdateForm, UserUpdateForm


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
    print(user.profile)
    return render(request, "users/profile.html", {"user": user})


@login_required
def profile_edit_view(request):
    user = request.user

    if request.method == "POST":
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if p_form.is_valid():

            p_form.save()
            messages.success(request, f"Acount Updated Successfully!")
            return redirect("profile")
        elif not p_form.is_valid():

            # Print errors for the ProfileUpdateForm
            for field, errors in p_form.errors.items():
                for error in errors:
                    print(f"Error in {field}: {error}")
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, "users/profile_update.html", {"p_form": p_form})


@login_required
def login_edit_view(request):
    if request.method == "POST":
        password_form = PasswordChangeForm(request.user, request.POST)

        if password_form.is_valid():
            update_session_auth_hash(request, password_form.user)
            messages.success(request, f"Acount Updated Successfully!")
            return redirect("profile")

    else:
        password_form = PasswordChangeForm(request.user)

    context = {
        "form": password_form,
    }
    return render(request, "users/login_update.html", context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


@login_required
def shelf_view(request, shelf):
    profile = request.user.profile
    if shelf == "read_list":
        list_name = "Read"
        results = profile.read_list.all()
    elif shelf == "reading_list":
        list_name = "Currently Reading"
        results = profile.reading_list.all()
    elif shelf == "tbr_list":
        list_name = "Want to Read"
        results = profile.tbr_list.all()
    else:
        # Handle invalid shelf values (optional)
        results = None

    return render(
        request,
        "bookshelf.html",
        {"user": request.user, "list_name": list_name, "results": results},
    )


def card(request):
    return render(
        request,
        "practice/card.html",
    )
