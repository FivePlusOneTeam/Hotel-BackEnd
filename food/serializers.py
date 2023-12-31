from rest_framework import serializers
from .models import *
# -------------------------------------------------------------------------------------------------------------------------------
class FoodSerializer(serializers.ModelSerializer):
    date = serializers.CharField(source='shamsi_date')
    class Meta:
        model = Food
        fields = ('price', 'name', 'meal', 'type', 'count','day','id','date','image')
# -------------------------------------------------------------------------------------------------------------------------------
class UserSerializerForFood(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('firstName', 'lastName') 
# -------------------------------------------------------------------------------------------------------------------------------
class FoodReservationListSerializer(serializers.ModelSerializer):
    user = UserSerializerForFood()
    food = FoodSerializer()
    remain_paid = serializers.IntegerField(source='remaining')
    total_price = serializers.IntegerField(source='price')
    date = serializers.CharField(source='shamsi_date')
    class Meta:
        model = FoodReservation
        fields = ('food','user','created','paid','been_paid','remain_paid','total_price','date')
# -------------------------------------------------------------------------------------------------------------------------------
class FoodReservationSerializer(serializers.ModelSerializer):
    food_id = serializers.IntegerField()
    class Meta:
        model = Food
        fields = ('food_id',)
# -------------------------------------------------------------------------------------------------------------------------------
class FoodImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('image',)
        partial = True
# -------------------------------------------------------------------------------------------------------------------------------