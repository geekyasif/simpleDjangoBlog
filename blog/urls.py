from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('' , views.home, name="home"),
   path('contact' , views.contact, name="contact"),
   path('<int:year>/<int:month>/<int:day>/<slug:post>/' , views.post_details, name="post_details"),
   path('<int:post_id>/share/' , views.post_share, name="post_share"),
]

