import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import urllib.parse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Global Trade Hub", layout="wide", page_icon="🌍")

SENDER_EMAIL = "dropshipmillionaire19@gmail.com"
SENDER_PASSWORD = "byyh oiii eibi cuov"
MY_WHATSAPP_LINK = "https://wa.me/66964474797?text=Hello%20CEO"

# เชื่อมต่อ Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 2. CORE FUNCTIONS ---
def get_user_data():
    try:
        return conn.read(ttl=0)
    except:
        return pd.DataFrame(columns=["username", "password", "email", "role"])

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
    except:
        return False

# --- 3. SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🌐 Global Hub")
    if not st.session_state['logged_in']:
        # คืนค่าเมนูที่หายไปตรงนี้ครับบอส
        mode = st.radio("Access Menu", ["Login", "Sign Up", "Forgot Password"])
    else:
        st.success(f"User: **{st.session_state.username}**")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
        st.divider()
        st.markdown(f'''<a href="{MY_WHATSAPP_LINK}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 10px; border-radius: 5px; width: 100%; cursor: pointer; font-weight: bold;">WhatsApp Support</button></a>''', unsafe_allow_html=True)

# --- 5. AUTHENTICATION PAGES ---
df_users = get_user_data()

if not st.session_state['logged_in']:
    if mode == "Login":
        st.title("🔐 Login")
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Sign In"):
            match = df_users[(df_users['username'] == u) & (df_users['password'] == p)]
            if not match.empty:
                st.session_state.logged_in = True
                st.session_state.username = u
                st.session_state.role = match.iloc[0]['role']
                st.rerun()
            else:
                st.error("Invalid Username or Password")

    elif mode == "Sign Up":
        st.title("📝 Register")
        nu = st.text_input("Username")
        ne = st.text_input("Email")
        np = st.text_input("Password", type="password")
        nr = st.selectbox("I am a", ["Buyer", "Seller"])
        if st.button("Create Account"):
            if nu and ne and np:
                new_row = pd.DataFrame([{"username": nu, "password": np, "email": ne, "role": nr}])
                save_to_sheets(pd.concat([df_users, new_row], ignore_index=True))
                send_email(ne, "Welcome", f"Hello {nu}, your account is ready!")
                st.success("Registration Success!")
                st.balloons()
            else:
                st.error("Please fill all fields")

    elif mode == "Forgot Password":
        st.title("🔑 Password Recovery")
        target_email = st.text_input("Enter your registered email")
        if st.button("Recover Password"):
            user_info = df_users[df_users['email'] == target_email]
            if not user_info.empty:
                pwd = user_info.iloc[0]['password']
                success = send_email(target_email, "Password Recovery", f"Your password is: {pwd}")
                if success:
                    st.success("📩 Password has been sent to your email.")
                else:
                    st.error("Failed to send email. Check your settings.")
            else:
                st.error("Email not found in our database.")
    st.stop()

# --- 6. CEO MAIN DASHBOARD (Visible only after login) ---
st.title(f"📊 {st.session_state.role} Command Center")

tab1, tab2 = st.tabs(["🎯 AI Lead Radar", "👥 User Database"])

with tab1:
    st.header("📡 AI Lead Radar (Scan Global Markets)")
    c1, c2 = st.columns(2)
    with c1:
        keyword = st.text_input("Product Name", "Sugar IC45")
        country = st.text_input("Target Country", "Dubai")
    with c2:
