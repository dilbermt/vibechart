from django.urls import path

from . import views

urlpatterns = [
    path("register/",views.register,name="register"),
    path("login/",views.login,name="login"),
    path("refresh-token/",views.refresh_token,name="refresh-token"),
    path("protected-view/",views.protected_view,name="protected"),
    path("logout/",views.logout,name="logout")
]
