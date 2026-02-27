import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. CONFIG & CONNECTION ---
st.set_page_config(page_title="Global Trade Hub", layout="wide")

# เชื่อมต่อกับ Google Sheets ที่บอสให้มา
# (บอสต้องติดตั้ง pip install st-gsheets-connection ด้วยนะครับ)
url = "https://docs.google.com/spreadsheets/d/1tKvEYFzklkgwXG2qCt9LxSs7qbf2d3oE2VccvaPEMOU/edit?gid=0#gid=0"
conn = st.connection("gsheets", type=GSheetsConnection)

# ข้อมูลอีเมลของ CEO
SENDER_EMAIL = "dropshipmillionaire19@gmail.com"
SENDER_PASSWORD = "byyh oiii eibi cuov"

# --- 2. FUNCTION: อ่านและเขียนข้อมูล ---
def get_user_data():
    return conn.read(spreadsheet=url, usecols=[0, 1, 2, 3])

def save_user_data(df):
    conn.update(spreadsheet=url, data=df)

# --- 3. EMAIL FUNCTION ---
def send_confirmation(receiver_email, username, role):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email
        msg['Subject'] = "Registration Confirmed - Global Trade Hub"
        body = f"Hello {username},\n\nYour account as a {role} has been created successfully."
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()
    except Exception as e:
        st.error(f"Email error: {e}")

# --- 4. SIGN UP LOGIC (จุดเปลี่ยนสำคัญ) ---
# (ในส่วน Sign Up ให้เพิ่มโค้ดบันทึกข้อมูลดังนี้)
# ... (ส่วนอินพุต username, email, password) ...

if st.button("Create Account"):
    existing_data = get_user_data()
    # ตรวจสอบว่าชื่อซ้ำไหม
    if new_user in existing_data['username'].values:
        st.error("Username already exists!")
    else:
        new_row = pd.DataFrame([{
            "username": new_user,
            "password": new_pw,
            "email": new_email,
            "role": new_role
        }])
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        save_user_data(updated_df)
        send_confirmation(new_email, new_user, new_role)
        st.success("Account saved to Google Sheets and Email sent!")
