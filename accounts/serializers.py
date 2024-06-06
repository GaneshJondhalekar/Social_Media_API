from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['first_name','last_name','email','password']


    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name',""),
            last_name=validated_data.get('last_name',"")

        )
        return user
    

class LoginSerializer(serializers.Serializer):
    email=serializers.CharField()
    password=serializers.CharField()

   
    def get_jwt_token(self,data):
        print("Hi>>>>>>>")
        email=data['email'].lower()

        user=authenticate(username=email,password=data['password'])
      
        if user is None:
            return {'data':{},'message':"Invalid credentials"}
        
        refresh=RefreshToken.for_user(user)
        access=refresh.access_token
        print(user,"Hi>>>>>>>")
        return {'data':{'token':{'access':str(access),'refresh':str(refresh)}},'message':'Login succesfull'}
    

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')