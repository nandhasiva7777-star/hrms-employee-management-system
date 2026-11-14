from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Employee, LeaveRequest, Attendance, Payroll, OnboardingTask
def bs(widget): widget.attrs.update({'class':'form-control'}); return widget
class EmployeeForm(forms.ModelForm):
    class Meta: model=Employee; fields=['emp_id','full_name','email','phone','department','designation','joining_date','salary']
    def __init__(self,*a,**k):
        super().__init__(*a,**k)
        for f in self.fields.values(): f.widget.attrs.update({'class':'form-control'})
        self.fields['joining_date'].widget=forms.DateInput(attrs={'type':'date','class':'form-control'})
class RegisterForm(UserCreationForm):
    class Meta: model=CustomUser; fields=['username','email','password1','password2','role']
    def __init__(self,*a,**k):
        super().__init__(*a,**k)
        for f in self.fields.values(): f.widget.attrs.update({'class':'form-control'})
class LeaveForm(forms.ModelForm):
    class Meta: model=LeaveRequest; fields=['leave_type','start_date','end_date','reason']
    def __init__(self,*a,**k):
        super().__init__(*a,**k)
        for f in self.fields.values(): f.widget.attrs.update({'class':'form-control'})
        self.fields['start_date'].widget=forms.DateInput(attrs={'type':'date','class':'form-control'})
        self.fields['end_date'].widget=forms.DateInput(attrs={'type':'date','class':'form-control'})
        self.fields['reason'].widget=forms.Textarea(attrs={'class':'form-control','rows':3})
class PayrollForm(forms.ModelForm):
    class Meta: model=Payroll; fields=['employee','month','basic','hra','allowances','deductions','working_days','present_days']
    def __init__(self,*a,**k):
        super().__init__(*a,**k)
        for f in self.fields.values(): f.widget.attrs.update({'class':'form-control'})
