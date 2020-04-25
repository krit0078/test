from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('index/',views.index),
    path('login/',views.login),
    path('logout/',views.logout),
    path('register/',views.register),
    path('viewcourse/',views.viewcourse),
    path('dashboard/',views.dashboard),
    path('classroom/<int:classroom_id>/',views.classroom),
    path('classroom/<int:classroom_id>/task/',views.classroom_task),
    path('classroom/<int:classroom_id>/score/',views.classroom_score),
    path('classroom/<int:classroom_id>/live/',views.classroom_live),
    path('ajax/check_email',views.check_email),
    path('ajax/get_ed_sublevel',views.get_ed_sublevel),
    path('ajax/update_cover',views.update_cover)
]