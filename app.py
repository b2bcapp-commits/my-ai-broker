import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import urllib.parse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Global Trade Hub", layout="wide", page_icon="🌍")

# อัปเดตข้อมูลอีเมลใหม่ของบอสตามที่แจ้ง
SENDER_EMAIL = "b2bcapp@gmail.com"
SENDER_PASSWORD = "xfym dbzl gekk jwig"
MY_WHATSAPP_LINK = "https://wa.me/66964474797?text=Hello%20CEO"

# เชื่อมต่อ Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 2. CORE FUNCTIONS ---
def get_user_data():
    try:
        return conn.read(ttl=0)
    except:
        return pd.DataFrame(columns=["username", "password", "email", "role"])

def save_to_sheets(updated_df):
    conn.update(data=updated_df)
    st.cache_data.clear()

def send_email(receiver, subject, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return False

# --- 3. UI STATE ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 4. SIDEBAR ---
df_users = get_user_data()
with st.sidebar:
    st.title("🌐 Global Hub")
    if not st.session_state['logged_in']:
        mode = st.radio("เมนูการเข้าถึง", ["Login", "Sign Up", "Forgot Password"])
    else:
        st.success(f"User: {st.session_state.username}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
        st.divider()
        st.markdown(f'''<a href="{MY_WHATSAPP_LINK}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 10px; border-radius: 5px; width: 100%; cursor: pointer; font-weight: bold;">WhatsApp CEO</button></a>''', unsafe_allow_html=True)

# --- 5. AUTH PAGES ---
if not st.session_state['logged_in']:
    if mode == "Login":
        st.title("🔐 เข้าสู่ระบบ")
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Sign In"):
            match = df_users[(df_users['username'].astype(str) == u) & (df_users['password'].astype(str) == p)]
            if not match.empty:
                st.session_state.logged_in = True
                st.session_state.username = u
                st.session_state.role = match.iloc[0]['role']
                st.session_state.user_email = match.iloc[0]['email']
                st.rerun()
            else:
                st.error("ข้อมูลไม่ถูกต้อง (กรุณาเช็ค Username/Password หรือสมัครสมาชิกใหม่)")
    
    elif mode == "Sign Up":
        st.title("📝 สมัครสมาชิก")
        nu = st.text_input("Username")
        ne = st.text_input("Email")
        np = st.text_input("Password", type="password")
        nr = st.selectbox("Role", ["Buyer", "Seller"])
        if st.button("สร้างบัญชี"):
            if nu and ne and np:
                new_data = pd.concat([df_users, pd.DataFrame([{"username": nu, "password": np, "email": ne, "role": nr}])], ignore_index=True)
                save_to_sheets(new_data)
                send_email(ne, "Welcome to Trade Hub", f"Hi {nu}, your account is ready!")
                st.success("สมัครสำเร็จ! กรุณาล็อกอิน")
                st.balloons()
            else:
                st.error("กรุณากรอกข้อมูลให้ครบ")

    elif mode == "Forgot Password":
        st.title("🔑 กู้คืนรหัสผ่าน")
        target = st.text_input("ระบุอีเมลที่ลงทะเบียน")
        if st.button("ส่งรหัสผ่าน"):
            match = df_users[df_users['email'] == target]
            if not match.empty:
                send_email(target, "Password Recovery", f"Your password is: {match.iloc[0]['password']}")
                st.success("ส่งรหัสผ่านไปทางอีเมลแล้ว!")
            else:
                st.error("ไม่พบอีเมลนี้ในฐานข้อมูล")
    st.stop()

# --- 6. MAIN CONTENT ---
st.title(f"📊 {st.session_state.role} Command Center")

if st.session_state.role == "CEO":
    tab1, tab2, tab3 = st.tabs(["📡 AI Lead Radar", "👥 Members", "📦 Product Management"])
    
    with tab1:
        st.header("🎯 ค้นหาลูกค้าใหม่")
        col1, col2 = st.columns(2)
        with col1:
            kw = st.text_input("สินค้า", "Sugar IC45")
            ct = st.text_input("ประเทศ", "Dubai")
        with col2:
            st.write("🔍 ช่องทางเจาะข้อมูล:")
            q = urllib.parse.quote(f"{kw} importer in {ct}")
            st.markdown(f"[🏢 สแกนบริษัทบน Google Maps](https://www.google.com/maps/search/{q})")
    
    with tab2:
        st.dataframe(get_user_data(), use_container_width=True)
    
    with tab3:
        st.header("➕ เพิ่มสินค้าใหม่ลงหน้าร้าน")
        with st.form("add_product"):
            p_name = st.text_input("ชื่อสินค้า (e.g. Sugar IC45)")
            p_price = st.text_input("ราคา/เงื่อนไข (e.g. $450/MT CIF)")
            p_desc = st.text_area("รายละเอียดสินค้า")
            if st.form_submit_button("ประกาศขาย"):
                prod_row = pd.DataFrame([{"username": p_name, "password": p_price, "email": p_desc, "role": "Product_Listing"}])
                save_to_sheets(pd.concat([df_users, prod_
