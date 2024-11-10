from django.urls import path

from . import views

urlpatterns = [
    path("",views.home),
    path("add-song",views.add_song),
    path("<int:id>/",views.get_song_details),
    path("update/<int:id>/",views.update_song),
    path("delete/<int:id>/",views.delete_song)
]
