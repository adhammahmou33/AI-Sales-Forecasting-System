import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression

# إعداد الصفحة
st.set_page_config(page_title="AI Sales Forecasting System", page_icon="📈", layout="wide")
# --- إضافة خلفية متحركة هادية ومتناسقة مع الدارك مود ---
# --- تكتيك الاختراق الكامل لـ CSS خلفية Streamlit ---
st.markdown(
    """
    <style>
    /* تصفير وإخفاء خلفيات المكونات الافتراضية تماماً لإظهار الأنيميشن */
    html, body, .stApp, .main, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: linear-gradient(125deg, #0e1117, #161b22, #0d1117, #1f242c) !important;
        background-size: 400% 400% !important;
        animation: GradientAnimation 12s ease infinite !important;
    }

    /* تأثير حركة الألوان الإنسيابية المهدئة للأعصاب */
    @keyframes GradientAnimation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* جعل كروت الـ Metrics زجاجية فخمة جداً (Glassmorphism) */
    div[data-testid="stMetricValue"], div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2) !important;
    }

    /* جعل لون الـ Expander متناسق وزجاجي */
    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("📈 AI Sales Forecasting System")
st.subheader("Predict future sales and analyze business performance using Machine Learning")

file_path = "Updatee_Sales_Analysis_Report.xlsx"

try:
    df = pd.read_excel(file_path)
    df.columns = [c.strip().title() for c in df.columns]
    
    # ---------------- 🎛️ قسم الفلاتر التفاعلية (Sidebar) ----------------
    st.sidebar.header("🎯 Dashboard Filters")
    
    if "Country" in df.columns:
        all_countries = ["All Countries"] + list(df["Country"].unique())
        selected_country = st.sidebar.selectbox("Select Country:", all_countries)
    else:
        selected_country = "All Countries"
        
    if "Type" in df.columns:
        all_types = ["All Types"] + list(df["Type"].unique())
        selected_type = st.sidebar.selectbox("Select Product Type:", all_types)
    else:
        selected_type = "All Types"

    # تطبيق الفلاتر
    df_filtered = df.copy()
    if selected_country != "All Countries":
        df_filtered = df_filtered[df_filtered["Country"] == selected_country]
    if selected_type != "All Types":
        df_filtered = df_filtered[df_filtered["Type"] == selected_type]

    st.sidebar.markdown("---")
    # ------------------------------------------------------------------

    st.success(f"🎉 Dashboard synced! Showing data for: {selected_country} | {selected_type}")
    
    # --- 1. عرض الأرقام الكبيرة ---
    st.markdown("### 📊 The Big Numbers")
    col1, col2, col3 = st.columns(3)
    
    total_profits = df_filtered["Profits"].sum() if "Profits" in df_filtered.columns else 0
    total_sales_count = len(df_filtered)
    avg_price = df_filtered["Price"].mean() if "Price" in df_filtered.columns else (df_filtered["Sales"].mean() if "Sales" in df_filtered.columns else 0)
    
    col1.metric("Total Sales Profits", f"${total_profits:,.2f}")
    col2.metric("Total Sales Count", f"{total_sales_count:,}")
    col3.metric("Average Price", f"${avg_price:,.2f}")
    
    st.markdown("---")
    
    # --- 2. قسم الرسومات البيانية التفاعلية مع ثيم الدارك مود ---
    st.markdown("### 🔍 Interactive Business Insights")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # الرسمة 1: بار تشارت الدول
        if "Country" in df_filtered.columns and "Profits" in df_filtered.columns:
            top_countries = df_filtered.groupby("Country")["Profits"].sum().sort_values(ascending=False).head(4).reset_index()
            fig1 = px.bar(top_countries, x="Country", y="Profits", title="Top Countries by Profits",
                          color="Profits", color_continuous_scale="Bluered")
            # تطبيق التعديل هنا 👇
            fig1.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig1, use_container_width=True)
            
        # الرسمة 2: باي تشارت الجنس
        if "Gender" in df_filtered.columns and "Profits" in df_filtered.columns:
            gender_profits = df_filtered.groupby("Gender")["Profits"].sum().reset_index()
            fig2 = px.pie(gender_profits, values="Profits", names="Gender", title="Profits Distribution by Gender", hole=0.4)
            # تطبيق التعديل هنا 👇
            fig2.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig2, use_container_width=True)

    with chart_col2:
        # الرسمة 3: بار تشارت البراندات
        if "Type" in df_filtered.columns and "Profits" in df_filtered.columns:
            top_types = df_filtered.groupby("Type")["Profits"].sum().sort_values(ascending=False).head(5).reset_index()
            fig3 = px.bar(top_types, x="Type", y="Profits", title="Top Product Types by Profits", color="Type")
            # تطبيق التعديل هنا 👇
            fig3.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig3, use_container_width=True)
            
        with st.expander("👀 View Filtered Data Snapshot"):
            st.dataframe(df_filtered.head(10), use_container_width=True)

    # --- 3. التنبؤ بالذكاء الاصطناعي مع ثيم الدارك مود ---
    if "Profits" in df_filtered.columns and len(df_filtered) > 1:
        st.markdown("---")
        st.markdown("### 🔮 AI Future Trend Forecasting")
        
        df_filtered['_Index'] = np.arange(len(df_filtered))
        X_model = df_filtered[['_Index']]
        y_model = df_filtered['Profits']
        
        model = LinearRegression()
        model.fit(X_model, y_model)
        
        future_steps = st.slider("Select steps to forecast into the future:", 5, 100, 20)
        future_idx = np.arange(len(df_filtered), len(df_filtered) + future_steps).reshape(-1, 1)
        predictions = model.predict(future_idx)
        
        pred_df = pd.DataFrame({
            'Index': np.append(df_filtered['_Index'].values, future_idx.flatten()),
            'Profits ($)': np.append(y_model.values, predictions),
            'Data Type': ['Historical'] * len(df_filtered) + ['AI Forecast'] * future_steps
        })
        
        fig_forecast = px.line(pred_df, x='Index', y='Profits ($)', color='Data Type', title="AI Linear Trend Prediction", markers=True)
        # تطبيق التعديل هنا 👇
        fig_forecast.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_forecast, use_container_width=True)
    else:
        st.warning("⚠️ Not enough data points to generate an AI Forecast.")

except Exception as e:
    st.error(f"❌ Error: {e}")