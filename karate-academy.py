import streamlit as st
import cv2
import numpy as np

st.set_page_config(page_title="الأكاديمية اليابانية للكاراتيه", layout="centered")

st.title("🥋 نظام الحضور الذكي")

menu = st.sidebar.radio("القائمة:", ["📱 تسجيل الحضور", "➕ إضافة لاعب"])

# شاشة تسجيل الحضور
if menu == "📱 تسجيل الحضور":
    st.header("📸 الكاميرا")
    img_file = st.camera_input("وجه الكاميرا على كود اللاعب")
    
    if img_file:
        st.success("✅ تم التقاط الصورة بنجاح! جاري معالجة الكود...")
        # هنا تقدر تضيف المنطق بتاع مقارنة الكود لو عايز

# شاشة إضافة لاعب
elif menu == "➕ إضافة لاعب":
    st.header("➕ إضافة بيانات لاعب جديد")
    c = st.text_input("كود اللاعب (ID):")
    n = st.text_input("اسم اللاعب:")
    if st.button("حفظ"):
        st.success(f"تم حفظ اللاعب: {n}")
