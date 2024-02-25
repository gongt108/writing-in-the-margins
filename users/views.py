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
from django.urls import reverse
from django.utils.decorators import method_decorator

from .forms import ProfileUpdateForm, UserUpdateForm
from base.models import Book, Notification
from base.forms import CreateOrEditNotificationForm


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


def account_delete(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data["username"]
            p = form.cleaned_data["password"]
            user = authenticate(username=u, password=p)

            if user.is_active:
                user.delete()
                login(request)
                return HttpResponseRedirect("/")
            else:
                error_message = "Your account is inactive."
                return render(
                    request,
                    "users/account_delete.html",
                    {"form": form, "error_message": error_message},
                )

    return render(request, "users/account_delete.html", {"form": form})


@login_required
def shelf_view(request, shelf):
    profile = request.user.profile
    if shelf == "read_list":
        list_name = "Read"
        current_list = profile.read_list
    elif shelf == "reading_list":
        list_name = "Currently Reading"
        current_list = profile.reading_list
    elif shelf == "tbr_list":
        list_name = "Want to Read"
        current_list = profile.tbr_list
    else:
        # Handle invalid shelf values (optional)
        results = None

    if current_list:
        results = current_list.all()

    if request.method == "POST":
        book_to_remove = Book.objects.get(book_id=request.POST["book_id_to_remove"])
        # Assuming current_list is a ManyToManyField related queryset
        current_list.remove(book_to_remove)

        # Save the changes
        profile.save()

        return HttpResponseRedirect(reverse("shelf-view", args=(shelf,)))

    return render(
        request,
        "bookshelf.html",
        {"user": request.user, "list_name": list_name, "results": results},
    )


@login_required
def notification_view(request):
    profile = request.user.profile
    notifications_list = profile.notifications_list.all()
    coen_form = CreateOrEditNotificationForm()

    if request.method == "POST":
        notification_id_to_delete_or_edit = request.POST[
            "notification_to_delete_or_edit"
        ]
        notification_to_delete_or_edit = Notification.objects.get(
            id=notification_id_to_delete_or_edit
        )
        if "remove_notification_button" in request.POST:
            notification_to_delete_or_edit.delete()
        elif "edit_notification_button" in request.POST:
            coen_form = CreateOrEditNotificationForm(request.POST)
            user = request.user
            price = request.POST["price"]
            email = request.POST["email"]

            if coen_form.is_valid():
                notification_to_delete_or_edit.price = price
                notification_to_delete_or_edit.email = email
                notification_to_delete_or_edit.save()

            else:
                print(coen_form.errors)
        return HttpResponseRedirect(reverse("notifications-list"))

    # return render(
    #     request,
    #     "bookshelf.html",
    #     {"user": request.user, "list_name": list_name, "results": results},
    # )
    return render(
        request,
        "notification_list.html",
        {"results": notifications_list, "coen_form": coen_form},
    )


def card(request):
    return render(
        request,
        "practice/card.html",
    )
