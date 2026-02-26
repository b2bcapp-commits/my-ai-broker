import streamlit as st
import pandas as pd
import webbrowser

# --- 1. CONFIG ---
st.set_page_config(page_title="Global Trade Platform", layout="wide", page_icon="🌐")

# ใส่ LINE ID หรือ Link OA ของคุณตรงนี้
LINE_ADMIN_URL = "https://line.me/ti/p/~YOUR_LINE_ID" # <-- เปลี่ยนเป็น ID ของคุณ

# --- 2. MULTI-LANGUAGE ---
texts = {
    "ไทย": {
        "contact_btn": "📱 ติดต่อแอดมิน (CEO)",
        "msg_placeholder": "พิมพ์ข้อความที่ต้องการแจ้ง...",
        "send_success": "ระบบเตรียมข้อความให้คุณแล้ว กรุณากดปุ่มด้านล่างเพื่อส่งทาง LINE",
        "match_interest": "🎯 สนใจดีลนี้"
    },
    "English": {
        "contact_btn": "📱 Contact Admin (CEO)",
        "msg_placeholder": "Type your message here...",
        "send_success": "Message prepared! Please click below to send via LINE.",
        "match_interest": "🎯 Interested in this Deal"
    },
    "简体中文": {
        "contact_btn": "📱 联系管理员 (CEO)",
        "msg_placeholder": "在此输入您的留言...",
        "send_success": "消息已准备好！请点击下方通过 LINE 发送。",
        "match_interest": "🎯 对此交易感兴趣"
    }
}

# --- [ส่วน Login และ Session State เหมือนเดิม แต่เพิ่มการเช็คภาษา] ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['role'] = None
    st.session_state['lang'] = "ไทย"

# (ข้ามส่วน Login ไปที่หน้าแสดงผลหลัก)
if st.session_state['logged_in']:
    curr_lang = st.session_state['lang']
    t = texts[curr_lang]
    role = st.session_state['role']

    # --- เพิ่มปุ่มใน Sidebar สำหรับทุก Role ---
    st.sidebar.divider()
    st.sidebar.subheader(t['contact_btn'])
    user_msg = st.sidebar.text_area(t['msg_placeholder'], height=100)
    
    if st.sidebar.button("📤 Send Message"):
        if user_msg:
            # สร้าง Link สำหรับส่งข้อความเข้า LINE
            st.sidebar.success(t['send_success'])
            st.sidebar.markdown(f"[![Line](https://img.shields.io/badge/LINE-00C300?style=for-the-badge&logo=line&logoColor=white)]({LINE_ADMIN_URL})")
        else:
            st.sidebar.error("กรุณาพิมพ์ข้อความก่อนส่ง")

    # --- หน้าต่างสำหรับ Buyer (ผู้ซื้อ) เพิ่มปุ่ม "สนใจดีล" ---
    if role == "Buyer":
        st.title("🛒 Global Buyer Marketplace")
        # ตัวอย่างข้อมูลสินค้า
        items = [{"สินค้า": "Sugar ICUMSA 45", "ราคา": "$4xx/MT"}, {"สินค้า": "Frozen Chicken", "ราคา": "Market Price"}]
        for item in items:
            with st.expander(f"📦 {item['สินค้า']}"):
                st.write(f"ราคาประมาณการ: {item['ราคา']}")
                if st.button(f"{t['match_interest']} ({item['สินค้า']})"):
                    st.toast(f"บันทึกความสนใจใน {item['สินค้า']} แล้ว แอดมินจะติดต่อกลับ!")
                    # ในอนาคตจะเชื่อมต่อ Database เพื่อเก็บ Log ตรงนี้

    # --- หน้าต่างสำหรับ CEO (แอดมิน) ---
    elif role == "CEO":
        st.title("📊 CEO Master Control")
        st.success("📢 ระบบแจ้งเตือน: ขณะนี้การแจ้งเตือนจะใช้ผ่าน LINE Messaging API แทน Notify เพื่อความเสถียร")
        
        # ส่วนแสดงผล Log การติดต่อ
        st.subheader("📝 รายการติดต่อจากผู้ใช้งาน (Logs)")
        mock_logs = pd.DataFrame([
            {"เวลา": "10:30", "จาก": "Buyer_China", "เรื่อง": "สนใจน้ำตาล 50,000 ตัน"},
            {"เวลา": "11:15", "จาก": "Seller_Thai", "เรื่อง": "อัปเดตสต็อกไก่แปรรูป"}
        ])
        st.table(mock_logs)
