import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("Sales Performance Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv('data/sales_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
products = st.sidebar.multiselect("Products", df['Product'].unique(), default=df['Product'].unique())
regions = st.sidebar.multiselect("Regions", df['Region'].unique(), default=df['Region'].unique())
df = df[df['Product'].isin(products) & df['Region'].isin(regions)]

# Metrics
c1, c2, c3 = st.columns(3)
c1.metric("Total Revenue", f"${df['Total'].sum():,.0f}")
c2.metric("Total Sales", f"{len(df):,}")
c3.metric("Average Sale", f"${df['Total'].mean():.0f}")

st.divider()

# Charts
# 1. Revenue by Product
fig, ax = plt.subplots(figsize=(10, 6))
rev = df.groupby('Product')['Total'].sum().sort_values()
sns.barplot(x=rev.values, y=rev.index, palette='viridis')
ax.set(xlabel='Revenue ($)', ylabel='Product', title='Revenue by Product')
st.pyplot(fig)

st.divider()

# 2. Monthly Trend
fig, ax = plt.subplots(figsize=(10, 6))
monthly = df.groupby(df['Date'].dt.to_period('M'))['Total'].sum()
monthly.plot(kind='line', marker='o')
ax.set(xlabel='Month', ylabel='Revenue ($)', title='Monthly Revenue Trend')
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
st.pyplot(fig)

st.divider()

# 3. Revenue by Region
fig, ax = plt.subplots(figsize=(8, 8))
region = df.groupby('Region')['Total'].sum()
ax.pie(region.values, labels=region.index, autopct='%1.1f%%', 
       colors=sns.color_palette('pastel'), startangle=90)
ax.set_title('Revenue Distribution by Region')
st.pyplot(fig)

st.divider()

# Raw data
st.dataframe(df, use_container_width=True)