import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import urllib.parse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Global Trade Hub", layout="wide", page_icon="🌍")

# อัปเดตข้อมูลอีเมลใหม่ของบอส
SENDER_EMAIL = "b2bcapp@gmail.com"
SENDER_PASSWORD = "xfym dbzl gekk jwig"
MY_WHATSAPP_LINK = "https://wa.me/66964474797?text=Hello%20CEO"

# เชื่อมต่อ Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 2. CORE FUNCTIONS ---
def get_user_data():
    try: return conn.read(ttl=0)
    except: return pd.DataFrame(columns=["username", "password", "email", "role"])

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
    except: return False

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
        st.success(f"ผู้ใช้งาน: {st.session_state.username}")
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
            match = df_users[(df_users['username'] == u) & (df_users['password'] == p)]
            if not match.empty:
                st.session_state.logged_in = True
                st.session_state.username = u
                st.session_state.role = match.iloc[0]['role']
                st.session_state.user_email = match.iloc[0]['email']
                st.rerun()
            else: st.error("ข้อมูลไม่ถูกต้อง")
    elif mode == "Sign Up":
        st.title("📝 สมัครสมาชิก")
        nu, ne, np = st.text_input("Username"), st.text_input("Email"), st.text_input("Password", type="password")
        nr = st.selectbox("Role", ["Buyer", "Seller"])
        if st.button("สร้างบัญชี"):
            new_data = pd.concat([df_users, pd.DataFrame([{"username": nu, "password": np, "email": ne, "role": nr}])], ignore_index=True)
            save_to_sheets(new_data)
            send_email(ne, "
