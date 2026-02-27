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

# เชื่อมต่อฐานข้อมูล (Sheet1 สำหรับ User, Sheet2 สำหรับ Products)
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 2. FUNCTIONS ---
def get_user_data():
    try: return conn.read(ttl=0)
    except: return pd.DataFrame(columns=["username", "password", "email", "role"])

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

# --- 5. AUTH PAGES (Login/Sign Up/Forgot) ---
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
            conn.update(data=new_data); st.cache_data.clear()
            send_email(ne, "Welcome", f"Hi {nu}, welcome aboard!")
            st.success("สำเร็จ!")
    elif mode == "Forgot Password":
        st.title("🔑 กู้คืนรหัสผ่าน")
        target = st.text_input("อีเมล")
        if st.button("ส่งรหัสผ่าน"):
            match = df_users[df_users['email'] == target]
            if not match.empty:
                send_email(target, "Password recovery", f"Your password is: {match.iloc[0]['password']}")
                st.success("ส่งแล้ว!")
    st.stop()

# --- 6. MAIN CONTENT (Marketplace & CEO Admin) ---
st.title(f"📊 {st.session_state.role} Control Center")

if st.session_state.role == "CEO" or st.session_state.username == "admin":
    tab1, tab2, tab3 = st.tabs(["📡 AI Lead Radar", "👥 Members", "📦 Product Management"])
    
    with tab1:
        st.header("🎯 ค้นหาลูกค้าใหม่")
        kw, ct = st.text_input("สินค้า"), st.text_input("ประเทศ")
        q = urllib.parse.quote(f"{kw} importer in {ct}")
        st.markdown(f"[🏢 สแกนบริษัทบน Google Maps](https://www.google.com/maps/search/{q})")
    
    with tab2: st.dataframe(df_users)
    
    with tab3:
        st.header("➕ เพิ่มสินค้าใหม่ลงหน้าร้าน")
        with st.form("add_product"):
            p_name = st.text_input("ชื่อสินค้า (e.g. Sugar IC45)")
            p_price = st.text_input("ราคา/เงื่อนไข (e.g. $450/MT CIF)")
            p_desc = st.text_area("รายละเอียดสินค้า")
            if st.form_submit_button("ประกาศขายสินค้า"):
                # ในที่นี้เราจะบันทึกลง Sheet เดิมโดยระบุ Role เป็น "Product" เพื่อเก็บข้อมูล
                prod_row = pd.DataFrame([{"username": p_name, "password": p_price, "email": p_desc, "role": "Product_Listing"}])
                conn.update(data=pd.concat([df_users, prod_row], ignore_index=True))
                st.success("สินค้าถูกเพิ่มลง Marketplace แล้ว!")

else: # ส่วนของ Buyer / Seller
    st.header("🛒 Global Marketplace")
    st.write("เลือกสินค้าที่คุณต้องการ และกดปุ่มสนใจเพื่อให้เจ้าหน้าที่ติดต่อกลับ")
    
    products = df_users[df_users['role'] == "Product_Listing"]
    if products.empty:
        st.info("ขออภัย ขณะนี้ยังไม่มีรายการสินค้า")
    else:
        for index, row in products.iterrows():
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(f"📦 {row['username']}")
                    st.write(f"**ราคา/เงื่อนไข:** {row['password']}")
                    st.write(f"**รายละเอียด:** {row['email']}")
                with col2:
                    if st.button(f"สนใจสินค้า", key=index):
                        # ส่งอีเมลหา CEO
                        alert_msg = f"User: {st.session_state.username} ({st.session_state.user_email}) สนใจสินค้า: {row['username']}"
                        send_email("dropshipmillionaire19@gmail.com", "New Inquiry!", alert_msg)
                        st.success("เราได้รับความสนใจของคุณแล้ว CEO จะติดต่อกลับโดยเร็วที่สุด")
                st.divider()
