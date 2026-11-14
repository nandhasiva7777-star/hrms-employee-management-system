# HRMS - Employee Management System | Python Django MySQL Bootstrap

## VS Code la Run Panna Guide (Step by Step)

### 1. Requirements Install pannunga
- Python 3.10+ - https://python.org/downloads
- VS Code + Python Extension
- MySQL 8 - https://dev.mysql.com/downloads/mysql/  (XAMPP use pannalum ok)
- Git (optional)

### 2. Project Open pannunga
```bash
cd hrms_project
code .
```

### 3. Virtual Environment
VS Code Terminal (Ctrl + `) la:
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 4. Packages Install
```bash
pip install -r requirements.txt
```

### 5. MySQL Database Create pannunga
MySQL Workbench / phpMyAdmin / Terminal la:
```sql
CREATE DATABASE hrms_db CHARACTER SET utf8mb4;
CREATE USER 'hrms_user'@'localhost' IDENTIFIED BY 'hrms1234';
GRANT ALL PRIVILEGES ON hrms_db.* TO 'hrms_user'@'localhost';
FLUSH PRIVILEGES;
```
> MySQL password vera na, `hrms/settings.py` la DATABASES la maathikonga.
> MySQL illa na, settings.py la sqlite option iruku - comment maathi use pannalam (keezha paaru).

### 6. Migrations + Admin Create
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
# Username: admin / Password: neenga kudunga
python manage.py create_demo_data
```

### 7. Run
```bash
python manage.py runserver
```
Browser la: http://127.0.0.1:8000/

### Login
- Admin: http://127.0.0.1:8000/admin/  (createsuperuser)
- HR Login: /login/  - HR role user
- Demo Data: 
  HR: hr@company.com / hr123456
  Employee: priya@company.com / emp123456
  Employee: arun@company.com / emp123456

### Features
- Employee Registration + Profile, Onboarding Checklist
- Attendance Mark (Check-in / Check-out), Monthly view
- Leave Apply / HR Approve / Reject
- Payroll Slip Generation (PDF Print)
- Admin Dashboard - Headcount, Attendance %, Leave Trends (Chart.js - Power BI style)
- Role-based Login: HR (full) / Employee (own data only)

### Folder Structure
```
hrms_project/
  manage.py
  requirements.txt
  hrms/ (settings, urls)
  employees/ (models, views, urls, forms)
  templates/ (base, dashboard, employees, attendance, leave, payroll)
  static/css/style.css
```

### SQLite ku Maara (MySQL vendam na)
hrms/settings.py la DATABASES block la sqlite lines uncomment pannunga, MySQL lines comment pannunga.
