# Django Stripe Shop

- A simple Django demo shop using Stripe Checkout for payment integration. This project includes a single-page shop with three products, quantity selection, order management, and user authentication (signup/login).

- Note: Stripe may not be available in some regions. For development and testing, you can use Stripe test keys.

---

# Features

- User authentication (signup, login, logout)

- Single-page shop UI with 3 products

- Quantity selection and "Buy" button

- Stripe Checkout integration (redirect to Stripe-hosted page)

- Order management (PENDING / PAID)

- Prevents double charges / duplicate orders

- Admin panel to manage products and orders

- Displays orders tied to user session

---

# Project Structure
django-stripe-shop/
├── shop/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── stripe_shop/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── templates/
│   └── shop/
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       └── signup.html
├── .env
├── db.sqlite3
├── manage.py
└── requirements.txt

---

# Installation / Setup

1. Clone the repo:
```
git clone <repo_url>
cd django-stripe-shop
```

2. Create a Python virtual environment:
```
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

3. Install dependencies:
```
pip install --upgrade pip
pip install -r requirements.txt
```

4. Create a .env file based on .env.example:
```
- Django
DJANGO_SECRET_KEY=replace-me-with-a-secret-key
DJANGO_DEBUG=True

- Database
DATABASE_URL=sqlite:///db.sqlite3

- Stripe (test keys for development)
STRIPE_PUBLISHABLE_KEY=pk_test_51XXXXXX
STRIPE_SECRET_KEY=sk_test_51XXXXXX
STRIPE_WEBHOOK_SECRET=whsec_testsecret

- Site URL
SITE_URL=http://localhost:8000
```

- You can use SQLite for testing (DATABASE_URL=sqlite:///db.sqlite3) if you do not have Postgres.

5. Apply migrations and create superuser:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

6. Seed initial products:
```
python manage.py shell

from shop.models import Product
Product.objects.create(name="Product A", price_cents=1999)
Product.objects.create(name="Product B", price_cents=2999)
Product.objects.create(name="Product C", price_cents=3999)
exit()
```

7. Running the Development Server
```
python manage.py runserver
```


Open http://localhost:8000
 to see the shop.

Admin panel: http://localhost:8000/admin

# Stripe Integration

- Uses Stripe Checkout (redirect flow)

- Stripe session ID stored in Order model to prevent duplicate charges

- Webhook endpoint /webhook/ marks orders as PAID

- Success URL: /success/

- Cancel URL: /

For local testing with Stripe, install Stripe CLI
 and forward webhooks:
```
stripe listen --forward-to localhost:8000/webhook/
```
Note: This project was designed to integrate with Stripe Checkout (test mode) as required in the assignment.
However, Stripe accounts are not generally available in India (they are invite-only), which means I could not generate real test API keys (pk_test_xxx, sk_test_xxx) to perform live test transactions.

- Because of this restriction, I implemented a mock Stripe flow that:

- Accepts product quantities from the user.

- Creates an order and marks it as PAID immediately after “Buy” is clicked.

- Prevents duplicate submissions and broken refresh states.

- Shows the paid order on the same page (like a real checkout).

## How This Maps to Real Stripe Flow

- If Stripe test keys were available, the flow would work like this:

User selects quantities and clicks Buy
→ Django creates an Order in PENDING state.

Checkout Session creation
→ Backend calls stripe.checkout.Session.create(...) with order details.

Redirect to Stripe-hosted Checkout
→ User enters test card details (e.g., 4242 4242 4242 4242).

On success
→ Stripe redirects back with a session_id.
→ Django verifies session and marks the order PAID.

My Orders list updates
→ Same-page UX shows the paid order.

This logic is already coded and ready — only the Stripe keys are missing.

## Stripe CLI (Optional)

- Normally, with Stripe CLI and test keys, we could:

- Run stripe listen --forward-to localhost:8000/webhook/ to forward webhook events.

- Use stripe trigger checkout.session.completed to simulate a successful payment.

- Again, this requires valid Stripe test keys, which are not currently available in India.

# Preventing Duplicate Charges

Client-side: disables "Buy" button after first click

Server-side: orders tied to session key; reuse pending order

Stripe session: unique stripe_session_id per order

Webhook: authoritative confirmation of payment

# Templates

base.html – Base layout

index.html – Product list & orders

signup.html – User registration

login.html – User login

# Requirements
Django>=4.2
psycopg2-binary>=2.9
stripe>=6.0
python-dotenv>=1.0
dj-database-url>=1.0
gunicorn>=20.1

---

# AI Assistance

ChatGPT was used for planning app structure and providing example code.

All code was reviewed and manually tested.

# Time Spent

8 hours 



