from django.urls import path
from .views import *

urlpatterns=[
    path('send/',SendFriendRequestView.as_view(),name="send_request"),
    path('accept_reject/',UpdateFriendRequestView.as_view(),name="update_request"),
    path('list_friends/',ListFriendsView.as_view(),name="list_friends"),
    path('pending/',ListPendingRequestsView.as_view(),name="pending_request"),
]