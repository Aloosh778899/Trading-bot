import streamlit as st
import yfinance as yf
import pandas as pd
import ephem
import datetime

st.set_page_config(page_title="Gold Astral Pro System", layout="centered")

st.title("Gold Astral Multi-Timeframe System")
st.markdown("### التحليل المدمج: السعر الفعلي + الزوايا الفلكية")

# حساب التأثير الفلكي
def get_astral_reading():
    sun = ephem.Sun()
    moon = ephem.Moon()
    now = ephem.now()
    sun.compute(now)
    moon.compute(now)
    
    # منطق تحليلي مبسط للزوايا (مثال للربط)
    phase = moon.phase
    if phase > 50:
        return "القمر في طور النمو (طاقة إيجابية للذهب)"
    return "القمر في طور الانحسار (حذر في التداول)"

if st.button("تشغيل التحليل الفلكي والسعري"):
    with st.spinner('جاري حساب الزوايا الفلكية ومطابقتها مع السعر...'):
        # السعر الفعلي
        gold = yf.Ticker("GC=F")
        hist = gold.history(period="1d")
        price = hist['Close'].iloc[-1]
        
        # التحليل الفلكي
        astral_msg = get_astral_reading()
        
        st.metric("السعر الفوري للذهب (XAUUSD)", f"${price:,.2f}")
        st.markdown("---")
        st.subheader("نتائج التحليل:")
        st.success(f"التحليل الفلكي الحالي: {astral_msg}")
        
        if price > 4400: # مثال لمنطق التداول
            st.warning("السعر الحالي مرتفع، التحليل الفلكي يوصي بالمراقبة.")
        else:
            st.success("السعر في منطقة دعم فلكية.")

st.sidebar.text("النسخة: Astral Pro v3.0")
