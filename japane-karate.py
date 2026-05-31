import pandas as pd
from datetime import datetime

# 1. تحميل بيانات اللاعبين (بافتراض وجود ملف Excel أو CSV)
# يفضل أن يحتوي الملف على أعمدة: [ID, Name, Subscription_Status]
def load_players(file_path):
    return pd.read_csv(file_path)

# 2. تسجيل حضور لاعب جديد
def mark_attendance(df, player_id):
    # البحث عن اللاعب في القائمة
    player = df[df['ID'] == player_id]
    
    if not player.empty:
        # إضافة سجل الحضور بالتاريخ الحالي
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"تم تسجيل حضور: {player['Name'].values[0]} في {date}")
        # هنا يمكنك إضافة كود لإرسال البيانات لـ Google Sheets
    else:
        print("خطأ: رقم اللاعب غير موجود في قاعدة البيانات.")

# 3. عرض بيانات اللاعبين
def display_players(df):
    print("--- قائمة اللاعبين المسجلين ---")
    print(df[['ID', 'Name', 'Subscription_Status']])

# مثال للاستخدام:
# players_df = load_players('players_data.csv')
# mark_attendance(players_df, 101)
