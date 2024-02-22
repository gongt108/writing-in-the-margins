"""
URL configuration for bookclub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from users import views as user_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("base.urls")),
    path("register/", user_view.signup_view, name="signup"),
    path("login/", user_view.login_view, name="login"),
    path("login/edit/", user_view.login_edit_view, name="login-edit"),
    path("profile/edit/", user_view.profile_edit_view, name="profile-edit"),
    path("profile/", user_view.profile_view, name="profile"),
    path("logout/", user_view.logout_view, name="logout"),
    path("card/", user_view.card, name="card"),
    path("__reload__/", include("django_browser_reload.urls")),
    path("django-rq/", include("django_rq.urls")),
]
