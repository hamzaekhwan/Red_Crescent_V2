from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.conf import settings
from polls.views import send_sms
import datetime

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    fullName=models.CharField(max_length=50 , blank=True, null=True)
    gender=models.CharField(max_length=50 , blank=True, null=True)
    rank=models.CharField(max_length=50 , blank=True, null=True)
    otp=models.CharField(max_length=50 , blank=True, null=True)
    location=models.CharField(max_length=50 , blank=True, null=True)
    operations=models.BooleanField(default=False)
    op_leader=models.BooleanField(default=False)
    is_verified=models.BooleanField(default=False)
    phone=models.CharField(max_length=50 , blank=True, null=True)
    image = models.ImageField(null=True, blank=True,
                              default='/placeholder.png')
    
    def __str__(self):
        return str(self.user)


       
@receiver(post_save , sender=User)
def create_user_profile(sender,instance,created , **kwargs):
    if created:
        Profile.objects.create(
            user = instance
        )

        
class Join_Request(models.Model): 
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    fullName=models.CharField(max_length=50 , blank=True, null=True)
    gender=models.CharField(max_length=50 , blank=True, null=True)
    rank=models.CharField(max_length=50 , blank=True, null=True)
    operations=models.BooleanField(default=False)
    op_leader=models.BooleanField(default=False)
    phone=models.CharField(max_length=50 , blank=True, null=True)
    accept=models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True,
                              default='/placeholder.png')


class Reservation(models.Model):
    day_in_month=models.IntegerField(blank=True,null=True)
    shift_time=models.CharField(max_length=50 , blank=True, null=True)


class Person_Reduce_Shift(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    number_of_shift=models.IntegerField(blank=True,null=True)



class Res_Done(models.Model):
    user=models.ForeignKey(User,unique=False , on_delete=models.CASCADE)
    reservation=models.ForeignKey(Reservation,unique=False , on_delete=models.CASCADE)
    person_rank=models.CharField(max_length=200,null=True,blank=True)
    location=models.CharField(max_length=200,null=True,blank=True)
    date=models.DateField()

class Res_Done_Op(models.Model):
    user=models.ForeignKey(User,unique=False , on_delete=models.CASCADE)
    reservation=models.ForeignKey(Reservation,unique=False , on_delete=models.CASCADE)
    location=models.CharField(max_length=200,null=True,blank=True)
    op_leader=models.BooleanField(default=False)
    date=models.DateField()    

class Cancel_Request(models.Model):
    person_wantcancel=models.ForeignKey(User,unique=False , on_delete=models.CASCADE,related_name ='person_wantcancel')
    person_substitute=models.ForeignKey(User,unique=False , on_delete=models.CASCADE,related_name='person_substitute')
    reservation=models.ForeignKey(Reservation,unique=False , on_delete=models.CASCADE,blank=True)
    type=models.CharField(max_length=200,null=True)
    location=models.CharField(max_length=200,null=True)
    person_wantcancel_name=models.CharField(max_length=200,null=True)
    person_substitute_name= models.CharField(max_length=200,null=True,blank=True)
    date=models.DateField()
    shift_time=models.CharField(max_length=200,null=True)
    time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    accept=models.BooleanField(default=False)

class Repair_Request(models.Model):
    person_wantrepair=models.ForeignKey(User,unique=False , on_delete=models.CASCADE)
    reservation=models.ForeignKey(Reservation,unique=False , on_delete=models.CASCADE)
    type=models.CharField(max_length=200,null=True)
    location=models.CharField(max_length=200,null=True)
    person_wantrepair_name=models.CharField(max_length=200,null=True)
    date=models.DateField()
    shift_time=models.CharField(max_length=200,null=True)
    time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    accept=models.BooleanField(default=False)

    
class Control_Center(models.Model):
    center=models.CharField(max_length=200)
    sought_max=models.IntegerField(blank=True,null=True)
    leader_max=models.IntegerField(blank=True,null=True)
    scout_max=models.IntegerField(blank=True,null=True)
    female_max=models.IntegerField(blank=True,null=True)
    start_res_day=models.IntegerField(blank=True,null=True)
    team_max_amb=models.IntegerField(blank=True,null=True)
    team_max_ob=models.IntegerField(blank=True,null=True)
    count_person_amb=models.IntegerField(blank=True,null=True)
    count_person_ob=models.IntegerField(blank=True,null=True)
    count_person_ob_min=models.IntegerField(blank=True,null=True)
    start=models.DateTimeField(default=datetime.datetime.now, blank=True)
    end=models.DateTimeField(default=datetime.datetime.now, blank=True)


class Reservations_Time(models.Model):
    center=models.CharField(max_length=200,blank=False)
    center_want_reserve=models.CharField(max_length=200,blank=False)
    rank=models.CharField(max_length=200,blank=False)
    max_person=models.IntegerField(blank=False)
    type=models.CharField(max_length=200,blank=False)
    start_time=models.DateTimeField(default=datetime.datetime.now, blank=False)
    end_time=models.DateTimeField(default=datetime.datetime.now, blank=False)
class Error_Message(models.Model):
    name=models.CharField(max_length=200,null=True,unique=True)
    message=models.TextField()


@receiver(reset_password_token_created)

def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):


    user=reset_password_token.user
    p=Profile.objects.get(user=user)
    message= " كود استرجاع الحساب الخاص بك هو" + reset_password_token.key
    phone=p.phone
    send_sms(message,phone)

   