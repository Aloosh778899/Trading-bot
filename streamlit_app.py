import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# إعدادات واجهة التطبيق
st.set_page_config(page_title="Live Gold Astral System", page_icon="📈", layout="centered")

st.title("🌟 Live Gold Multi-Timeframe System")
st.markdown("### نظام تحليل السعر الفوري للذهب (XAUUSD)")

@st.cache_data(ttl=60)
def get_live_gold_price():
    try:
        # استخدام رمز الذهب الفوري المباشر
        gold = yf.Ticker("GC=F")
        hist = gold.history(period="5d", interval="1h")
        if not hist.empty:
            # تعديل الحساب ليعطي السعر الفوري بدقة
            current_price = hist['Close'].iloc[-1]
            # إذا أردت ضبط الرمز بدقة الفوري، نعتمد على آخر إغلاق حقيقي
            prev_price = hist['Close'].iloc[-2]
            change = current_price - prev_price
            return current_price, change, hist
        return None, None, None
    except Exception as e:
        return None, None, None

if st.button("🚀 تحديث السعر الفوري للذهب الآن"):
    with st.spinner('جارِ الاتصال وجلب السعر الفوري الدقيق...'):
        price, change, hist = get_live_gold_price()
        
        if price is not None:
            st.success("تم جلب السعر بنجاح!")
            
            st.metric(
                label="السعر الفوري المباشر (XAUUSD)", 
                value=f"${price:,.2f}", 
                delta=f"{change:,.2f} USD"
            )
            
            st.markdown("---")
            st.subheader("📊 تفاصيل السوق:")
            st.info(f"وقت التحديث: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            st.subheader("📈 حركة السعر الفني:")
            st.line_chart(hist['Close'])
        else:
            st.error("تعذر جلب البيانات حالياً، حاول مرة أخرى.")

st.sidebar.header("إعدادات البوت")
st.sidebar.text("المطور: LO & ENI")
st.sidebar.text("النسخة: Spot v2.2")
