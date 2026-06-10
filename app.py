import streamlit as st
import pandas as pd
import plotly.express as px
from analysis import (df, get_route_summary, get_shipmode_summary,
                      get_region_summary, get_state_summary, threshold)

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nassau Candy – Shipping Analysis",
    page_icon="🍬",
    layout="wide"
)

st.title("🍬 Nassau Candy Distributor – Shipping Route Efficiency")
st.markdown("*Factory-to-Customer logistics intelligence dashboard*")

# ── SIDEBAR FILTERS ────────────────────────────────────────────────────────────
st.sidebar.header("🔧 Filters")
st.sidebar.markdown("Use these to explore specific segments of the data.")

regions = st.sidebar.multiselect(
    "Region",
    options=sorted(df['Region'].unique()),
    default=sorted(df['Region'].unique())
)

ship_modes = st.sidebar.multiselect(
    "Ship Mode",
    options=sorted(df['Ship Mode'].unique()),
    default=sorted(df['Ship Mode'].unique())
)

lt_thresh = st.sidebar.slider(
    "Max Lead Time Filter (days)",
    min_value=int(df['Lead Time'].min()),
    max_value=int(df['Lead Time'].max()),
    value=int(df['Lead Time'].max()),
    help="Slide left to exclude very long lead times from analysis"
)

# ── APPLY FILTERS ──────────────────────────────────────────────────────────────
filtered = df[
    (df['Region'].isin(regions)) &
    (df['Ship Mode'].isin(ship_modes)) &
    (df['Lead Time'] <= lt_thresh)
]

if filtered.empty:
    st.warning("No data matches your current filters. Please adjust the sidebar.")
    st.stop()

# ── KPI CARDS ──────────────────────────────────────────────────────────────────
st.subheader("📌 Key Metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Orders",      f"{len(filtered):,}")
c2.metric("Avg Lead Time",     f"{filtered['Lead Time'].mean():.1f} days")
c3.metric("Delayed Shipments", f"{filtered['Is Delayed'].sum():,}")
c4.metric("Delay Rate",        f"{filtered['Is Delayed'].mean()*100:.1f}%")

st.divider()

# ── TABS ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📦 Route Efficiency",
    "🗺️ Geographic View",
    "🚚 Ship Mode Analysis",
    "🔍 Route Drill-Down"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — ROUTE EFFICIENCY
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### Route Performance Leaderboard")
    st.caption("Each route = Factory → Customer Region. Ranked by average lead time.")

    route_df = get_route_summary(filtered)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🏆 Top 10 Most Efficient Routes**")
        st.dataframe(
            route_df.head(10)[['Route', 'Avg_Lead_Time', 'Efficiency_Score', 'Total_Shipments']],
            use_container_width=True, hide_index=True
        )
    with col2:
        st.markdown("**⚠️ Bottom 10 Least Efficient Routes**")
        st.dataframe(
            route_df.tail(10)[['Route', 'Avg_Lead_Time', 'Delay_Rate', 'Total_Shipments']],
            use_container_width=True, hide_index=True
        )

    st.markdown("---")
    fig = px.bar(
        route_df,
        x='Avg_Lead_Time', y='Route',
        orientation='h',
        color='Efficiency_Score',
        color_continuous_scale='RdYlGn',
        title='Average Lead Time by Route (Green = Efficient, Red = Slow)',
        labels={'Avg_Lead_Time': 'Avg Lead Time (days)', 'Route': ''}
    )
    fig.update_layout(height=550, coloraxis_colorbar_title="Efficiency")
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — GEOGRAPHIC VIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### US Shipping Performance Map")
    st.caption("Darker red = slower delivery. Use this to identify geographic bottlenecks.")

    state_df = get_state_summary(filtered)

    fig_map = px.choropleth(
        state_df,
        locations='State/Province',
        locationmode='USA-states',
        color='Avg_Lead_Time',
        hover_name='State/Province',
        hover_data={'Orders': True, 'Delay_Rate': True, 'Avg_Lead_Time': ':.1f'},
        color_continuous_scale='RdYlGn_r',
        scope='usa',
        title='Average Shipping Lead Time by State'
    )
    fig_map.update_layout(height=500)
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("---")
    st.markdown("### Regional Performance Comparison")
    region_df = get_region_summary(filtered)

    col1, col2 = st.columns(2)
    with col1:
        fig_reg = px.bar(
            region_df, x='Region', y='Avg_Lead_Time',
            color='Avg_Lead_Time', color_continuous_scale='RdYlGn_r',
            title='Avg Lead Time by Region',
            labels={'Avg_Lead_Time': 'Avg Lead Time (days)'}
        )
        st.plotly_chart(fig_reg, use_container_width=True)
    with col2:
        fig_delay = px.bar(
            region_df, x='Region', y='Delay_Rate',
            color='Delay_Rate', color_continuous_scale='Reds',
            title='Delay Rate by Region (%)',
            labels={'Delay_Rate': 'Delay Rate (%)'}
        )
        st.plotly_chart(fig_delay, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — SHIP MODE ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Shipping Method Comparison")
    st.caption("Evaluating speed vs cost tradeoffs across Standard, First, Second Class, and Same Day.")

    sm_df = get_shipmode_summary(filtered)

    col1, col2 = st.columns(2)
    with col1:
        fig_sm1 = px.bar(
            sm_df, x='Ship Mode', y='Avg_Lead_Time',
            color='Ship Mode',
            title='Average Lead Time by Ship Mode',
            labels={'Avg_Lead_Time': 'Avg Lead Time (days)'}
        )
        st.plotly_chart(fig_sm1, use_container_width=True)
    with col2:
        fig_sm2 = px.scatter(
            sm_df, x='Avg_Cost', y='Avg_Lead_Time',
            size='Orders', color='Ship Mode',
            title='Cost vs Speed (bubble size = order volume)',
            labels={'Avg_Cost': 'Avg Cost ($)', 'Avg_Lead_Time': 'Avg Lead Time (days)'}
        )
        st.plotly_chart(fig_sm2, use_container_width=True)

    st.markdown("#### Full Summary Table")
    st.dataframe(sm_df, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — ROUTE DRILL-DOWN
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### Inspect a Specific Route")
    st.caption("Select any route to see order-level detail and lead time distribution.")

    route_options = get_route_summary(filtered)['Route'].tolist()
    selected_route = st.selectbox("Select a Route", route_options)

    route_data = filtered[filtered['Route'] == selected_route]

    col1, col2, col3 = st.columns(3)
    col1.metric("Orders on this route", len(route_data))
    col2.metric("Avg Lead Time",        f"{route_data['Lead Time'].mean():.1f} days")
    col3.metric("Delay Rate",           f"{route_data['Is Delayed'].mean()*100:.1f}%")

    fig_hist = px.histogram(
        route_data, x='Lead Time', nbins=20,
        title=f'Lead Time Distribution – {selected_route}',
        color_discrete_sequence=['#2196F3']
    )
    fig_hist.add_vline(x=threshold, line_dash="dash", line_color="red",
                       annotation_text="Delay Threshold")
    st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("#### Order-Level Data")
    st.dataframe(
        route_data[['Order ID', 'City', 'State/Province', 'Ship Mode',
                    'Lead Time', 'Is Delayed', 'Sales', 'Gross Profit']]
        .sort_values('Lead Time', ascending=False),
        use_container_width=True, hide_index=True
    )
