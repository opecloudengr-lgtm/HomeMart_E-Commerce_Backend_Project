# HomeMart Backend

A mini e-commerce REST API built with **Flask*, **SQLAlchemy**, **Flask-Migrate**,
**Flask-JWT-Extended**, and **Marshmallow**. It supports three roles —
**Super Admin**, **Admin**, and **Customer** — each with their own dashboard
and permissions.

---

## 1. Project Structure

```
homemart/
├── app/
│   ├── __init__.py          # App factory: builds & configures the Flask app
│   ├── extensions.py        # Shared extension instances (db, jwt, ma, migrate)
│   ├── models/               # Database tables (SQLAlchemy models)
│   │   ├── user.py           # Users: super_admin / admin / customer
│   │   ├── category.py       # Product categories
│   │   ├── product.py        # Products
│   │   ├── cart.py           # Cart items
│   │   ├── wishlist.py       # Wishlist items
│   │   ├── order.py          # Orders + order items
│   │   └── payment.py        # Payments (mock gateway)
│   ├── schemas/               # Marshmallow schemas (model <-> JSON)
│   ├── routes/                 # All API endpoints, grouped by feature
│   │   ├── auth_routes.py        # Register / login / refresh / me
│   │   ├── superadmin_routes.py  # Super admin dashboard + manage admins/categories
│   │   ├── admin_routes.py       # Admin dashboard + manage products/orders
│   │   ├── customer_routes.py    # Customer dashboard
│   │   ├── product_routes.py     # Public product browsing
│   │   ├── cart_routes.py        # Cart actions
│   │   ├── wishlist_routes.py    # Wishlist actions
│   │   ├── order_routes.py       # Checkout + order history
│   │   └── payment_routes.py     # Mock payment
│   └── utils/
│       └── decorators.py     # @role_required() access-control decorator
├── config.py                 # App configuration (reads from .env)
├── run.py                    # Starts the dev server
├── seed.py                   # Creates the FIRST super admin account
├── requirements.txt
└── .env.example               # Copy to .env and fill in your own secrets
```

---

## 2. How the 3 Roles Work

All users live in ONE `users` table with a `role` column:

| Role         | Created by                              | Can do |
|--------------|------------------------------------------|--------|
| `super_admin`| `seed.py` (only once, directly on server) | Create/manage admins, manage categories, see store-wide dashboard |
| `admin`      | An existing super admin (via API)         | Create/manage products, view & update orders, see admin dashboard |
| `customer`   | Public `/auth/register` endpoint      | Browse, cart, wishlist, checkout, pay, see personal dashboard |

Every protected route is locked down with a `@role_required("role_name")`
decorator (see `app/utils/decorators.py`), so a customer token can never
call an admin-only endpoint, etc.

---

## 3. Setup Instructions

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create your .env file
cp .env.example .env
# then open .env and change the secret keys / super admin password

# 4. Initialize the database
flask --app run.py db init
flask --app run.py db migrate -m "initial tables"
flask --app run.py db upgrade

# 5. Create the first Super Admin account
python seed.py

# 6. Start the server
python run.py
```

The API will be running at `http://127.0.0.1:5000`.

---

## 4. Authentication

Every protected endpoint expects a header:

```
Authorization: Bearer <your_access_token>
```

You get `access_token` (and `refresh_token`) back from `POST /auth/login`.
Access tokens expire after 1 hour — use `POST /auth/refresh` with your
refresh token to get a new one without logging in again.

---

## 5. Full Endpoint Reference

### Auth (public)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Create a customer account (auto-sends an email-verification OTP) |
| POST | `/auth/login` | Log in (any role) |
| POST | `/auth/refresh` | Get a new access token |
| GET  | `/auth/me` | Get your own profile |
| POST | `/auth/send-otp` | Send/resend an OTP `{email, purpose}` — purpose is `email_verification` or `password_reset` |
| POST | `/auth/verify-email` | Confirm email with the OTP `{email, otp}` |
| POST | `/auth/reset-password` | Reset password with the OTP `{email, otp, new_password}` |
| POST | `/auth/logout` | Revoke your current access token (requires `Authorization` header) |
| POST | `/auth/logout-refresh` | Revoke your refresh token (send it as the Bearer token) |

### Products & Categories (public — no login needed)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/products` | Browse products (filters: `category_id`, `search`, `min_price`, `max_price`) |
| GET | `/products/<id>` | View one product |
| GET | `/products/categories` | List categories |

### Cart (customer only)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/cart` | View your cart |
| POST | `/cart/add` | Add a product `{product_id, quantity}` |
| PATCH | `/cart/<item_id>` | Update quantity `{quantity}` |
| DELETE | `/cart/<item_id>` | Remove item |

### Wishlist (customer only)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/wishlist` | View your wishlist |
| POST | `/wishlist/add` | Add a product `{product_id}` |
| DELETE | `/wishlist/<item_id>` | Remove item |
| POST | `/wishlist/<item_id>/move-to-cart` | Move item into your cart |

### Orders & Checkout (customer only)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/orders/checkout` | Turn your cart into an order `{shipping_address}` |
| GET | `/orders` | View your order history |
| GET | `/orders/<id>` | View one order in detail |

### Payment (customer only — mock gateway)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/payments/pay/<order_id>` | Pay for a pending order `{method}` |
| GET | `/payments/<order_id>` | View payment/receipt for an order |

### Admin Dashboard (admin only)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/admin/dashboard` | Admin stats: products, low stock, orders |
| POST | `/admin/products` | Create a product |
| PUT | `/admin/products/<id>` | Edit a product |
| DELETE | `/admin/products/<id>` | Deactivate a product |
| GET | `/admin/products` | List all products (incl. inactive) |
| GET | `/admin/orders` | View every customer order |
| PATCH | `/admin/orders/<id>/status` | Update order status `{status}` |

### Super Admin Dashboard (super admin only)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/superadmin/dashboard` | Store-wide stats + revenue |
| POST | `/superadmin/admins` | Create a new admin |
| GET | `/superadmin/admins` | List all admins |
| PATCH | `/superadmin/admins/<id>/toggle-active` | Activate/deactivate an admin |
| GET | `/superadmin/users` | List every user in the system |
| POST | `/superadmin/categories` | Create a category |
| DELETE | `/superadmin/categories/<id>` | Delete a category |

### Customer Dashboard (customer only)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/customer/dashboard` | Cart/wishlist counts, order totals, recent orders |

---

## 6. Mock Email OTP & Logout

**OTP (One-Time-Passcode):** There's no real email provider wired in
(nothing like Flask-Mail/SendGrid is in `requirements.txt`), so
"sending" an email is mocked in `app/utils/mailer.py` — it just prints
the code to your terminal, e.g.:

```
==================================================
📧  MOCK EMAIL SENT (no real email was sent)
To:      jane@example.com
Subject: Verify your HomeMart email
Body:    Your HomeMart OTP code is: 048213
         This code expires in 10 minutes.
==================================================
```

Copy that code from your terminal and use it with `/auth/verify-email`
or `/auth/reset-password`. To go live later, only the inside of
`send_otp_email()` needs to change — swap the `print()` calls for a real
API call to your email provider.

- **Verify email after registering:** `POST /auth/register` ->
  check your terminal for the code -> `POST /auth/verify-email`
- **Forgot password:** `POST /auth/send-otp` with
  `{"email": "...", "purpose": "password_reset"}` -> check terminal ->
  `POST /auth/reset-password` with the code + new password

**Logout:** JWTs are normally stateless (they stay valid until they
expire even if you "log out"). To make logout actually invalidate a
token immediately, `POST /auth/logout` stores that token's unique
ID in a `token_blocklist` table; every future request checks that table
first (see `app/__init__.py`), so a blocklisted token is rejected even
though it hasn't technically expired yet.

---

That's the correct approach. Test the API in the same order a real e-commerce system would be used.

The flow should be:

1. **Super Admin** → Create categories and admins.
2. **Admin** → Create products.
3. **Customer 1** → Register, verify email, shop, checkout, pay.
4. **Customer 2** → Register, verify email, shop.
5. Test authentication, refresh tokens, logout, authorization, and error cases.

---

# SESSION 1 — SUPER ADMIN

> The Super Admin account is assumed to already exist from `seed.py`.

## 1. Login

**POST**

```
http://127.0.0.1:5000/auth/login
```

Body

```json
{
    "email": "superadmin@homemart.com",
    "password": "SuperAdmin123!"
}
```

Save

```
access_token
refresh_token
```

---

## 2. Get Profile

**GET**

```
http://127.0.0.1:5000/auth/me
```

Headers

```
Authorization: Bearer SUPER_ADMIN_ACCESS_TOKEN
```

---

## 3. Dashboard

**GET**

```
http://127.0.0.1:5000/superadmin/dashboard
```

Headers

```
Authorization: Bearer SUPER_ADMIN_ACCESS_TOKEN
```

---

## 4. Create Categories

### Electronics

**POST**

```
http://127.0.0.1:5000/superadmin/categories
```

Headers

```
Authorization: Bearer SUPER_ADMIN_ACCESS_TOKEN
```

Body

```json
{
    "name": "Electronics"
}
```

---

### Fashion

```json
{
    "name": "Fashion"
}
```

---

### Groceries

```json
{
    "name": "Groceries"
}
```

---

### Furniture

```json
{
    "name": "Furniture"
}
```

---

### Phones

```json
{
    "name": "Phones"
}
```

---

## 5. Create Admin

**POST**

```
http://127.0.0.1:5000/superadmin/admins
```

Headers

```
Authorization: Bearer SUPER_ADMIN_ACCESS_TOKEN
```

Body

```json
{
    "name": "John Admin",
    "email": "admin@homemart.com",
    "password": "Admin123!"
}
```

---

## 6. View All Admins

**GET**

```
http://127.0.0.1:5000/superadmin/admins
```

---

## 7. View Users

**GET**

```
http://127.0.0.1:5000/superadmin/users
```

---

## 8. Refresh Token

**POST**

```
http://127.0.0.1:5000/auth/refresh
```

Headers

```
Authorization: Bearer SUPER_ADMIN_REFRESH_TOKEN
```

---

## 9. Logout

**POST**

```
http://127.0.0.1:5000/auth/logout
```

Headers

```
Authorization: Bearer SUPER_ADMIN_ACCESS_TOKEN
```

---

# SESSION 2 — ADMIN

---

## 1. Login

**POST**

```
http://127.0.0.1:5000/auth/login
```

Body

```json
{
    "email": "admin@homemart.com",
    "password": "Admin123!"
}
```

---

## 2. Dashboard

**GET**

```
http://127.0.0.1:5000/admin/dashboard
```

Headers

```
Authorization: Bearer ADMIN_ACCESS_TOKEN
```

---

# Create Products

Use the category IDs created earlier.

---

## Product 1

**POST**

```
http://127.0.0.1:5000/admin/products
```

```json
{
    "name": "iPhone 15 Pro",
    "description": "Apple flagship smartphone",
    "price": 1200,
    "stock": 15,
    "category_id": 5
}
```

---

## Product 2

```json
{
    "name": "Samsung Galaxy S25",
    "description": "Android flagship",
    "price": 950,
    "stock": 20,
    "category_id": 5
}
```

---

## Product 3

```json
{
    "name": "Dell XPS 15",
    "description": "High-performance laptop",
    "price": 1800,
    "stock": 10,
    "category_id": 1
}
```

---

## Product 4

```json
{
    "name": "Sony WH-1000XM6",
    "description": "Noise cancelling headphones",
    "price": 399,
    "stock": 30,
    "category_id": 1
}
```

---

## Product 5

```json
{
    "name": "Nike Air Max",
    "description": "Running shoes",
    "price": 180,
    "stock": 40,
    "category_id": 2
}
```

---

## Product 6

```json
{
    "name": "Office Chair",
    "description": "Ergonomic office chair",
    "price": 250,
    "stock": 12,
    "category_id": 4
}
```

---

## Product 7

```json
{
    "name": "Dining Table",
    "description": "6-Seater Wooden Table",
    "price": 650,
    "stock": 8,
    "category_id": 4
}
```

---

## Product 8

```json
{
    "name": "Rice 50kg",
    "description": "Premium long grain rice",
    "price": 95,
    "stock": 50,
    "category_id": 3
}
```

---

## View Products

**GET**

```
http://127.0.0.1:5000/admin/products
```

---

## Update Product

**PUT**

```
http://127.0.0.1:5000/admin/products/1
```

```json
{
    "price": 1150,
    "stock": 25
}
```

---

## View Orders

**GET**

```
http://127.0.0.1:5000/admin/orders
```

---

## Update Order Status

**PATCH**

```
http://127.0.0.1:5000/admin/orders/1/status
```

```json
{
    "status": "processing"
}
```

Later

```json
{
    "status": "shipped"
}
```

Later

```json
{
    "status": "delivered"
}
```

---

## Logout

**POST**

```
http://127.0.0.1:5000/auth/logout
```

---

# SESSION 3 — CUSTOMER 1

---

## Register

**POST**

```
http://127.0.0.1:5000/auth/register
```

```json
{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "password": "Passw0rd!"
}
```

---

## Verify Email

Check the terminal.

Example

```
483921
```

**POST**

```
http://127.0.0.1:5000/auth/verify-email
```

```json
{
    "email": "jane@example.com",
    "otp": "483921"
}
```

---

## Login

**POST**

```
http://127.0.0.1:5000/auth/login
```

```json
{
    "email": "jane@example.com",
    "password": "Passw0rd!"
}
```

---

## Customer Dashboard

**GET**

```
http://127.0.0.1:5000/customer/dashboard
```

---

## Browse Products

**GET**

```
http://127.0.0.1:5000/products
```

---

## Search

**GET**

```
http://127.0.0.1:5000/products?search=iphone
```

---

## Category Filter

**GET**

```
http://127.0.0.1:5000/products?category_id=5
```

---

## Price Filter

**GET**

```
http://127.0.0.1:5000/products?min_price=100&max_price=1000
```

---

## Product Details

**GET**

```
http://127.0.0.1:5000/products/1
```

---

## Add to Wishlist

**POST**

```
http://127.0.0.1:5000/wishlist/add
```

```json
{
    "product_id": 1
}
```

---

## View Wishlist

**GET**

```
http://127.0.0.1:5000/wishlist
```

---

## Move Wishlist Item to Cart

**POST**

```
http://127.0.0.1:5000/wishlist/1/move-to-cart
```

---

## Add Another Product

**POST**

```
http://127.0.0.1:5000/cart/add
```

```json
{
    "product_id": 3,
    "quantity": 1
}
```

---

## View Cart

**GET**

```
http://127.0.0.1:5000/cart
```

---

## Update Quantity

**PATCH**

```
http://127.0.0.1:5000/cart/1
```

```json
{
    "quantity": 3
}
```

---

## Checkout

**POST**

```
http://127.0.0.1:5000/orders/checkout
```

```json
{
    "shipping_address": "12 Allen Avenue, Ikeja, Lagos"
}
```

---

## View Orders

**GET**

```
http://127.0.0.1:5000/orders
```

---

## Order Details

**GET**

```
http://127.0.0.1:5000/orders/1
```

---

## Pay

**POST**

```
http://127.0.0.1:5000/payments/pay/1
```

```json
{
    "method": "card"
}
```

---

## Payment Receipt

**GET**

```
http://127.0.0.1:5000/payments/1
```

---

## Refresh Token

**POST**

```
http://127.0.0.1:5000/auth/refresh
```

---

## Logout

**POST**

```
http://127.0.0.1:5000/auth/logout
```

---

# SESSION 4 — CUSTOMER 2

## Register

**POST**

```
http://127.0.0.1:5000/auth/register
```

```json
{
    "name": "Michael Johnson",
    "email": "michael@example.com",
    "password": "Passw0rd!"
}
```

Verify the email with the OTP printed in the terminal.

---

## Login

**POST**

```
http://127.0.0.1:5000/auth/login
```

```json
{
    "email": "michael@example.com",
    "password": "Passw0rd!"
}
```

---

## Add Products

**POST**

```
http://127.0.0.1:5000/cart/add
```

```json
{
    "product_id": 2,
    "quantity": 2
}
```

---

**POST**

```
http://127.0.0.1:5000/cart/add
```

```json
{
    "product_id": 8,
    "quantity": 1
}
```

---

## Checkout

**POST**

```
http://127.0.0.1:5000/orders/checkout
```

```json
{
    "shipping_address": "5 Ring Road, Ibadan, Oyo"
}
```

---

## Pay

**POST**

```
http://127.0.0.1:5000/payments/pay/2
```

```json
{
    "method": "bank_transfer"
}
```

---

# FINAL AUTHORIZATION TESTS

These tests verify your role-based access control and authentication logic.

| Test                                          | Method                 | Endpoint                                     | Expected Result              |
| --------------------------------------------- | ---------------------- | -------------------------------------------- | ---------------------------- |
| Customer accesses `/admin/dashboard`          | GET                    | `http://127.0.0.1:5000/admin/dashboard`      | 403 Forbidden                |
| Customer accesses `/superadmin/dashboard`     | GET                    | `http://127.0.0.1:5000/superadmin/dashboard` | 403 Forbidden                |
| Admin accesses `/superadmin/dashboard`        | GET                    | `http://127.0.0.1:5000/superadmin/dashboard` | 403 Forbidden                |
| No token on `/cart`                           | GET                    | `http://127.0.0.1:5000/cart`                 | 401 Unauthorized             |
| Expired access token                          | Any protected endpoint | `http://127.0.0.1:5000/...`                  | 401 Unauthorized             |
| Refresh with valid refresh token              | POST                   | `http://127.0.0.1:5000/auth/refresh`         | 200 OK with new access token |
| Reuse revoked access token after logout       | GET                    | `http://127.0.0.1:5000/auth/me`              | 401 Unauthorized             |
| Delete inactive product as customer           | DELETE                 | `http://127.0.0.1:5000/admin/products/1`     | 403 Forbidden                |
| Checkout with an empty cart                   | POST                   | `http://127.0.0.1:5000/orders/checkout`      | 400 Bad Request              |
| Add a nonexistent product (`product_id: 999`) | POST                   | `http://127.0.0.1:5000/cart/add`             | 404 Not Found                |

This sequence exercises every major API in a realistic order: bootstrap the system as **Super Admin**, populate the catalog as **Admin**, complete full shopping journeys as **Customers**, and finish with authentication and authorization edge-case tests.
