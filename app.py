import streamlit as st
import pandas as pd
import qrcode
from PIL import Image
from datetime import datetime
import os
import cv2
import numpy as np

st.set_page_config(page_title="الأكاديمية اليابانية للكاراتيه")

st.title("🥋 الأكاديمية اليابانية للكاراتيه")

if "players" not in st.session_state:
    st.session_state.players = {}

if "attendance" not in st.session_state:
    st.session_state.attendance = []

menu = st.sidebar.radio(
    "القائمة",
    ["إضافة لاعب", "تسجيل حضور", "اللاعبين", "سجل الحضور"]
)

# -------------------
# إضافة لاعب
# -------------------

if menu == "إضافة لاعب":

    name = st.text_input("اسم اللاعب")
    code = st.text_input("كود اللاعب")

    if st.button("حفظ اللاعب"):

        if name and code:

            st.session_state.players[code] = {
                "name": name
            }

            qr = qrcode.make(code)

            if not os.path.exists("qr_codes"):
                os.makedirs("qr_codes")

            qr_path = f"qr_codes/{code}.png"
            qr.save(qr_path)

            st.success("تم إضافة اللاعب")

            st.image(qr_path, width=200)

# -------------------
# تسجيل حضور
# -------------------

elif menu == "تسجيل حضور":

    method = st.radio(
        "طريقة التسجيل",
        ["الكود", "QR"]
    )

    # بالكود

    if method == "الكود":

        code = st.text_input("اكتب الكود")

        if st.button("تسجيل الحضور"):

            if code in st.session_state.players:

                now = datetime.now()

                st.session_state.attendance.append({
                    "اللاعب":
                    st.session_state.players[code]["name"],
                    "الكود": code,
                    "التاريخ": now.strftime("%Y-%m-%d"),
                    "الوقت": now.strftime("%H:%M:%S")
                })

                st.success("تم تسجيل الحضور")

            else:
                st.error("الكود غير موجود")

    # QR

    else:

        uploaded = st.file_uploader(
            "ارفع صورة QR",
            type=["png", "jpg", "jpeg"]
        )

        if uploaded:

            file_bytes = np.asarray(
                bytearray(uploaded.read()),
                dtype=np.uint8
            )

            img = cv2.imdecode(
                file_bytes,
                cv2.IMREAD_COLOR
            )

            detector = cv2.QRCodeDetector()

            data, bbox, _ = detector.detectAndDecode(img)

            if data:

                st.success(f"تم قراءة الكود: {data}")

                if data in st.session_state.players:

                    now = datetime.now()

                    st.session_state.attendance.append({
                        "اللاعب":
                        st.session_state.players[data]["name"],
                        "الكود": data,
                        "التاريخ": now.strftime("%Y-%m-%d"),
                        "الوقت": now.strftime("%H:%M:%S")
                    })

                    st.success("تم تسجيل الحضور")

                else:
                    st.error("اللاعب غير موجود")

            else:
                st.error("لم يتم العثور على QR")

# -------------------
# اللاعبين
# -------------------

elif menu == "اللاعبين":

    if st.session_state.players:

        rows = []

        for code, player in st.session_state.players.items():

            rows.append({
                "الاسم": player["name"],
                "الكود": code
            })

        st.dataframe(pd.DataFrame(rows))

# -------------------
# سجل الحضور
# -------------------

elif menu == "سجل الحضور":

    if st.session_state.attendance:

        st.dataframe(
            pd.DataFrame(
                st.session_state.attendance
            )
        )

    else:
        st.info("لا يوجد حضور")
