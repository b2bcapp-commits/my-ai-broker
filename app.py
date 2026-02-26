import streamlit as st
import pandas as pd

# --- 1. การตั้งค่าเบื้องต้น ---
st.set_page_config(page_title="Global Trade Platform", layout="wide")

# --- 2. ฐานข้อมูลผู้ใช้ (แก้ไขรหัสผ่านที่นี่) ---
USER_CREDENTIALS = {
    "admin": {"password": "789", "role": "CEO", "name": "CEO Master"},
    "seller": {"password": "123", "role": "Seller", "name": "Thai Supplier"},
    "buyer": {"password": "456", "role": "Buyer", "name": "Global Investor"}
}

# --- 3. ระบบจัดการการเข้าสู่ระบบ (Session State) ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['role'] = None
    st.session_state['user_name'] = ""

# --- 4. หน้าจอ Login ---
if not st.session_state['logged_in']:
    st.title("🔐 Global Brokerage Platform")
    st.subheader("กรุณาเข้าสู่ระบบเพื่อดำเนินการ")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        user = st.text_input("ชื่อผู้ใช้ (Username)")
        pw = st.text_input("รหัสผ่าน (Password)", type="password")
        if st.button("เข้าสู่ระบบ"):
            if user in USER_CREDENTIALS and USER_CREDENTIALS[user]["password"] == pw:
                st.session_state['logged_in'] = True
                st.session_state['role'] = USER_CREDENTIALS[user]["role"]
                st.session_state['user_name'] = USER_CREDENTIALS[user]["name"]
                st.rerun()
            else:
                st.error("❌ ข้อมูลไม่ถูกต้อง")
    st.stop()

# --- 5. หน้าต่างการทำงานหลัก (หลัง Login) ---
role = st.session_state['role']
st.sidebar.title(f"👤 {st.session_state['user_name']}")
st.sidebar.info(f"บทบาท: {role}")

if st.sidebar.button("ออกจากระบบ (Logout)"):
    st.session_state['logged_in'] = False
    st.rerun()

# แยกเมนูตามบทบาท
if role == "CEO":
    st.title("📊 ศูนย์ควบคุม CEO")
    st.write("ยินดีต้อนรับครับบอส หน้าต่างนี้มีไว้คุมดีลทั่วโลก")
    st.metric("ค่าคอมมิชชั่นสะสม (คาดการณ์)", "฿15M", "+2M")
    
elif role == "Seller":
    st.title("🏭 หน้าต่างผู้ขาย (Seller)")
    st.write("อัปโหลดสินค้าของคุณเพื่อให้ผู้ซื้อทั่วโลกเห็น")
    st.text_input("ชื่อสินค้าส่งออก")
    st.button("ลงทะเบียนสินค้า")

elif role == "Buyer":
    st.title("🛒 หน้าต่างผู้ซื้อ (Buyer)")
    st.write("ค้นหาสินค้าที่ผ่านการตรวจสอบ Due Diligence แล้ว")
    st.dataframe(pd.DataFrame({"สินค้า": ["น้ำตาล", "ไก่"], "สถานะ": ["Verified", "Verified"]}))
