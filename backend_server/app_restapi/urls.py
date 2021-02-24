import os
from django.conf.urls import url, include
from app_restapi import views as app_view
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^home/$', app_view.Home.as_view()),
    url(r'^current_user/', app_view.GetUser.as_view()),
    url(r'^user/create$', app_view.UserCreateList.as_view()),
    url(r'^user-profile/edit$', app_view.ProfileUpdateDestroy.as_view()),
    url(r'^user-profile$', app_view.ProfileCreateList.as_view()),
    # url(r'^booking/$',app_view.RoomBooking.as_view()),
    # url(r'^free-rooms/$',app_view.FreeRoomsList.as_view()),

]