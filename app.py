import streamlit as st
import pandas as pd
import os
import qrcode
from datetime import datetime
import cv2
import numpy as np

st.set_page_config(page_title="الأكاديمية اليابانية للكاراتيه", layout="wide")

st.title("🥋 الأكاديمية اليابانية للكاراتيه")

PLAYERS_FILE = "players.csv"
ATTENDANCE_FILE = "attendance.csv"

# ---------------- ملفات ----------------
if not os.path.exists(PLAYERS_FILE):
    pd.DataFrame(columns=["name", "code", "sessions"]).to_csv(PLAYERS_FILE, index=False)

if not os.path.exists(ATTENDANCE_FILE):
    pd.DataFrame(columns=["name", "code", "date", "time"]).to_csv(ATTENDANCE_FILE, index=False)

players = pd.read_csv(PLAYERS_FILE)
attendance = pd.read_csv(ATTENDANCE_FILE)

# ---------------- قائمة ----------------
menu = st.sidebar.selectbox(
    "القائمة",
    [
        "إضافة لاعب",
        "تسجيل حضور",
        "اللاعبين",
        "سجل الحضور",
        "الاشتراكات",
        "تجديد الاشتراك"
    ]
)

# ================= إضافة لاعب =================
if menu == "إضافة لاعب":

    st.header("إضافة لاعب")

    name = st.text_input("اسم اللاعب")
    code = st.text_input("كود اللاعب")

    if st.button("إضافة"):

        if name == "" or code == "":
            st.error("املأ البيانات")

        elif code in players["code"].astype(str).values:
            st.error("الكود موجود")

        else:
            new_player = pd.DataFrame([{
                "name": name,
                "code": code,
                "sessions": 8
            }])

            players = pd.concat([players, new_player], ignore_index=True)
            players.to_csv(PLAYERS_FILE, index=False)

            qr = qrcode.make(code)
            qr.save(f"{code}.png")

            st.success("تم إضافة اللاعب")
            st.image(f"{code}.png")

# ================= حضور =================
elif menu == "تسجيل حضور":

    method = st.radio("طريقة التسجيل", ["كود", "QR (صورة)"])

    # كود
    if method == "كود":

        code = st.text_input("ادخل الكود")

        if st.button("تسجيل"):

            if code not in players["code"].astype(str).values:
                st.error("الكود غير موجود")

            else:
                idx = players.index[players["code"].astype(str) == code][0]
                sessions = int(players.loc[idx, "sessions"])

                if sessions <= 0:
                    st.error("❌ الاشتراك منتهي")

                else:
                    players.loc[idx, "sessions"] = sessions - 1
                    players.to_csv(PLAYERS_FILE, index=False)

                    now = datetime.now()

                    new_att = pd.DataFrame([{
                        "name": players.loc[idx, "name"],
                        "code": code,
                        "date": now.strftime("%Y-%m-%d"),
                        "time": now.strftime("%H:%M:%S")
                    }])

                    attendance = pd.concat([attendance, new_att], ignore_index=True)
                    attendance.to_csv(ATTENDANCE_FILE, index=False)

                    st.success("تم تسجيل الحضور")
                    st.info(f"المتبقي: {sessions-1}")

    # QR صورة
    else:

        file = st.file_uploader("ارفع QR", type=["png", "jpg", "jpeg"])

        if file:

            file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            detector = cv2.QRCodeDetector()
            data, _, _ = detector.detectAndDecode(img)

            if data in players["code"].astype(str).values:

                idx = players.index[players["code"].astype(str) == data][0]
                sessions = int(players.loc[idx, "sessions"])

                if sessions <= 0:
                    st.error("❌ الاشتراك منتهي")

                else:
                    players.loc[idx, "sessions"] = sessions - 1
                    players.to_csv(PLAYERS_FILE, index=False)

                    now = datetime.now()

                    new_att = pd.DataFrame([{
                        "name": players.loc[idx, "name"],
                        "code": data,
                        "date": now.strftime("%Y-%m-%d"),
                        "time": now.strftime("%H:%M:%S")
                    }])

                    attendance = pd.concat([attendance, new_att], ignore_index=True)
                    attendance.to_csv(ATTENDANCE_FILE, index=False)

                    st.success("تم تسجيل الحضور")
                    st.info(f"المتبقي: {sessions-1}")

            else:
                st.error("QR غير صحيح")

# ================= لاعبين =================
elif menu == "اللاعبين":

    st.dataframe(players)

# ================= سجل حضور =================
elif menu == "سجل الحضور":

    st.dataframe(attendance)

# ================= اشتراكات =================
elif menu == "الاشتراكات":

    st.header("📋 الاشتراكات")

    data = []

    for i in range(len(players)):

        s = int(players.loc[i, "sessions"])

        if s <= 0:
            status = "❌ منتهي"
        elif s <= 2:
            status = "⚠️ قرب يخلص"
        else:
            status = "✅ ساري"

        data.append({
            "الاسم": players.loc[i, "name"],
            "الكود": players.loc[i, "code"],
            "المتبقي": s,
            "الحالة": status
        })

    df = pd.DataFrame(data)
    st.dataframe(df)

    if any(df["الحالة"] == "❌ منتهي"):
        st.error("في اشتراكات منتهية")

    if any(df["الحالة"] == "⚠️ قرب يخلص"):
        st.warning("في اشتراكات قربت تخلص")

# ================= تجديد =================
elif menu == "تجديد الاشتراك":

    st.header("تجديد اشتراك")

    if len(players) > 0:

        name = st.selectbox("اختار اللاعب", players["name"].tolist())

        if st.button("تجديد 8 حصص"):

            idx = players.index[players["name"] == name][0]
            players.loc[idx, "sessions"] = 8
            players.to_csv(PLAYERS_FILE, index=False)

            st.success("تم التجديد")
