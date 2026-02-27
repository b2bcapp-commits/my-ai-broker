import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. SETTINGS (ข้อมูลของ CEO) ---
st.set_page_config(page_title="Global Trade Hub", layout="wide", page_icon="🌍")

# ข้อมูลอีเมลจากภาพ image_bf317a และ image_bf387c
SENDER_EMAIL = "dropshipmillionaire19@gmail.com"  
SENDER_PASSWORD = "byyh oiii eibi cuov" # App Password 16 หลัก

MY_LINE_LINK = "https://line.me/ti/p/~YOUR_LINE_ID"
MY_WHATSAPP_LINK = "https://wa.me/66964474797?text=Hello%20CEO,%20I%20am%20interested%20in%20trading."

# --- 2. EMAIL CORE ---
def send_email(receiver_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(0) # ปิด log เพื่อความสะอาด
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()
        return True, "Email Sent Successfully"
    except Exception as e:
        return False, f"Email Error: {str(e)}"

# --- 3. PERSISTENT DATABASE ---
# หมายเหตุ: ในขั้นตอนนี้เราใช้ Session State ก่อน หากต้องการถาวรจริง 
# บอสต้องต่อ Google Sheets ผ่าน st.connection('gsheets') ครับ
if 'user_db' not in st.session_state:
    st.session_state['user_db'] = {
        "admin": {"password": "789", "role": "CEO", "email": SENDER_EMAIL},
        "ptwpro": {"password": "password", "role": "Buyer", "email": "dropshipmillionaire19@gmail.com"}
    }

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 4. NAVIGATION ---
with st.sidebar:
    st.title("🌐 Global Hub")
    if not st.session_state['logged_in']:
        mode = st.radio("Menu", ["Login", "Sign Up", "Forgot Password"])
    else:
        st.write(f"Logged in: **{st.session_state['current_user']}**")
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()
        st.divider()
        st.subheader("📱 Direct Support")
        # ปุ่ม WhatsApp สากล
        st.markdown(f'''
        <a href="{MY_WHATSAPP_LINK}" target="_blank">
            <button style="background-color: #25D366; color: white; border: none; padding: 12px; border-radius: 8px; width: 100%; cursor: pointer; font-weight: bold; margin-bottom: 8px;">
                WhatsApp (+66 964474797)
            </button>
        </a>
        ''', unsafe_allow_html=True)
        st.markdown(f'''
        <a href="{MY_LINE_LINK}" target="_blank">
            <button style="background-color: #00c300; color: white; border: none; padding: 12px; border-radius: 8px; width: 100%; cursor: pointer; font-weight: bold;">
                Contact via LINE
            </button>
        </a>
        ''', unsafe_allow_html=True)

# --- 5. CORE PAGES ---
if not st.session_state['logged_in']:
    if mode == "Login":
        st.title("🔐 เข้าสู่ระบบ")
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Sign In"):
            db = st.session_state['user_db']
            if user in db and db[user]["password"] == pw:
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = user
                st.rerun()
            else:
                st.error("❌ ข้อมูลไม่ถูกต้อง")

    elif mode == "Sign Up":
        st.title("📝 สมัครสมาชิกใหม่")
        new_u = st.text_input("Username")
        new_e = st.text_input("Email")
        new_p = st.text_input("Password", type="password")
        new_r = st.selectbox("Role", ["Buyer", "Seller"])
        
        if st.button("Create Account"):
            if new_u and new_e and new_p:
                st.session_state['user_db'][new_u] = {"password": new_p, "role": new_r, "email": new_e}
                
                # ส่งอีเมล
                sub = "Registration Confirmed - Global Trade Hub"
                content = f"Welcome {new_u}!\n\nYou are registered as {new_r}.\nAccess the platform anytime."
                status, msg = send_email(new_e, sub, content)
                
                if status:
                    st.success(f"✅ สำเร็จ! ส่งอีเมลยืนยันไปที่ {new_e} แล้ว")
                    st.balloons()
                else:
                    st.warning(f"ลงทะเบียนสำเร็จ แต่ระบบแจ้งเตือนอีเมลติดขัด: {msg}")
            else:
                st.error("กรุณากรอกข้อมูลให้ครบ")

    elif mode == "Forgot Password":
        st.title("🔑 กู้คืนรหัสผ่าน")
        f_email = st.text_input("ระบุอีเมลที่ลงทะเบียน")
        if st.button("Request Recovery"):
            found = False
            for u, data in st.session_state['user_db'].items():
                if data['email'] == f_email:
                    found = True
                    sub = "Your Password Recovery"
                    content = f"สวัสดี {u},\n\nรหัสผ่านของคุณคือ: {data['password']}"
                    send_email(f_email, sub, content)
                    break
            if found:
                st.success("📩 ข้อมูลรหัสผ่านถูกส่งไปยังอีเมลของคุณแล้ว")
            else:
                st.error("ไม่พบอีเมลนี้ในฐานข้อมูล")
    st.stop()

# --- 6. USER DASHBOARDS ---
role = st.session_state['user_db'][st.session_state['current_user']]['role']

if role == "CEO":
    st.title("📊 CEO Command Center")
    col1, col2 = st.columns(2)
    col1.metric("สมาชิกทั้งหมด", len(st.session_state['user_db']))
    col2.metric("สถานะ WhatsApp", "เชื่อมต่อแล้ว")
    st.subheader("📋 ฐานข้อมูลสมาชิก (User DB)")
    st.table(pd.DataFrame(st.session_state['user_db']).T)
else:
    st.title(f"🌍 {role} Dashboard")
    st.write(f"ยินดีต้อนรับคุณ **{st.session_state['current_user']}** เข้าสู่แพลตฟอร์มการค้าระดับโลก")
    st.info("คุณสามารถเลือกดูดีลสินค้าที่ได้รับการรับรองได้จากเมนูด้านซ้าย (เร็วๆ นี้)")
