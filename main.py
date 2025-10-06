import streamlit as st
import pandas as pd
import altair as alt

# Page setup
st.set_page_config(
    page_title="Waves of Change: The Ripple Effect of Store KPIs",
    page_icon=":key:",
    layout="wide"
)

st.title("Waves of Change: Explore the Ripple Effect of Store KPIs")
st.subheader("See how small improvements in KPI can add up to big results")
st.markdown("---")

# Layout: three columns. Left for inputs, center for results, right for insight
left_col, center, right_col = st.columns([0.36, 0.44, 0.20], gap="large")

with left_col:
    # Base KPI inputs
    st.header("Base KPI Settings")

    annual_visitors = st.number_input( # Number of store visitors each year
        "Total yearly visitors",
        min_value=100_000, max_value=10_000_000, value=350_000, step=1000,
        help="How many people visit the store over a full year."
    )

    hitrate = st.slider( # Share of visitors that make a purchase. 
        "Hitrate (%)",
        0.0, 100.0, 25.0,
        help="Share of visitors that make a purchase."
    )

    average_purchase_value = st.number_input( # Average spend per receipt.
        "Average purchase per transaction (SEK)",
        min_value=0.0, max_value=2_000.0, value=500.0, step=10.0,
        help="Average spend per receipt."
    )

    products_per_customer = st.number_input( # Average number of products per receipt.
        "Products per customer (average items per receipt)",
        min_value=0.9, max_value=100.0, value=1.7, step=0.01,
        help="Average number of products per purchase."
    )

    profit_margin = st.slider( # Gross profit margin as a percent of revenue.
        "Profit margin (%)",
        0.0, 100.0, 8.0,
        help="Gross profit margin as a percent of revenue."
    )

    st.markdown("---")

    # Scenario adjustments
    st.header("Scenario Adjustments")

    # Initialize reset counter in session state
    if 'reset_counter' not in st.session_state:
        st.session_state.reset_counter = 0

    hitrate_change_pp = st.slider(
        "Change in hitrate (percentage points)",
        -5.0, 10.0, 0.0,
        key=f"hitrate_slider_{st.session_state.reset_counter}",
        help="Additive change in hitrate in percentage points. Example: from 20.0% to 21.0% is +1.0 p.p."
    )

    average_purchase_change_sek = st.slider(
        "Change in average purchase (SEK)",
        -(average_purchase_value), (average_purchase_value), 0.0, 1.0,
        key=f"purchase_slider_{st.session_state.reset_counter}",
        help="Additive change in SEK. Example: +20 SEK turns 500 SEK into 520 SEK."
    )

    products_per_customer_change = st.slider(
        "Change in products per customer",
        -(products_per_customer), 2.0, 0.0, 0.01,
        key=f"products_slider_{st.session_state.reset_counter}",
        help="Additive change to average items per receipt. Example: +0.1 turns 1.7 into 1.8."
    )

    if st.button("Reset Scenario Adjustments", type="primary", use_container_width=True):
        st.session_state.reset_counter += 1
        st.rerun()

# Calculation function
def calculate_kpis(total_yearly_visitors, hitrate_percent, avg_purchase_sek, avg_items_per_receipt, margin_percent):
    """Return total_purchases, total_revenue, total_products_sold, total_profit."""
    total_purchases = total_yearly_visitors * (hitrate_percent / 100.0) # Total purchases is the number of visitors times the hitrate.
    total_revenue = total_purchases * avg_purchase_sek # Total revenue is the number of purchases times the average purchase value.
    total_products_sold = total_purchases * avg_items_per_receipt # Total products sold is the number of purchases times the average number of products per receipt.
    total_profit = total_revenue * (margin_percent / 100.0) # Total profit is the number of purchases times the average number of products per receipt times the gross profit margin.
    return total_purchases, total_revenue, total_products_sold, total_profit

# Base scenario
base_purchases, base_revenue, base_products_sold, base_profit = calculate_kpis(
    annual_visitors, hitrate, average_purchase_value, products_per_customer, profit_margin
)

# New scenario with adjustments
scenario_purchases, scenario_revenue, scenario_products_sold, scenario_profit = calculate_kpis(
    annual_visitors,
    hitrate + hitrate_change_pp,  # additive in percentage points
    average_purchase_value + average_purchase_change_sek,  # additive in SEK
    products_per_customer + products_per_customer_change,  # additive in items
    profit_margin
)

# Prepare data for visualization
data = pd.DataFrame(data={
    "KPI": ["Total Purchases", "Revenue (SEK)", "Products Sold", "Profit (SEK)"],
    "Base": [base_purchases, base_revenue, base_products_sold, base_profit],
    "Scenario": [scenario_purchases, scenario_revenue, scenario_products_sold, scenario_profit]
})

data["Change (Value)"] = data.apply(
    lambda row: (row["Scenario"] - row["Base"]), 
    axis=1
)

# Calculate percentage change
data["Change (%)"] = data.apply(
    lambda row: ((row["Scenario"] / row["Base"] - 1.0) * 100.0) if row["Base"] != 0 else 0.0, 
    axis=1
)

with center:
    st.header("Results")

    m1, m2, m3, m4 = st.columns(4) # Metrics for each KPI.
    m1.metric("Purchases", f"{scenario_purchases:,.0f}", f"{(scenario_purchases/base_purchases-1)*100:+.1f}%") # Calculate percentage change and display.
    m2.metric("Revenue (SEK)", f"{scenario_revenue:,.0f}", f"{(scenario_revenue/base_revenue-1)*100:+.1f}%")
    m3.metric("Products sold", f"{scenario_products_sold:,.0f}", f"{(scenario_products_sold/base_products_sold-1)*100:+.1f}%")
    m4.metric("Profit (SEK)", f"{scenario_profit:,.0f}", f"{(scenario_profit/base_profit-1)*100:+.1f}%")
    # Compact table
    st.markdown("#### Result effect")
    st.dataframe(
        data.style.format({
            "Base": "{:,.0f}",
            "Scenario": "{:,.0f}",
            "Change": "{:,.0f}",
            "Change (%)": "{:+.1f}%"
        }),
        use_container_width=True,
        hide_index=True,
    )
    


    # --- Visualizing the ripple effect with conditional colors ---
    st.markdown("#### Visualizing the ripple effect")

    # Fixed axis range
    ymin, ymax = -100, 100

    zero_line = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(
        strokeDash=[4, 4],
        color="gray"
    ).encode(y="y:Q")

    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("KPI:N", sort=None, title="Key Performance Indicator"),
            y=alt.Y("Change (%):Q", title="Percentage Change (%)",
                    scale=alt.Scale(domain=[ymin, ymax], nice=False)),
            color=alt.condition(
                alt.datum["Change (%)"] < 0,
                alt.value("#e45755"),  # Negative change
                alt.value("#2ca02c")   # Positive change
            ),
            tooltip=[
                alt.Tooltip("KPI:N"),
                alt.Tooltip("Base:Q", format=",.0f"),
                alt.Tooltip("Scenario:Q", format=",.0f"),
                alt.Tooltip("Change:Q", format=",.0f"),
                alt.Tooltip("Change (%):Q", format="+.1f")
            ]
        )
        .properties(height=500)
    )

    st.altair_chart(chart + zero_line, use_container_width=True)
    st.markdown("---")
    with right_col:
    # Short insight
        st.subheader("Insight")
        st.write(
            f"""
            With these adjustments: hitrate {hitrate:.1f}% → {hitrate + hitrate_change_pp:.1f}% 
            ({hitrate_change_pp:+.1f} p.p.), average purchase {average_purchase_value + average_purchase_change_sek:.1f} SEK 
            ({average_purchase_change_sek:+.1f} SEK), and products per customer {products_per_customer + products_per_customer_change:.2f} 
            ({products_per_customer_change:+.2f}),
            yearly profit changes by **{data.loc[3, 'Change (%)']:+.1f}%**.

            Small KPI improvements can compound into large results across a full year.
            """
        )
