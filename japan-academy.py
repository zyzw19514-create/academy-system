import streamlit as st
import cv2
from pyzbar.pyzbar import decode
import numpy as np

st.set_page_config(page_title="أكاديمية الكاراتيه", layout="centered")

# قاعدة بيانات اللاعبين (هتتحفظ طول ما البرنامج شغال)
if 'players_db' not in st.session_state:
    st.session_state.players_db = {"101": "أحمد محمد", "102": "زياد أحمد"}

# القائمة الجانبية
menu = st.sidebar.radio("القائمة:", ["📱 تسجيل الحضور (كاميرا)", "➕ إضافة لاعب جديد"])

# 1. شاشة تسجيل الحضور (بالكاميرا)
if menu == "📱 تسجيل الحضور (كاميرا)":
    st.header("🥋 تسجيل الحضور")
    img_file = st.camera_input("وجه الكاميرا على كود اللاعب")
    
    if img_file:
        bytes_data = img_file.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        decoded = decode(cv2_img)
        
        if decoded:
            p_id = decoded[0].data.decode('utf-8')
            if p_id in st.session_state.players_db:
                st.success(f"✅ تم حضور اللاعب: {st.session_state.players_db[p_id]}")
            else:
                st.error("❌ الكود غير مسجل في النظام!")
        else:
            st.warning("🔄 لم يتم العثور على كود، حاول مرة أخرى.")

# 2. شاشة إضافة لاعبين
elif menu == "➕ إضافة لاعب جديد":
    st.header("➕ إضافة لاعب جديد")
    new_id = st.text_input("أدخل كود اللاعب (ID):")
    new_name = st.text_input("اسم اللاعب:")
    
    if st.button("حفظ اللاعب"):
        if new_id and new_name:
            st.session_state.players_db[new_id] = new_name
            st.success(f"🎉 تم إضافة {new_name} بنجاح!")
        else:
            st.error("يرجى ملء البيانات أولاً.")
