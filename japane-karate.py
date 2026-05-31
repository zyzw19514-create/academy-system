import streamlit as st
import pandas as pd
import qrcode
import cv2
import numpy as np
from pyzbar.pyzbar import decode

# إعداد السيستم
if 'players' not in st.session_state:
    st.session_state.players = pd.DataFrame(columns=["الاسم", "الكود"])

st.title("🥋 سيستم الأكاديمية الاحترافي")

tab1, tab2 = st.tabs(["📸 تسجيل حضور", "➕ إضافة لاعب"])

# تبويب الإضافة: هنا بيتحول الرقم لـ QR
with tab2:
    name = st.text_input("اسم اللاعب:")
    code = st.text_input("كود اللاعب:")
    if st.button("حفظ وتوليد QR"):
        # حفظ البيانات
        new_row = pd.DataFrame({"الاسم": [name], "الكود": [code]})
        st.session_state.players = pd.concat([st.session_state.players, new_row], ignore_index=True)
        # توليد الـ QR
        qr = qrcode.make(code)
        qr.save("code.png")
        st.success("تم الحفظ!")
        st.image("code.png")

# تبويب الحضور: هنا بنقرأ الـ QR اللي ولدناه
with tab1:
    img_file = st.camera_input("صور الـ QR كود")
    if img_file:
        bytes_data = img_file.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        decoded = decode(cv2_img)
        if decoded:
            scanned = decoded[0].data.decode('utf-8')
            if scanned in st.session_state.players['الكود'].values:
                st.success(f"✅ حضور اللاعب: {scanned}")
            else:
                st.error("❌ كود غير مسجل!")
