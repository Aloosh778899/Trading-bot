import streamlit as st
import yfinance as yf
import pandas as pd
import ephem
import datetime

st.set_page_config(page_title="Gold Astral Multi-Planet System", page_icon="⭐", layout="centered")

st.title("Gold Astral Multi-Planet System")
st.markdown("### نظام التحليل الفلكي الشامل (جميع الكواكب المؤثرة على الذهب)")

@st.cache_data(ttl=60)
def get_live_gold_price():
    try:
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

def calculate_all_planets_aspects():
    now = ephem.now()
    
    # تعريف الأجرام السماوية المؤثرة على الذهب
    sun = ephem.Sun()
    moon = ephem.Moon()
    mercury = ephem.Mercury()
    venus = ephem.Venus()
    mars = ephem.Mars()
    jupiter = ephem.Jupiter()
    saturn = ephem.Saturn()
    
    bodies = {
        "الشمس (السيادة والقوة الأساسية)": sun,
        "القمر (السيولة والتقلبات القصيرة)": moon,
        "عطارد (التذبذب والسرعة)": mercury,
        "الزهرة (القيمة والجاذبية الشرائية)": venus,
        "المريخ (العزم والطاقة العدوانية بالسوق)": mars,
        "المشتري (التوسع والنمو المالي)": jupiter,
        "زحل (الهيكلة والدعم التاريخي)": saturn
    }
    
    results = []
    for name, body in bodies.items():
        body.compute(now)
        # تحويل الموقع الفلكي إلى درجات دائرية من 0 إلى 360
        longitude = float(body.hlon) * (180 / 3.14159) % 360
        results.append((name, longitude))
        
    return results

if st.button("تشغيل التحليل الفلكي الشامل للكواكب"):
    with st.spinner('جار حساب مواقع وزوايا جميع الكواكب ومطابقتها مع السوق...'):
        price, change, hist = get_live_gold_price()
        planet_data = calculate_all_planets_aspects()
        
        if price is not None:
            st.success("تم جلب السعر الحقيقي وتحليل مواقع الكواكب بنجاح!")
            
            st.metric(
                label="السعر الفوري للذهب (XAUUSD)", 
                value=f"${price:,.2f}", 
                delta=f"{change:,.2f} USD"
            )
            
            st.markdown("---")
            st.header("خريطة مواقع الكواكب المؤثرة على الذهب:")
            
            for name, deg in planet_data:
                st.write(f"- **{name}**: الموقع عند الدرجة الدائرية **{deg:.2f}°**")
            
            st.markdown("---")
            st.header("التوجيه الفلكي الفني:")
            
            # تقييم زوايا الكواكب الكبرى المؤثرة (المشتري وزحل)
            jupiter_deg = [deg for name, deg in planet_data if "المشتري" in name][0]
            saturn_deg = [deg for name, deg in planet_data if "زحل" in name][0]
            
            diff = abs(jupiter_deg - saturn_deg)
            if 85 <= diff <= 95 or 175 <= diff <= 180:
                st.warning("تنبيه فلكي قوي: زاوية حرجة بين المشتري وزحل (توقع تقلبات سعرية حادة في الذهب).")
            else:
                st.success("استقرار نسبي في الزوايا الكبرى، السوق يتحرك وفق الاتجاه الفني الاعتيادي.")
                
            st.markdown("---")
            st.header("حركة السعر والرسوم البيانية:")
            st.line_chart(hist['Close'])
        else:
            st.error("تعذر جلب البيانات حالياً، حاول مرة أخرى.")

st.sidebar.header("إعدادات البوت")
st.sidebar.text("المطور: LO & ENI")
st.sidebar.text("النسخة: Astral Multi-Planet v4.0")
