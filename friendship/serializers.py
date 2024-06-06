from rest_framework import serializers
from .models import FriendRequest

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'

class FriendRequestActionSerializer(serializers.Serializer):
    from_user = serializers.EmailField()
    action = serializers.ChoiceField(choices=['accept', 'reject'])