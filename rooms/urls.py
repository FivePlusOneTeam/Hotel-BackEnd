from django.urls import path
from .api_views import *

name = "rooms"

urlpatterns = [
    path('rooms/type/', RoomTypeAllListAPIView.as_view(), name='all-room-list'), 
    path('rooms/type/<int:pk>/', RoomTypeDetailView.as_view(), name='room-detail'),
    path('rooms/type/create/', RoomTypeCreateAPIView.as_view(), name='room-create'),
    path('rooms/type/delete/<int:pk>/', RoomTypeDeleteView.as_view(), name='room-delete'),
    path('rooms/type/update/<int:pk>/', RoomTypeUpdateView.as_view(), name='room-update'),

    path('rooms/', RoomAllListAPIView.as_view(), name='all-room-list'), 
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('rooms/create/', RoomCreateAPIView.as_view(), name='room-create'),
    path('rooms/delete/<int:pk>/', RoomDeleteView.as_view(), name='room-delete'),
    path('rooms/update/<int:pk>/', RoomUpdateView.as_view(), name='room-update'),

    path('rooms/reservation/', ReservationRoomAPIView.as_view(), name='room-reservation'),
    path('rooms/reservation/all/', ReservationAllListAPIView.as_view(), name='all-reservation'),
]
