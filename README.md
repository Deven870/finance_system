# 💰 Finance Tracker - Simple Money Management Backend

A simple, easy-to-use backend system to track your income and expenses. See your spending patterns, manage transactions, and get financial insights in one place.

## 🎯 What This Does

This is a **backend system** that lets you:

✅ **Record your money**
- Add income (salary, freelance work, investments)
- Add expenses (food, rent, entertainment)
- Organize with categories

✅ **See patterns in your spending**
- How much you spent this month
- Where most of your money goes
- Income vs. expenses comparison

✅ **Control who sees what**
- Some users can only view transactions
- Others can create new transactions
- Admins can manage everything

✅ **Work with other apps**
- Clean API that any app can use
- Easy testing through your browser
- Works with mobile apps, dashboards, etc.

## 🛠️ Built With (Simple Explanation)

| What | Tool | Why? |
|------|------|------|
| **Web Framework** | FastAPI | Fast, simple, generates API docs automatically |
| **Database** | SQLite | No setup needed, stores data locally |
| **Database Tool** | SQLAlchemy | Makes database operations simple with Python code |
| **Input Checking** | Pydantic | Makes sure data is correct before we use it |
| **Security** | JWT + Argon2 | Safe passwords and secure tokens for authentication |
| **Server** | Uvicorn | The engine that runs the web app |

## � Project Layout (What Goes Where)

```
finance_system/
│
├── 📄 main.py                          ← Start here! Runs the whole app
├── 📄 database.py                      ← Database connection stuff
├── 📄 dependencies.py                  ← Security checks for routes
├── 📄 seed_data.py                     ← Creates demo data for testing
├── 📄 requirements.txt                 ← List of packages to install
├── 📄 .env                             ← Configuration (secret keys, etc)
├── 📄 README.md                        ← This file!
│
├── 📁 models/                          ← Database table structures
│   ├── user.py                         (Who can use the system)
│   └── transaction.py                  (Records of money in/out)
│
├── 📁 schemas/                         ← Input/output validation
│   ├── user.py                         (What user data should look like)
│   └── transaction.py                  (What transaction data looks like)
│
├── 📁 routes/                          ← API endpoints (the "buttons" users click)
│   ├── auth.py                         (Login/register)
│   ├── transactions.py                 (Add/edit/delete money records)
│   └── analytics.py                    (See financial summaries)
│
├── 📁 services/                        ← Business logic (the brain)
│   ├── auth_service.py                 (Handle passwords & tokens)
│   └── analytics_service.py            (Calculate summaries)
│
├── 📁 venv/                            ← Python packages (ignore this)
└── 💾 finance_system.db                ← Where data is stored
```

## 🚀 Quick Start (5 Minutes)

### **Step 1: Download & Setup**

```bash
# Go to the project folder
cd finance_system

# Create a Python "workspace" (keeps packages separate)
python -m venv venv

# Activate it (turn it on)
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install everything you need
pip install -r requirements.txt
```

### **Step 2: Populate with Demo Data**

```bash
# Create the database with 3 test users and 75 sample transactions
python seed_data.py
```

You'll see something like:
```
✅ Created user: viewer@example.com (UserRole.VIEWER)
✅ Created user: analyst@example.com (UserRole.ANALYST)
✅ Created user: admin@example.com (UserRole.ADMIN)
✅ Created 75 demo transactions
```

### **Step 3: Start the Server**

```bash
# Run the app
python main.py
```

You should see:
```
INFO: Uvicorn running on http://0.0.0.0:8000
```

**That's it! The server is running!** 🎉

---

## 🌐 Using the Application

### **Option 1: Test in Your Browser (EASIEST)**

1. Open: **http://localhost:8000/docs**
2. You'll see an interactive menu of all features
3. Click on any feature to test it
4. No need for special tools!

### **Option 2: Using Command Line (cURL)**

```bash
# Login and get a token
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# You'll get back something like:
# {"access_token": "eyJ0eXAi...", "token_type": "bearer"}

# Use that token in other requests:
curl -H "Authorization: Bearer eyJ0eXAi..." \
  http://localhost:8000/transactions
```

## 📖 API Documentation

### **Interactive Testing (Best Way)**

Open your browser: **http://localhost:8000/docs**

This shows you everything you can do:
- Click any feature to see details
- Click "Try it out" to test it
- See real-world examples
- Check response formats

---

## 🔐 Login & Test Users

Three test accounts are included by default:

### **Viewer Account** (Can only see transactions)
```
Email:    viewer@example.com
Password: password123
```

### **Analyst Account** (Can see + create transactions)
```
Email:    analyst@example.com
Password: password123
```

### **Admin Account** (Can do everything)
```
Email:    admin@example.com
Password: password123
```

---

## 📝 How to Use (Step by Step)

### **Login Process**

1. Go to **http://localhost:8000/docs**
2. Find **POST /auth/login**
3. Enter email and password
4. Click "Execute"
5. Copy the "access_token" you get back

### **Make Requests**

1. Click the green **"Authorize"** button at the top
2. Paste: `Bearer YOUR_TOKEN_HERE`
3. Click "Authorize"
4. Now test other features!

---

## 💡 What Each Feature Does

### **Transactions** (Money Records)

| Action | What It Does |
|--------|-------------|
| `GET /transactions` | See all your money records |
| `POST /transactions` | Add a new transaction (admin/analyst only) |
| `PUT /transactions/{id}` | Edit a transaction (admin only) |
| `DELETE /transactions/{id}` | Remove a transaction (admin only) |

### **Analytics** (See Patterns)

| Feature | What It Shows |
|---------|--------------|
| `/analytics/summary` | Total income, expenses, balance |
| `/analytics/by-category` | How much you spent in each category |
| `/analytics/monthly` | Monthly breakdown |
| `/analytics/recent` | Your last 10 transactions |
| `/analytics/trends` | Spending insights |

## 👥 User Roles (What Can Each Person Do?)

### **👁️ Viewer** (Can only look)
- View their transactions
- See analytics & summaries
- **Cannot** create, edit, or delete

### **📊 Analyst** (Can view & create)
- View & create transactions
- See detailed analytics
- **Cannot** edit or delete other's transactions

### **🔑 Admin** (Can do everything)
- Create, view, edit, delete transactions
- Manage users
- Full system access

## � All API Features

### **🔑 Login & Register**
- `POST /auth/register` - Create new account
- `POST /auth/login` - Get access token

### **💸 Money Records**
- `GET /transactions` - See all records (with filters)
- `GET /transactions/{id}` - See one record
- `POST /transactions` - Add new record
- `PUT /transactions/{id}` - Update record
- `DELETE /transactions/{id}` - Remove record

### **📊 Financial Summary**
- `GET /analytics/summary` - Balance + income + expenses
- `GET /analytics/by-category` - Spending by category
- `GET /analytics/monthly` - Monthly trends
- `GET /analytics/recent` - Last 10 transactions
- `GET /analytics/trends` - Spending patterns

### **System**
- `GET /` - Welcome message
- `GET /health` - Check if API is running

## � Real Examples

### **Example 1: Login**

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com", "password":"password123"}'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 43200
}
```

---

### **Example 2: Add a Transaction**

First, get the token from login above. Then:

```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X POST "http://localhost:8000/transactions" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 45.99,
    "transaction_type": "expense",
    "category": "food",
    "date": "2026-04-02",
    "description": "Lunch at cafe"
  }'
```

---

### **Example 3: See Your Money Summary**

```bash
TOKEN="your_token_here"

curl -X GET "http://localhost:8000/analytics/summary" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "user_id": 1,
  "total_income": 15000.50,
  "total_expenses": 3200.75,
  "balance": 11799.75
}
```

---

### **Example 4: Filter Transactions**

```bash
# See all food expenses from March
curl -X GET "http://localhost:8000/transactions?category=food&start_date=2026-03-01&end_date=2026-03-31" \
  -H "Authorization: Bearer $TOKEN"
```

---

### **Example 5: See Category Breakdown**

```bash
curl -X GET "http://localhost:8000/analytics/by-category" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "user_id": 1,
  "income": {
    "salary": 12000,
    "freelance": 2500
  },
  "expenses": {
    "food": 450.25,
    "transport": 320,
    "utilities": 280
  }
}
```

## ✅ How to Test Everything

### **Using Your Browser (Easiest - No Setup Needed)**

1. Make sure the server is running: `python main.py`
2. Open: **http://localhost:8000/docs**
3. You'll see a list of all features
4. For each feature:
   - Click it to expand
   - Click "Try it out"
   - Fill in values
   - Click "Execute"
   - See the response

### **Test Workflow**

1. **Login** (top of the page)
   - Find `POST /auth/login`
   - Use `admin@example.com` / `password123`
   - Copy the `access_token`

2. **Authorize**
   - Click green "Authorize" button
   - Paste: `Bearer YOUR_TOKEN`
   - Click "Authorize"

3. **Try Any Feature**
   - Click on `GET /transactions`
   - Click "Try it out"
   - Click "Execute"
   - See your transactions!

---

## ⚙️ Configuration

Edit `.env` file to change settings:

```env
# Database file location
DATABASE_URL=sqlite:///./finance_system.db

# Secret key for tokens (change in production!)
SECRET_KEY=your-secret-key-change-in-production-min32chars

# Token algorithm (don't change unless you know what you're doing)
ALGORITHM=HS256

# How long tokens last (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## ✅ How to Test Everything

### **Using Your Browser (Easiest - No Setup Needed)**

1. Make sure the server is running: `python main.py`
2. Open: **http://localhost:8000/docs**
3. You'll see a list of all features
4. For each feature:
   - Click it to expand
   - Click "Try it out"
   - Fill in values
   - Click "Execute"
   - See the response

### **Test Workflow**

1. **Login** (top of the page)
   - Find `POST /auth/login`
   - Use `admin@example.com` / `password123`
   - Copy the `access_token`

2. **Authorize**
   - Click green "Authorize" button
   - Paste: `Bearer YOUR_TOKEN`
   - Click "Authorize"

3. **Try Any Feature**
   - Click on `GET /transactions`
   - Click "Try it out"
   - Click "Execute"
   - See your transactions!

---

## ⚙️ Configuration

Edit `.env` file to change settings:

```env
# Database file location
DATABASE_URL=sqlite:///./finance_system.db

# Secret key for tokens (change in production!)
SECRET_KEY=your-secret-key-change-in-production-min32chars

# Token algorithm (don't change unless you know what you're doing)
ALGORITHM=HS256

# How long tokens last (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🐛 If Something Goes Wrong

### **Common Issues**

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run: `pip install -r requirements.txt` |
| Port 8000 in use | Kill the process or use different port |
| Database errors | Delete `finance_system.db` and run `python seed_data.py` again |
| Token expired | Login again to get a new token |
| Access denied | Make sure you have the right role (use admin account for testing) |

### **Error Messages**

| Error | Meaning |
|-------|---------|
| `401 Unauthorized` | Your token is missing or expired - login again |
| `403 Forbidden` | You don't have permission - use admin account |
| `404 Not Found` | That transaction doesn't exist |
| `422 Validation Error` | Data format is wrong - check your JSON |

---

## 💾 Database Explained

The system stores data in **finance_system.db** - a file on your computer.

**Two tables:**

1. **users** - Who can log in
   - id, email, password (encrypted), name, role

2. **transactions** - Money records
   - id, user_id, amount, type, category, date, notes

**That's it!** No complex setup needed.

---

## 🔒 Security Notes

- ✅ Passwords are **never stored** - only encrypted versions
- ✅ Tokens **expire** - you have to login again
- ✅ Data is **validated** - wrong data is rejected
- ✅ Roles **protect features** - viewers can't delete
- ✅ Each user **only sees their data**

---

## 📊 Categories Available

### Income
- `salary` - Regular job
- `freelance` - Freelance work
- `investment` - Investment returns
- `other_income` - Other income

### Expenses  
- `food` - Groceries and dining
- `transport` - Travel and cars
- `utilities` - Electricity, water, internet
- `entertainment` - Movies, games, fun
- `healthcare` - Medical expenses
- `education` - Learning and courses
- `other_expense` - Other spending
- ✅ Seed data for testing

## 📚 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org)
- [Pydantic Validation](https://docs.pydantic.dev)
- [JWT Authentication](https://python-jose.readthedocs.io)

## 📄 License

This project is open source and available under the MIT License.

## 💡 Future Enhancements

- [ ] Budget planning and tracking
- [ ] Recurring transactions
- [ ] Data export (CSV/PDF)
- [ ] Multi-currency support
- [ ] Bank statement import
- [ ] Advanced charting/visualization API
- [ ] User-to-user transfers
- [ ] Transaction tagging system
- [ ] Mobile app integration
- [ ] Email notifications

---

## 📌 Key Takeaways

### **What This Project Shows**
✅ **Clean Code** - Organized, easy to understand, well structured  
✅ **Smart Design** - Separates concerns, reuses code effectively  
✅ **Works!** - All features tested and functional  
✅ **Secure** - Passwords encrypted, tokens validated, roles enforced  
✅ **Ready to Learn From** - Comments explain the "why"  
✅ **Easy to Extend** - Add new features without breaking existing ones  

### **Perfect For**
- Learning backend development
- Understanding API design
- Seeing role-based access in action
- Building your own finance app
- Portfolio project
- Interview preparation

### **Not For**
- Real money management (not production-ready)
- Millions of users (uses SQLite)
- Highly complex financial calculations
- Replacing real banking software

---

## 🤝 Questions?

### **Common Q&A**

**Q: Can I use this with a real database?**  
A: Yes! Replace SQLite with PostgreSQL or MySQL - just update connection strings.

**Q: How do I deploy this?**  
A: Use services like Heroku, AWS, or DigitalOcean. Google "deploy FastAPI" for guides.

**Q: Can I add more roles?**  
A: Yes! Edit `models/user.py` RoleEnum and add new role checking in `dependencies.py`.

**Q: How do I make a web interface?**  
A: This is just the backend. Build a React/Vue frontend that calls these APIs.

**Q: Is this safe for real money?**  
A: Not yet - needs more security, audit, and compliance testing for production use.

---

## 📚 Want to Learn More?

- **FastAPI** - https://fastapi.tiangolo.com (great docs!)
- **SQLAlchemy** - https://docs.sqlalchemy.org (database guide)
- **JWT Tokens** - https://jwt.io (understand tokens)
- **REST APIs** - Google "REST API best practices"
- **Python** - https://python.org (obviously!)

---

**🎉 You're ready to go! Start with `python main.py` and open http://localhost:8000/docs**