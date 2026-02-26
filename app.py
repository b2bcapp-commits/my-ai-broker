import streamlit as st
import pandas as pd

# --- 1. SETTINGS ---
st.set_page_config(page_title="Global Trade Platform", layout="wide", page_icon="🌐")

# --- 2. DATABASE ---
USER_CREDENTIALS = {
    "admin": {"password": "789", "role": "CEO", "name": "CEO Master"},
    "seller": {"password": "123", "role": "Seller", "name": "Thai Supplier"},
    "buyer": {"password": "456", "role": "Buyer", "name": "Global Investor"}
}

# --- 3. SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['role'] = None
    st.session_state['lang'] = "ไทย"

# --- 4. LOGIN PAGE ---
if not st.session_state['logged_in']:
    st.title("🔐 Login System")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if user in USER_CREDENTIALS and USER_CREDENTIALS[user]["password"] == pw:
            st.session_state['logged_in'] = True
            st.session_state['role'] = USER_CREDENTIALS[user]["role"]
            st.rerun()
        else:
            st.error("Invalid Username or Password")
    st.stop()

# --- 5. MAIN APP ---
role = st.session_state['role']
lang = st.sidebar.selectbox("🌐 Language", ["ไทย", "English", "简体中文"])

if st.sidebar.button("Log out"):
    st.session_state['logged_in'] = False
    st.rerun()

# --- CONTACT CEO BUTTON (ปุ่มทัก LINE) ---
st.sidebar.divider()
st.sidebar.subheader("📱 Contact CEO")
line_msg = st.sidebar.text_area("ข้อความถึง CEO (Message)", height=100)
# ใส่ Link LINE OA หรือ LINE ส่วนตัวของคุณที่นี่
my_line_link = "https://line.me/ti/p/~YOUR_ID" 

if st.sidebar.button("ส่งข้อความ (Send)"):
    if line_msg:
        st.sidebar.success("ระบบบันทึกข้อความแล้ว กรุณากดปุ่มด้านล่างเพื่อยืนยันส่งใน LINE")
        st.sidebar.markdown(f"[![Line](https://img.shields.io/badge/LINE-00C300?style=for-the-badge&logo=line&logoColor=white)]({my_line_link})")

# --- DASHBOARDS ---
if role == "CEO":
    st.title("📊 ศูนย์ควบคุม CEO อัจฉริยะ")
    c1, c2, c3 = st.columns(3)
    c1.metric("ค่าคอมมิชชั่นสะสม", "฿15.2M", "+2.1M")
    c2.metric("ผู้ขายในระบบ", "42", "Verified")
    c3.metric("ผู้ซื้อสนใจ", "128", "Hot")
    
    st.divider()
    st.subheader("📝 รายการติดต่อล่าสุด (Logs)")
    st.write("1. Buyer_China: สนใจน้ำตาล 50,000 ตัน")
    st.write("2. Seller_TH: อัปเดตสต็อกไก่แช่แข็ง")

elif role == "Seller":
    st.title("🏭 ระบบผู้ขาย (Seller Portal)")
    st.text_input("ชื่อสินค้าที่ต้องการเสนอ")
    st.file_uploader("แนบใบรับรอง (SGS/Cert)")
    st.button("ลงทะเบียนสินค้า")

elif role == "Buyer":
    st.title("🛒 ตลาดผู้ซื้อ (Buyer Marketplace)")
    st.info("รายการสินค้าที่ตรวจสอบแล้ว")
    df = pd.DataFrame({
        "สินค้า": ["Sugar IC45", "Chicken Wings", "Diesel EN590"],
        "สถานะ": ["✅ Verified", "✅ Verified", "✅ Verified"]
    })
    st.table(df)
