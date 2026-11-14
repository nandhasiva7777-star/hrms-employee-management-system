from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
class CustomUser(AbstractUser):
    ROLE_CHOICES=[('HR','HR'),('EMPLOYEE','Employee'),('ADMIN','Admin')]
    role=models.CharField(max_length=20, choices=ROLE_CHOICES, default='EMPLOYEE')
    def is_hr(self): return self.role in ('HR','ADMIN') or self.is_superuser
class Department(models.Model):
    name=models.CharField(max_length=100, unique=True)
    def __str__(self): return self.name
class Employee(models.Model):
    user=models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee_profile', null=True, blank=True)
    emp_id=models.CharField(max_length=20, unique=True)
    full_name=models.CharField(max_length=150); email=models.EmailField()
    phone=models.CharField(max_length=15, blank=True)
    department=models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    designation=models.CharField(max_length=100, default='Software Developer')
    joining_date=models.DateField(default=timezone.now)
    salary=models.DecimalField(max_digits=10, decimal_places=2, default=30000)
    photo=models.ImageField(upload_to='photos/', blank=True, null=True)
    is_active=models.BooleanField(default=True)
    def __str__(self): return f"{self.emp_id} - {self.full_name}"
class OnboardingTask(models.Model):
    employee=models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='onboarding')
    title=models.CharField(max_length=200); is_done=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.employee.full_name} - {self.title}"
class Attendance(models.Model):
    STATUS=[('Present','Present'),('Absent','Absent'),('Half Day','Half Day'),('On Leave','On Leave')]
    employee=models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance')
    date=models.DateField(default=timezone.now)
    check_in=models.TimeField(null=True, blank=True); check_out=models.TimeField(null=True, blank=True)
    status=models.CharField(max_length=20, choices=STATUS, default='Present')
    class Meta: unique_together=('employee','date')
    def __str__(self): return f"{self.employee.full_name} {self.date} {self.status}"
class LeaveRequest(models.Model):
    TYPE=[('Casual','Casual'),('Sick','Sick'),('Earned','Earned'),('LOP','LOP')]
    STATUS=[('Pending','Pending'),('Approved','Approved'),('Rejected','Rejected')]
    employee=models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    leave_type=models.CharField(max_length=20, choices=TYPE, default='Casual')
    start_date=models.DateField(); end_date=models.DateField(); reason=models.TextField()
    status=models.CharField(max_length=20, choices=STATUS, default='Pending')
    applied_at=models.DateTimeField(auto_now_add=True)
    @property
    def days(self): return (self.end_date-self.start_date).days+1
    def __str__(self): return f"{self.employee.full_name} {self.leave_type} {self.status}"
class Payroll(models.Model):
    employee=models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payrolls')
    month=models.CharField(max_length=20, help_text='Ex: 2026-11')
    basic=models.DecimalField(max_digits=10, decimal_places=2); hra=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    allowances=models.DecimalField(max_digits=10, decimal_places=2, default=0); deductions=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    working_days=models.IntegerField(default=22); present_days=models.IntegerField(default=22)
    created_at=models.DateTimeField(auto_now_add=True)
    @property
    def net_pay(self): return float(self.basic)+float(self.hra)+float(self.allowances)-float(self.deductions)
    class Meta: unique_together=('employee','month')
    def __str__(self): return f"{self.employee.full_name} - {self.month}"
