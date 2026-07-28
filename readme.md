# HomeMart Backend

A mini e-commerce REST API built with **Flask**, **SQLAlchemy**, **Flask-Migrate**,
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

## 7. Example Flow (using curl)

```bash
# 1. Register a customer
curl -X POST http://127.0.0.1:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","email":"jane@example.com","password":"Passw0rd!"}'

# 2. Log in
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"jane@example.com","password":"Passw0rd!"}'
# copy the "access_token" from the response

# 3. Browse products
curl http://127.0.0.1:5000/products

# 4. Add a product to cart (replace TOKEN and product_id)
curl -X POST http://127.0.0.1:5000/cart/add \
  -H "Authorization: Bearer TOKEN" -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'

# 5. Checkout
curl -X POST http://127.0.0.1:5000/orders/checkout \
  -H "Authorization: Bearer TOKEN" -H "Content-Type: application/json" \
  -d '{"shipping_address": "12 Allen Avenue, Ikeja, Lagos"}'

# 6. Pay for the order (replace order_id)
curl -X POST http://127.0.0.1:5000/payments/pay/1 \
  -H "Authorization: Bearer TOKEN" -H "Content-Type: application/json" \
  -d '{"method": "card"}'

# 7. Verify your email (copy the code printed in your server terminal)
curl -X POST http://127.0.0.1:5000/auth/verify-email \
  -H "Content-Type: application/json" \
  -d '{"email": "jane@example.com", "otp": "048213"}'

# 8. Log out (revokes the access token you're sending)
curl -X POST http://127.0.0.1:5000/auth/logout \
  -H "Authorization: Bearer TOKEN"
```

---

## 8. Notes on Design Decisions

- **One `users` table, one `role` column** — simpler than 3 separate
  tables since all account types share the same core fields.
- **Prices stored as `Numeric`, not `Float`** — avoids floating-point
  rounding errors with money.
- **Order items snapshot the price at purchase time** — so a later price
  change by an admin never rewrites a customer's past receipt.
- **Products are soft-deleted** (`is_active=False`), never hard-deleted —
  keeps old orders valid and intact.
- **Payment is mocked** — swap the logic inside `pay_for_order()` in
  `payment_routes.py` for a real gateway (Stripe/Paystack/Flutterwave)
  when you're ready to go live; nothing else needs to change.
- **Super admins are never created via a public endpoint** — only through
  `seed.py`, run directly on the server, to prevent privilege escalation.
- **OTPs are single-use and time-limited** (10 minutes) — each `Otp` row
  has an `is_used` flag and `expires_at`, so a code can't be replayed or
  used after it goes stale.
- **`/send-otp` gives the same response whether or not the email exists**
  — this stops the endpoint being used to check which emails are
  registered on the platform (a common security leak in "forgot
  password" flows).
- **Logout uses a token blocklist, not just deleting the token
  client-side** — deleting a token on the frontend doesn't stop someone
  who already copied it from still using it; the server-side blocklist
  actually revokes it.
