import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. CONFIG ---
st.set_page_config(page_title="Global Trade Hub", layout="wide", page_icon="🌍")

# ข้อมูลการติดต่อ CEO
SENDER_EMAIL = "dropshipmillionaire19@gmail.com"
SENDER_PASSWORD = "byyh oiii eibi cuov"
MY_WHATSAPP_LINK = "https://wa.me/66964474797?text=Hello%20CEO"

# เชื่อมต่อ Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 2. FUNCTIONS ---
def get_user_data():
    # ดึงข้อมูลจาก Google Sheets
    return conn.read(ttl=0)

def send_email(receiver, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver, msg.as_string())
        server.quit()
        return True
    except:
        return False

# --- 3. UI LOGIC ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

with st.sidebar:
    st.title("🌐 Global Hub")
    if not st.session_state['logged_in']:
        mode = st.radio("Menu", ["Login", "Sign Up", "Forgot Password"])
    else:
        st.write(f"Logged in: **{st.session_state['username']}**")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
        st.divider()
        st.markdown(f'''<a href="{MY_WHATSAPP_LINK}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 10px; border-radius: 5px; width: 100%; cursor: pointer; font-weight: bold;">WhatsApp CEO</button></a>''', unsafe_allow_html=True)

# --- 4. DATA PROCESSING ---
try:
    df_users = get_user_data()
except Exception as e:
    st.error("⚠️ กรุณาตรวจสอบการตั้งค่า Secrets (ลิงก์ Google Sheets ไม่ถูกต้อง)")
    st.stop()

# --- 5. PAGES ---
if not st.session_state['logged_in']:
    if mode == "Login":
        st.title("🔐 Login")
        u_input = st.text_input("Username")
        p_input = st.text_input("Password", type="password")
        if st.button("Sign In"):
            match = df_users[(df_users['username'] == u_input) & (df_users['password'] == p_input)]
            if not match.empty:
                st.session_state.logged_in = True
                st.session_state.username = u_input
                st.session_state.role = match.iloc[0]['role']
                st.rerun()
            else:
                st.error("Invalid Username or Password")

    elif mode == "Sign Up":
        st.title("📝 Register New Member")
        nu = st.text_input("Choose Username")
        ne = st.text_input("Email Address")
        np = st.text_input("Set Password", type="password")
        nr = st.selectbox("Role", ["Buyer", "Seller"])
        
        if st.button("Create Account"):
            if nu and ne and np:
                if nu in df_users['username'].astype(str).values:
                    st.error("This username is already taken!")
                else:
                    # สร้าง Row ใหม่
                    new_data = pd.DataFrame([{"username": nu, "password": np, "email": ne, "role": nr}])
                    updated_df = pd.concat([df_users, new_data], ignore_index=True)
                    # บันทึกลง Google Sheets
                    conn.update(data=updated_df)
                    # ส่งอีเมล
                    send_email(ne, "Welcome to Trade Hub", f"Hi {nu}, your {nr} account is ready!")
                    st.success("✅ Success! Your data is saved to Google Sheets.")
                    st.balloons()
            else:
                st.error("Please fill all fields")

    elif mode == "Forgot Password":
        st.title("🔑 Recovery")
        target_email = st.text_input("Enter your registered email")
        if st.button("Recover"):
            user_info = df_users[df_users['email'] == target_email]
            if not user_info.empty:
                pwd = user_info.iloc[0]['password']
                send_email(target_email, "Password Recovery", f"Your password is: {pwd}")
                st.success("📩 รหัสผ่านถูกส่งไปยังอีเมลของคุณแล้ว")
            else:
                st.error("ไม่พบอีเมลนี้ในระบบ")
    st.stop()

# --- 6. DASHBOARDS ---
st.title(f"📊 {st.session_state.role} Command Center")
if st.session_state.role == "CEO":
    st.write("Database Members (Live from Google Sheets):")
    st.dataframe(df_users)
else:
    st.info(f"Welcome, {st.session_state.username}! สแตนบายรอดีลใหม่จาก CEO ได้เลยครับ")
