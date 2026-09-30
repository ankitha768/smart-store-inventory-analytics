import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Kirana Shop Inventory Analytics",
    page_icon="🛒",
    layout="wide",
)

DEFAULT_PRODUCTS = pd.DataFrame(
    [
        {"SKU": "KIR-1001", "Product": "Sona Masoori Rice", "Category": "Rice & Grains", "Unit": "kg", "Price": 62.0, "Stock": 85, "Reorder Level": 25},
        {"SKU": "KIR-1002", "Product": "Toor Dal", "Category": "Pulses", "Unit": "kg", "Price": 145.0, "Stock": 18, "Reorder Level": 20},
        {"SKU": "KIR-1003", "Product": "Sugar", "Category": "Staples", "Unit": "kg", "Price": 48.0, "Stock": 42, "Reorder Level": 15},
        {"SKU": "KIR-1004", "Product": "Sunflower Oil", "Category": "Edible Oils", "Unit": "litre", "Price": 142.0, "Stock": 12, "Reorder Level": 15},
        {"SKU": "KIR-1005", "Product": "Tata Salt", "Category": "Staples", "Unit": "pack", "Price": 28.0, "Stock": 36, "Reorder Level": 12},
        {"SKU": "KIR-1006", "Product": "Aashirvaad Atta", "Category": "Rice & Grains", "Unit": "kg", "Price": 68.0, "Stock": 24, "Reorder Level": 10},
        {"SKU": "KIR-1007", "Product": "Parle-G Biscuits", "Category": "Snacks", "Unit": "pack", "Price": 10.0, "Stock": 65, "Reorder Level": 20},
        {"SKU": "KIR-1008", "Product": "Milk", "Category": "Dairy", "Unit": "litre", "Price": 64.0, "Stock": 9, "Reorder Level": 12},
        {"SKU": "KIR-1009", "Product": "Tea Powder", "Category": "Beverages", "Unit": "pack", "Price": 120.0, "Stock": 16, "Reorder Level": 8},
        {"SKU": "KIR-1010", "Product": "Bath Soap", "Category": "Personal Care", "Unit": "bar", "Price": 38.0, "Stock": 28, "Reorder Level": 10},
    ]
)

DEFAULT_SALES = pd.DataFrame(
    [
        {"Date": "2026-09-24", "SKU": "KIR-1001", "Product": "Sona Masoori Rice", "Quantity": 8, "Unit Price": 62.0},
        {"Date": "2026-09-25", "SKU": "KIR-1002", "Product": "Toor Dal", "Quantity": 3, "Unit Price": 145.0},
        {"Date": "2026-09-26", "SKU": "KIR-1004", "Product": "Sunflower Oil", "Quantity": 4, "Unit Price": 142.0},
        {"Date": "2026-09-27", "SKU": "KIR-1007", "Product": "Parle-G Biscuits", "Quantity": 12, "Unit Price": 10.0},
        {"Date": "2026-09-28", "SKU": "KIR-1008", "Product": "Milk", "Quantity": 6, "Unit Price": 64.0},
        {"Date": "2026-09-29", "SKU": "KIR-1003", "Product": "Sugar", "Quantity": 7, "Unit Price": 48.0},
    ]
)

if "products" not in st.session_state:
    st.session_state.products = DEFAULT_PRODUCTS.copy()
if "sales" not in st.session_state:
    st.session_state.sales = DEFAULT_SALES.copy()

products = st.session_state.products
sales = st.session_state.sales.copy()
sales["Revenue"] = sales["Quantity"] * sales["Unit Price"]

st.title("🛒 Kirana Shop Inventory Analytics")
st.caption("Streamlit portfolio dashboard • grocery stock, daily sales, revenue and reorder monitoring")

with st.sidebar:
    st.header("Shop Filters")
    categories = sorted(products["Category"].unique())
    selected_categories = st.multiselect("Category", categories, default=categories)
    search = st.text_input("Search product or SKU", placeholder="e.g. rice")
    st.divider()
    st.info("Self-contained demo data — no MySQL or external database is required for Streamlit deployment.")

filtered = products[products["Category"].isin(selected_categories)].copy()
if search.strip():
    q = search.strip().lower()
    filtered = filtered[
        filtered["Product"].str.lower().str.contains(q, regex=False)
        | filtered["SKU"].str.lower().str.contains(q, regex=False)
    ]

reorder_count = int((filtered["Stock"] <= filtered["Reorder Level"]).sum())
units = int(filtered["Stock"].sum())
revenue = float(sales["Revenue"].sum())
sales_count = int(len(sales))

m1, m2, m3, m4 = st.columns(4)
m1.metric("Products", len(filtered))
m2.metric("Stock Units", f"{units:,}")
m3.metric("Sales Entries", sales_count)
m4.metric("Total Revenue", f"₹{revenue:,.0f}")

st.subheader("📦 Inventory overview")
left, right = st.columns([2.2, 1])

with left:
    display = filtered.copy()
    display["Status"] = display.apply(
        lambda r: "🔴 Reorder" if r["Stock"] <= r["Reorder Level"] else "🟢 Healthy",
        axis=1,
    )
    st.dataframe(display, use_container_width=True, hide_index=True)

with right:
    st.markdown("### 🚨 Reorder alerts")
    alerts = filtered[filtered["Stock"] <= filtered["Reorder Level"]]
    if alerts.empty:
        st.success("No reorder alerts.")
    else:
        for _, row in alerts.iterrows():
            st.warning(
                f"**{row['Product']}** — {int(row['Stock'])} {row['Unit']} left "
                f"(reorder at {int(row['Reorder Level'])})"
            )

st.subheader("📊 Sales analytics")
c1, c2 = st.columns(2)

with c1:
    revenue_by_date = sales.groupby("Date", as_index=True)["Revenue"].sum()
    st.markdown("**Daily sales revenue**")
    st.line_chart(revenue_by_date, height=280)

with c2:
    category_revenue = (
        sales.merge(products[["SKU", "Category"]], on="SKU", how="left")
        .groupby("Category")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )
    st.markdown("**Revenue by grocery category**")
    st.bar_chart(category_revenue, height=280)

st.subheader("🧾 Record a kirana sale")
with st.form("sale_form", clear_on_submit=True):
    sku = st.selectbox(
        "Product",
        products["SKU"],
        format_func=lambda x: (
            f"{x} — {products.loc[products['SKU'].eq(x), 'Product'].iloc[0]}"
        ),
    )
    quantity = st.number_input(
        "Quantity sold",
        min_value=1,
        max_value=100,
        value=1,
        step=1,
        help="For example, 2 means 2 kg, 2 litres, 2 packs, or 2 bars depending on the product unit.",
    )
    submitted = st.form_submit_button("Record sale", type="primary")

if submitted:
    idx = st.session_state.products.index[
        st.session_state.products["SKU"].eq(sku)
    ][0]
    available = int(st.session_state.products.at[idx, "Stock"])

    if quantity > available:
        st.error(f"Only {available} units of this product are available.")
    else:
        st.session_state.products.at[idx, "Stock"] = available - quantity
        product_name = st.session_state.products.at[idx, "Product"]
        unit = st.session_state.products.at[idx, "Unit"]
        unit_price = float(st.session_state.products.at[idx, "Price"])

        new_sale = pd.DataFrame(
            [
                {
                    "Date": pd.Timestamp.now().strftime("%Y-%m-%d"),
                    "SKU": sku,
                    "Product": product_name,
                    "Quantity": quantity,
                    "Unit Price": unit_price,
                }
            ]
        )
        st.session_state.sales = pd.concat(
            [st.session_state.sales, new_sale], ignore_index=True
        )
        st.success(f"Recorded {quantity} {unit} × {product_name}.")
        st.rerun()

st.caption(
    "Portfolio demo for a small Indian kirana shop • Streamlit Community Cloud ready."
)
