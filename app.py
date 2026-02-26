import streamlit as st

# --- 1. ระบบฐานข้อมูลรหัสผ่าน (จำลอง) ---
# ในอนาคตสามารถเชื่อมต่อกับฐานข้อมูลจริงได้
USER_CREDENTIALS = {
    "admin_ceo": {"password": "ceo789", "role": "CEO"},
    "seller_01": {"password": "sale123", "role": "Seller"},
    "buyer_99": {"password": "buy456", "role": "Buyer"}
}

# --- 2. ฟังก์ชันตรวจสอบการเข้าสู่ระบบ ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['role'] = None

if not st.session_state['logged_in']:
    st.title("🔐 Global Brokerage Login")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if user in USER_CREDENTIALS and USER_CREDENTIALS[user]["password"] == pw:
            st.session_state['logged_in'] = True
            st.session_state['role'] = USER_CREDENTIALS[user]["role"]
            st.rerun()
        else:
            st.error("รหัสผ่านไม่ถูกต้อง")
else:
    # --- 3. หน้าต่างหลังจาก Login แยกตามบทบาท ---
    role = st.session_state['role']
    st.sidebar.title(f"👤 Role: {role}")
    
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.rerun()

    if role == "CEO":
        st.title("📊 CEO Dashboard (Master Control)")
        st.write("มองเห็นการเคลื่อนไหวของทั้งผู้ซื้อและผู้ขาย")
        # โค้ดส่วนจัดการค่าคอมมิชชั่นและอนุมัติเอกสาร

    elif role == "Seller":
        st.title("🏭 Seller Portal (ระบบผู้ขาย)")
        st.write("อัปโหลดสินค้าและสถานะสต็อกของคุณ")
        with st.expander("📥 ลงทะเบียนสินค้าใหม่"):
            st.text_input("ชื่อสินค้า (เช่น น้ำมันปาล์ม)")
            st.file_uploader("อัปโหลดใบรับรองคุณภาพ (SGS/ISO)")

    elif role == "Buyer":
        st.title("🛒 Buyer Portal (ระบบผู้ซื้อ)")
        st.write("ค้นหาสินค้าที่ผ่านการตรวจสอบ Due Diligence แล้ว")
        # แสดงรายการสินค้าที่ CEO อนุมัติแล้วเท่านั้น
        st.info("รายการแนะนำ: น้ำตาล ICUMSA 45 (Verified)")
