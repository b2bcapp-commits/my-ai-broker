import streamlit as st
import pandas as pd

# --- 1. CONFIG ---
st.set_page_config(page_title="Global Trade Hub", layout="wide", page_icon="🌍")

# ช่องทางติดต่อ CEO (เปลี่ยน YOUR_NUMBER เป็นเบอร์โทรศัพท์ของคุณ เช่น 66812345678)
MY_LINE_LINK = "https://line.me/ti/p/~YOUR_LINE_ID"
MY_WHATSAPP_LINK = "https://wa.me/66812345678" 

# --- 2. DATABASE SIMULATION (เก็บในตัวแปรชั่วคราว) ---
if 'user_db' not in st.session_state:
    st.session_state['user_db'] = {
        "admin": {"password": "789", "role": "CEO", "email": "ceo@trade.com"},
        "seller": {"password": "123", "role": "Seller", "email": "seller@test.com"},
        "buyer": {"password": "456", "role": "Buyer", "email": "buyer@test.com"}
    }

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['current_user'] = None

# --- 3. LOGIN / SIGNUP / RESET LOGIC ---
st.sidebar.title("🌐 Access Control")
auth_mode = st.sidebar.radio("เลือกดำเนินการ", ["Login", "Sign Up", "Forgot Password"])

if not st.session_state['logged_in']:
    if auth_mode == "Login":
        st.title("🔐 Login to Global Trade Hub")
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Sign In"):
            db = st.session_state['user_db']
            if user in db and db[user]["password"] == pw:
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = user
                st.rerun()
            else:
                st.error("Invalid credentials")

    elif auth_mode == "Sign Up":
        st.title("📝 Register New Account")
        new_user = st.text_input("Create Username")
        new_email = st.text_input("Your Email")
        new_pw = st.text_input("Set Password", type="password")
        new_role = st.selectbox("I am a...", ["Buyer", "Seller"])
        if st.button("Create Account"):
            if new_user and new_pw and new_email:
                st.session_state['user_db'][new_user] = {"password": new_pw, "role": new_role, "email": new_email}
                st.success("Registration Successful! Please switch to Login.")
            else:
                st.warning("Please fill all fields")

    elif auth_mode == "Forgot Password":
        st.title("🔑 Password Recovery")
        reset_email = st.text_input("Enter your registered email")
        if st.button("Send Reset Link"):
            st.info(f"ระบบกำลังส่งลิงก์เปลี่ยนรหัสผ่านไปยัง {reset_email}...")
            st.success("📩 ลิงก์ถูกส่งเรียบร้อยแล้ว! (กรุณาตรวจสอบใน Inbox หรือ Junk Mail)")
    st.stop()

# --- 4. MAIN APP (AFTER LOGIN) ---
user_info = st.session_state['user_db'][st.session_state['current_user']]
role = user_info['role']

# Sidebar สำหรับติดต่อ
st.sidebar.divider()
st.sidebar.write(f"Logged in as: **{st.session_state['current_user']}**")
st.sidebar.subheader("📱 Quick Contact")
st.sidebar.markdown(f"[![Line](https://img.shields.io/badge/LINE-00C300?style=for-the-badge&logo=line&logoColor=white)]({MY_LINE_LINK})")
st.sidebar.markdown(f"[![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)]({MY_WHATSAPP_LINK})")

if st.sidebar.button("Logout"):
    st.session_state['logged_in'] = False
    st.rerun()

# --- 5. DASHBOARDS ---
if role == "CEO":
    st.title("📊 CEO Master Dashboard")
    st.subheader("Manage Global Deals & Users")
    st.write("Current Registered Users:", len(st.session_state['user_db']))
    st.dataframe(pd.DataFrame(st.session_state['user_db']).T) # แสดงตารางสมาชิกทั้งหมด

elif role == "Seller":
    st.title("🏭 Seller Portal")
    st.write("ลงทะเบียนสินค้าของคุณเพื่อเสนอต่อผู้ซื้อทั่วโลก")
    with st.form("product_form"):
        p_name = st.text_input("ชื่อสินค้า (เช่น ICUMSA 45)")
        p_price = st.text_input("ราคาต่อหน่วย (USD)")
        submit = st.form_submit_button("บันทึกข้อมูล")
        if submit:
            st.success("ข้อมูลถูกส่งไปยัง CEO แล้ว")

elif role == "Buyer":
    st.title("🛒 Premium Marketplace")
    st.write("รายการสินค้าพรีเมียมที่ผ่านการคัดกรองแล้ว")
    st.table(pd.DataFrame({
        "Product": ["Sugar IC45", "Chicken Wings", "Fuel Oil"],
        "Status": ["Verified", "Verified", "Verified"]
    }))
