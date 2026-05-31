import streamlit as st
import qrcode
from io import BytesIO
import pandas as pd

# 1. إعدادات الصفحة والديزاين الاحترافي (أسود ملكي وذهبي)
st.set_page_config(page_title="الأكاديمية اليابانية للكاراتيه", page_icon="🥋", layout="centered")

st.markdown("""
    <style>
    /* خلفية التطبيق والنصوص */
    .stApp {
        background-color: #121212;
        color: #FFFFFF;
    }
    /* الهيدر الرئيسي الفخم */
    .main-header {
        text-align: center;
        padding: 25px;
        background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
        border-radius: 15px;
        border-bottom: 5px solid #D4AF37;
        box-shadow: 0 4px 15px rgba(0,0,0,0.6);
        margin-bottom: 30px;
    }
    .main-header h1 {
        color: #D4AF37 !important;
        font-size: 2.3rem !important;
        margin: 0;
        font-family: 'Cairo', sans-serif;
    }
    /* كارت بيانات اللاعب */
    .player-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 12px;
        border-right: 6px solid #28a745;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    /* أزرار السيستم */
    div.stButton > button {
        background-color: #D4AF37 !important;
        color: #121212 !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px !important;
        font-size: 16px !important;
        transition: all 0.3s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #FFFFFF !important;
        transform: translateY(-2px);
    }
    /* خانات الكتابة */
    .stTextInput > div > div > input {
        background-color: #1e1e1e !important;
        color: #FFF !important;
        border: 1px solid #444 !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #D4AF37 !important;
        box-shadow: 0 0 8px rgba(212,175,55,0.5) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# الهيدر باسم الأكاديمية الصحيح
st.markdown('<div class="main-header"><h1>🥋 الأَكَادِيمِيَّة اليَابَانِيَّة لِلكَارَاتِيه</h1></div>', unsafe_allow_html=True)

# 2. قاعدة بيانات اللاعبين المؤقتة في الذاكرة
if 'players_db' not in st.session_state:
    st.session_state.players_db = {
        "101": {"name": "أحمد محمد", "phone": "01012345678", "sessions": 8},
        "102": {"name": "زياد أحمد", "phone": "01098765432", "sessions": 12}
    }

# القائمة الجانبية الأنيقة
st.sidebar.markdown("<h3 style='text-align:center; color:#D4AF37;'>لوحة التحكم</h3>", unsafe_allow_html=True)
choice = st.sidebar.radio("اختر الشاشة:", ["📱 شاشة تسجيل الحضور اليومي", "🔐 لوحة تحكم الإدارة والتعديل"])

# ----------------- الشاشة الأولى: تسجيل الحضور بسكان الـ QR -----------------
if choice == "📱 شاشة تسجيل الحضور اليومي":
    st.markdown("<h3 style='color: #D4AF37; text-align:right;'>توجيه: مرر كود اللاعب أو استخدم جهاز المسح</h3>", unsafe_allow_html=True)
    
    player_id = st.text_input("اضغط هنا قبل استخدام القارئ الإلكتروني (الاسكانر):", key="scan_input")
    
    if player_id:
        if player_id in st.session_state.players_db:
            player = st.session_state.players_db[player_id]
            
            # كارت عرض البيانات والجملة المظبوطة
            st.markdown(f"""
            <div class="player-card">
                <h2 style='color: #28a745; text-align: right; margin: 0;'>✅ تم تسجيل حضور اللاعب: {player['name']}</h2>
                <p style='text-align: right; margin: 10px 0 0 0; color: #aaa; font-size: 1.1rem;'>رقم هاتف ولي الأمر: {player['phone']}</p>
                <p style='text-align: right; margin: 5px 0 0 0; color: #D4AF37; font-weight: bold; font-size: 1.2rem;'>الرصيد الحالي: {player['sessions']} حصة</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("خصم حصة واحدة وتأكيد الحضور 🥋"):
                if player['sessions'] > 0:
                    st.session_state.players_db[player_id]['sessions'] -= 1
                    st.balloons() # تأثير احتفالي بالبالونات
                    st.success(f"🎯 تم الخصم بنجاح! الرصيد المتبقي للاعب {player['name']} هو: {st.session_state.players_db[player_id]['sessions']} حصة.")
                else:
                    st.error("⚠️ تنبيه: رصيد الحصص انتهى (0 حصة)! يرجى تجديد الاشتراك من لوحة الإدارة.")
        else:
            st.error("❌ عذراً، هذا الكود غير مسجل في نظام الأكاديمية!")

# ----------------- الشاشة الثانية: لوحة الإدارة -----------------
elif choice == "🔐 لوحة تحكم الإدارة والتعديل":
    st.markdown("<h3 style='color: #D4AF37; text-align:right;'>صلاحيات الإدارة</h3>", unsafe_allow_html=True)
    admin_pass = st.text_input("أدخل كلمة المرور السرية لفتح الصلاحيات:", type="password")
    
    if admin_pass == "1234":
        st.success("🔓 تم الدخول بنجاح.")
        
        tab1, tab2, tab3 = st.tabs(["➕ إضافة لاعب جديد", "✏️ تعديل بيانات وشحن حصص", "📋 كشف المشتركين"])
        
        with tab1:
            st.write("### ➕ تسجيل لاعب جديد وتوليد الـ QR")
            new_id = st.text_input("أدخل كود الـ ID الجديد:")
            new_name = st.text_input("اسم اللاعب بالكامل:")
            new_phone = st.text_input("رقم موبايل ولي الأمر:")
            new_sessions = st.number_input("عدد حصص الاشتراك:", min_value=1, max_value=48, value=8)
            
            if st.button("حفظ اللاعب وإنشاء كود الـ QR"):
                if new_id and new_name:
                    if new_id not in st.session_state.players_db:
                        st.session_state.players_db[new_id] = {"name": new_name, "phone": new_phone, "sessions": new_sessions}
                        st.success(f"🎉 تم حفظ اللاعب {new_name} في السيستم!")
                        
                        # توليد QR كود شيك جداً
                        qr = qrcode.QRCode(version=1, box_size=10, border=3)
                        qr.add_data(new_id)
                        qr.make(fit=True)
                        img = qr.make_image(fill_color="#121212", back_color="white")
                        
                        buf = BytesIO()
                        img.save(buf)
                        st.image(buf.getvalue(), caption=f"كود QR جاهز للطباعة للاعب: {new_name}")
                    else:
                        st.error("⚠️ هذا الكود مستخدم بالفعل!")
                else:
                    st.warning("برجاء ملء خانة الكود والاسم!")
                    
        with tab2:
            st.write("### ✏️ تعديل بيانات لاعب أو تجديد اشتراك")
            edit_id = st.text_input("ادخل كود اللاعب المراد تعديله:")
            if edit_id in st.session_state.players_db:
                player_to_edit = st.session_state.players_db[edit_id]
                
                edit_name = st.text_input("تعديل الاسم:", value=player_to_edit['name'])
                edit_phone = st.text_input("تعديل رقم الهاتف:", value=player_to_edit['phone'])
                edit_sessions = st.number_input("تعديل رصيد الحصص الحالي (شحن):", min_value=0, value=player_to_edit['sessions'])
                
                if st.button("حفظ التعديلات الجديدة 💾"):
                    st.session_state.players_db[edit_id]['name'] = edit_name
                    st.session_state.players_db[edit_id]['phone'] = edit_phone
                    st.session_state.players_db[edit_id]['sessions'] = edit_sessions
                    st.success("✅ تم تحديث البيانات بنجاح!")
            elif edit_id:
                st.error("❌ الكود غير صحيح أو غير موجود.")
                
        with tab3:
            st.write("### 📋 جدول كشف جميع اللاعبين")
            if st.session_state.players_db:
                df = pd.DataFrame.from_dict(st.session_state.players_db, orient='index')
                df.index.name = 'الكود (ID)'
                df.columns = ['اسم اللاعب', 'رقم هاتف ولي الأمر', 'الحصص المتبقية']
                st.dataframe(df, use_container_width=True)
            else:
                st.info("لا يوجد لاعبين مسجلين حالياً.")
                
    elif admin_pass != "":
        st.error("❌ كلمة المرور خطأ!")
