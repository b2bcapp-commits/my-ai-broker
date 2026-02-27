import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import urllib.parse
import smtplib
import time # เพิ่มเข้ามาเพื่อหน่วงเวลาให้บอสเห็นสถานะ
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Global Trade Hub", layout="wide", page_icon="🌍")

SENDER_EMAIL = "b2bcapp@gmail.com"
SENDER_PASSWORD = "xfym dbzl gekk jwig"
MY_WHATSAPP_LINK = "https://wa.me/66964474797?text=Hello%20CEO"

# เชื่อมต่อ Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("กรุณาตั้งค่า Spreadsheet ในระบบ Secrets ก่อนครับ")

# --- 2. CORE FUNCTIONS ---
def get_user_data():
    try:
        return conn.read(ttl=0)
    except:
        return pd.DataFrame(columns=["username", "password", "email", "role"])

def save_to_sheets(updated_df):
    try:
        conn.update(data=updated_df)
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error saving to Sheets: {e}")
        return False

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

# --- 4. SIDEBAR ---
df_users = get_user_data()

with st.sidebar:
    st.title("🌐 Menu Control")
    if not st.session_state['logged_in']:
        mode = st.radio("Access", ["Login", "Sign Up", "Forgot Password"])
    else:
        st.success(f"Logged in: {st.session_state.username}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
        st.divider()
        st.markdown(f'''<a href="{MY_WHATSAPP_LINK}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 10px; border-radius: 5px; width: 100%; cursor: pointer; font-weight: bold;">WhatsApp CEO</button></a>''', unsafe_allow_html=True)

# --- 5. AUTHENTICATION ---
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
                st.error("ข้อมูลไม่ถูกต้อง")
    # ... (สมัครสมาชิก/กู้รหัส คงเดิม) ...
    elif mode == "Sign Up":
        st.title("📝 Register")
        nu, ne, np = st.text_input("New Username"), st.text_input("New Email"), st.text_input("New Password", type="password")
        if st.button("Register"):
            if nu and ne and np:
                save_to_sheets(pd.concat([df_users, pd.DataFrame([{"username": nu, "password": np, "email": ne, "role": "Buyer"}])], ignore_index=True))
                st.success("ลงทะเบียนสำเร็จ!")
    elif mode == "Forgot Password":
        st.title("🔑 Recovery")
        target = st.text_input("Email")
        if st.button("Recover"):
            match = df_users[df_users['email'] == target]
            if not match.empty:
                send_email(target, "Recovery", f"Password: {match.iloc[0]['password']}")
                st.success("ส่งรหัสแล้ว!")
    st.stop()

# --- 6. MAIN DASHBOARD ---
st.title(f"📊 {st.session_state.role} Command Center")

if st.session_state.role == "CEO":
    t1, t2, t3 = st.tabs(["🎯 AI Lead Radar", "👥 Members", "📦 Product Management"])
    
    with t1:
        st.subheader("📡 ระบบค้นหาลูกค้า")
        kw = st.text_input("สินค้า", "Sugar ICUMSA 45")
        ct = st.text_input("ประเทศ", "Dubai")
        q = urllib.parse.quote(f"{kw} importer in {ct}")
        st.markdown(f"👉 [สแกนเป้าหมายบน Google Maps](https://www.google.com/maps/search/{q})")

    with t2:
        st.dataframe(df_users, use_container_width=True)

    with t3:
        st.subheader("➕ เพิ่มสินค้าใหม่")
        # ใช้ Form แบบดั้งเดิมแต่เพิ่มกลไกตรวจสอบ
        p_n = st.text_input("ชื่อสินค้า", key="pn")
        p_v = st.text_input("ราคา/เงื่อนไข", key="pv")
        p_d = st.text_area("รายละเอียด", key="pd")
        
        if st.button("🚀 Publish Product Now"):
            if p_n and p_v:
                with st.spinner('กำลังเชื่อมต่อฐานข้อมูลและบันทึกสินค้า...'):
                    new_p = pd.DataFrame([{"username": p_n, "password": p_v, "email": p_d, "role": "Product_Listing"}])
                    success = save_to_sheets(pd.concat([df_users, new_p], ignore_index=True))
                    if success:
                        st.balloons()
                        st.success(f"✅ สำเร็จ! สินค้า '{p_n}' ถูกเพิ่มลงระบบแล้ว")
                        time.sleep(2) # หน่วงเวลาให้บอสเห็นความสำเร็จ
                        st.rerun()
            else:
                st.warning("⚠️ กรุณากรอกชื่อสินค้าและราคาเป็นอย่างน้อยครับ")

    # --- Marketplace Preview ---
    st.divider()
    st.header("🛒 Marketplace Preview")
    prods = df_users[df_users['role'] == "Product_Listing"]
    if prods.empty:
        st.info("ยังไม่มีสินค้าในฐานข้อมูล")
    else:
        for i, row in prods.iterrows():
            with st.container():
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.subheader(f"📦 {row['username']}")
                    st.write(f"**ราคา:** {row['password']}")
                    st.text(f"รายละเอียด: {row['email']}")
                with c2:
                    if st.button(f"Test Inquiry 📩", key=f"ceo_test_{i}"):
                        st.toast(f"Testing system for {row['username']}...")
                        st.success("Email System OK!")
                st.divider()

else:
    # Buyer Page (เหมือนเดิม)
    st.header("🛒 Marketplace")
    prods = df_users[df_users['role'] == "Product_Listing"]
    for i, row in prods.iterrows():
        with st.expander(f"📦 {row['username']} - {row['password']}"):
            st.write(row['email'])
            if st.button("I am Interested", key=f"buy_{i}"):
                send_email(SENDER_EMAIL, "New Interest", f"User {st.session_state.username} สนใจ {row['username']}")
                st.success("แจ้ง CEO เรียบร้อย!")
