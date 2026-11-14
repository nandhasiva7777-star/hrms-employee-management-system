from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from employees.models import Department, Employee, Attendance, LeaveRequest, Payroll
from django.utils import timezone
from datetime import date, timedelta
User=get_user_model()
class Command(BaseCommand):
    help='Create demo HR, Employees, Attendance, Leave, Payroll'
    def handle(self,*a,**k):
        hr,_=User.objects.get_or_create(username='hr', defaults={'email':'hr@company.com','role':'HR','is_staff':True})
        hr.set_password('hr123456'); hr.save()
        for name,email,uname,dept,desig,sal in [('Priya Sharma','priya@company.com','priya','IT','Developer',45000),('Arun Kumar','arun@company.com','arun','HR','HR Executive',32000),('Divya M','divya@company.com','divya','Finance','Accountant',38000)]:
            u,_=User.objects.get_or_create(username=uname, defaults={'email':email,'role':'EMPLOYEE'})
            u.set_password('emp123456'); u.save()
            d,_=Department.objects.get_or_create(name=dept)
            emp,_=Employee.objects.get_or_create(emp_id=f'EMP{uname.upper()}001', defaults={'user':u,'full_name':name,'email':email,'department':d,'designation':desig,'salary':sal,'joining_date':date(2024,1,15)})
            emp.user=u; emp.save()
            Attendance.objects.get_or_create(employee=emp, date=timezone.now().date(), defaults={'status':'Present','check_in':timezone.now().time()})
            LeaveRequest.objects.get_or_create(employee=emp, start_date=date.today(), end_date=date.today()+timedelta(days=1), defaults={'leave_type':'Casual','reason':'Family function','status':'Pending'})
            Payroll.objects.get_or_create(employee=emp, month='2026-11', defaults={'basic':sal,'hra':sal*0.2,'allowances':3000,'deductions':1500,'working_days':22,'present_days':20})
        self.stdout.write(self.style.SUCCESS('Demo ready! HR: hr / hr123456 | Employee: priya / emp123456'))
