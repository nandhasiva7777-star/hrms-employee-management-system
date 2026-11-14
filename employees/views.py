from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from datetime import date
from .models import *
from .forms import *
DEFAULT_TASKS=['Offer Letter Signed','ID Card Issued','Laptop / System Allotted','HR Induction Completed','Bank Details Submitted','PF / ESI Documents']

def home(request): return redirect('dashboard') if request.user.is_authenticated else redirect('login_view')
def login_view(request):
    if request.method=='POST':
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user()); return redirect('dashboard')
        messages.error(request,'Invalid username / password')
    else: form=AuthenticationForm()
    return render(request,'login.html',{'form':form})
def logout_view(request): logout(request); return redirect('login_view')
def register_view(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            u=form.save(); login(request,u); messages.success(request,'Account created!'); return redirect('dashboard')
    else: form=RegisterForm()
    return render(request,'register.html',{'form':form})
@login_required
def dashboard(request):
    total=Employee.objects.count(); active=Employee.objects.filter(is_active=True).count()
    today=timezone.now().date()
    present=Attendance.objects.filter(date=today, status='Present').count()
    att_pct=round((present/total*100) if total else 0,1)
    pending=LeaveRequest.objects.filter(status='Pending').count()
    # Leave trends by type
    leave_data=list(LeaveRequest.objects.values('leave_type').annotate(c=Count('id')))
    dept_data=list(Employee.objects.values('department__name').annotate(c=Count('id')))
    # My data for employee
    my_emp=getattr(request.user,'employee_profile',None)
    my_att=Attendance.objects.filter(employee=my_emp).order_by('-date')[:5] if my_emp else []
    my_leaves=LeaveRequest.objects.filter(employee=my_emp).order_by('-applied_at')[:5] if my_emp else []
    return render(request,'dashboard.html',{'total':total,'active':active,'present':present,'att_pct':att_pct,'pending':pending,'leave_data':leave_data,'dept_data':dept_data,'my_att':my_att,'my_leaves':my_leaves,'my_emp':my_emp})
@login_required
def employee_list(request):
    q=request.GET.get('q','')
    emps=Employee.objects.all()
    if q: emps=emps.filter(full_name__icontains=q)
    return render(request,'employees/list.html',{'employees':emps,'q':q})
@login_required
def employee_create(request):
    if not request.user.is_hr() and not request.user.is_superuser: messages.error(request,'HR only'); return redirect('dashboard')
    if request.method=='POST':
        form=EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            emp=form.save()
            for t in DEFAULT_TASKS: OnboardingTask.objects.create(employee=emp, title=t)
            messages.success(request,f'{emp.full_name} added + Onboarding checklist created'); return redirect('employee_list')
    else: form=EmployeeForm()
    return render(request,'employees/form.html',{'form':form,'title':'Add Employee'})
@login_required
def employee_detail(request, pk):
    emp=get_object_or_404(Employee, pk=pk)
    tasks=emp.onboarding.all(); att=emp.attendance.all().order_by('-date')[:10]; leaves=emp.leaves.all().order_by('-applied_at')[:10]
    return render(request,'employees/detail.html',{'emp':emp,'tasks':tasks,'att':att,'leaves':leaves})
@login_required
def toggle_task(request, pk):
    t=get_object_or_404(OnboardingTask, pk=pk); t.is_done=not t.is_done; t.save(); return redirect('employee_detail', pk=t.employee.pk)
@login_required
def attendance_view(request):
    today=timezone.now().date(); my_emp=getattr(request.user,'employee_profile',None)
    if request.method=='POST' and my_emp:
        att,_=Attendance.objects.get_or_create(employee=my_emp, date=today)
        if 'check_in' in request.POST: att.check_in=timezone.now().time(); att.status='Present'
        if 'check_out' in request.POST: att.check_out=timezone.now().time()
        att.save(); messages.success(request,'Attendance updated'); return redirect('attendance_view')
    records=Attendance.objects.filter(date=today) if request.user.is_hr() else Attendance.objects.filter(employee=my_emp).order_by('-date')[:30]
    return render(request,'attendance.html',{'records':records,'today':today})
@login_required
def leave_list(request):
    my_emp=getattr(request.user,'employee_profile',None)
    leaves=LeaveRequest.objects.all().order_by('-applied_at') if request.user.is_hr() else LeaveRequest.objects.filter(employee=my_emp).order_by('-applied_at')
    return render(request,'leave_list.html',{'leaves':leaves})
@login_required
def leave_apply(request):
    my_emp=getattr(request.user,'employee_profile',None)
    if not my_emp: messages.error(request,'Ungaluku Employee profile illa. HR kitta create panna sollunga.'); return redirect('dashboard')
    if request.method=='POST':
        form=LeaveForm(request.POST)
        if form.is_valid():
            l=form.save(commit=False); l.employee=my_emp; l.save(); messages.success(request,'Leave applied!'); return redirect('leave_list')
    else: form=LeaveForm()
    return render(request,'leave_form.html',{'form':form})
@login_required
def leave_action(request, pk, action):
    if not request.user.is_hr(): return redirect('dashboard')
    l=get_object_or_404(LeaveRequest, pk=pk); l.status='Approved' if action=='approve' else 'Rejected'; l.save(); messages.success(request,f'Leave {l.status}'); return redirect('leave_list')
@login_required
def payroll_list(request):
    my_emp=getattr(request.user,'employee_profile',None)
    pays=Payroll.objects.all().order_by('-month') if request.user.is_hr() else Payroll.objects.filter(employee=my_emp).order_by('-month')
    return render(request,'payroll_list.html',{'pays':pays})
@login_required
def payroll_create(request):
    if not request.user.is_hr(): return redirect('dashboard')
    if request.method=='POST':
        form=PayrollForm(request.POST)
        if form.is_valid(): form.save(); messages.success(request,'Payroll created'); return redirect('payroll_list')
    else: form=PayrollForm()
    return render(request,'payroll_form.html',{'form':form})
@login_required
def payroll_slip(request, pk):
    p=get_object_or_404(Payroll, pk=pk); return render(request,'payroll_slip.html',{'p':p})
