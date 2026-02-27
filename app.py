import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import urllib.parse

# --- 1. CONFIG & CONNECTION ---
st.set_page_config(page_title="Global Trade Hub - CEO", layout="wide", page_icon="🌍")
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 2. DATA FUNCTIONS ---
def get_user_data():
    return conn.read(ttl=0)

def save_new_lead(new_row):
    df = get_user_data()
    updated_df = pd.concat([df, new_row], ignore_index=True)
    conn.update(data=updated_df)
    st.cache_data.clear()

# --- 3. SIDEBAR (เมนูเดิมของบอส) ---
with st.sidebar:
    st.title("🌐 CEO Hub")
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.warning("Please login as CEO first.")
        st.stop()
    
    st.write(f"Logged in: **{st.session_state.username}**")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    st.divider()
    st.subheader("📱 Direct Contact")
    whatsapp_url = "https://wa.me/66964474797?text=Hello%20CEO"
    st.markdown(f'''<a href="{whatsapp_url}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 10px; border-radius: 5px; width: 100%; cursor: pointer; font-weight: bold;">WhatsApp CEO</button></a>''', unsafe_allow_html=True)

# --- 4. MAIN CEO DASHBOARD ---
st.title("📊 CEO Command & Control Center")

tab1, tab2, tab3 = st.tabs(["📡 AI Lead Radar", "👥 User Database", "➕ Add New Deals"])

# --- TAB 1: AI LEAD RADAR (เจาะฐานข้อมูลสาธารณะ) ---
with tab1:
    st.header("🎯 ระบบสแกนหาลูกค้าอัจฉริยะ (Free Tools)")
    col1, col2 = st.columns(2)
    
    with col1:
        keyword = st.text_input("ชื่อสินค้า (เช่น Sugar IC45, Rice, Frozen Chicken)", "Sugar")
        country = st.text_input("ประเทศเป้าหมาย (เช่น Dubai, USA, Malaysia)", "Dubai")
    
    with col2:
        st.write("🔍 กดเลือกช่องทางที่ต้องการสแกน:")
        # สร้าง URL สำหรับ Search เชิงลึก
        query = f"{keyword} importer in {country}"
        li_query = f'site:linkedin.com/in/ "purchasing manager" AND "{keyword}" AND "{country}"'
        gmaps_url = f"https://www.google.com/maps/search/{urllib.parse.quote(query)}"
        linkedin_url = f"https://www.google.com/search?q={urllib.parse.quote(li_query)}"
        
        st.markdown(f"[✈️ สแกนบริษัทบน Google Maps]({gmaps_url})")
        st.markdown(f"[👔 สแกนตัวบุคคลบน LinkedIn]({linkedin_url})")
        st.info("ระบบจะนำบอสไปยังฐานข้อมูลที่ถูกกรองไว้แล้วเฉพาะ 'ผู้ซื้อตัวจริง' เท่านั้น")

    st.divider()
    st.subheader("📥 บันทึกรายชื่อที่พบ")
    with st.expander("คลิกเพื่อกรอกข้อมูลลูกค้าใหม่ลง Google Sheets"):
        with st.form("new_lead_form"):
            c1, c2, c3 = st.columns(3)
            l_name = c1.text_input("ชื่อลูกค้า/บริษัท")
            l_email = c2.text_input("อีเมล/เบอร์โทร")
            l_note = c3.text_input("หมายเหตุ (เช่น สนใจน้ำตาล)")
            submit_lead = st.form_submit_button("บันทึกลงฐานข้อมูลถาวร")
            if submit_lead:
                # บันทึกลง Sheet (ใช้โครงสร้าง username, password, email, role ตามเดิม)
                new_lead = pd.DataFrame([{"username": l_name, "password": "N/A", "email": l_email, "role": f"Lead: {l_note}"}])
                save_new_lead(new_lead)
                st.success(f"บันทึกข้อมูล {l_name} เรียบร้อยแล้ว!")

# --- TAB 2: USER DATABASE ---
with tab2:
    st.header("👥 รายชื่อสมาชิกทั้งหมดในระบบ")
    df_users = get_user_data()
    st.dataframe(df_users, use_container_width=True)

# --- TAB 3: ADD NEW DEALS ---
with tab3:
    st.header("📦 ลงรายการสินค้าใหม่ (Coming Soon)")
    st.info("ฟีเจอร์นี้จะช่วยให้บอสลงประกาศขายสินค้าเพื่อให้ Buyer เห็นในหน้าแรกครับ")import streamlit as st
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
