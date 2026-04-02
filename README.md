# 💰 Finance Tracker API

**A simple, clean Python backend to manage your money.**

This is a personal finance tracker built with FastAPI. It lets users:
- 📝 Track income and expenses
- 📊 See financial summaries and trends
- 🔐 Different access levels for different users
- 🔍 Find transactions by date, category, or type

No need to understand the technical jargon - the API does the heavy lifting while you focus on your finances.

## 🎯 What This Project Does

**Core Idea:** A backend system that lets users track their spending and income, see where their money goes, and understand their financial patterns.

**Who Can Use It:**
- **Viewers** - Can only look at their transactions (read-only, safe access)
- **Analysts** - Can add transactions and see detailed breakdowns
- **Admins** - Can manage everything (create, edit, delete records)

**What It Tracks:**
- Income (salary, freelance work, investments)
- Expenses (food, rent, shopping, etc.)
- Dates for each transaction
- Categories to organize spending
- Notes to remember why you spent money

## 🛠️ Tech Stack (Made Simple)

| What | Why | Human Explanation |
|------|-----|-------------------|
| **FastAPI** | Fast, modern | Web framework that handles HTTP requests |
| **SQLite** | Simple storage | Database that lives in one file (easy!) |
| **SQLAlchemy** | Database tool | Lets us work with data using Python instead of SQL |
| **JWT Tokens** | Secure login | Each user gets a token to prove they're logged in |
| **Pydantic** | Validation | Checks that data is correct before saving |

## � Project Layout (Where Everything Lives)

```
finance_system/
├── main.py                 ← Start here (the main app)
├── database.py             ← Connects to the database
├── dependencies.py         ← Checks if user is logged in
├── seed_data.py            ← Creates demo test data
│
├── models/                 ← How data is structured
│   ├── user.py            (User accounts & roles)
│   └── transaction.py     (Income & expense records)
│
├── schemas/               ← Rules for accepting data
│   ├── user.py           (User input rules)
│   └── transaction.py    (Transaction input rules)
│
├── routes/                ← API endpoints (what users call)
│   ├── auth.py           (Login & sign up)
│   ├── transactions.py   (Add/view/edit transactions)
│   └── analytics.py      (See summaries & trends)
│
└── services/              ← The logic that makes it work
    ├── auth_service.py   (Login logic)
    └── analytics_service.py (Summary calculations)
```

**Simple Explanation:**
- **models/** = The shape of your data
- **schemas/** = The rules for data going in and out
- **routes/** = The doors for users to enter
- **services/** = The brain that does the work

## 🚀 Get Started in 3 Minutes

### **Step 1: Download & Setup** (one-time only)

```bash
# Go to the project folder
cd finance_system

# Create a "sandbox" for this project (keeps it isolated)
python -m venv venv

# Activate the sandbox
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install everything needed
pip install -r requirements.txt
```

### **Step 2: Create Demo Data** (one-time only)

```bash
python seed_data.py
```

This creates a database with:
- 3 test users (viewer, analyst, admin)
- 75 sample transactions
- Ready to test immediately

### **Step 3: Start the Server**

```bash
python main.py
```

You should see:
```
Starting Finance System API
📖 API Docs:     http://localhost:8000/docs
🔑 ReDoc:        http://localhost:8000/redoc
```

**✅ Done! Your API is live!**

## 🌐 Test the API (Easy Way!)

### **Open This in Your Browser**

```
http://localhost:8000/docs
```

You'll see an **interactive playground** where you can:
- ✅ See all available endpoints
- ✅ Click "Try it out" on any endpoint
- ✅ Type in values and test immediately
- ✅ See responses in real-time

**No coding needed!** It's like PostMan but built-in.

### **First Time? Do This:**

1. Scroll down to **POST /auth/login**
2. Click **"Try it out"**
3. Enter one of these:
   ```json
   {
     "email": "admin@example.com",
     "password": "password123"
   }
   ```
4. Click **"Execute"**
5. Copy the `access_token` from the response
6. Click the green **"Authorize"** button at the top
7. Paste: `Bearer <your-token>`
8. Now you can test any endpoint!

### **Endpoints to Try**

| What | Endpoint |
|------|----------|
| See all transactions | GET /transactions |
| Add a transaction | POST /transactions |
| Financial summary | GET /analytics/summary |
| Spending by category | GET /analytics/by-category |
| Monthly trends | GET /analytics/monthly |
| Recent activity | GET /analytics/recent |

## 🔐 Login & Permissions

### **Three Types of Users**

#### 👁️ **Viewer** (Read Only)
- Can view their own transactions
- Can see summaries and analytics
- **Cannot** create, edit, or delete
- **Best for:** Reading-only access

#### 👨‍💼 **Analyst** (Create & Analyze)
- Can view transactions
- Can add new transactions
- Can see detailed analytics
- **Cannot** edit or delete other's things
- **Best for:** Someone who enters data

#### 👨‍💻 **Admin** (Full Control)
- Can do EVERYTHING
- Create, edit, delete transactions
- Manage users
- See all data
- **Best for:** Administrators

### **Demo Accounts Ready to Use**

Just copy and paste these into the login form:

```
Viewer Account:
  Email:    viewer@example.com
  Password: password123

Analyst Account:
  Email:    analyst@example.com
  Password: password123

Admin Account:
  Email:    admin@example.com
  Password: password123
```

**🚨 Important:** These are demo accounts for testing only. In production, change the passwords!

## 🎯 What Each Role Can Do

```
                VIEWER   ANALYST   ADMIN
View own txns    ✅       ✅       ✅
Create txns      ❌       ✅       ✅
Edit txns        ❌       ❌       ✅
Delete txns      ❌       ❌       ✅
View analytics   ✅       ✅       ✅
Manage users     ❌       ❌       ✅
```

**Example:** A viewer tries to create a transaction → API says "Nope, not allowed!"

## 📡 All Available Endpoints

### **Login (Don't Need Token)**
- `POST /auth/register` - Sign up a new account
- `POST /auth/login` - Log in and get a token

### **View Your Transactions (Everyone)**
- `GET /transactions` - See all your transactions
  - Can filter by: type (income/expense), category, date range
  
### **Create/Edit/Delete (Admin & Analyst)**
- `POST /transactions` - Add a new transaction
- `PUT /transactions/{id}` - Change a transaction (admin only)
- `DELETE /transactions/{id}` - Remove a transaction (admin only)

### **See Your Money Summary (Everyone)**
- `GET /analytics/summary` - Quick overview (total income, expenses, balance)
- `GET /analytics/by-category` - How much in each category
- `GET /analytics/monthly` - Monthly view
- `GET /analytics/recent` - Last 10 transactions
- `GET /analytics/trends` - Insights (averages, top categories)

### **System Check**
- `GET /` - Is the API running?
- `GET /health` - Detailed health status

## � Real-World Examples

### **1. Login & Get a Token**

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "password123"
  }'
```

**Response:** You get a token like this:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 43200
}
```

**Copy that token!** You'll use it for all other requests.

### **2. List Your Transactions**

```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X GET "http://localhost:8000/transactions" \
  -H "Authorization: Bearer $TOKEN"
```

### **3. Add a New Expense**

```bash
curl -X POST "http://localhost:8000/transactions" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 45.99,
    "transaction_type": "expense",
    "category": "food",
    "date": "2026-04-02",
    "description": "Groceries"
  }'
```

### **4. See Your Balance**

```bash
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

### **5. Filter Transactions**

Show only expenses from January-February:
```bash
curl -X GET "http://localhost:8000/transactions?transaction_type=expense&start_date=2026-01-01&end_date=2026-02-28" \
  -H "Authorization: Bearer $TOKEN"
```

### **6. See Breakdown by Category**

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
    "rent": 1200,
    "utilities": 150
  }
}
```

### **7. See Monthly Trends**

```bash
curl -X GET "http://localhost:8000/analytics/monthly" \
  -H "Authorization: Bearer $TOKEN"
```

## 🧪 Easiest Way to Test (Swagger UI)

If you don't want to use the command line, just use the web interface!

1. Go to: `http://localhost:8000/docs`
2. Click any endpoint
3. Click "Try it out"
4. Fill in the values
5. Click "Execute"
6. See the response immediately

**That's it!** No terminal knowledge needed.

## 🛡️ Security Features

- **Password Hashing**: Bcrypt with automatic hashing
- **JWT Tokens**: Signed tokens with 30-minute expiration
- **Role-Based Guards**: Middleware checks permissions before execution
- **Input Validation**: Pydantic schemas reject malformed data
- **Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **CORS**: Configurable Cross-Origin Resource Sharing

## ⚙️ Configuration

Edit `.env` file to customize:

```env
DATABASE_URL=sqlite:///./finance_system.db    # Database connection
SECRET_KEY=your-secret-key-32-chars-min       # JWT signing key
ALGORITHM=HS256                               # JWT algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=30                # Token expiration
```

**Important**: Change `SECRET_KEY` in production to a secure 32+ character string.

## 🐛 Debugging & Logging

The API includes detailed logging:

```bash
# Run with debug mode
python main.py  # Already in debug/reload mode

# View logs
# All requests and responses are logged to console
```

## 📝 Error Handling

API returns proper HTTP status codes:

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 201 | Resource created |
| 400 | Bad request (validation failed) |
| 401 | Unauthorized (invalid/missing token) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Resource not found |
| 422 | Validation error (malformed data) |

Example error response:
```json
{
  "detail": "Only admins can delete transactions"
}
```

## 🧬 Database Schema

### Users Table
- `id` (Primary Key)
- `email` (Unique)
- `hashed_password`
- `full_name`
- `role` (viewer, analyst, admin)
- `is_active` (0 = inactive, 1 = active)
- `created_at`, `updated_at`

### Transactions Table
- `id` (Primary Key)
- `user_id` (Foreign Key → Users)
- `amount` (Positive decimal)
- `transaction_type` (income, expense)
- `category` (salary, food, etc.)
- `date` (Transaction date)
- `description`, `notes`
- `created_at`, `updated_at`

## 📊 Categories

### Income Categories
- `salary` - Regular salary/wages
- `freelance` - Freelance work
- `investment` - Investment returns
- `other_income` - Miscellaneous income

### Expense Categories
- `food` - Groceries and dining
- `transport` - Transportation costs
- `utilities` - Electric, water, internet
- `entertainment` - Movies, games, hobbies
- `healthcare` - Medical expenses
- `education` - Learning and courses
- `other_expense` - Miscellaneous

## 🚦 What's Tested

The project demonstrates:
- ✅ Clean code architecture (separation of concerns)
- ✅ Proper async/await patterns
- ✅ Role-based access control
- ✅ JWT authentication
- ✅ Database modeling with SQLAlchemy
- ✅ Input validation with Pydantic
- ✅ Error handling and HTTP status codes
- ✅ Business logic (analytics, summaries)
- ✅ API documentation (Swagger/ReDoc)
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