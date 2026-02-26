import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Pro AI Broker Online", layout="wide")

# 🔗 1. วางลิงก์ Google Sheets ของคุณที่นี่ (ต้องเปิด Share เป็น Anyone with link เรียบร้อยแล้ว)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1om2aUXoNaPYfsmrI1IZjFL_94U9fZVqGg81cE65Jw28/edit?usp=sharing"

# เชื่อมต่อระบบ Cloud Database
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    return conn.read(spreadsheet=SHEET_URL, ttl="0")

st.title("🏙️ AI Wealth Real Estate Online")

# แสดงข้อมูลจาก Google Sheets
try:
    df = get_data()
    # แสดงตารางดีล
    st.subheader("🔍 ดีลทองคำในพอร์ตของคุณ")
    st.dataframe(df, use_container_width=True)
except Exception as e:
    st.warning("ระบบกำลังรอการเชื่อมต่อกับ Google Sheets... โปรดตรวจสอบลิงก์ในโค้ด")
    st.error(f"รายละเอียดข้อผิดพลาด: {e}")

# ปุ่มสำหรับเพิ่มดีลทดสอบจากมือถือ
st.divider()
st.subheader("➕ เพิ่มข้อมูลด่วน")
if st.button("🚀 บันทึกดีลทดสอบลง Google Sheet"):
    new_data = pd.DataFrame([{
        "ทำเล": "ทดสอบจากระบบ Cloud",
        "ประเภท": "ที่ดินเปล่า",
        "Date_Added": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
    }])
    # อัปเดตข้อมูล
    if 'df' in locals():
        updated_df = pd.concat([df, new_data], ignore_index=True)
    else:
        updated_df = new_data
        
    conn.update(spreadsheet=SHEET_URL, data=updated_df)
    st.success("✅ บันทึกสำเร็จ! ข้อมูลจะไปปรากฏใน Google Sheets ของคุณทันที")
