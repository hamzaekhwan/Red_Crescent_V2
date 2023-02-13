from django.contrib import admin
from .models import *
from polls.views import send_sms
# Register your models here.

class Join_Request_Admin(admin.ModelAdmin):
    actions=['active_selected_users']
    def active_selected_users(self,request,queryset):
        for j in queryset:
            if j.accept==True:
                user=User.objects.get(username=j.user)
                user.is_active=True
                user.save()
            else:
                User.objects.filter(username=j.user ).delete()
            Join_Request.objects.filter(id=j.id).delete()
        self.message_user(request,'users activated successfully')
    def has_delete_permission(self, request, obj=None):
        return False

class Reservation_Admin(admin.ModelAdmin):
    # Other stuff here
    list_filter= ['id']
    
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False    
    def save_model(self, request, obj, form, change):
        pass
    def delete_model(self, request, obj):
        pass

    def save_related(self, request, form, formsets, change):
        pass    

class Repair_Request_Admin(admin.ModelAdmin):
    actions=["confirm_the_requests_repair"]
    def confirm_the_requests_repair(self,request,queryset):
        for j in queryset:
            if j.accept==True:
                p=Profile.objects.get(user=j.person_wantrepair)
                phone=p.phone
                if j.type=="اسعاف" and Res_Done.objects.filter(user=j.person_wantrepair,reservation=j.reservation,location=j.location,date=j.date).exists()==False :              
                    person_rank=p.rank
                    Res_Done.objects.create(user=j.person_wantrepair,person_rank=person_rank,reservation=j.reservation,location=j.location,date=j.date)
                    message=" تم الموافقة على طلب ترميم مناوبة الاسعاف في" + str(j.date) +" " +j.shift_time
                    send_sms(message,phone)

                elif  j.type=="عمليات" and Res_Done_Op.objects.filter(user=j.person_wantrepair,reservation=j.reservation,op_leader=False,location=j.location,date=j.date).exists()==False :
                    Res_Done_Op.objects.create(user=j.person_wantrepair,reservation=j.reservation,op_leader=False,location=j.location,date=j.date)
                    message=" تم الموافقة على طلب ترميم مناوبة العمليات في" + str(j.date) +" " +j.shift_time,
                    send_sms(message,phone)
                    
                elif  j.type=="قائد قطاع" and Res_Done_Op.objects.filter(user=j.person_wantrepair,reservation=j.reservation,op_leader=True,location=j.location,date=j.date).exists()==False :  
                    Res_Done_Op.objects.create(user=j.person_wantrepair,reservation=j.reservation,op_leader=True,location=j.location,date=j.date)  
                    message=" تم الموافقة على طلب ترميم مناوبة قائد القطاع في" + str(j.date) +" " +j.shift_time,
                    send_sms(message,phone)
                self.message_user(request,'تمت الموافقة')   
admin.site.register(Profile)
admin.site.register(Person_Reduce_Shift)
admin.site.register(Res_Done)
admin.site.register(Res_Done_Op)
admin.site.register(Cancel_Request)
admin.site.register(Repair_Request,Repair_Request_Admin)
admin.site.register(Reservation,Reservation_Admin)
admin.site.register(Join_Request,Join_Request_Admin)
admin.site.register(Error_Message)
admin.site.register(Control_Center)
admin.site.register(Reservations_Time)