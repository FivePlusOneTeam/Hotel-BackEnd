
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import *
from .models import User
from random import randint
from rest_framework.views import APIView
from rest_framework import permissions
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from .utils import *
from rest_framework.generics import DestroyAPIView,UpdateAPIView
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import *
# -------------------------------------------------------------------------------------------------------------------------------
"""
    api's in api_views.py :

    1- GetCSRFToken --> get crrf token for login
    2- login --> login user
    3- user_create  --> create one account with email & National Code
    4- code_validation --> It checks whether the code is the same as the code in the database

"""
# -------------------------------------------------------------------------------------------------------------------------------
@method_decorator(ensure_csrf_cookie, name='dispatch')
class get_csrf_token(APIView):
    """
        Get And Set csrf cookie for FrontEnd(React)
    """
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response({'success': "CSRF cookie set"})
# -------------------------------------------------------------------------------------------------------------------------------
@api_view(['GET'])
def get_endpoint(request):
    endpoints = [
        '/accounts/token',
        '/accounts/token/refresh',
        '/accounts/user/create/',
        '/accounts/user/validation/'
    ]

    return Response(endpoints)
# -------------------------------------------------------------------------------------------------------------------------------
class UserCreateView(APIView):
    def post(self, request):
        """
        Create User with Post Api

        Sample json :
        {
        "email" : "TahaM8000@gmail.com",
        "nationalCode" : "0112037754",
        "firstName" : "Taha",
        "lastName" : "Mousavi",
        "password" : "1234jj5678"
        }

        """

        info = UserSerializer(data=request.data)
        code = randint(1000, 9999)

        if info.is_valid():
            # Check if the nationalCode is duplicated
            if User.objects.filter(nationalCode=info.validated_data['nationalCode']).exists():
                return Response({'message': 'The national code is duplicated.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the email is duplicated
            if User.objects.filter(email=info.validated_data['email']).exists():
                return Response({'message': 'The email is duplicated.'}, status=status.HTTP_400_BAD_REQUEST)

            User(nationalCode=info.validated_data['nationalCode'],
                 email=info.validated_data['email'],
                 is_active=False,
                 firstName=info.validated_data['firstName'],
                 lastName=info.validated_data['lastName'],
                 code=code).save()

            user = User.objects.get(email=info.validated_data['email'])
            user.set_password(info.validated_data['password'])
            user.save()

            # send Code to User
            send_mail(info.validated_data['email'], code)

            return Response({'message': 'User was created and code sent.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
# -------------------------------------------------------------------------------------------------------------------------------
class PasswordChangeRequest(APIView):
    def post(self, request):
        """
            Password change request

            Sample json :
            {
            "email" : "TahaM8000@gmail.com",
            }

        """

        info = PasswordChangeRequestSerializer(data=request.data)
        

        if info.is_valid():
            user = User.objects.get(email=info.validated_data['email'])

            user.can_change_password = True
            code = randint(1000, 9999)
            user.code = code
            user.save()

            # send Code to User
            send_mail(info.validated_data['email'], code)
            
            return Response({'message': 'code sent.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
# -------------------------------------------------------------------------------------------------------------------------------
class ChangePassword(APIView):
    def post(self, request):
        """
            It change user password if can_change_password is active.

            Sample json :
            {
            "email" : "TahaM8000@gmail.com",
            "password" : "338dsfs3fsaengh7",
            "code" : 7676
            }

        """

        info = PasswordChangeSerializer(data=request.data)
        

        if info.is_valid():
            user = User.objects.get(email=info.validated_data['email'])
            if (user.can_change_password):
                if(user.code == int(info.validated_data['code'])):
                    print(info.validated_data.get('password'))
                    user.set_password(info.validated_data.get('password'))
                    user.can_change_password = False
                    user.code = randint(1000, 9999)
                    user.save()

                    return Response({'message': 'password changed.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'wrong code!'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
# -------------------------------------------------------------------------------------------------------------------------------
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def code_validation(request):
    """
        It checks whether the code is the same as the code in the database

        Sample json :
        {
        "email" : "TahaM8000@gmail.com",
        "code" : "8817"
        }

    """

    info = CodeValidationSerializers(data=request.data)
    

    if info.is_valid():
        user = User.objects.get(email=info.validated_data['email'])
        if (user.code == int(info.validated_data['code'])):
            
            user.is_active = True
            user.save()
            return Response({'message': 'code is right.'}, status=status.HTTP_200_OK)
        return Response({'message': 'wrong code!'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
# -------------------------------------------------------------------------------------------------------------------------------
class UserDeleteView(DestroyAPIView):
    permission_classes = [IsManager]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
# -------------------------------------------------------------------------------------------------------------------------------
class UserUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        if 'password' in serializer.validated_data:
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        serializer.save()
# -------------------------------------------------------------------------------------------------------------------------------
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated,IsHotelManager]

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            serializer = UserDetailSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'user not found.'}, status=status.HTTP_404_NOT_FOUND)
# -------------------------------------------------------------------------------------------------------------------------------
class TestView(APIView):
    permission_classes = [IsManager]

    def get(self, request):
        return Response({'message':'you can see'}, status=status.HTTP_200_OK)
# -------------------------------------------------------------------------------------------------------------------------------
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """

            Sample json :
            {
            "email" : "TahaM8000@gmail.com"
            }

        """

        info = PasswordChangeRequestSerializer(data=request.data)
        

        if info.is_valid():
            try:
                user = User.objects.get(email=info.validated_data['email'])
                serializer = UserDetailSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'detail': 'user not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
# -------------------------------------------------------------------------------------------------------------------------------
