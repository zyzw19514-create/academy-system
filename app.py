import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="الأكاديمية اليابانية للكاراتيه",
    layout="wide"
)

st.title("🥋 الأكاديمية اليابانية للكاراتيه")

CSV_FILE = "players.csv"

# إنشاء الملف لو مش موجود
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["name", "code", "sessions"]).to_csv(
        CSV_FILE,
        index=False
    )

df = pd.read_csv(CSV_FILE)

menu = st.sidebar.selectbox(
    "القائمة",
    [
        "إضافة لاعب",
        "تسجيل حضور",
        "اللاعبين"
    ]
)

# ------------------------
# إضافة لاعب
# ------------------------

if menu == "إضافة لاعب":

    st.header("إضافة لاعب جديد")

    name = st.text_input("اسم اللاعب")
    code = st.text_input("كود اللاعب")

    if st.button("إضافة"):

        if name and code:

            if code in df["code"].astype(str).values:
                st.error("الكود مستخدم بالفعل")

            else:

                new_player = pd.DataFrame(
                    [{
                        "name": name,
                        "code": code,
                        "sessions": 8
                    }]
                )

                df = pd.concat(
                    [df, new_player],
                    ignore_index=True
                )

                df.to_csv(
                    CSV_FILE,
                    index=False
                )

                st.success("تم إضافة اللاعب")

# ------------------------
# تسجيل حضور
# ------------------------

elif menu == "تسجيل حضور":

    st.header("تسجيل حضور")

    code = st.text_input("ادخل الكود")

    if st.button("تسجيل"):

        player_index = df.index[
            df["code"].astype(str) == code
        ]

        if len(player_index) == 0:

            st.error("الكود غير موجود")

        else:

            idx = player_index[0]

            remaining = int(
                df.loc[idx, "sessions"]
            )

            if remaining <= 0:

                st.error(
                    "الاشتراك منتهي"
                )

            else:

                df.loc[idx, "sessions"] = (
                    remaining - 1
                )

                df.to_csv(
                    CSV_FILE,
                    index=False
                )

                st.success(
                    f"تم تسجيل حضور {df.loc[idx,'name']}"
                )

                st.info(
                    f"المتبقي {remaining-1} حصص"
                )

# ------------------------
# عرض اللاعبين
# ------------------------

elif menu == "اللاعبين":

    st.header("اللاعبين")

    st.dataframe(df)
