 
# Cafe Management System ☕


This project is ideal for learning about:
- GUI development with Tkinter  
- Database integration with MySQL  
- CRUD operations in real-world applications  

---


---



## ⚙️ Installation


### 1. Install dependencies  
Make sure you have **Python 3.x** installed. Install required packages:  
```bash
pip install mysql-connector-python
```

### 2. Set up MySQL  
Ensure that **MySQL Server** is installed and running on your system.  

---

## 🗄 Database Setup

1. Open your MySQL Workbench or terminal.  
2. Run the SQL script (`create_database.sql` or from screenshot above):  
   ```sql
   CREATE DATABASE IF NOT EXISTS cafe_db;
   USE cafe_db;

   CREATE TABLE IF NOT EXISTS cafe_orders (
       order_id INT PRIMARY KEY,
       customer_name VARCHAR(255),
       item VARCHAR(255),
       price DECIMAL(10, 2)
   );

   INSERT INTO cafe_orders (order_id, customer_name, item, price) VALUES
   (1, 'John Doe', 'Coffee', 5.00),
   (2, 'Jane Smith', 'Sandwich', 7.50),
   (3, 'Alice Johnson', 'Tea', 3.75);
   

3. Update your MySQL password in `cafe_management.py`:
   ```python
   password="YOUR_PASSWORD"
   

---

## ▶️ Usage

Run the Python script:  
```bash
python cafe_management.py
```

The GUI will open where you can:  
- Add orders by filling in the fields and clicking **Add**  
- Update selected orders by clicking **Update**  
- Delete an order with **Delete**  
- Refresh the order list with **Refresh**  

---

## 📦 Dependencies
- **Python 3.x**  
- **Tkinter** (comes with Python)  
- **mysql-connector-python**  

Install via:  bash
pip install mysql-connector-python


---

## 🔧 Configuration
In `cafe_management.py`, update the following for your MySQL setup:
```python
host="localhost",
user="root",
password="YOUR_PASSWORD",  
database="cafe_db"
```

---


## 👨‍💻 Contributors
- vedrajmane-vedcodes

---

  
