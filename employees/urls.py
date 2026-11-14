from django.urls import path
from . import views
urlpatterns=[
 path('', views.home, name='home'), path('login/', views.login_view, name='login_view'), path('logout/', views.logout_view, name='logout_view'),
 path('register/', views.register_view, name='register_view'), path('dashboard/', views.dashboard, name='dashboard'),
 path('employees/', views.employee_list, name='employee_list'), path('employees/add/', views.employee_create, name='employee_create'),
 path('employees/<int:pk>/', views.employee_detail, name='employee_detail'), path('onboarding/<int:pk>/toggle/', views.toggle_task, name='toggle_task'),
 path('attendance/', views.attendance_view, name='attendance_view'),
 path('leaves/', views.leave_list, name='leave_list'), path('leaves/apply/', views.leave_apply, name='leave_apply'),
 path('leaves/<int:pk>/<str:action>/', views.leave_action, name='leave_action'),
 path('payroll/', views.payroll_list, name='payroll_list'), path('payroll/add/', views.payroll_create, name='payroll_create'),
 path('payroll/<int:pk>/slip/', views.payroll_slip, name='payroll_slip'),
]
