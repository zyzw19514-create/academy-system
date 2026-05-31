import streamlit as st
import pandas as pd
from datetime import datetime
from pyzbar.pyzbar import decode
import cv2
import numpy as np

# 1. إعداد البيانات (لو مش موجودة بننشئها)
if 'players' not in st.session_state:
    st.session_state.players = pd.DataFrame(columns=["الاسم", "الكود", "انتهاء الاشتراك"])
if 'attendance' not in st.session_state:
    st.session_state.attendance = []

st.title("🥋 أكاديمية الكاراتيه")

# 2. التبويبات
tab1, tab2 = st.tabs(["📸 تسجيل حضور", "⚙️ الإدارة"])

with tab1:
    st.subheader("سكان بالكاميرا")
    img_file = st.camera_input("وجه الكاميرا للكود")
    
    if img_file:
        bytes_data = img_file.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        decoded = decode(cv2_img)
        
        if decoded:
            code = decoded[0].data.decode('utf-8')
            st.success(f"✅ تم تسجيل حضور الكود: {code}")
            st.session_state.attendance.append({"الكود": code, "الوقت": datetime.now().strftime("%H:%M")})
        else:
            st.warning("🔄 لم يتم التعرف على كود.. حاول مرة أخرى")

with tab2:
    st.subheader("إضافة لاعب جديد")
    name = st.text_input("اسم اللاعب:")
    code = st.text_input("الكود:")
    date = st.date_input("تاريخ انتهاء الاشتراك:")
    
    if st.button("حفظ اللاعب"):
        new_player = pd.DataFrame({"الاسم": [name], "الكود": [code], "انتهاء الاشتراك": [str(date)]})
        st.session_state.players = pd.concat([st.session_state.players, new_player], ignore_index=True)
        st.success(f"تم إضافة {name} بنجاح!")
    
    st.divider()
    st.subheader("قائمة اللاعبين")
    st.table(st.session_state.players)
