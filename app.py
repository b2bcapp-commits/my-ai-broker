import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. CONFIGURATION (ข้อมูลของ CEO) ---
st.set_page_config(page_title="Global Trade Hub", layout="wide", page_icon="🌍")

SENDER_EMAIL = "your-email@gmail.com"  # <--- บอสเปลี่ยนเป็นอีเมล Gmail ของบอสที่นี่
SENDER_PASSWORD = "byyh oiii eibi cuov" # รหัสจากภาพ image_bf387c.png

MY_LINE_LINK = "https://line.me/ti/p/~YOUR_LINE_ID"
MY_WHATSAPP_LINK = "https://wa.me/66964474797?text=I%20am%20interested%20in%20your%20trade%20deals"

# --- 2. EMAIL FUNCTION ---
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
    except Exception as e:
        st.error(f"Email Error: {e}")
        return False

# --- 3. DATABASE (ใช้ Session State จำลองไปก่อน) ---
if 'user_db' not in st.session_state:
    st.session_state['user_db'] = {
        "admin": {"password": "789", "role": "CEO", "email": SENDER_EMAIL}
    }

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 4. AUTH UI ---
with st.sidebar:
    st.title("🌐 Menu")
    if not st.session_state['logged_in']:
        mode = st.radio("Access", ["Login", "Sign Up", "Forgot Password"])
    else:
        st.write(f"Logged in as: **{st.session_state['current_user']}**")
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()
        st.divider()
        st.subheader("📱 Quick Contact")
        st.markdown(f'<a href="{MY_WHATSAPP_LINK}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 10px; border-radius: 5px; width: 100%; cursor: pointer; font-weight: bold; margin-bottom: 5px;">WhatsApp</button></a>', unsafe_allow_html=True)
        st.markdown(f'<a href="{MY_LINE_LINK}" target="_blank"><button style="background-color: #00c300; color: white; border: none; padding: 10px; border-radius: 5px; width: 100%; cursor: pointer; font-weight: bold;">LINE</button></a>', unsafe_allow_html=True)

# --- 5. PAGES ---
if not st.session_state['logged_in']:
    if mode == "Login":
        st.title("🔐 Login")
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

    elif mode == "Sign Up":
        st.title("📝 Register Account")
        new_user = st.text_input("Username")
        new_email = st.text_input("Email")
        new_pw = st.text_input("Set Password", type="password")
        new_role = st.selectbox("I am a", ["Buyer", "Seller"])
        if st.button("Create Account"):
            if new_user and new_email and new_pw:
                st.session_state['user_db'][new_user] = {"password": new_pw, "role": new_role, "email": new_email}
                # ส่งอีเมลยืนยัน
                subject = "Welcome to Global Trade Hub"
                body = f"Hello {new_user},\n\nRegistration successful as {new_role}.\nYou can now access our platform.\n\nRegards,\nCEO Master"
                send_email(new_email, subject, body)
                st.success(f"ลงทะเบียนสำเร็จ! ส่งอีเมลยืนยันไปที่ {new_email} แล้ว")
                st.balloons()
            else:
                st.error("Please fill all fields")

    elif mode == "Forgot Password":
        st.title("🔑 Recovery")
        target_email = st.text_input("Enter your registered email")
        if st.button("Request Reset"):
            # ค้นหาอีเมล
            found = False
            for u, data in st.session_state['user_db'].items():
                if data['email'] == target_email:
                    found = True
                    subject = "Password Reset Request"
                    body = f"Hello {u},\n\nYour password is: {data['password']}\n\nYou can change it after logging in."
                    send_email(target_email, subject, body)
                    break
            if found:
                st.success("📩 ส่งข้อมูลการกู้รหัสไปยังอีเมลของท่านแล้ว")
            else:
                st.error("ไม่พบอีเมลนี้ในระบบ")
    st.stop()

# --- 6. DASHBOARDS (CEO ONLY) ---
user_data = st.session_state['user_db'][st.session_state['current_user']]
if user_data['role'] == "CEO":
    st.title("📊 CEO Command Center")
    st.write("Current Members:", len(st.session_state['user_db']))
    st.table(pd.DataFrame(st.session_state['user_db']).T)
else:
    st.title(f"🌍 {user_data['role']} Dashboard")
    st.info("ระบบกำลังดึงข้อมูลดีลล่าสุด...")
