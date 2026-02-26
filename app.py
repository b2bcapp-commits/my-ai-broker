import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Pro Land AI v2.0", layout="wide", page_icon="🏢")

# 🔗 ลิงก์เดิมของคุณ (ห้ามเปลี่ยนรหัส ID นะครับ)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1om2aUXoNaPYfsmrI1IZjFL_94U9fZVqGg81cE65Jw28/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    return conn.read(spreadsheet=SHEET_URL, ttl="0")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: เมนูใหม่ ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/609/609803.png", width=100)
st.sidebar.title("Wealth Management")
menu = st.sidebar.selectbox("เลือกฟังก์ชัน", ["📊 แดชบอร์ดวิเคราะห์", "➕ บันทึกดีลใหม่", "🧮 เครื่องคิดเลขภาษี/โอน"])

df = get_data()

if menu == "📊 แดชบอร์ดวิเคราะห์":
    st.title("📈 วิเคราะห์พอร์ตดีลทองคำ")
    
    # สรุปข้อมูลสำคัญ (Metrics)
    c1, c2, c3 = st.columns(3)
    c1.metric("จำนวนดีลทั้งหมด", len(df))
    c2.metric("ราคาเฉลี่ยต่อหน่วย", f"{df['ราคาต่อหน่วย'].mean():,.0f} บ.")
    c3.metric("ดีลความเสี่ยงต่ำ", len(df[df['Risk_Score'] < 30]))

    # แสดงตารางพร้อมแถบสีความเสี่ยง
    st.subheader("🗂️ รายการทรัพย์สินทั้งหมด")
    def highlight_risk(s):
        return ['background-color: #ffcccc' if s.Risk_Score > 50 else 'background-color: #d1e7dd' if s.Risk_Score < 30 else '' for _ in s]
    
    st.dataframe(df.style.apply(highlight_risk, axis=1), use_container_width=True)

elif menu == "➕ บันทึกดีลใหม่":
    st.title("📝 เพิ่มข้อมูลดีลใหม่")
    with st.form("add_form"):
        col1, col2 = st.columns(2)
        with col1:
            loc = st.text_input("ทำเล (เช่น ราชพฤกษ์)")
            land_type = st.selectbox("ประเภท", ["ที่ดินเปล่า", "ตึกแถว", "คอนโด", "บ้านเดี่ยว"])
            price = st.number_input("ราคาต่อหน่วย (ตร.ว. ละ)", value=0)
        with col2:
            title_deed = st.text_input("เลขที่โฉนด")
            city_color = st.selectbox("สีผังเมือง", ["แดง (พาณิชย์)", "ส้ม (หนาแน่นมาก)", "เหลือง (หนาแน่นน้อย)", "เขียว (เกษตร)"])
            risk = st.slider("ประเมินความเสี่ยง (0-100)", 0, 100, 20)
            
        submitted = st.form_submit_button("🚀 บันทึกลงระบบ Cloud")
        if submitted:
            new_row = pd.DataFrame([{
                "ทำเล": loc, "ประเภท": land_type, "เลขที่โฉนด": title_deed,
                "ราคาต่อหน่วย": price, "สีผังเมือง": city_color, "Risk_Score": risk,
                "Date_Added": pd.Timestamp.now().strftime("%Y-%m-%d")
            }])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(spreadsheet=SHEET_URL, data=updated_df)
            st.success("บันทึกสำเร็จ! ข้อมูลถูกส่งไปที่ Google Sheets แล้ว")
            st.balloons()

elif menu == "🧮 เครื่องคิดเลขภาษี/โอน":
    st.title("⚖️ ประมาณการค่าใช้จ่ายวันโอน")
    price_deal = st.number_input("ราคาซื้อขายจริง (บาท)", value=1000000)
    gov_price = st.number_input("ราคาประเมินราชการ (บาท)", value=800000)
    
    # สูตรคำนวณเบื้องต้น
    transfer_fee = gov_price * 0.02
    duty_fee = max(price_deal, gov_price) * 0.005 # อากรสแตมป์
    
    st.write(f"1. ค่าธรรมเนียมการโอน (2%): **{transfer_fee:,.0f} บาท**")
    st.write(f"2. ค่าอากรสแตมป์ (0.5%): **{duty_fee:,.0f} บาท**")
    st.info("หมายเหตุ: ยังไม่รวมภาษีเงินได้บุคคลธรรมดาหัก ณ ที่จ่าย")
