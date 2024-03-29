from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser
from config.utils import jalali_converter_with_hour
from django.utils import timezone
from django.db import models
from .managers import MyUserManager
#--------------------------------------------------------
class User(AbstractBaseUser):
    """
        main User object that extends django-user
        username --> email

    """
    role_choice = (
        ('u','کاربر عادی'),
        ('m','مدیر هتل'),
        ('d','معاون هتل'),
        ('a','پذیرش هتل'),
        ('r','مدیر رستوران'),
    ) 
    email = models.EmailField(unique=True)
    nationalCode = models.CharField(unique=True, max_length=10)
    firstName = models.CharField(max_length=100, null=True, blank=True)
    lastName = models.CharField(max_length=100, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='users/',default ='users/image.jpg') 

    can_change_password = models.BooleanField(default=False)

    code = models.IntegerField(blank=True,null=True)

    role = models.CharField(max_length=1,choices=role_choice,default='u')
    employee_id = models.IntegerField(unique=True,null=True,blank=True)

    REQUIRED_FIELDS = ['nationalCode']
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return str(self.email) + " - " + str(self.firstName) + " " + str(self.lastName)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def total_price(self):
        room_reservations = self.reservations.filter(paid=False)
        food_reservations = self.food_reservations.filter(paid=False)

        total = 0
        for reservation in room_reservations:
            total += reservation.remaining()

        print(total)
        for reservation in food_reservations:
            total += reservation.remaining()

        print(total)


        return total

    def all_payed(self):
        for reservation in self.reservations.filter(paid=False):
            reservation.payed()

        for reservation in self.food_reservations.filter(paid=False):
            reservation.payed()
        
        return 0


    @property
    def is_staff(self):
        return self.is_admin
#--------------------------------------------------------
class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    text = models.TextField()


    def __str__(self):
        return str(self.name) + " - " + str(self.subject)
#--------------------------------------------------------
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created = models.DateField(auto_now_add=True)
    valid = models.BooleanField(default=False)
    rating = models.FloatField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])


    def __str__(self):
        return f"{self.user}"

    def star_rating(self):
        return self.rating * 20

    def shamsi_date(self):
        return jalali_converter_with_hour(self.created) 
    
    def days_since_creation(self):
        now = timezone.now()
        created_naive = timezone.make_naive(self.created, timezone.get_default_timezone())
        created_aware = timezone.make_aware(created_naive, timezone.get_default_timezone())
        days = (now - created_aware).days
        return f"{days} روز پیش"
#--------------------------------------------------------
from food.models import Food
class FoodComment(Comment):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.user} - {self.food}"
#--------------------------------------------------------
from rooms.models import RoomType
class RoomComment(Comment):
    room = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.user} - {self.room}"
#--------------------------------------------------------
class Payments(models.Model):
    ref_id = models.CharField(max_length=100,null=True,blank=True)
    authority = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="payments")
    amount = models.IntegerField()


    def __str__(self):
        return str(self.user) + " - " + str(self.amount)
#--------------------------------------------------------
