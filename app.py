import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import urllib.parse
import smtplib
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
    except:
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

# --- 4. SIDEBAR NAVIGATION ---
df_users = get_user_data()

with st.sidebar:
    st.title("🌐 Menu")
    if not st.session_state['logged_in']:
        mode = st.radio("Access", ["Login", "Sign Up", "Forgot Password"])
    else:
        st.success(f"User: {st.session_state.username}")
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
            match = df_users[(df_users['username'].astype(str) == u) & (df_users['password'].astype(str) == p)]
            if not match.empty:
                st.session_state.logged_in = True
                st.session_state.username = u
                st.session_state.role = match.iloc[0]['role']
                st.session_state.user_email = match.iloc[0]['email']
                st.rerun()
            else:
                st.error("ข้อมูลไม่ถูกต้อง")

    elif mode == "Sign Up":
        st.title("📝 สมัครสมาชิก")
        nu = st.text_input("New Username")
        ne = st.text_input("Email Address")
        np = st.text_input("New Password", type="password")
        nr = st.selectbox("I am a", ["Buyer", "Seller"])
        if st.button("Register"):
            if nu and ne and np:
                new_row = pd.DataFrame([{"username": nu, "password": np, "email": ne, "role": nr}])
                save_to_sheets(pd.concat([df_users, new_row], ignore_index=True))
                send_email(ne, "Welcome", f"Hello {nu}, welcome to B2B Global Hub!")
                st.success("ลงทะเบียนสำเร็จ!")
            else:
                st.error("กรุณากรอกข้อมูลให้ครบทุกช่อง")

    elif mode == "Forgot Password":
        st.title("🔑 กู้คืนรหัสผ่าน")
        target_email = st.text_input("ใส่อีเมลของคุณ")
        if st.button("Send My Password"):
            match = df_users[df_users['email'] == target_email]
            if not match.empty:
                send_email(target_email, "Recovery", f"Your password is: {match.iloc[0]['password']}")
                st.success("ส่งข้อมูลไปทางอีเมลแล้วครับ")
            else:
                st.error("ไม่พบอีเมลนี้")
    st.stop()

# --- 6. DASHBOARD (CEO / MARKETPLACE) ---
st.title(f"📊 {st.session_state.role} Command Center")

if st.session_state.role == "CEO":
    t1, t2, t3 = st.tabs(["🎯 Lead Radar", "👥 Members", "📦 Products"])
    
    with t1:
        st.subheader("📡 ระบบค้นหาลูกค้าทั่วโลก")
        kw = st.text_input("ระบุสินค้า", "Sugar")
        ct = st.text_input("ระบุประเทศ", "Dubai")
        query = urllib.parse.quote(f"{kw} importer in {ct}")
        st.markdown(f"👉 [สแกนเป้าหมายบน Google Maps](https://www.google.com/maps/search/{query})")
    
    with t2:
        st.dataframe(df_users, use_container_width=True)
    
    with t3:
        st.subheader("➕ เพิ่มสินค้าใหม่")
        with st.form("add_p"):
            p_n = st.text_input("ชื่อสินค้า")
            p_v = st.text_input("ราคา/เงื่อนไข")
            p_d = st.text_area("รายละเอียด")
            if st.form_submit_button("Post Product"):
                new_p = pd.DataFrame([{"username": p_n, "password": p_v, "email": p_d, "role": "Product_Listing"}])
                save_to_sheets(pd.concat([df_users, new_p], ignore_index=True))
                st.success("เพิ่มสินค้าเรียบร้อย")

else:
    st.header("🛒 Global Marketplace")
    prods = df_users[df_users['role'] == "Product_Listing"]
    if prods.empty:
        st.info("ยังไม่มีสินค้าในระบบ")
    else:
        for i, row in prods.iterrows():
            with st.expander(f"📦 {row['username']} - {row['password']}"):
                st.write(row['email'])
                if st.button("I am Interested", key=i):
                    msg = f"User {st.session_state.username} สนใจสินค้า {row['username']}"
                    send_email(SENDER_EMAIL, "New Inquiry!", msg)
                    st.success("แจ้ง CEO เรียบร้อยแล้ว")
