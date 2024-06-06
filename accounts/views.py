from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .pegination import CustomPagination
from.serializers import UserRegistrationSerializer,LoginSerializer,UserSearchSerializer
from.models import User

# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        try:
            data=request.data
            serializer=UserRegistrationSerializer(data=data)
            print(data)
            if serializer.is_valid():
                serializer.save()# here when save called serializer create method will call which is defined in ResgisterSerializer
                return Response({
                    'message':"User registration successfull"
                },status=status.HTTP_201_CREATED)
            return Response({
                    'data':serializer.errors,
                    'message':"something wents wrong"
                },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({
                'data':{},
                'message':"something wents wrong"
            },status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(APIView):
    def post(self,request):
        try:
            data=request.data
            serializer=LoginSerializer(data=data)
            if serializer.is_valid():
                response=serializer.get_jwt_token(serializer.validated_data)
              
                return Response(response,status=status.HTTP_200_OK)
            
            return Response({
                'data':serializer.errors,
                'message':"something wents wrong"
            },status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            return Response({
                'data':{},
                'message':"something wents wrong"
            },status=status.HTTP_400_BAD_REQUEST)
        
        
class UserSearchView(generics.ListAPIView):
    serializer_class = UserSearchSerializer
    #permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination # Define this class as shown later

    def get_queryset(self):
        queryset = User.objects.all()
        keyword = self.request.query_params.get('keyword', None)
        print(keyword,"........")
        if keyword:
            if '@' in keyword:
                queryset = queryset.filter(email__iexact=keyword)
                
            else:
                queryset = queryset.filter(Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword))
        return queryset