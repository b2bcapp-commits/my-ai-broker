import streamlit as st
import pandas as pd

# --- 1. CONFIG ---
st.set_page_config(page_title="Global Trade AI", layout="wide", page_icon="📈")

# ลิงก์ LINE OA ของคุณ (เอามาจากหน้าเพิ่มเพื่อนใน LINE OA Manager)
# หรือใช้ไอดี LINE ส่วนตัวของคุณแทนที่ YOUR_ID
MY_LINE_LINK = "https://line.me/ti/p/~YOUR_ID" 

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['role'] = None

# --- 3. LOGIN PAGE ---
if not st.session_state['logged_in']:
    st.title("🔐 Global Trade Master Login")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "admin" and pw == "789":
            st.session_state['logged_in'] = True
            st.session_state['role'] = "CEO"
            st.rerun()
        elif user == "buyer" and pw == "456":
            st.session_state['logged_in'] = True
            st.session_state['role'] = "Buyer"
            st.rerun()
        elif user == "seller" and pw == "123":
            st.session_state['logged_in'] = True
            st.session_state['role'] = "Seller"
            st.rerun()
        else:
            st.error("Invalid Credentials")
    st.stop()

# --- 4. MAIN INTERFACE ---
role = st.session_state['role']

# Sidebar สำหรับติดต่อ
with st.sidebar:
    st.title("🌐 Menu")
    if st.button("Log out"):
        st.session_state['logged_in'] = False
        st.rerun()
    
    st.divider()
    st.subheader("📱 ติดต่อฝ่ายสนับสนุน (CEO)")
    st.write("หากมีข้อสงสัย หรือต้องการปิดดีลด่วน")
    st.markdown(f'''
    <a href="{MY_LINE_LINK}" target="_blank">
        <button style="background-color: #00c300; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; width: 100%;">
            Chat with CEO via LINE
        </button>
    </a>
    ''', unsafe_allow_html=True)

# --- 5. DASHBOARDS ---
if role == "CEO":
    st.title("📊 CEO Command Center")
    c1, c2, c3 = st.columns(3)
    c1.metric("Est. Commission", "฿15.2M", "+12%")
    c2.metric("Active Deals", "24", "Verified")
    c3.metric("New Leads", "8", "Action Required")
    
    st.divider()
    st.subheader("🔔 รายการที่ต้องอนุมัติ (Pending Approval)")
    st.write("- Seller_01: ลงทะเบียน น้ำตาล IC45 (Brazil)")
    st.write("- Buyer_Asia: สนใจซื้อ ไก่แช่แข็ง (500 Tons)")

elif role == "Buyer":
    st.title("🛒 Marketplace (Verified Only)")
    st.info("รายการสินค้าที่ผ่านการทำ Due Diligence เรียบร้อยแล้ว")
    df = pd.DataFrame({
        "Product": ["Sugar IC45", "Chicken Wings", "Diesel EN590"],
        "Origin": ["Thailand", "Brazil", "Kazakhstan"],
        "Cert": ["SGS Verified", "DLD Verified", "Verified"]
    })
    st.table(df)
    if st.button("🎯 สนใจปิดดีล/ขอข้อมูลเพิ่ม"):
        st.success("กรุณากดปุ่ม LINE ที่แถบด้านซ้ายเพื่อรับเอกสาร POP ฉบับเต็ม")

elif role == "Seller":
    st.title("🏭 Seller Portal")
    st.subheader("ลงทะเบียนสินค้าใหม่")
    st.text_input("ชื่อสินค้า/ประเภท")
    st.number_input("จำนวนที่สามารถส่งมอบได้ (MT)")
    st.file_uploader("แนบใบ Cert/SGS")
    if st.button("ส่งให้ CEO ตรวจสอบ"):
        st.balloons()
        st.success("ข้อมูลส่งถึงบอสแล้ว! เราจะติดต่อกลับหลังตรวจสอบเอกสาร")
