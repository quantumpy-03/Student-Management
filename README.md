# Student Management System

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Django](https://img.shields.io/badge/Django-6.0.2-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Overview
The **Student Management System** is a comprehensive web application built with **Django** designed to streamline the administration of student records. It provides a secure and efficient way to manage student data, including personal profiles and academic records, leveraging a **MySQL** database for robust data handling.

> For detailed technical specifications, please refer to the Project Documentation.

## ✨ Features
- **Student Profile Management**: Create, view, update, and delete student records easily.
- **Image Processing**: Integrated support for uploading and handling student photos using **Pillow**.
- **Database Connectivity**: Configured for **MySQL** (via PyMySQL) for reliable data storage.
- **Admin Dashboard**: Utilizes Django's powerful built-in admin interface for quick administrative tasks.
- **Modern Architecture**: Built on the latest Django framework standards.

## 🛠️ Tech Stack
- **Backend**: Python, Django
- **Database**: MySQL
- **Libraries**: Pillow, PyMySQL, sqlparse

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- MySQL Server installed and running

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/quantumpy-03/Student-Management.git
   cd Student-Management
   ```

2. **Set up a Virtual Environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Configuration**
   - Create a MySQL database (e.g., `student_db`).
   - Update the `DATABASES` setting in `studentrecordsys/settings.py` with your MySQL credentials.

5. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start the Server**
   ```bash
   python manage.py runserver
   ```

## 📖 Usage
1. Access the application at `http://127.0.0.1:8000/`.
2. Log in to the admin panel at `http://127.0.0.1:8000/admin/` (you may need to create a superuser first using `python manage.py createsuperuser`).
3. Use the dashboard to add or modify student records.

## 🤝 Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

## 📄 License
MIT License - see LICENSE file.

## 🙏 Acknowledgments
- Built with Django.