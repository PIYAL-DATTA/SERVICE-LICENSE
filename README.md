# 🎫 Service License Management System

A robust and efficient **Django-based** web application designed to track, manage, and monitor service licenses and domain renewals. This system provides a centralized dashboard for administrators to oversee license cycles, handle registrations, and export critical data.

---

## ✨ Features

- **📂 Centralized License Tracking**: Manage service names, types, activation dates, and renewal deadlines in one place.
- **🔐 Secure Admin Authentication**: Role-based access with secure sign-in, login, and registration workflows.
- **📝 Interactive Entry Forms**: User-friendly forms for capturing detailed license and owner information.
- **📊 Data Export Capabilities**: Export license tables to **PDF** and **CSV** formats for offline reporting and auditing.
- **♻️ Smart Recycle Bin**: Safely delete records with the ability to restore them or perform permanent deletions.
- **⚡ Real-time Day Counting**: Automatically tracks remaining days until renewal for proactive management.
- **🛠️ Inline Editing**: Update license details directly through an intuitive edit interface.

---

## 🚀 Tech Stack

- **Backend**: [Django 4.x](https://www.djangoproject.com/) (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Django Templates
- **Database**: SQLite3
- **Dependency Management**: Pipenv
- **Reporting**: ReportLab & xhtml2pdf (PDF Generation), Python CSV Module

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Pipenv (`pip install pipenv`)

### Steps to Run Locally

1. **Clone the Repository**
   ```bash
   git clone https://github.com/PIYAL-DATTA/SERVICE-LICENSE.git
   cd SERVICE-LICENSE
   ```

2. **Install Dependencies**
   ```bash
   pipenv install
   ```

3. **Activate Virtual Environment**
   ```bash
   pipenv shell
   ```

4. **Navigate to Web Project**
   ```bash
   cd webproject
   ```

5. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

The application will be available at `http://127.0.0.1:8000/`.

---

## 📂 Project Structure

```text
SERVICE-LICENSE/
├── webproject/           # Root Django project
│   ├── manage.py         # Django CLI
│   ├── webapp/          # Core application logic
│   │   ├── models.py     # Database schemas (User, Account, DeletedUsers)
│   │   ├── views.py      # Business logic and request handling
│   │   ├── urls.py       # Application routing
│   │   └── templates/    # HTML interfaces
│   └── webproject/      # Settings and configuration
├── Pipfile               # Dependency definitions
└── README.md             # Project documentation
```

---


## 👨‍💻 Developed By

**Piyal Datta**  
*GitHub*: [PIYAL-DATTA](https://github.com/PIYAL-DATTA)


