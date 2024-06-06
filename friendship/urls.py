from django.urls import path
from .views import *

urlpatterns=[
    path('send/',SendFriendRequestView.as_view(),name="send_request"),
    path('accept_reject/',UpdateFriendRequestView.as_view(),name="update_request"),
]