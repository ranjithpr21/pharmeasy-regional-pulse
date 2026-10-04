"""Part 4 - PharmEasy Regional Pulse dashboard. Run: streamlit run app.py"""
import os, sqlite3
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DB = "pharmeasy.db"
BASE, HILITE, MUTED = "#1f5f99", "#e8710a", "#b8c2cc"   # highlight reserved for flagship flagged region (Guntur)
FLAGSHIP = "Guntur"
MONTH_LABEL = {"2026-04": "Apr 2026", "2026-05": "May 2026", "2026-06": "Jun 2026"}

st.set_page_config(page_title="PharmEasy Regional Pulse", layout="wide")
if not os.path.exists(DB):
    import build_db; build_db.build()

@st.cache_data
def load():
    con = sqlite3.connect(DB)
    df = pd.read_sql("SELECT * FROM orders_clean", con)
    con.close()
    df["month"] = df["order_date"].str[:7]
    return df
df = load()
inr = lambda x: f"₹{x:,.0f}"
months = sorted(df["month"].unique())

# ---------- Executive summary (CII, built from real numbers) ----------
tot_s, tot_p, tot_n = df.sales_inr.sum(), df.profit_inr.sum(), df.order_id.nunique()
ms = df.groupby("month").sales_inr.sum()
rm = df.pivot_table(index="region", columns="month", values="sales_inr", aggfunc="sum")
g = (rm.loc[FLAGSHIP, months[1]] / rm.loc[FLAGSHIP, months[0]] - 1) * 100
g2 = (rm.loc[FLAGSHIP, months[2]] / rm.loc[FLAGSHIP, months[1]] - 1) * 100
cat_share = (df.groupby("category").sales_inr.sum() / tot_s * 100).sort_values(ascending=False)
st.title("PharmEasy Regional Pulse")
st.info(
    f"**Executive summary.** Across Apr–Jun 2026 the desk booked {inr(tot_s)} in sales and {inr(tot_p)} in profit from {tot_n:,} orders. "
    f"Network sales were nearly flat month to month ({(ms[months[1]]/ms[months[0]]-1)*100:+.1f}% then {(ms[months[2]]/ms[months[1]]-1)*100:+.1f}%), so the story is regional. "
    f"{cat_share.index[0]} ({cat_share.iloc[0]:.1f}%) and {cat_share.index[1]} ({cat_share.iloc[1]:.1f}%) lead categories, and {FLAGSHIP} swung {g:+.2f}% Apr→May then {g2:+.2f}% in June. "
    f"Treat the {FLAGSHIP} jump as an alert to review, not a trend to act on, until July data confirms it. "
    f"Use the region filter below to drill from overview to category to detail.")

# ---------- Region filter (connects all levels) ----------
region = st.selectbox("Region filter", ["All regions"] + sorted(df.region.unique()))
view = df if region == "All regions" else df[df.region == region]
label = region if region != "All regions" else "all regions"

# ---------- Level 1: Overview ----------
st.header("1 · Overview")
c1, c2, c3 = st.columns(3)
c1.metric("Total sales (INR)", inr(view.sales_inr.sum()))
c2.metric("Total profit (INR)", inr(view.profit_inr.sum()))
c3.metric("Order count (distinct order_id)", f"{view.order_id.nunique():,}")

def style(fig, title, x, y):
    fig.update_layout(title=title, xaxis_title=x, yaxis_title=y, template="plotly_white", height=380, showlegend=False)
    return fig

a, b = st.columns(2)
tot_r = rm.sum(axis=1).sort_values(ascending=False)
fig = go.Figure(go.Bar(x=tot_r.index, y=tot_r.values, marker_color=[HILITE if r == FLAGSHIP else BASE for r in tot_r.index]))
fig.update_yaxes(rangemode="tozero")
a.plotly_chart(style(fig, "Which regions sold the most in Apr–Jun 2026?", "Region", "Total sales (INR)"), width="stretch")

fig = go.Figure()
show = [r for r in rm.index] if region == "All regions" else [region]
for r in show:
    color = HILITE if r == FLAGSHIP else (BASE if region != "All regions" else MUTED)
    fig.add_trace(go.Scatter(x=[MONTH_LABEL[m] for m in months], y=rm.loc[r, months].values, mode="lines+markers",
                             name=r, line=dict(color=color, width=3 if color != MUTED else 1.5)))
fig.update_yaxes(rangemode="tozero")
ttl = "How did monthly sales move by region?" if region == "All regions" else f"How did {region}'s monthly sales move?"
fig = style(fig, ttl, "Month (2026)", "Sales (INR)")
if region == "All regions":
    fig.update_layout(showlegend=True)
    fig.add_annotation(text=f"{FLAGSHIP} highlighted", x=1, y=rm.loc[FLAGSHIP, months[1]], showarrow=False, font=dict(color=HILITE))
b.plotly_chart(fig, width="stretch")

# ---------- Level 2: Category ----------
st.header(f"2 · Category breakdown ({label})")
cat = view.groupby("category").sales_inr.sum().sort_values(ascending=False)
a, b = st.columns(2)
fig = go.Figure(go.Bar(x=cat.values, y=cat.index, orientation="h", marker_color=BASE))
fig.update_xaxes(rangemode="tozero"); fig.update_yaxes(autorange="reversed")
a.plotly_chart(style(fig, f"Which category drives sales in {label}?", "Sales (INR)", "Category"), width="stretch")
shades = ["#08306b", "#2171b5", "#4292c6", "#6baed6", "#9ecae1", "#c6dbef"]   # single hue, 6 slices
fig = go.Figure(go.Pie(labels=cat.index, values=cat.values, hole=0.45, marker=dict(colors=shades), sort=False,
                       textinfo="percent"))
fig.update_layout(title=f"What share of sales does each category hold in {label}? (% of INR sales)", height=380, template="plotly_white")
b.plotly_chart(fig, width="stretch")

# ---------- Level 3: Detail ----------
st.header(f"3 · Detail: region × month ({label})")
d = view.groupby(["region", "month"]).agg(orders=("order_id", "nunique"), sales_inr=("sales_inr", "sum"),
                                          profit_inr=("profit_inr", "sum")).reset_index()
d["mom_sales_pct"] = d.sort_values(["region", "month"]).groupby("region").sales_inr.pct_change().mul(100).round(2)
d["flag_gt_8pct"] = d.mom_sales_pct.abs() > 8
d[["sales_inr", "profit_inr"]] = d[["sales_inr", "profit_inr"]].round(2)
st.dataframe(d, width="stretch", hide_index=True)
st.caption("Flag = |MoM sales change| > 8%: a fixed operational-alert rule, not a statistical test. Most regions cross it most months.")
