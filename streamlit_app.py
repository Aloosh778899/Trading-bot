import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# إعدادات واجهة التطبيق
st.set_page_config(page_title="Live Gold Astral System", page_icon="📈", layout="centered")

st.title("🌟 Live Gold Multi-Timeframe System")
st.markdown("### نظام تحليل الذهب الحقيقي (بيانات حية من السوق المالي)")

@st.cache_data(ttl=60)
def get_live_gold_price():
    try:
        # جلب بيانات الذهب الحية الفعلية من السوق (عقود الذهب الآجلة GC=F)
        gold = yf.Ticker("GC=F")
        hist = gold.history(period="5d", interval="1h")
        if not hist.empty:
            current_price = hist['Close'].iloc[-1]
            prev_price = hist['Close'].iloc[-2]
            change = current_price - prev_price
            return current_price, change, hist
        return None, None, None
    except Exception as e:
        return None, None, None

# زر التشغيل الحقيقي
if st.button("🚀 جلب أسعار السوق الحية وتحليلها"):
    with st.spinner('جارِ الاتصال بالأسواق المالية وجلب البيانات الحية...'):
        price, change, hist = get_live_gold_price()
        
        if price is not None:
            st.success("تم الاتصال بنجاح وجلب السعر الحقيقي الفعلي للذهب!")
            
            # عرض السعر الحقيقي والتغير
            st.metric(
                label="السعر الحقيقي للذهب (XAUUSD / GC=F)", 
                value=f"${price:,.2f}", 
                delta=f"{change:,.2f} USD"
            )
            
            st.markdown("---")
            st.subheader("📊 تحليل الحركة السعرية الحية:")
            st.info(f"وقت التحديث المباشر: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            if change >= 0:
                st.markdown("### 🟢 **الاتجاه اللحظي:** صاعد (إشارة إيجابية بالسوق الحقيقي)")
            else:
                st.markdown("### 🔴 **الاتجاه اللحظي:** هابط (ضغط بيعي بالسوق الحقيقي)")
                
            # عرض الرسم البياني الحقيقي للأسعار
            st.subheader("📈 رسم بياني لحركة السعر الأخيرة:")
            st.line_chart(hist['Close'])
        else:
            st.error("تعذر جلب البيانات الحية حالياً بسبب ضغط الشبكة، حاول مرة أخرى.")

st.sidebar.header("إعدادات البوت")
st.sidebar.text("المطور: LO & ENI")
st.sidebar.text("المصدر: أسواق المال العالمية (Live API)")
st.sidebar.text("النسخة: Real-Data v2.0")
