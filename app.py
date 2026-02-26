import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. CONFIGURATION (ข้อมูลของ CEO) ---
st.set_page_config(page_title="Global Trade Hub", layout="wide", page_icon="🌍")

# ข้อมูลสำหรับส่งอีเมล (จากรูป image_bf317a และ image_bf387c)
SENDER_EMAIL = "b2bcapp@gmail.com"  
SENDER_PASSWORD = "byyh oiii eibi cuov" 

MY_LINE_LINK = "https://line.me/ti/p/~YOUR_LINE_ID"
MY_WHATSAPP_LINK = "https://wa.me/66964474797?text=สวัสดีครับ%20ผมสนใจดีลการค้าครับ"

# --- 2. EMAIL FUNCTION ---
def send_email(receiver_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # เชื่อมต่อ Gmail Server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()
        return True, "Success"
    except Exception as e:
        return False, str(e)

# --- 3. DATABASE (จำลองระบบสมาชิก) ---
if 'user_db' not in st.session_state:
    st.session_state['user_db'] = {
        "admin": {"password": "789", "role": "CEO", "email": SENDER_EMAIL}
    }

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🌐 Global Trade Hub")
    if not st.session_state['logged_in']:
        mode = st.radio("Access Menu", ["Login", "Sign Up", "Forgot Password"])
    else:
        st.write(f"Logged in as: **{st.session_state['current_user']}**")
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()
        st.divider()
        st.subheader("📱 ติดต่อฝ่ายสนับสนุน (CEO)")
        # ปุ่ม WhatsApp สากล
        st.markdown(f'''
        <a href="{MY_WHATSAPP_LINK}" target="_blank">
            <button style="background-color: #25D366; color: white; border: none; padding: 10px; border-radius: 5px; width: 100%; cursor: pointer; font-weight: bold; margin-bottom: 5px;">
                WhatsApp (+66 964474797)
            </button>
        </a>
        ''', unsafe_allow_html=True)
        # ปุ่ม LINE
        st.markdown(f'''
        <a href="{MY_LINE_LINK}" target="_blank">
            <button style="background-color: #00c300; color: white; border: none; padding: 10px; border-radius: 5px; width: 100%; cursor: pointer; font-weight: bold;">
                Chat via LINE
            </button>
        </a>
        ''', unsafe_allow_html=True)

# --- 5. AUTH PAGES ---
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
                st.error("❌ ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

    elif mode == "Sign Up":
        st.title("📝 Register New Account")
        new_user = st.text_input("Username (ชื่อผู้ใช้)")
        new_email = st.text_input("Email (อีเมลสำหรับรับแจ้งเตือน)")
        new_pw = st.text_input("Set Password (ตั้งรหัสผ่าน)", type="password")
        new_role = st.selectbox("I am a (บทบาท)", ["Buyer", "Seller"])
        
        if st.button("Create Account"):
            if new_user and new_email and new_pw:
                # บันทึกข้อมูล
                st.session_state['user_db'][new_user] = {"password": new_pw, "role": new_role, "email": new_email}
                
                # ส่งอีเมลยืนยัน
                subject = "Registration Successful - Global Trade Hub"
                body = f"เรียนคุณ {new_user},\n\nการลงทะเบียนในบทบาท {new_role} สำเร็จเรียบร้อยแล้ว\nคุณสามารถเข้าใช้งานระบบได้ทันที\n\nขอบคุณที่ใช้บริการ\nCEO Master"
                
                success, error_msg = send_email(new_email, subject, body)
                if success:
                    st.success(f"✅ ลงทะเบียนสำเร็จ! ส่งอีเมลยืนยันไปที่ {new_email} แล้ว")
                    st.balloons()
                else:
                    st.warning(f"ลงทะเบียนสำเร็จ แต่ระบบอีเมลขัดข้อง: {error_msg}")
            else:
                st.error("กรุณากรอกข้อมูลให้ครบทุกช่อง")

    elif mode == "Forgot Password":
        st.title("🔑 กู้คืนรหัสผ่าน")
        f_email = st.text_input("กรอกอีเมลที่ลงทะเบียนไว้")
        if st.button("ส่งรหัสผ่านเข้าอีเมล"):
            found = False
            for u, data in st.session_state['user_db'].items():
                if data['email'] == f_email:
                    found = True
                    subject = "Your Password Recovery"
                    body = f"สวัสดีคุณ {u},\n\nรหัสผ่านของคุณคือ: {data['password']}\nกรุณาเข้าสู่ระบบและเปลี่ยนรหัสผ่านเพื่อความปลอดภัย"
                    send_email(f_email, subject, body)
                    break
            if found:
                st.success("📩 ระบบส่งข้อมูลรหัสผ่านไปยังอีเมลของคุณแล้ว")
            else:
                st.error("ไม่พบอีเมลนี้ในระบบสมัครสมาชิก")
    st.stop()

# --- 6. MAIN CONTENT ---
current_role = st.session_state['user_db'][st.session_state['current_user']]['role']

if current_role == "CEO":
    st.title("📊 CEO Command Center")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users", len(st.session_state['user_db']))
    col2.metric("System Status", "Live")
    col3.metric("Contact Info", "WhatsApp Ready")
    
    st.subheader("👥 รายชื่อสมาชิกทั้งหมด (Database)")
    st.table(pd.DataFrame(st.session_state['user_db']).T)
else:
    st.title(f"🌍 {current_role} Dashboard")
    st.write(f"สวัสดีคุณ **{st.session_state['current_user']}** ยินดีต้อนรับสู่ระบบจับคู่การค้าระดับโลก")
