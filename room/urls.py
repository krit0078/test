from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('index/',views.index),
    path('login/',views.login),
    path('logout/',views.logout),
    path('register/',views.register),
    path('dashboard/',views.dashboard),
    path('ajax/check_email',views.check_email),
    path('ajax/get_ed_sublevel',views.get_ed_sublevel)
]