from django.shortcuts import render
from rest_framework import generics
from .models import FriendRequest
from rest_framework.permissions import IsAuthenticated
from .serializers import FriendRequestSerializer,FriendRequestActionSerializer
from accounts.models import User
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from django.db.models import Q
from accounts.serializers import UserSearchSerializer

# Create your views here.
class SendFriendRequestView(generics.CreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        to_user_email = request.data.get('to_user')
        try:
            to_user = User.objects.get(email=to_user_email.lower())
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        from_user = request.user

        # Check rate limit
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        if FriendRequest.objects.filter(from_user=from_user, timestamp__gte=one_minute_ago).count() >= 3:
            return Response({'error': 'Rate limit exceeded. You can only send 3 friend requests per minute.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendRequest(from_user=from_user, to_user=to_user)
        friend_request.save()

        return Response({'status': 'Friend request sent'}, status=status.HTTP_201_CREATED)
    

class UpdateFriendRequestView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestActionSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email= serializer.validated_data['from_user']
        action = serializer.validated_data['action']

        from_user=User.objects.filter(email=email).first()

        try:
            friend_request = FriendRequest.objects.get(from_user=from_user, to_user=request.user)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)

        if action == 'accept':
            friend_request.status = 'accepted'
            from_user.profile.friends.add(request.user)
            request.user.profile.friends.add(from_user)
        elif action == 'reject':
            friend_request.status = 'rejected'

        friend_request.save()
        return Response({'status': f'Friend request {action}ed'}, status=status.HTTP_200_OK)
    

class ListFriendsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        friends=user.profile.friends.all()
        serializer = UserSearchSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListPendingRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pending_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
        serializer = FriendRequestSerializer(pending_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)