import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- 1. SETTINGS ---
st.set_page_config(page_title="Power Reset Mode", layout="wide")

# เชื่อมต่อฐานข้อมูล
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # บังคับให้อ่านค่าใหม่ล่าสุดเสมอ (ttl=0)
    df = conn.read(ttl=0)
except Exception as e:
    st.error(f"การเชื่อมต่อผิดพลาด: {e}")
    st.stop()

# --- 2. DEBUG MODE (บอสจะเห็นว่าแอปเห็นข้อมูลอะไรอยู่) ---
with st.expander("🔍 ตรวจสอบฐานข้อมูล (Debug)"):
    st.write("แอปมองเห็นข้อมูลใน Google Sheets ตามนี้ครับ:")
    st.dataframe(df)

# --- 3. LOGIN LOGIC ---
st.title("🔐 เข้าสู่ระบบ (BethofenPro)")

# พยายามจับคู่ชื่อหัวตาราง (ไม่ว่าบอสจะพิมพ์ไทยหรืออังกฤษ)
u_input = st.text_input("Username")
p_input = st.text_input("Password", type="password")

if st.button("Sign In"):
    # ตรวจสอบว่ามีข้อมูล BethofenPro ไหม
    # เราจะค้นหาจากทุกช่องในตาราง
    found = False
    for index, row in df.iterrows():
        # เช็คว่าแถวไหนมี BethofenPro และรหัส Pronet@1234
        if str(u_input).strip() in [str(val).strip() for val in row.values] and \
           str(p_input).strip() in [str(val).strip() for val in row.values]:
            found = True
            st.session_state.logged_in = True
            st.session_state.username = u_input
            break
    
    if found:
        st.success("✅ ล็อกอินสำเร็จ!")
        st.balloons()
        # ส่วนแสดงผลของ CEO
        st.divider()
        st.header(f"Welcome back, {u_input}!")
        st.write("ตอนนี้แอปเชื่อมต่อกับ Google Sheets ของบอสได้สมบูรณ์แล้วครับ")
    else:
        st.error("❌ ยังไม่พบชื่อนี้ในระบบ หรือข้อมูลไม่ตรงกับใน Sheets")
        st.info("คำแนะนำ: ตรวจสอบในตาราง Debug ด้านบนว่ามีชื่อ BethofenPro หรือยัง")
