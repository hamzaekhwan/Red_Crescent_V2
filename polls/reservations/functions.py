
from django.contrib.auth.models import User  
from polls.models import *
from rest_framework.views import *
from rest_framework.decorators import *
from rest_framework.response import *
from polls.models import *
from .serializers import *
import datetime
from django.utils import timezone
import calendar

def valid_reserve(pid,weekNumber,type,team_max_amb,sought_max,leader_max,scout_max,female_max,start_res_day,team_max_ob,team_max_ob_leader) :
   
    d = datetime.datetime.now()
    year_num=int(d.strftime("%Y"))
    if  int(timezone.now().today().day)>= start_res_day:
                
            if int(d.strftime("%m"))==12:
                        month_num=1
                        year_num=year_num+1
            else:
                    month_num=month_num+1
                    year_num=int(d.strftime("%Y"))
    else:
                month_num=int(d.strftime("%m"))
                year_num=int(d.strftime("%Y"))

    user=User.objects.get(id=pid)
    p=Profile.objects.get(user=user)
    valid=[]
    a=[]
    reservations = list(Reservation.objects.all())
   

    if weekNumber=='الأسبوع الأول':
            for j in reservations[:21]:
                a.append(j)
   
    elif weekNumber=='الأسبوع الثاني':    
            for j in  reservations[21:43]:
                a.append(j)
    elif weekNumber=='الأسبوع الثالث':

            for j in reservations[42:64]:
                a.append(j)
    elif weekNumber=='الأسبوع الرابع':

            for j in reservations[63:85]:
                a.append(j)
    elif weekNumber=='الأسبوع الخامس':

           

            if calendar.monthrange(year_num, month_num)[1]==31:
                for j in reservations[84:94]:
                    a.append(j)
            if calendar.monthrange(year_num, month_num)[1]==30:
                for j in reservations[84:91]:
                    a.append(j)      
            if calendar.monthrange(year_num, month_num)[1]==29:
                for j in reservations[84:88]:
                    a.append(j)
    if type=="اسعاف" :
       
        for i in a:   
            
                
                r=Res_Done.objects.filter(reservation=i,location=p.location,date__month=month_num,date__year=year_num)
                rr=Res_Done.objects.filter(reservation=i,person_rank=p.rank,location=p.location,date__month=month_num,date__year=year_num)
                rrr= Res_Done.objects.filter(reservation=i,user_id=pid,date__month=month_num,date__year=year_num)
                rrrr=Res_Done_Op.objects.filter(reservation=i,user_id=pid,date__month=month_num,date__year=year_num)
                if p.rank=='scout':
                    if p.gender=='male':
                        if rrr.exists():
                            valid.append('حجزته مسبقا')
                        elif r.count()>=team_max_amb  or rr.count()>=scout_max or rrrr.exists()  :
                            valid.append('غير متاح')
                        else:
                            valid.append('متاح')    
                    elif p.gender=='female':   
                        if rrr.exists():
                            valid.append('حجزته مسبقا')
                        elif  r.count()>=team_max_amb or count_of_female_in_shift(i,p.location,month_num,year_num) >=female_max or   is_third(i.id) or rr.count()>=scout_max or rrrr.exists()  :
                            valid.append('غير متاح')
                        else :
                            valid.append('متاح')    
                if p.rank=='sought':
                    
                    if p.gender=='male':
                    
                        if rrr.exists():
                            valid.append('حجزته مسبقا')
                        elif r.count()>=team_max_amb  or rr.count()>=sought_max  or rrrr.exists()  :
                            valid.append('غير متاح')
                        else:
                            valid.append('متاح')    
                    elif p.gender=='female':   
                        if rrr.exists():
                            valid.append('حجزته مسبقا')
                        elif  r.count()>=team_max_amb   or count_of_female_in_shift(i,p.location,month_num,year_num) >=female_max or  is_third(i.id) or rr.count()>=sought_max or rrrr.exists() :
                            valid.append('غير متاح')
                        else :
                            valid.append('متاح')   

                    
                if p.rank=='leader':
                    if p.gender=='male':
                        if rrr.exists():
                            valid.append('حجزته مسبقا')
                        elif r.count()>=team_max_amb  or rr.count()>=leader_max or rrrr.exists() :
                            valid.append('غير متاح')
                        else:
                            valid.append('متاح')    
                    elif p.gender=='female':   
                        if rrr.exists():
                            valid.append('حجزته مسبقا')
                        elif  r.count()>=team_max_amb or count_of_female_in_shift(i,p.location,month_num,year_num) >=female_max  or  is_third(i.id) or rr.count()>=leader_max or rrrr.exists() :
                            valid.append('غير متاح')
                        else :
                            valid.append('متاح')                       
            
          


               
    if type=="عمليات" :
        if   p.operations == True and p.op_leader == False :  
            for i in a:         
                r= Res_Done_Op.objects.filter(reservation=i,user_id=pid,date__month=month_num,date__year=year_num)
                rr=Res_Done_Op.objects.filter(reservation=i,location=p.location,date__month=month_num,date__year=year_num)
                rrr= Res_Done.objects.filter(reservation=i,user_id=pid,date__month=month_num,date__year=year_num) 
                if p.gender=='male':
                    if r.exists():
                        valid.append('حجزته مسبقا')
                    elif rr.count()>=team_max_ob or rrr.exists() :
                        valid.append('غير متاح')
                    else:
                        valid.append('متاح')
                elif p.gender=='female':
                    if r.exists():
                        valid.append('حجزته مسبقا')
                    elif  rr.count()>=team_max_ob or  is_third(i.id) or rrr.exists():
                        valid.append('غير متاح')
                    else :
                        valid.append('متاح')
        elif  p.operations == True and p.op_leader == True :
            for i in a:         
               
                r= Res_Done_Op.objects.filter(reservation=i,user_id=pid,date__month=month_num,date__year=year_num)  
                rr=Res_Done_Op.objects.filter(reservation=i,location=p.location,op_leader=True,date__month=month_num,date__year=year_num)
                rrr= Res_Done.objects.filter(reservation=i,user_id=pid,date__month=month_num,date__year=year_num) 
                if p.gender=='male':
                    if r.exists():
                        valid.append('حجزته مسبقا')
                    elif rr.count()>=team_max_ob_leader or rrr.exists() :
                        valid.append('غير متاح')
                    else:
                        valid.append('متاح')
                elif p.gender=='female':
                    if r.exists():
                        valid.append('حجزته مسبقا')
                    elif  rr.count()>=team_max_ob_leader or  is_third(i.id) or rrr.exists():
                        valid.append('غير متاح')
                    else :
                        valid.append('متاح')
     

        else:
            for i in a:

                valid.append('غير متاح')
    if weekNumber=='الأسبوع الأول':
            valid.insert(0, '1')
            valid.insert(4, '2')
            valid.insert(8, '3')
            valid.insert(12, '4')
            valid.insert(16, '5')
            valid.insert(20, '6')
            valid.insert(24, '7')
    elif weekNumber=='الأسبوع الثاني':   
            valid.insert(0, '8')
            valid.insert(4, '9')
            valid.insert(8, '10')
            valid.insert(12, '11')
            valid.insert(16, '12')
            valid.insert(20, '13')
            valid.insert(24, '14')
    elif weekNumber=='الأسبوع الثالث':
            valid.insert(0, '15')
            valid.insert(4, '16')
            valid.insert(8, '17')
            valid.insert(12, '18')
            valid.insert(16, '19')
            valid.insert(20, '20')
            valid.insert(24, '21')
    elif weekNumber=='الأسبوع الرابع':
            valid.insert(0, '22')
            valid.insert(4, '23')
            valid.insert(8, '24')
            valid.insert(12, '25')
            valid.insert(16, '26')
            valid.insert(20, '27')   
            valid.insert(24, '28') 
    elif  weekNumber== 'الأسبوع الخامس':   

            
            if calendar.monthrange(year_num, month_num)[1]==31:
                
                for i in range (0,16):
                    valid.append('')
                   
                valid.insert(0, '29')
                valid.insert(4, '30')
                valid.insert(8, '31') 
            if calendar.monthrange(year_num, month_num)[1]==30:
                for i in range (0,20):
                    valid.append('')
                valid.insert(0, '29')
                valid.insert(4, '30')    
            if calendar.monthrange(year_num, month_num)[1]==29:
                for i in range (0,24):
                    valid.append('')
                valid.insert(0, '29')  
    
                   
    return valid 


def reserve(user,type,location,team_max_amb,sought_max,leader_max,scout_max,female_max,start_res_day,team_max_ob,team_max_ob_leader):
    person=Profile.objects.get(user=user)
    d = datetime.datetime.now()
    check_valid=Reservations_Time.objects.filter(type=type,
    rank=person.rank,
    center=location,
    center_want_reserve=person.location,
    start_time__lt=d,
    end_time__gt=d) 
    
    if type=="اسعاف":
       if check_valid.exists()==True:
        return True
       else:
        return False 

    elif type=="عمليات":
        if check_valid.exists()==True:
            return True
        else:
            return False 



def count_of_female_in_shift(r,location,month_num,year_num):
    count=0
    r= Res_Done.objects.filter(reservation=r,location=location,date__month=month_num,date__year=year_num)
    for i in r:
        user=i.user
        p=Profile.objects.get(user=user)
        if p.gender=='female':
            count=count+1
    return count 

def is_third(rid):
  rid=int(rid)
  l=[3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57,60,63,66,69,72,75,78,81,84,87,90,93]
  if rid in l:
    return True
  else:
    return False       