import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Smart Store Inventory Analytics",
    page_icon="📦",
    layout="wide",
)

DEFAULT_PRODUCTS = pd.DataFrame(
    [
        {"SKU": "SKU-1001", "Product": "Wireless Mouse", "Category": "Accessories", "Price": 799.0, "Stock": 18, "Reorder Level": 10},
        {"SKU": "SKU-1002", "Product": "Mechanical Keyboard", "Category": "Accessories", "Price": 2499.0, "Stock": 7, "Reorder Level": 8},
        {"SKU": "SKU-1003", "Product": "USB-C Hub", "Category": "Accessories", "Price": 1599.0, "Stock": 12, "Reorder Level": 6},
        {"SKU": "SKU-1004", "Product": "27-inch Monitor", "Category": "Displays", "Price": 18999.0, "Stock": 4, "Reorder Level": 5},
        {"SKU": "SKU-1005", "Product": "Webcam", "Category": "Cameras", "Price": 3299.0, "Stock": 22, "Reorder Level": 8},
        {"SKU": "SKU-1006", "Product": "Laptop Stand", "Category": "Accessories", "Price": 1199.0, "Stock": 15, "Reorder Level": 5},
    ]
)

DEFAULT_SALES = pd.DataFrame(
    [
        {"Date": "2026-09-24", "SKU": "SKU-1001", "Product": "Wireless Mouse", "Quantity": 3, "Unit Price": 799.0},
        {"Date": "2026-09-25", "SKU": "SKU-1002", "Product": "Mechanical Keyboard", "Quantity": 2, "Unit Price": 2499.0},
        {"Date": "2026-09-26", "SKU": "SKU-1004", "Product": "27-inch Monitor", "Quantity": 1, "Unit Price": 18999.0},
        {"Date": "2026-09-27", "SKU": "SKU-1005", "Product": "Webcam", "Quantity": 4, "Unit Price": 3299.0},
        {"Date": "2026-09-28", "SKU": "SKU-1003", "Product": "USB-C Hub", "Quantity": 2, "Unit Price": 1599.0},
    ]
)

if "products" not in st.session_state:
    st.session_state.products = DEFAULT_PRODUCTS.copy()
if "sales" not in st.session_state:
    st.session_state.sales = DEFAULT_SALES.copy()

products = st.session_state.products
sales = st.session_state.sales.copy()
sales["Revenue"] = sales["Quantity"] * sales["Unit Price"]

st.title("📦 Smart Store Inventory Analytics")
st.caption("Streamlit portfolio dashboard • inventory, sales, revenue and reorder monitoring")

with st.sidebar:
    st.header("Filters")
    categories = sorted(products["Category"].unique())
    selected_categories = st.multiselect("Category", categories, default=categories)
    search = st.text_input("Search product or SKU", placeholder="e.g. keyboard")
    st.divider()
    st.info("This Streamlit version uses local session data, so it deploys without an external database.")

filtered = products[products["Category"].isin(selected_categories)].copy()
if search.strip():
    q = search.strip().lower()
    filtered = filtered[
        filtered["Product"].str.lower().str.contains(q)
        | filtered["SKU"].str.lower().str.contains(q)
    ]

reorder_count = int((filtered["Stock"] <= filtered["Reorder Level"]).sum())
units = int(filtered["Stock"].sum())
revenue = float(sales["Revenue"].sum())
sales_count = int(len(sales))

m1, m2, m3, m4 = st.columns(4)
m1.metric("Products", len(filtered))
m2.metric("Units in Stock", f"{units:,}")
m3.metric("Sales Transactions", sales_count)
m4.metric("Revenue", f"₹{revenue:,.0f}")

st.subheader("Inventory overview")
left, right = st.columns([2, 1])
with left:
    display = filtered.copy()
    display["Status"] = display.apply(
        lambda r: "🔴 Reorder" if r["Stock"] <= r["Reorder Level"] else "🟢 Healthy",
        axis=1,
    )
    st.dataframe(display, use_container_width=True, hide_index=True)
with right:
    st.markdown("### Reorder alerts")
    alerts = filtered[filtered["Stock"] <= filtered["Reorder Level"]]
    if alerts.empty:
        st.success("No reorder alerts.")
    else:
        for _, row in alerts.iterrows():
            st.warning(f"**{row['Product']}** — {int(row['Stock'])} left (reorder at {int(row['Reorder Level'])})")

st.subheader("Sales analytics")
c1, c2 = st.columns(2)
with c1:
    revenue_by_date = sales.groupby("Date", as_index=True)["Revenue"].sum()
    st.line_chart(revenue_by_date, height=280)
with c2:
    category_revenue = (
        sales.merge(products[["SKU", "Category"]], on="SKU", how="left")
        .groupby("Category")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(category_revenue, height=280)

st.subheader("Record a sale")
with st.form("sale_form", clear_on_submit=True):
    sku = st.selectbox(
        "Product",
        products["SKU"],
        format_func=lambda x: f"{x} — {products.loc[products['SKU'].eq(x), 'Product'].iloc[0]}",
    )
    quantity = st.number_input("Quantity", min_value=1, max_value=100, value=1, step=1)
    submitted = st.form_submit_button("Record sale", type="primary")

if submitted:
    idx = st.session_state.products.index[st.session_state.products["SKU"].eq(sku)][0]
    available = int(st.session_state.products.at[idx, "Stock"])
    if quantity > available:
        st.error(f"Only {available} units are available.")
    else:
        st.session_state.products.at[idx, "Stock"] = available - quantity
        product_name = st.session_state.products.at[idx, "Product"]
        unit_price = float(st.session_state.products.at[idx, "Price"])
        new_sale = pd.DataFrame(
            [{
                "Date": pd.Timestamp.now().strftime("%Y-%m-%d"),
                "SKU": sku,
                "Product": product_name,
                "Quantity": quantity,
                "Unit Price": unit_price,
            }]
        )
        st.session_state.sales = pd.concat([st.session_state.sales, new_sale], ignore_index=True)
        st.success(f"Recorded {quantity} × {product_name}.")
        st.rerun()

st.caption("Portfolio demo: Streamlit Community Cloud can run this app directly from the repository.")
