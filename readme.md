# schl_schdl - Web application for managing a childcare provider

**Description:**

This is a web application designed for a childcare provider company.

**Features:**

* **Client management:**
    * Register and manage client profiles.
    * View order and payment history.
* **Payment processing:**
    * Secure payments through Stripe.
* **Schedule management:**
    * Create and manage schedules for different groups.
* **Attendance tracking:**
    * Track children's attendance at classes.
* **Reporting:**
    * Quickly generate reports on attendance, payments, etc.
* **Notifications:**
    * Automatically notify parents about classes, schedule changes, etc.
* **Marketing campaigns:**
    * Tools for running marketing campaigns and attracting new customers.
* **Personal accounts:**
    * Personal accounts for parents, teachers, and administrators with access to relevant information.

**Technologies:**

* **Python** - main programming language
* **Flask** - web framework
* **SQLAlchemy** - ORM for working with databases
* **Stripe** - payment system
* **Twilio** - SMS notifications
* **and others** (see requirements.txt file)


**Installation:**

1. Clone the repository:

```
git clone git@github.com:gavrilov/schl_schdl_public.git
```

2. Create a virtual environment and install dependencies:

```
python -m venv venv
pip install -r requirements.txt
```

3. Configure the application configuration (see config.py file).

4. Run the application:

```
gunicorn app:create_app
```
