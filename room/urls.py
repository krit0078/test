from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('index/',views.index),
    path('login/',views.login),
    path('changepass/<str:token>/',views.changepass),
    path('logout/',views.logout),
    path('register/',views.register),
    path('viewcourse/',views.viewcourse),
    path('profile/',views.profile),
    path('dashboard/',views.dashboard),
    path('overview/',views.overview),
    path('classroom/<int:classroom_id>/',views.classroom),
    path('classroom/<int:classroom_id>/steam/<int:steam_id>',views.delete_steam),
    path('classroom/<int:classroom_id>/task/',views.classroom_task),
    path('classroom/<int:classroom_id>/task/<int:task_id>/delete',views.delete_task),
    path('classroom/<int:classroom_id>/task/<int:task_id>/sub_task/<int:sub_task_id>/delete',views.delete_sub_task),
    path('classroom/<int:classroom_id>/score/',views.classroom_score),
    path('classroom/<int:classroom_id>/live/',views.classroom_live),
    path('classroom/<int:classroom_id>/live/<int:live_id>',views.delete_live),
    path('classroom/<int:classroom_id>/task/<int:task_id>/main',views.main),
    path('classroom/<int:classroom_id>/task/<int:task_id>/score/',views.main_score),
    path('classroom/<int:classroom_id>/task/<int:task_id>/resource',views.resource),
    path('classroom/<int:classroom_id>/task/<int:task_id>/resource/<int:resource_id>/delete',views.delete_resource),
    path('classroom/<int:classroom_id>/task/<int:task_id>/scaffolding',views.scaffolding),
    path('classroom/<int:classroom_id>/task/<int:task_id>/global/',views.global_group),
    path('classroom/<int:classroom_id>/task/<int:task_id>/addgroup/',views.add_group),
    path('classroom/<int:classroom_id>/task/<int:task_id>/group/<int:group_id>',views.view_group),
    path('classroom/<int:classroom_id>/task/<int:task_id>/group/<int:group_id>/delete',views.delete_group),
    path('classroom/<int:classroom_id>/task/<int:task_id>/group/<int:group_id>/colla/<int:colla_id>/delete',views.delete_colla),
    path('classroom/<int:classroom_id>/task/<int:task_id>/coach/',views.coaching),
    path('classroom/<int:classroom_id>/task/<int:task_id>/coach/<int:coach_id>/delete',views.delete_coach),
    path('classroom/<int:classroom_id>/task/<int:task_id>/turnedin/<int:turnedin_id>/delete',views.delete_turnin),
    path('ajax/check_email',views.check_email),
    path('ajax/get_email',views.get_email),
    path('ajax/get_ed_sublevel',views.get_ed_sublevel),
    path('ajax/update_cover',views.update_cover),
    path('ajax/fetch_og',views.fetch_og),
    path('ajax/update_user',views.update_user),
    path('api/task/classroom/<int:classroom_id>/id/<int:task_id>',views.api_task_detail),
    path('api/resource/classroom/<int:classroom_id>/task/<int:task_id>/id/<int:resource_id>',views.api_resource_detail),
    path('api/member/<str:command>',views.api_member_detail),
    path('api/level',views.api_level),
    path('api/course/<int:classroom_id>',views.api_course),
    path('api/enrolment/<int:enrol_id>',views.api_enrolment)
]