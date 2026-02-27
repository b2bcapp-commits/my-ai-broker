import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import urllib.parse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. SETTING ---
st.set_page_config(page_title="Global Trade Hub", layout="wide", page_icon="🌍")

SENDER_EMAIL = "dropshipmillionaire19@gmail.com"
SENDER_PASSWORD = "byyh oiii eibi cuov"
MY_WHATSAPP_LINK = "https://wa.me/66964474797?text=Hello%20CEO"

# เชื่อมต่อฐานข้อมูล
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 2. FUNCTIONS ---
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
    except:
        return False

# --- 3. UI STATE ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 4. SIDEBAR NAVIGATION ---
df_users = get_user_data()

with st.sidebar:
    st.title("🌐 Global Hub")
    if not st.session_state['logged_in']:
        mode = st.radio("เมนูการเข้าถึง", ["Login", "Sign Up", "Forgot Password"])
    else:
        st.success(f"ผู้ใช้งาน: {st.session_state.username}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
        st.divider()
        st.markdown(f'''<a href="{MY_WHATSAPP_LINK}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 10px; border-radius: 5px; width: 100%; cursor: pointer; font-weight: bold;">WhatsApp CEO</button></a>''', unsafe_allow_html=True)

# --- 5. AUTHENTICATION PAGES ---
if not st.session_state['logged_in']:
    if mode == "Login":
        st.title("🔐 เข้าสู่ระบบ")
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Sign In"):
            match = df_users[(df_users['username'] == u) & (df_users['password'] == p)]
            if not match.empty:
                st.session_state.logged_in = True
                st.session_state.username = u
                st.session_state.role = match.iloc[0]['role']
                st.rerun()
            else:
                st.error("Username หรือ Password ไม่ถูกต้อง")

    elif mode == "Sign Up":
        st.title("📝 สมัครสมาชิก")
        nu = st.text_input("Username")
        ne = st.text_input("Email")
        np = st.text_input("Password", type="password")
        nr = st.selectbox("ฉันเป็นใคร", ["Buyer", "Seller"])
        if st.button("สร้างบัญชี"):
            if nu and ne and np:
                new_data = pd.DataFrame([{"username": nu, "password": np, "email": ne, "role": nr}])
                save_to_sheets(pd.concat([df_users, new_data], ignore_index=True))
                send_email(ne, "ยินดีต้อนรับ", f"คุณ {nu} สมัครสมาชิกสำเร็จแล้ว!")
                st.success("ลงทะเบียนสำเร็จ!")
                st.balloons()
            else:
                st.error("กรุณากรอกข้อมูลให้ครบ")

    elif mode == "Forgot Password":
        st.title("🔑 กู้คืนรหัสผ่าน")
        target = st.text_input("กรอกอีเมลที่ลงทะเบียนไว้")
        if st.button("ส่งรหัสผ่านให้ฉัน"):
            user_info = df_users[df_users['email'] == target]
            if not user_info.empty:
                pwd = user_info.iloc[0]['password']
                if send_email(target, "กู้คืนรหัสผ่าน", f"รหัสผ่านของคุณคือ: {pwd}"):
                    st.success("📩 ส่งรหัสผ่านไปที่อีเมลแล้วครับ!")
                else:
                    st.error("เกิดข้อผิดพลาดในการส่งอีเมล")
            else:
                st.error("ไม่พบอีเมลนี้ในระบบ")
    st.stop()

# --- 6. MAIN CONTENT (CEO & USER DASHBOARD) ---
st.title(f"📊 {st.session_state.role} Dashboard")

# ถ้าเป็น CEO ให้เห็นระบบเรดาร์หาลูกค้า
if st.session_state.role == "CEO" or st.session_state.username == "admin":
    tab1, tab2 = st.tabs(["📡 AI Lead Radar", "👥 ฐานข้อมูลสมาชิก"])
    
    with tab1:
        st.header("🎯 เจาะฐานข้อมูลลูกค้าทั่วโลก")
        col1, col2 = st.columns(2)
        with col1:
            kw = st.text_input("สินค้าที่ค้นหา", "Sugar IC45")
            ct = st.text_input("ประเทศเป้าหมาย", "Dubai")
        with col2:
            st.write("🔍 กดสแกนทันที:")
            q = urllib.parse.quote(f"{kw} importer in {ct}")
            li = urllib.parse.quote(f'site:linkedin.com/in/ "purchasing manager" AND "{kw}" AND "{ct}"')
            st.markdown(f"• [🏢 สแกนบริษัทบน Google Maps](https://www.google.com/maps/search/{q})")
            st.markdown(f"• [👤 สแกนรายชื่อคนบน LinkedIn](https://www.google.com/search?q={li})")
        
        st.divider()
        st.subheader("📥 บันทึกรายชื่อใหม่")
        with st.form("save_lead"):
            c_name = st.text_input("ชื่อบริษัท/ลูกค้า")
            c_mail = st.text_input("อีเมล/เบอร์โทร")
            c_note = st.text_input("ความต้องการ")
            if st.form_submit_button("บันทึกลง Google Sheets"):
                lead = pd.DataFrame([{"username": c_name, "password": "N/A", "email": c_mail, "role": f"Lead: {c_note}"}])
                save_to_sheets(pd.concat([df_users, lead], ignore_index=True))
                st.success("บันทึกเรียบร้อย!")
    
    with tab2:
        st.dataframe(get_user_data(), use_container_width=True)
else:
    st.info(f"ยินดีต้อนรับคุณ {st.session_state.username}! ตอนนี้ระบบกำลังเตรียมรายการสินค้าใหม่สำหรับคุณ")
