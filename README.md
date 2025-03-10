# 🛍️ Django E-commerce Project
## **Deployed [Here](refresh.up.railway.app)**


A **full-featured E-commerce web application** built with Django, PostgreSQL, and Stripe for online transactions.  
This project includes **cart management, checkout with Stripe, real-time updates with AJAX & HTMX, background tasks with Celery, and webhook integrations.**

---

## **🚀 Features**
✅ **User Authentication** (Register, Login, Logout, Profile Management)  
✅ **Cart Management** (Add, Remove, Update Items in Cart)  
✅ **Secure Checkout with Stripe** (Credit Card Payments)  
✅ **Webhooks for Payment Processing** (Real-time order status updates)  
✅ **Asynchronous Background Tasks** (Celery + Redis)  
✅ **AJAX & HTMX for Dynamic UI** (Real-time cart & checkout updates)  
✅ **Pagination for Products & Orders**  
✅ **PostgreSQL Database Integration** (Production-Ready)  
✅ **Admin Dashboard** (Manage Users, Orders, and Products)  
✅ **Django REST Framework API** (Expose API Endpoints for Products & Orders)  

---

## **🛠️ Technologies Used**
- **Django** (Backend Framework)
- **Django REST Framework** (API Development)
- **PostgreSQL** (Database)
- **Celery + Redis** (Background Task Processing)
- **HTMX & AJAX** (Dynamic UI Updates)
- **Stripe** (Payment Gateway)
- **Webhooks** (For Real-Time Payment & Order Updates)
- **Bootstrap** (Responsive UI)
- **Gunicorn & Nginx** (Production Deployment)
- **Docker & Docker Compose** (Optional Containerization)

---

## **📦 Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/ThisisAngelina/ecommerce.git
cd ecommerce
```

### **2️⃣ Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**
```bash
cd .. # Go back to the root directory
pip install -r requirements.txt
```
### **4️⃣ Configure Environment Variables**

See the sampleenv.txt file for the variables your .env file must include

### **5️⃣ Populate the database**

In settings.py, specify sqlite3 as your database

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",  # Stores the database file in the project root
    }
}
```

You can then upload sample products manually or user the **faker** library.


### **6️⃣ Apply Migrations & Create Superuser**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### **7️⃣ Run Redis broker, Celery Worker, and Stripe webhook connections**
```bash
stripe listen --forward-to localhost:8000/payment/webhook-stripe/
redis-server
celery -A ecommerce worker -l info
```

Set your DEBUG=TRUE in settings.py and run your local server:
```bash
python manage.py runserver
```

## **📜 License**

This project is licensed under the MIT License.
