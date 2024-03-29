from rest_framework import serializers
from .models import User,ContactUs,Comment,RoomComment,FoodComment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
#-----------------------------------------------------------
class EnhancedTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        # ...
        return token
#-----------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'nationalCode', 'firstName', 'lastName', 'password']

    def validate_nationalCode(self, value):
        if len(value) != 10:
            raise serializers.ValidationError("nationalCode must be 10 digits.")
        

        check = int(value[9])
        test = [int(i) for i in value[:9]]
        weights = [10, 9, 8, 7, 6, 5, 4, 3, 2]
        result = sum(x * y for x, y in zip(test, weights)) % 11

        if result < 2:
            if(check != result):
                raise serializers.ValidationError("nationalCode not valid.")
        else:
            if(check != 11 - result):
                raise serializers.ValidationError("nationalCode not valid.")

        return value
#-----------------------------------------------------------
class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = [ 'firstName', 'lastName', 'password']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)
        return representation
#-----------------------------------------------------------
class UpdateRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'role']
    
    
#-----------------------------------------------------------
class CodeValidationSerializers(serializers.ModelSerializer):
    email = serializers.CharField()
    code = serializers.CharField()
    class Meta:
        model = User
        fields = ['email', 'code']
#-----------------------------------------------------------
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'nationalCode', 'firstName', 'lastName', 'role','image']
#-----------------------------------------------------------
class PasswordChangeRequestSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    class Meta:
        model = User
        fields = [ 'email']
#-----------------------------------------------------------
class PasswordChangeSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    code = serializers.CharField()
    password = serializers.CharField()
    class Meta:
        model = User
        fields = [ 'email', 'code','password']
#-----------------------------------------------------------
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'nationalCode', 'firstName', 'lastName', 'role','employee_id','image']
#-----------------------------------------------------------
class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'nationalCode', 'firstName', 'lastName', 'role','password']
#-----------------------------------------------------------
class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('image',)
        partial = True
#-----------------------------------------------------------
class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ('name','email','subject','text')
#-----------------------------------------------------------
class RoomCommentCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    room_id = serializers.IntegerField()
    class Meta:
        model = RoomComment
        fields = ('user_id','room_id','text','rating',)
#-----------------------------------------------------------
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    text = serializers.CharField(required=False)
    class Meta:
        model = Comment
        fields = "__all__"
#-----------------------------------------------------------
class FoodCommentCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    food_id = serializers.IntegerField()
    class Meta:
        model = FoodComment
        fields = ('user_id','food_id','text','rating',)
#-----------------------------------------------------------