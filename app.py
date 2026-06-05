import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="INSTACART ONLINE GROCERY SHOPPING", layout="wide")

# Custom CSS forbuttons
st.markdown("""
<style>
div.stButton > button {
    background-color: #006D77 !important;   /* dark turquoise */
    color: white !important;
    border-radius: 8px;
    padding: 0.6em 1.2em;
    font-weight: 600;
    border: none;
}
div.stButton > button:hover {
    background-color: #005A63 !important;
}
</style>
""", unsafe_allow_html=True)


# ============================
# GLOBAL STYLE 
# ============================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap" rel="stylesheet">

<style>

html, body, [class*="css"]  {
    font-family: 'Montserrat', sans-serif !important;
    font-size: 20px !important;
}

/* H1 — Largest */
h1 {
    font-size: 54px !important;
    font-weight: 700 !important;
    margin-bottom: 20px !important;
}

/* H2 — Medium */
h2 {
    font-size: 32px !important;
    font-weight: 600 !important;
    margin-top: 25px !important;
    margin-bottom: 15px !important;
}

/* H3 — Smaller */
h3 {
    font-size: 26px !important;
    font-weight: 600 !important;
    margin-top: 20px !important;
    margin-bottom: 10px !important;
}


/* Header text */
.header-container h1 {
    color: white !important;
}

/* Buttons inside header */
.header-container .stButton>button {
    background-color: #FFD447 !important; /* Amarillo */
    color: #0A5F63 !important;            /* Turquesa para contraste */
    border-radius: 8px !important;
    font-size: 22px !important;
    padding: 12px 24px !important;
    border: none !important;
    font-weight: 600 !important;
}

.header-container .stButton>button:hover {
    background-color: #FFE58F !important; /* Amarillo más claro */
}

</style>
""", unsafe_allow_html=True)




# ============================
# TOP MENU
# ============================
st.markdown('<div class="header-container">', unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>INSTACART ONLINE GROCERY SHOPPING</h1>", unsafe_allow_html=True)

# SUBTITLE 
st.markdown(
    "<p style='font-size:18px; color:#006D77; font-family:Montserrat;text-align:center;'>"
    "Select the button of the section you want to explore."
    "</p>",
    unsafe_allow_html=True
)

menu = st.columns(3)

# Default section
if "section" not in st.session_state:
    st.session_state.section = "1. OVERVIEW"

with menu[0]:
    if st.button("1. OVERVIEW"):
        st.session_state.section = "1. OVERVIEW"

with menu[1]:
    if st.button("2. RECOMMENDATION SYSTEM"):
        st.session_state.section = "2. RECOMMENDATION SYSTEM"

with menu[2]:
    if st.button("3. MARKET BASKET ANALYSIS"):
        st.session_state.section = "3. MARKET BASKET ANALYSIS"

st.markdown('</div>', unsafe_allow_html=True)

section = st.session_state.section




# ---------------------------------------------------------
# SECTION 1 — OVERVIEW (UPDATED WITH 2 ROWS + INTERACTIVE CHART)
# ---------------------------------------------------------
if section == "1. OVERVIEW":
    st.header("1. Overview of the Dataset")

    # ============================
    # ROW 1 — TEXT ONLY
    # ============================
    st.subheader("Dataset Summary")
    st.write("""
    The dataset was reduced using a hybrid sampling technique to keep the most important patterns while 
    making the dashboard faster and easier to use.
    """)

    # KPIs in a horizontal row
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric("Total Orders (Original)", "3M+")
    kpi2.metric("Total Orders (Sample)", "50K")
    kpi3.metric("Products", "49K+")
    kpi4.metric("Departments", "21")

    st.markdown("---")

    # ============================
    # ROW 2 — INTERACTIVE CHART (PLOTLY)
    # ============================
    st.subheader("Department Distribution: Original vs Sample (Interactive)")

    import plotly.graph_objects as go

    # Load data
    orig_prop = pd.read_csv("orig_department_prop.csv", index_col=0)
    sample_prop = pd.read_csv("sample_department_prop.csv", index_col=0)

    # Align indexes
    orig_prop = orig_prop.reindex(sample_prop.index)

    # Create interactive bar chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=orig_prop.index,
        y=orig_prop.values.flatten(),
        name="Original",
        marker_color="#4C72B0"
    ))

    fig.add_trace(go.Bar(
        x=sample_prop.index,
        y=sample_prop.values.flatten(),
        name="Sampled",
        marker_color="#55A868"
    ))

    fig.update_layout(
        barmode="group",
        xaxis_title="Department",
        yaxis_title="Proportion",
        title="Original vs Sample Department Distribution",
        height=500,
        font=dict(family="Montserrat", size=18),
        legend=dict(font=dict(size=16))
    )

    st.plotly_chart(fig, use_container_width=True)

    


# ---------------------------------------------------------
# SECTION 2 — RECOMMENDATION SYSTEM 
# ---------------------------------------------------------
elif section == "2. RECOMMENDATION SYSTEM":
    st.header("2. Recommendation System (Item-Item)")
    st.write("Select a product to see its top 3 recommended items.")

    col1, col2 = st.columns(2)

    # LEFT COLUMN — DROPDOWN
    with col1:
        st.subheader("Choose a Product")

        recs = pd.read_csv("item_item_recommendations.csv")

        product_list = sorted(recs["product_name"].unique())
        selected_product = st.selectbox("Select a product:", product_list)

        filtered = recs[recs["product_name"] == selected_product]
        top3 = filtered.sort_values("score", ascending=False).head(3)

    # RIGHT COLUMN — INTERACTIVE PLOTLY BAR CHART
    with col2:
        st.subheader("Top 3 Recommended Products")

        if top3.empty:
            st.write("No recommendations available for this product.")
        else:
            import plotly.graph_objects as go

            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=top3["recommended_product"],
                y=top3["score"],
                marker_color=["#4C72B0", "#55A868", "#C44E52"],
                hovertemplate="<b>%{x}</b><br>Score: %{y:.3f}<extra></extra>"
            ))

            fig.update_layout(
                xaxis_title="Recommended Product",
                yaxis_title="Similarity Score",
                height=450,
                font=dict(family="Montserrat", size=18),
                margin=dict(l=20, r=20, t=20, b=20),
                showlegend=False
            )

            st.plotly_chart(fig, use_container_width=True)



# ---------------------------------------------------------
# SECTION 3 — MARKET BASKET ANALYSIS
# ---------------------------------------------------------
elif section == "3. MARKET BASKET ANALYSIS":
    st.header("3. Market Basket Analysis (MBA)")

    # ============================
    # ROW 1 — GENERAL DESCRIPTION
    # ============================
    st.markdown("""
    ### 🛒 Market Basket Insights  
    Understand how products behave together inside customer baskets. This section includes:
    - Products that frequently appear together
    - Items that accompany low‑support products
    - Hero, Promotion, and Low Support product groups  
    """)

    import plotly.express as px

    # Load MBA summary file
    mba = pd.read_csv("mba_summary.csv")

    # Load FP-Growth rules
    fp = pd.read_csv("fp_rules.csv")

    # Clean antecedents/consequents
    fp["antecedents"] = fp["antecedents"].str.replace("{", "").str.replace("}", "")
    fp["consequents"] = fp["consequents"].str.replace("{", "").str.replace("}", "")

    # Product list for dropdown
    product_list = sorted(set(fp["antecedents"].unique()) | set(fp["consequents"].unique()))

    # ============================
    # ROW 2A — DROPDOWN 
    # ============================
    st.markdown("### 🔗 Co‑Occurrence Recommendations")

    selected_product = st.selectbox("Select a product:", product_list)

    # Filter FP-Growth rules
    filtered = fp[fp["antecedents"] == selected_product]

    # Limit to top 5 by lift
    top5 = filtered.sort_values("lift", ascending=False).head(5)

    # ============================
    # ROW 2B — 
    # ============================
    col_graph, col_table = st.columns([2, 1.2])

    # ---- LEFT: GRAPH ----
    with col_graph:
        if not top5.empty:
            fig_co = px.bar(
                top5,
                x="lift",
                y="consequents",
                orientation="h",
                color="lift",
                color_continuous_scale="Blues",
                labels={"consequents": "Recommended Product", "lift": "Lift"},
            )
            fig_co.update_layout(
                height=350,
                font=dict(family="Montserrat", size=16),
                margin=dict(l=10, r=10, t=10, b=10),
                coloraxis_showscale=False
            )
            fig_co.update_yaxes(autorange="reversed")
            st.plotly_chart(fig_co, use_container_width=True)
        else:
            st.write("No co‑occurrence patterns found for this product.")

    # ---- RIGHT: TABLE ----
    with col_table:
        if not top5.empty:
            st.write("**Top Co‑Occurring Items**")
            st.dataframe(
                top5[["consequents", "support", "confidence", "lift"]]
                .rename(columns={
                    "consequents": "Product",
                    "support": "Support",
                    "confidence": "Confidence",
                    "lift": "Lift"
                }),
                use_container_width=True,
                height=350
            )
        else:
            st.write("No data available.")

    st.markdown("---")

    # ============================
    # PREPARE HERO / PROMO / LOW DATA
    # ============================
    hero = mba[mba["category"] == "hero"].sort_values("support", ascending=False).head(5)
    promo = mba[mba["category"] == "promo"].sort_values("support", ascending=False).head(5)
    low = mba[mba["category"] == "low"].sort_values("support", ascending=True).head(5)

    # ============================
    # ROW 3 — HERO PRODUCTS 
    # ============================
    st.markdown("### ⭐ Hero Products")
    row1_col1, row1_col2 = st.columns([1, 2])

    with row1_col1:
        st.write("""
        **Hero Products**  
        These items have the highest support and represent the core of customer demand.
        """)

    with row1_col2:
        if not hero.empty:
            fig1 = px.bar(
                hero,
                x="support",
                y="product_name",
                orientation="h",
                color="support",
                color_continuous_scale="Teal",
                labels={"support": "Support", "product_name": "Product"},
            )
            fig1.update_layout(
                height=350,
                font=dict(family="Montserrat", size=16),
                margin=dict(l=10, r=10, t=10, b=10),
                coloraxis_showscale=False
            )
            fig1.update_yaxes(autorange="reversed")
            st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    # ============================
    # ROW 4 — PROMOTION CANDIDATES 
    # ============================
    st.markdown("### 📈 Promotion Candidates")
    row2_col1, row2_col2 = st.columns([1, 2])

    with row2_col1:
        st.write("""
        **Promotion Candidates**  
        These items have moderate support and respond well to targeted promotions.
        """)

    with row2_col2:
        if not promo.empty:
            fig2 = px.bar(
                promo,
                x="support",
                y="product_name",
                orientation="h",
                color="support",
                color_continuous_scale="Sunset",
                labels={"support": "Support", "product_name": "Product"},
            )
            fig2.update_layout(
                height=350,
                font=dict(family="Montserrat", size=16),
                margin=dict(l=10, r=10, t=10, b=10),
                coloraxis_showscale=False
            )
            fig2.update_yaxes(autorange="reversed")
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # ============================
    # ROW 5 — LOW SUPPORT ITEMS 
    # ============================
    st.markdown("### ⚠️ Low Support Items")
    row3_col1, row3_col2 = st.columns([1, 2])

    with row3_col1:
        st.write("""
        **Low Support Items**  
        These products are rarely purchased and may require review or removal.
        """)

    with row3_col2:
        if not low.empty:
            fig3 = px.bar(
                low,
                x="support",
                y="product_name",
                orientation="h",
                color="support",
                color_continuous_scale="Reds",
                labels={"support": "Support", "product_name": "Product"},
            )
            fig3.update_layout(
                height=350,
                font=dict(family="Montserrat", size=16),
                margin=dict(l=10, r=10, t=10, b=10),
                coloraxis_showscale=False
            )
            fig3.update_yaxes(autorange="reversed")
            st.plotly_chart(fig3, use_container_width=True)



