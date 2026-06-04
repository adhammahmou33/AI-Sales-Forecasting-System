import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
from analytics import get_basic_status, process_date_columns
from data_loader import load_data

# إعداد الصفحة
st.set_page_config(page_title="AI Sales Forecasting System", page_icon="📈", layout="wide")

st.title("📈 AI Sales Forecasting System")
st.subheader("Predict future sales and analyze business performance using Machine Learning")

# تحديد مسار ملف الأكسيل المتاح في الفولدر عندك
file_path = "Updatee_Sales_Analysis_Report.xlsx"

try:
    # استخدام الدالة بتاعتك المحملة من data_loader
    df = load_data(file_path)
    
    # 1. عرض الأرقام الكبيرة باستخدام الدالة بتاعتك من analytics
    results = get_basic_status(df)
    
    st.markdown("### 📊 The Big Numbers")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales Profits", f"${results['Total_Sales_profits']:,.2f}")
    col2.metric("Total Sales Count", f"{results['total Sales Count']:,}")
    col3.metric("Average Price", f"${results['average price']:,.2f}")
    
    st.markdown("---")
    
    # معالجة التواريخ بالدالة بتاعتك
    df = process_date_columns(df)
    
    # 2. قسم الرسومات البيانية التفاعلية باستخدام Plotly
    st.markdown("### 🔍 Business Analytics Insights")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # أعلى 4 دول تحقيقاً للأرباح
        if "Country" in df.columns and "Profits" in df.columns:
            top_countries = df.groupby("Country")["Profits"].sum().sort_values(ascending=False).head(4).reset_index()
            fig1 = px.bar(top_countries, x="Country", y="Profits", title="Top 4 Countries by Profits",
                          color="Profits", color_continuous_scale="Viridis")
            st.plotly_chart(fig1, use_container_width=True)
            
        # توزيع الأرباح حسب الجنس (Pie Chart)
        if "Gender" in df.columns and "Profits" in df.columns:
            gender_profits = df.groupby("Gender")["Profits"].sum().reset_index()
            fig2 = px.pie(gender_profits, values="Profits", names="Gender", title="Profits Distribution by Gender", hole=0.3)
            st.plotly_chart(fig2, use_container_width=True)

    with chart_col2:
        # أعلى 5 أنواع تحقيقاً للأرباح
        if "Type" in df.columns and "Profits" in df.columns:
            top_types = df.groupby("Type")["Profits"].sum().sort_values(ascending=False).head(5).reset_index()
            fig3 = px.bar(top_types, x="Type", y="Profits", title="Top 5 Types by Profits", color="Type")
            st.plotly_chart(fig3, use_container_width=True)
            
        with st.expander("👀 View Data Snapshot"):
            st.dataframe(df.head(10), use_container_width=True)

    # 3. قسم التنبؤ الذكي بالذكاء الاصطناعي (AI Forecasting)
    if "Profits" in df.columns:
        st.markdown("---")
        st.markdown("### 🔮 AI Future Trend Forecasting")
        
        df['_Index'] = np.arange(len(df))
        X_model = df[['_Index']]
        y_model = df['Profits']
        
        model = LinearRegression()
        model.fit(X_model, y_model)
        
        future_steps = st.slider("Select steps to forecast into the future:", 5, 50, 10)
        future_idx = np.arange(len(df), len(df) + future_steps).reshape(-1, 1)
        predictions = model.predict(future_idx)
        
        pred_df = pd.DataFrame({
            'Step': np.append(df['_Index'].values, future_idx.flatten()),
            'Value': np.append(y_model.values, predictions),
            'Data Type': ['Historical'] * len(df) + ['AI Forecast'] * future_steps
        })
        
        fig_forecast = px.line(pred_df, x='Step', y='Value', color='Data Type', title="AI Linear Trend Prediction", markers=True)
        st.plotly_chart(fig_forecast, use_container_width=True)

except Exception as e:
    st.error(f"❌ Error loading data or running analytics: {e}")