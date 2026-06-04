import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression

# إعداد الصفحة لتكون احترافية وعريضة والتفاعل سريع
st.set_page_config(page_title="AI Sales Forecasting System", page_icon="📈", layout="wide")

st.title("📈 AI Sales Forecasting System")
st.subheader("Predict future sales and analyze business performance using Machine Learning")

# تحديد مسار ملف الأكسيل المتاح في الفولدر
file_path = "Updatee_Sales_Analysis_Report.xlsx"

try:
    # قراءة البيانات مباشرة هنا لضمان التفاعل
    df = pd.read_excel(file_path)
    
    st.success("🎉 Data loaded and synchronized successfully!")
    
    # تنظيف أسماء الأعمدة (تأمين ضد الحروف الكابيتال والسمول)
    df.columns = [c.strip().title() for c in df.columns]
    
    # --- 1. عرض الأرقام الكبيرة (KPIs) ---
    st.markdown("### 📊 The Big Numbers")
    col1, col2, col3 = st.columns(3)
    
    # التأكد من وجود الأعمدة الحسابية قبل الجمع
    total_profits = df["Profits"].sum() if "Profits" in df.columns else 0
    total_sales_count = len(df)
    avg_price = df["Price"].mean() if "Price" in df.columns else (df["Sales"].mean() if "Sales" in df.columns else 0)
    
    col1.metric("Total Sales Profits", f"${total_profits:,.2f}")
    col2.metric("Total Sales Count", f"{total_sales_count:,}")
    col3.metric("Average Price", f"${avg_price:,.2f}")
    
    st.markdown("---")
    
    # --- 2. قسم الرسومات البيانية التفاعلية الكاملة بـ Plotly ---
    st.markdown("### 🔍 Interactive Business Insights")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # الرسمة 1: أعلى 4 دول تحقيقاً للأرباح
        if "Country" in df.columns and "Profits" in df.columns:
            top_countries = df.groupby("Country")["Profits"].sum().sort_values(ascending=False).head(4).reset_index()
            fig1 = px.bar(top_countries, x="Country", y="Profits", title="Top 4 Countries by Profits",
                          color="Profits", color_continuous_scale="Bluered")
            st.plotly_chart(fig1, use_container_width=True)
            
        # الرسمة 2: توزيع الأرباح حسب الجنس (Pie Chart تفاعلي)
        if "Gender" in df.columns and "Profits" in df.columns:
            gender_profits = df.groupby("Gender")["Profits"].sum().reset_index()
            fig2 = px.pie(gender_profits, values="Profits", names="Gender", title="Profits Distribution by Gender", hole=0.4)
            st.plotly_chart(fig2, use_container_width=True)

    with chart_col2:
        # الرسمة 3: أعلى 5 أنواع تحقيقاً للأرباح
        if "Type" in df.columns and "Profits" in df.columns:
            top_types = df.groupby("Type")["Profits"].sum().sort_values(ascending=False).head(5).reset_index()
            fig3 = px.bar(top_types, x="Type", y="Profits", title="Top 5 Types by Profits", 
                          color="Type", color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig3, use_container_width=True)
            
        # عرض عينة تفاعلية من البيانات للزوار
        with st.expander("👀 View Data Snapshot"):
            st.dataframe(df.head(10), use_container_width=True)

    # --- 3. قسم التنبؤ بالذكاء الاصطناعي (AI Forecasting) ---
    if "Profits" in df.columns:
        st.markdown("---")
        st.markdown("### 🔮 AI Future Trend Forecasting")
        
        # تجهيز البيانات للموديل
        df['_Index'] = np.arange(len(df))
        X_model = df[['_Index']]
        y_model = df['Profits']
        
        model = LinearRegression()
        model.fit(X_model, y_model)
        
        # Slider تفاعلي يغير التنبؤ لحظياً
        future_steps = st.slider("Select lines/steps to forecast into the future:", 5, 100, 20)
        future_idx = np.arange(len(df), len(df) + future_steps).reshape(-1, 1)
        predictions = model.predict(future_idx)
        
        # دمج البيانات للعرض على الرسمة
        pred_df = pd.DataFrame({
            'Index': np.append(df['_Index'].values, future_idx.flatten()),
            'Profits ($)': np.append(y_model.values, predictions),
            'Data Type': ['Historical'] * len(df) + ['AI Forecast'] * future_steps
        })
        
        fig_forecast = px.line(pred_df, x='Index', y='Profits ($)', color='Data Type', 
                               title="AI Linear Trend Prediction Dashboard", markers=True)
        st.plotly_chart(fig_forecast, use_container_width=True)

except Exception as e:
    st.error(f"❌ Error displaying the dashboard components: {e}")