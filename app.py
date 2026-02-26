import streamlit as st
import pandas as pd

# --- 1. CONFIG & MULTI-LANGUAGE DICTIONARY ---
st.set_page_config(page_title="Global Trade Platform", layout="wide", page_icon="🌐")

texts = {
    "ไทย": {
        "title": "ศูนย์ควบคุม CEO อัจฉริยะ",
        "welcome": "ยินดีต้อนรับครับบอส",
        "role": "บทบาท",
        "logout": "ออกจากระบบ",
        "seller_portal": "🏭 หน้าต่างผู้ขาย (Seller)",
        "buyer_portal": "🛒 หน้าต่างผู้ซื้อ (Buyer)",
        "add_prod": "ลงทะเบียนสินค้าใหม่",
        "verify_status": "สถานะการตรวจสอบ",
        "comm_est": "ค่าคอมมิชชั่นสะสม (คาดการณ์)"
    },
    "English": {
        "title": "Smart CEO Command Center",
        "welcome": "Welcome, CEO",
        "role": "Role",
        "logout": "Logout",
        "seller_portal": "🏭 Seller Portal",
        "buyer_portal": "🛒 Buyer Marketplace",
        "add_prod": "Register New Product",
        "verify_status": "Verification Status",
        "comm_est": "Total Est. Commission"
    },
    "简体中文": {
        "title": "智能首席执行官指挥中心",
        "welcome": "欢迎, 首席执行官",
        "role": "角色",
        "logout": "登出",
        "seller_portal": "🏭 卖家门户",
        "buyer_portal": "🛒 买家市场",
        "add_prod": "注册新产品",
        "verify_status": "核实状态",
        "comm_est": "预计佣金总额"
    }
}

# --- 2. AUTHENTICATION DATABASE ---
USER_CREDENTIALS = {
    "admin": {"password": "789", "role": "CEO", "name": "CEO Master"},
    "seller": {"password": "123", "role": "Seller", "name": "Thai Supplier"},
    "buyer": {"password": "456", "role": "Buyer", "name": "Global Investor"}
}

# --- 3. SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['role'] = None
    st.session_state['user_name'] = ""
    st.session_state['lang'] = "ไทย"

# --- 4. LOGIN PAGE ---
if not st.session_state['logged_in']:
    st.title("🔐 Global Trade Platform")
    lang_choice = st.radio("Language / 语言", ["ไทย", "English", "简体中文"], horizontal=True)
    st.session_state['lang'] = lang_choice
    
    with st.container():
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Login"):
            if user in USER_CREDENTIALS and USER_CREDENTIALS[user]["password"] == pw:
                st.session_state['logged_in'] = True
                st.session_state['role'] = USER_CREDENTIALS[user]["role"]
                st.session_state['user_name'] = USER_CREDENTIALS[user]["name"]
                st.rerun()
            else:
                st.error("❌ Invalid Credentials / ข้อมูลไม่ถูกต้อง")
    st.stop()

# --- 5. APP INTERFACE ---
curr_lang = st.session_state['lang']
t = texts[curr_lang]
role = st.session_state['role']

# Sidebar
st.sidebar.title(f"👤 {st.session_state['user_name']}")
st.sidebar.write(f"{t['role']}: {role}")
new_lang = st.sidebar.selectbox("🌐 Switch Language", ["ไทย", "English", "简体中文"], index=["ไทย", "English", "简体中文"].index(curr_lang))
if new_lang != curr_lang:
    st.session_state['lang'] = new_lang
    st.rerun()

if st.sidebar.button(t['logout']):
    st.session_state['logged_in'] = False
    st.rerun()

# --- ROLE-BASED DASHBOARD ---
if role == "CEO":
    st.title(f"📊 {t['title']}")
    st.subheader(t['welcome'])
    
    col1, col2, col3 = st.columns(3)
    col1.metric(t['comm_est'], "฿15.2M", "+฿2.1M")
    col2.metric("Active Sellers", "42", "Verified")
    col3.metric("Global Buyers", "128", "Hot Interest")
    
    st.divider()
    st.write("🔍 **Admin Insight:** ระบบตรวจพบความสนใจซื้อ 'น้ำตาล' จากตลาดจีนเพิ่มขึ้น 20%")

elif role == "Seller":
    st.title(t['seller_portal'])
    with st.form("seller_form"):
        st.subheader(t['add_prod'])
        p_name = st.text_input("Product Name / 商品名称")
        p_origin = st.text_input("Origin / 产地")
        p_price = st.number_input("Target Price (USD)")
        p_file = st.file_uploader("Upload SGS/Cert (PDF/JPG)")
        if st.form_submit_button("Submit to CEO"):
            st.success("Sent! Waiting for CEO Verification.")

elif role == "Buyer":
    st.title(t['buyer_portal'])
    st.info("Verified Products only / เฉพาะสินค้าที่ผ่านการตรวจสอบแล้ว")
    # ตัวอย่างข้อมูลสินค้าที่ผู้ซื้อจะเห็น
    data = {
        "Product": ["ICUMSA 45 Sugar", "Frozen Chicken Wings", "Diesel EN590"],
        "Origin": ["Brazil/Thailand", "Thailand", "Global"],
        "Status": ["✅ Verified", "✅ Verified", "✅ Verified"]
    }
    st.table(pd.DataFrame(data))
    if st.button("Request Full POP / สนใจสั่งซื้อ"):
        st.warning("Please contact CEO for NCNDA Agreement.")
