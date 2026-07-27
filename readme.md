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
│   │   ├── auth_routes.py        # Register / login / refresh / profile
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
| `customer`   | Public `/api/auth/register` endpoint      | Browse, cart, wishlist, checkout, pay, see personal dashboard |

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

You get `access_token` (and `refresh_token`) back from `POST /api/auth/login`.
Access tokens expire after 1 hour — use `POST /api/auth/refresh` with your
refresh token to get a new one without logging in again.

---

## 5. Full Endpoint Reference

### Auth (public)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Create a customer account |
| POST | `/api/auth/login` | Log in (any role) |
| POST | `/api/auth/refresh` | Get a new access token |
| GET  | `/api/auth/me` | Get your own profile |

### Products & Categories (public — no login needed)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/products` | Browse products (filters: `category_id`, `search`, `min_price`, `max_price`) |
| GET | `/api/products/<id>` | View one product |
| GET | `/api/products/categories` | List categories |

### Cart (customer only)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/cart` | View your cart |
| POST | `/api/cart/add` | Add a product `{product_id, quantity}` |
| PATCH | `/api/cart/<item_id>` | Update quantity `{quantity}` |
| DELETE | `/api/cart/<item_id>` | Remove item |

### Wishlist (customer only)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/wishlist` | View your wishlist |
| POST | `/api/wishlist/add` | Add a product `{product_id}` |
| DELETE | `/api/wishlist/<item_id>` | Remove item |
| POST | `/api/wishlist/<item_id>/move-to-cart` | Move item into your cart |

### Orders & Checkout (customer only)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/orders/checkout` | Turn your cart into an order `{shipping_address}` |
| GET | `/api/orders` | View your order history |
| GET | `/api/orders/<id>` | View one order in detail |

### Payment (customer only — mock gateway)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/payments/pay/<order_id>` | Pay for a pending order `{method}` |
| GET | `/api/payments/<order_id>` | View payment/receipt for an order |

### Admin Dashboard (admin only)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/admin/dashboard` | Admin stats: products, low stock, orders |
| POST | `/api/admin/products` | Create a product |
| PUT | `/api/admin/products/<id>` | Edit a product |
| DELETE | `/api/admin/products/<id>` | Deactivate a product |
| GET | `/api/admin/products` | List all products (incl. inactive) |
| GET | `/api/admin/orders` | View every customer order |
| PATCH | `/api/admin/orders/<id>/status` | Update order status `{status}` |

### Super Admin Dashboard (super admin only)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/superadmin/dashboard` | Store-wide stats + revenue |
| POST | `/api/superadmin/admins` | Create a new admin |
| GET | `/api/superadmin/admins` | List all admins |
| PATCH | `/api/superadmin/admins/<id>/toggle-active` | Activate/deactivate an admin |
| GET | `/api/superadmin/users` | List every user in the system |
| POST | `/api/superadmin/categories` | Create a category |
| DELETE | `/api/superadmin/categories/<id>` | Delete a category |

### Customer Dashboard (customer only)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/customer/dashboard` | Cart/wishlist counts, order totals, recent orders |

---

## 6. Example Flow (using curl)

```bash
# 1. Register a customer
curl -X POST http://127.0.0.1:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","email":"jane@example.com","password":"Passw0rd!"}'

# 2. Log in
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"jane@example.com","password":"Passw0rd!"}'
# copy the "access_token" from the response

# 3. Browse products
curl http://127.0.0.1:5000/api/products

# 4. Add a product to cart (replace TOKEN and product_id)
curl -X POST http://127.0.0.1:5000/api/cart/add \
  -H "Authorization: Bearer TOKEN" -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'

# 5. Checkout
curl -X POST http://127.0.0.1:5000/api/orders/checkout \
  -H "Authorization: Bearer TOKEN" -H "Content-Type: application/json" \
  -d '{"shipping_address": "12 Allen Avenue, Ikeja, Lagos"}'

# 6. Pay for the order (replace order_id)
curl -X POST http://127.0.0.1:5000/api/payments/pay/1 \
  -H "Authorization: Bearer TOKEN" -H "Content-Type: application/json" \
  -d '{"method": "card"}'
```

---

## 7. Notes on Design Decisions

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
