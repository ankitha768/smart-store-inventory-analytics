# Smart Store Inventory Analytics

A **Streamlit-first inventory and sales analytics application** built with Python. It provides an interactive portfolio dashboard for inventory monitoring, sales analytics, revenue tracking, and reorder alerts.

The repository also retains the original Django/REST implementation under `config/`, `inventory/`, `sales/`, and `analytics/` for reference and backend-oriented evaluation.

## 🚀 Streamlit deployment

The Streamlit app entry point is:

```text
streamlit_app.py
```

### Run locally

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run streamlit_app.py
```

Open the local URL shown by Streamlit, usually `http://localhost:8501`.

### Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Open Streamlit Community Cloud and create a new app.
3. Select repository: `ankitha768/smart-store-inventory-analytics`.
4. Select branch: `main`.
5. Set the main file to: `streamlit_app.py`.
6. Deploy.

No MySQL server or environment secret is required for the Streamlit portfolio demo. The deployed dashboard uses session-state sample data so it can run as a self-contained Python application.

## Features

- 📦 Inventory overview with category and product filters.
- 📊 Sales revenue and category analytics.
- 🚨 Automatic reorder alerts.
- 🧾 Record-sale workflow with stock validation.
- 💰 Revenue, transaction, product, and stock KPIs.
- 🐍 Python-only Streamlit deployment path.
- 🗃️ Original Django/REST implementation retained for backend reference.

## Screenshots

### Product dashboard
![Product overview](docs/screenshots/product-overview.svg)

### Inventory dashboard
![Inventory dashboard](https://raw.githubusercontent.com/ankitha768/smart-store-inventory-analytics/main/docs/screenshots/inventory-dashboard.svg)

### Analytics flow
![Analytics flow](https://raw.githubusercontent.com/ankitha768/smart-store-inventory-analytics/main/docs/screenshots/analytics.svg)

## Streamlit architecture

```mermaid
flowchart LR
A[Streamlit UI] --> B[Session State]
B --> C[Inventory Data]
B --> D[Sales Data]
C --> E[KPIs + Reorder Alerts]
D --> F[Revenue + Sales Analytics]
C --> G[Record Sale]
G --> B
```

## Project structure

```text
streamlit_app.py
requirements.txt
.streamlit/config.toml
docs/screenshots/
config/                 # original Django configuration
inventory/              # original Django inventory app
sales/                  # original Django sales app
analytics/              # original Django analytics app
templates/
fixtures/
tests/
```

## Legacy Django/API setup

The original Django implementation is retained separately from the Streamlit deployment path.

```bash
pip install -r requirements-django.txt
python manage.py migrate
python manage.py runserver
```

The legacy API includes JWT authentication, product/sales endpoints, and an analytics summary endpoint.

## Notes

- Streamlit deployment is intentionally self-contained and does not depend on MySQL.
- Streamlit session state is temporary; data entered during a session is not a permanent database record.
- The repository's visual assets are documentation mockups, not screenshots of a live deployed instance.
