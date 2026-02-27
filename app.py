import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Global Trade Hub", layout="wide", page_icon="🌍")

# ข้อมูลการติดต่อ
SENDER_EMAIL = "dropshipmillionaire19@gmail.com"
SENDER_PASSWORD = "byyh oiii eibi cuov"
MY_WHATSAPP_LINK = "https://wa.me/66964474797?text=Hello%20CEO"

# เชื่อมต่อ Google Sheets ผ่าน Secrets ที่บอสตั้งค่าไว้
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 2. FUNCTIONS ---
def get_user_data():
    # อ่านข้อมูลล่าสุดจาก Google Sheets
    return conn.read(ttl=0)

def send_email(receiver_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()
        return True
    except:
        return False

# --- 3. AUTHENTICATION UI ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

with st.sidebar:
    st.title("🌐 Menu")
    if not st.session_state['logged_in']:
        mode = st.radio("Access", ["Login", "Sign Up", "Forgot Password"])
    else:
        st.write(f"User: **{st.session_state['username']}**")
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()
        st.divider()
        st.markdown(f'''<a href="{MY_WHATSAPP_LINK}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 10px; border-radius: 5px; width: 100%; cursor: pointer; font-weight: bold;">WhatsApp CEO</button></a>''', unsafe_allow_html=True)

# --- 4. MAIN PAGES ---
df_users = get_user_data()

if not st.session_state['logged_in']:
    if mode == "Login":
        st.title("🔐 Login")
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Sign In"):
            user_match = df_users[(df_users['username'] == u) & (df_users['password'] == p)]
            if not user_match.empty:
                st.session_state['logged_in'] = True
                st.session_state['username'] = u
                st.session_state['role'] = user_match.iloc[0]['role']
                st.rerun()
            else:
                st.error("Invalid Username or Password")

    elif mode == "Sign Up":
        st.title("📝 Register New Member")
        new_user = st.text_input("Username") # ตัวแปร new_user ถูกสร้างที่นี่แล้วครับ
        new_email = st.text_input("Email")
        new_pw = st.text_input("Password", type="password")
        new_role = st.selectbox("I am a", ["Buyer", "Seller"])
        
        if st.button("Create Account"):
            if new_user and new_email and new_pw:
                if new_user in df_users['username'].values:
                    st.error("Username already taken!")
                else:
                    # บันทึกลง Google Sheets
                    new_row = pd.DataFrame([{"username": new_user, "password": new_pw, "email": new_email, "role": new_role}])
                    updated_df = pd.concat([df_users, new_row], ignore_index=True)
                    conn.update(data=updated_df)
                    
                    # ส่งอีเมลยืนยัน
                    send_email(new_email, "Welcome to Trade Hub", f"Hello {new_user}, your {new_role} account is ready.")
                    
                    st.success("Registration Successful! Your data is saved.")
                    st.balloons()
            else:
                st.error("Please fill all fields")

    elif mode == "Forgot Password":
        st.title("🔑 Password Recovery")
        target = st.text_input("Registered Email")
        if st.button("Send My Password"):
            user_info = df_users[df_users['email'] == target]
            if not user_info.empty:
                pwd = user_info.iloc[0]['password']
                send_email(target, "Password Recovery", f"Your password is: {pwd}")
                st.success("Email sent!")
            else:
                st.error("Email not found")
    st.stop()

# --- 5. DASHBOARDS ---
st.title(f"📊 {st.session_state['role']} Command Center")
if st.session_state['role'] == "CEO":
    st.write("Full User Database (Real-time from Google Sheets):")
    st.dataframe(df_users)
else:
    st.info(f"Welcome, {st.session_state['username']}! Explore global verified deals below.")
