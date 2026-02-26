import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Global Broker Terminal", layout="wide", page_icon="🌐")

# --- DICTIONARY: ระบบฐานข้อมูลภาษา ---
lang_pack = {
    "ไทย": {
        "title": "ศูนย์บัญชาการนายหน้าโลก",
        "sidebar_title": "เมนูควบคุม",
        "industry_label": "ประเภทธุรกิจ",
        "menu_label": "เมนู",
        "dash": "แดชบอร์ดภาพรวม",
        "search": "ค้นหา & ตรวจสอบ",
        "add": "บันทึกชิ้นงานใหม่",
        "verify_status": "ยืนยันการตรวจสอบเอกสาร (Due Diligence)",
        "save_btn": "บันทึกเข้าระบบกลาง",
        "lang_select": "เลือกภาษา (Language)"
    },
    "English": {
        "title": "Global Broker Command Center",
        "sidebar_title": "Control Panel",
        "industry_label": "Industry Type",
        "menu_label": "Menu",
        "dash": "Overview Dashboard",
        "search": "Search & Verification",
        "add": "Add New Deal",
        "verify_status": "Due Diligence Verified",
        "save_btn": "Save to Global System",
        "lang_select": "Select Language"
    },
    "简体中文 (Mainland China)": {
        "title": "全球经纪人指挥中心",
        "sidebar_title": "控制面板",
        "industry_label": "业务类型",
        "menu_label": "菜单",
        "dash": "数据总览",
        "search": "搜索与核查",
        "add": "新增交易",
        "verify_status": "尽职调查已核實 (Due Diligence)",
        "save_btn": "保存到全球系统",
        "lang_select": "选择语言"
    },
    "繁體中文 (HK/Taiwan)": {
        "title": "全球經紀人指揮中心",
        "sidebar_title": "控制面板",
        "industry_label": "業務類型",
        "menu_label": "選單",
        "dash": "數據總覽",
        "search": "搜索與核查",
        "add": "新增交易",
        "verify_status": "盡職調查已核實 (Due Diligence)",
        "save_btn": "保存到全球系統",
        "lang_select": "選擇語言"
    }
}

# --- SELECT LANGUAGE ---
st.sidebar.title("🌐 Language Settings")
selected_lang = st.sidebar.selectbox("Language", list(lang_pack.keys()))
text = lang_pack[selected_lang]

# --- SIDEBAR CONTROL ---
st.sidebar.divider()
st.sidebar.title(f"🛠️ {text['sidebar_title']}")
industry = st.sidebar.selectbox(text['industry_label'], [
    "🏢 Real Estate / 房地产 / อสังหาฯ", 
    "🍬 Sugar / 糖贸易 / น้ำตาล", 
    "🍗 Poultry / 禽肉贸易 / ชิ้นส่วนไก่"
])

menu_choice = st.sidebar.radio(text['menu_label'], [text['dash'], text['search'], text['add']])

# --- MAIN UI ---
st.title(f"{text['title']}")

if menu_choice == text['dash']:
    st.subheader(f"📊 {industry}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Status", "Active", delta="Verified")
    col2.metric("Market", "Global", delta="2026")
    col3.metric("Security", "L/C & SBLC", delta="Safe")
    
    st.info("💡 ข้อมูลจะปรับตามภาษาที่คุณเลือก เพื่อใช้พรีเซนต์ให้ลูกค้าต่างชาติเห็นความน่าเชื่อถือ")

elif menu_choice == text['add']:
    st.subheader(f"📥 {text['add']}")
    with st.form("global_form"):
        col1, col2 = st.columns(2)
        with col1:
            subject = st.text_input("Deal Subject / 交易主题 / หัวข้อดีล")
            origin = st.text_input("Origin / 产地 / แหล่งที่มา")
        with col2:
            qty = st.text_input("Quantity / 数量 / จำนวน")
            price = st.text_input("Price / 价格 / ราคา")
        
        verified = st.checkbox(text['verify_status'])
        
        if st.form_submit_button(text['save_btn']):
            st.success("Successfully Saved / 保存成功 / บันทึกสำเร็จ!")
            st.balloons()
