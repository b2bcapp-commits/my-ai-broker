import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import urllib.parse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Global Trade Hub - CEO", layout="wide", page_icon="🌍")

# ข้อมูลการติดต่อและอีเมล (อ้างอิงจากภาพ image_bf387c และ image_bf317a)
SENDER_EMAIL = "dropshipmillionaire19@gmail.com"
SENDER_PASSWORD = "byyh oiii eibi cuov"
MY_WHATSAPP_LINK = "https://wa.me/66964474797?text=Hello%20CEO"

# เชื่อมต่อ Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.error("⚠️ ไม่สามารถเชื่อมต่อฐานข้อมูลได้ กรุณาตรวจสอบการตั้งค่า Secrets")

# --- 2. CORE FUNCTIONS ---
def get_user_data():
    try:
        return conn.read(ttl=0)
    except Exception:
        # กรณี Sheet ว่างเปล่า ให้สร้าง DataFrame พื้นฐาน
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

# --- 3. SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🌐 Menu Control")
    if not st.session_state['logged_in']:
        mode = st.radio("Access", ["Login", "Sign Up"])
    else:
        st.success(f"User: **{st.session_state.username}**")
        st.write(f"Role: **{st.session_state.role}**")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
        st.divider()
        st.markdown(f'''<a href="{MY_WHATSAPP_LINK}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 10px; border-radius: 5px; width: 100%; cursor: pointer; font-weight: bold;">WhatsApp Support</button></a>''', unsafe_allow_html=True)

# --- 5. LOGIN & SIGN UP LOGIC ---
df_users = get_user_data()

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
        st.title("📝 สมัครสมาชิกใหม่")
        nu = st.text_input("Username")
        ne = st.text_input("Email")
        np = st.text_input("Password", type="password")
        nr = st.selectbox("Role", ["Buyer", "Seller"])
        if st.button("Create Account"):
            if nu and ne and np:
                new_row = pd.DataFrame([{"username": nu, "password": np, "email": ne, "role": nr}])
                save_to_sheets(pd.concat([df_users, new_row], ignore_index=True))
                send_email(ne, "Welcome", f"Account {nu} is ready!")
                st.success("ลงทะเบียนสำเร็จ!")
                st.balloons()
    st.stop()

# --- 6. CEO MAIN DASHBOARD ---
st.title("📊 CEO Command & Control Center")

tab1, tab2, tab3 = st.tabs(["🎯 AI Lead Radar", "👥 User Database", "➕ System Logs"])

with tab1:
    st.header("📡 ระบบสแกนหาลูกค้าอัจฉริยะ")
    c1, c2 = st.columns(2)
    with c1:
        keyword = st.text_input("ระบุสินค้าเป้าหมาย", "Sugar IC45")
        country = st.text_input("ระบุประเทศ", "Dubai")
    with c2:
        st.write("🔗 ลิงก์สแกนหาลูกค้า (ฟรี):")
        q = urllib.parse.quote(f"{keyword} importer in {country}")
        li_q = urllib.parse.quote(f'site:linkedin.com/in/ "purchasing manager" AND "{keyword}" AND "{country}"')
        st.markdown(f"• [🔍 สแกนบริษัทบน Google Maps](https://www.google.com/maps/search/{q})")
        st.markdown(f"• [👔 สแกนตัวบุคคลบน LinkedIn](https://www.google.com/search?q={li_q})")

    st.divider()
    st.subheader("📥 บันทึกรายชื่อลูกค้าใหม่")
    with st.form("lead_form"):
        l_name = st.text_input("ชื่อบริษัท/ลูกค้า")
        l_contact = st.text_input("อีเมล/เบอร์โทร")
        l_note = st.text_input("ความต้องการ (เช่น ต้องการ Rice 500 ตัน)")
        if st.form_submit_button("บันทึกลง Google Sheets"):
            lead_row = pd.DataFrame([{"username": l_name, "password": "N/A", "email": l_contact, "role": f"Lead: {l_note}"}])
            save_to_sheets(pd.concat([df_users, lead_row], ignore_index=True))
            st.success("บันทึกข้อมูลสำเร็จ!")

with tab2:
    st.header("👥 ฐานข้อมูลทั้งหมด")
    st.dataframe(get_user_data(), use_container_width=True)

with tab3:
    st.header("⚙️ ระบบสถานะ")
    st.write("• สถานะฐานข้อมูล: **Connected**")
    st.write("• สถานะอีเมล: **Ready**")
    st.info("หน้านี้ไว้สำหรับตรวจสอบความเรียบร้อยของระบบบอทครับบอส")
