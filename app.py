import streamlit as st

from utils.charts import bar_chart, funnel_chart, line_chart, pie_chart
from utils.data_loader import filtered_data, load_data
from utils.kpi_calculator import (
    channel_performance,
    executive_kpis,
    format_currency,
    format_number,
    monthly_trend,
    onboarding_summary,
    product_mix,
    region_performance,
    risk_distribution,
)


st.set_page_config(page_title="Digital Banking Analytics", layout="wide")

st.title("Digital Banking Analytics Application")
st.caption(
    "A business-facing dashboard for onboarding, engagement, fraud exposure, and regional KPI monitoring."
)

raw_df = load_data()

st.sidebar.header("Filters")
region_options = sorted(raw_df["region"].unique().tolist())
channel_options = sorted(raw_df["acquisition_channel"].unique().tolist())
product_options = sorted(raw_df["product_type"].unique().tolist())

selected_regions = st.sidebar.multiselect("Region", region_options, default=region_options)
selected_channels = st.sidebar.multiselect("Acquisition Channel", channel_options, default=channel_options)
selected_products = st.sidebar.multiselect("Product Type", product_options, default=product_options)

view = st.sidebar.radio(
    "View",
    [
        "Executive Overview",
        "Onboarding Funnel",
        "Fraud and Risk",
        "Customer Engagement",
        "Regional Performance",
    ],
)

df = filtered_data(raw_df, selected_regions, selected_channels, selected_products)

if df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

kpis = executive_kpis(df)

if view == "Executive Overview":
    row1 = st.columns(4)
    row1[0].metric("Applications", format_number(kpis["total_applications"]))
    row1[1].metric("Verification Rate", f"{kpis['verification_rate']}%")
    row1[2].metric("Activation Rate", f"{kpis['activation_rate']}%")
    row1[3].metric("Total Spend", format_currency(kpis["total_spend"]))

    row2 = st.columns(4)
    row2[0].metric("Transactions", format_number(kpis["total_transactions"]))
    row2[1].metric("Fraud Cases", format_number(kpis["fraud_cases"]))
    row2[2].metric("Fraud Amount", format_currency(kpis["fraud_amount"]))
    row2[3].metric("Avg Login Days", kpis["avg_login_days"])

    trend = monthly_trend(df)
    channels = channel_performance(df)

    left, right = st.columns(2)
    left.plotly_chart(line_chart(trend, "month", "applications", "Monthly Application Trend"), use_container_width=True)
    right.plotly_chart(bar_chart(channels, "acquisition_channel", "activation_rate", "Activation Rate by Channel"), use_container_width=True)

    st.subheader("Channel Performance Summary")
    show_channels = channels[[
        "acquisition_channel",
        "applications",
        "verification_rate",
        "activation_rate",
        "fraud_rate",
        "total_spend",
    ]].copy()
    show_channels["total_spend"] = show_channels["total_spend"].round(0)
    st.dataframe(show_channels, use_container_width=True, hide_index=True)

elif view == "Onboarding Funnel":
    funnel = onboarding_summary(df)
    channels = channel_performance(df)

    left, right = st.columns([1, 1])
    left.plotly_chart(funnel_chart(funnel), use_container_width=True)
    right.plotly_chart(bar_chart(channels, "acquisition_channel", "verification_rate", "Verification Rate by Channel"), use_container_width=True)

    st.subheader("Business Insight")
    best_channel = channels.sort_values("activation_rate", ascending=False).iloc[0]["acquisition_channel"]
    weakest_channel = channels.sort_values("activation_rate", ascending=True).iloc[0]["acquisition_channel"]
    st.write(
        f"The strongest onboarding conversion is currently coming from **{best_channel}**, while **{weakest_channel}** is showing the lowest activation rate. This is the kind of view I would use in a review with product and operations teams to discuss onboarding friction and channel quality."
    )

    st.subheader("Onboarding Stage Summary")
    st.dataframe(funnel, use_container_width=True, hide_index=True)

elif view == "Fraud and Risk":
    trend = monthly_trend(df)
    risk = risk_distribution(df)
    region_df = region_performance(df)

    left, right = st.columns(2)
    left.plotly_chart(line_chart(trend, "month", "fraud_cases", "Monthly Fraud Case Trend"), use_container_width=True)
    right.plotly_chart(pie_chart(risk, "retention_risk", "customers", "Retention Risk Mix"), use_container_width=True)

    st.subheader("Region-Level Risk View")
    show_regions = region_df[["region", "applications", "activation_rate", "fraud_amount", "avg_logins"]].copy()
    show_regions["fraud_amount"] = show_regions["fraud_amount"].round(0)
    st.dataframe(show_regions, use_container_width=True, hide_index=True)

    st.info(
        "This section is useful for showing how operational reporting can connect customer performance with fraud exposure and retention monitoring in one place."
    )

elif view == "Customer Engagement":
    products = product_mix(df)
    regions = region_performance(df)

    left, right = st.columns(2)
    left.plotly_chart(pie_chart(products, "product_type", "customers", "Product Mix"), use_container_width=True)
    right.plotly_chart(bar_chart(regions, "region", "avg_logins", "Average Login Days by Region"), use_container_width=True)

    st.subheader("Engagement Snapshot")
    activated_df = df[df["activation_status"] == "Activated"].copy()
    engagement = (
        activated_df.groupby("product_type", as_index=False)
        .agg(
            customers=("customer_id", "count"),
            avg_transactions=("monthly_transactions", "mean"),
            avg_spend=("monthly_spend", "mean"),
            avg_login_days=("login_days_30", "mean"),
        )
        .round(1)
    )
    st.dataframe(engagement, use_container_width=True, hide_index=True)

elif view == "Regional Performance":
    regions = region_performance(df)
    channels = channel_performance(df)

    left, right = st.columns(2)
    left.plotly_chart(bar_chart(regions, "region", "activation_rate", "Activation Rate by Region"), use_container_width=True)
    right.plotly_chart(bar_chart(channels, "acquisition_channel", "applications", "Applications by Channel"), use_container_width=True)

    st.subheader("Regional KPI Table")
    show_regions = regions.copy()
    show_regions["total_spend"] = show_regions["total_spend"].round(0)
    show_regions["fraud_amount"] = show_regions["fraud_amount"].round(0)
    st.dataframe(show_regions, use_container_width=True, hide_index=True)

    top_region = regions.iloc[0]["region"]
    st.success(
        f"Based on the current filtered view, **{top_region}** is the strongest region by activation rate. This is a simple but effective stakeholder talking point for monthly business reviews."
    )
