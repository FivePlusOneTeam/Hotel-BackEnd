from django.urls import path
from .api_views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

name = "accounts"

urlpatterns = [
    path('csrf/', get_csrf_token.as_view(), name='csrf'),

    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='user-delete'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('users/detail/<int:pk>/', UserDetailPKView.as_view(), name='user-pk-detail'),
    path('users/detail/', UserDetailView.as_view(), name='user-detail'),
    path('users/update/image/<int:pk>/', ProfileImageUpdateView.as_view(), name='user-update-image'),

    path('users/update/password/', PasswordChangeRequest.as_view(), name='user-chagne-password-request'),
    path('users/change/password/', ChangePassword.as_view(), name='user-chagne-password'),
    path('users/validation/', code_validation, name='code_validation'),
    
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('employees/', EmployeeListView.as_view(), name='employees'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('users/role/update/<int:pk>/', UpdateRoleView.as_view(), name='role-update'),

    path('contact/email/', ContactUs.as_view(), name='contactus-email'),
    
    path('comments/room/create/', RoomCommentCreateView.as_view(), name='comments-room-create'),
    path('comments/food/create/', FoodCommentCreateView.as_view(), name='comments-food-create'),
    path('comments/delete/<int:pk>/', CommentDeleteView.as_view(), name='comments-delete'),
    path('comments/update/<int:pk>/', CommentUpdateView.as_view(), name='comments-update'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
