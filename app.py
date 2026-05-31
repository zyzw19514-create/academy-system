import streamlit as st
from datetime import datetime, timedelta

# تهيئة قاعدة البيانات في ذاكرة الصفحة
if "players_db" not in st.session_state:
    st.session_state.players_db = {}

st.title("🥋 نظام إدارة أكاديمية الياباني")
st.write("مستشار والدك الذكي لمتابعة الحضور والغياب والاشتراكات")

# القائمة الجانبية للتنقل
menu = ["تسجيل لاعب جديد", "سكانر الحضور والغياب", "عرض جميع اللاعبين"]
choice = st.sidebar.selectbox("اختر الشاشة", menu)

# --- الشاشة الأولى: تسجيل لاعب جديد ---
if choice == "تسجيل لاعب جديد":
    st.header("➕ تسجيل لاعب وتفعيل اشتراك")
    
    player_id = st.text_input("أدخل كود اللاعب (رقم مميز):")
    player_name = st.text_input("اسم اللاعب:")
    phone = st.text_input("رقم موبايل ولي الأمر:")
    
    if st.button("تفعيل الاشتراك (8 حصص / شهر)"):
        if player_id and player_name:
            if player_id in st.session_state.players_db:
                st.error("❌ هذا الكود مسجل مسبقاً للاعب آخر!")
            else:
                start_date = datetime.now()
                end_date = start_date + timedelta(days=30)
                
                st.session_state.players_db[player_id] = {
                    "name": player_name,
                    "phone": phone,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d"),
                    "remaining_lessons": 8,
                    "status": "Active"
                }
                st.success(f"✅ تم تسجيل الكابتن [{player_name}] بنجاح! اشتراكه ساري حتى {end_date.strftime('%Y-%m-%d')}")
        else:
            st.warning("⚠️ يرجى ملء خانة الكود والاسم!")

# --- الشاشة الثانية: سكانر الحضور والغياب ---
elif choice == "سكانر الحضور والغياب":
    st.header("🔍 شاشة تسجيل الحضور اليومي")
    st.write("تخيل أن هذا المربع هو القارئ الإلكتروني عند دخول اللاعب")
    
    scanned_id = st.text_input("مرر كود اللاعب هنا (اضغط Enter بعد الكتابة):")
    
    if scanned_id:
        if scanned_id in st.session_state.players_db:
            player = st.session_state.players_db[scanned_id]
            current_date = datetime.now()
            expiration_date = datetime.strptime(player["end_date"], "%Y-%m-%d")
            
            # فحص الصلاحية بالتواريخ
            if current_date > expiration_date:
                player["status"] = "Expired"
                st.error(f"🚨 دخول مرفوض! اشتراك اللاعب [{player['name']}] منتهي الصلاحية من يوم {player['end_date']}.")
            
            # فحص عدد الحصص
            elif player["remaining_lessons"] <= 0:
                st.error(f"🚨 دخول مرفوض! اللاعب [{player['name']}] استهلك الـ 8 حصص بالكامل.")
            
            # لو كله تمام اخصم حصة وسجل حضور
            else:
                player["remaining_lessons"] -= 1
                st.success(f"🟢 تم تسجيل حضور الكابتن: {player['name']}")
                st.metric(label="الحصص المتبقية له", value=player["remaining_lessons"])
                st.info(f"📅 تاريخ نهاية صلاحية الاشتراك: {player['end_date']}")
        else:
            st.error("❌ كود غير مسجل in النظام!")

# --- الشاشة الثالثة: عرض البيانات والتقارير ---
elif choice == "عرض جميع اللاعبين":
    st.header("📊 قائمة المشتركين الحالية")
    if st.session_state.players_db:
        for p_id, info in st.session_state.players_db.items():
            st.write(f"**كود:** {p_id} | **الاسم:** {info['name']} | **الحصص المتبقية:** {info['remaining_lessons']} | **ينتهي يوم:** {info['end_date']} | **الحالة:** {info['status']}")
            st.text("---------------------------------------------------------")
    else:
        st.info("لا يوجد لاعبون مسجلون حالياً.")