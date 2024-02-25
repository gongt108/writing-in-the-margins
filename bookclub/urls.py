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
    path("profile/watchlist/", user_view.notification_view, name="notifications-list"),
    path("profile/delete/", user_view.account_delete, name="profile-delete"),
    path("profile/<str:shelf>/", user_view.shelf_view, name="shelf-view"),
    path("profile/", user_view.profile_view, name="profile"),
    path("logout/", user_view.logout_view, name="logout"),
    path("card/", user_view.card, name="card"),
    path("__reload__/", include("django_browser_reload.urls")),
    path("django-rq/", include("django_rq.urls")),
]
