import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="CEO Dashboard", layout="wide")

# --- FORCE CONNECT FUNCTION ---
def load_data():
    try:
        # เชื่อมต่อแบบไม่ใช้ Cache เพื่อป้องกันค่าค้าง
        conn = st.connection("gsheets", type=GSheetsConnection)
        return conn.read(ttl=0)
    except Exception as e:
        st.error(f"⚠️ กำลังพยายามเชื่อมต่อใหม่... (Error: {e})")
        return None

# --- UI LOGIC ---
st.title("🌍 BethofenPro Command Center")

df = load_data()

if df is not None:
    st.success("✅ เชื่อมต่อฐานข้อมูลสำเร็จ!")
    
    # ปุ่มทางลัดเข้าหน้าจัดการสินค้าทันที ไม่ต้อง Login ซ้ำ
    tab1, tab2 = st.tabs(["📦 Marketplace Management", "👥 Database View"])
    
    with tab1:
        st.subheader("➕ เพิ่มสินค้าใหม่ (ส่งตรงถึง Sheets)")
        with st.form("quick_post", clear_on_submit=True):
            p_name = st.text_input("ชื่อสินค้า")
            p_price = st.text_input("ราคา/เงื่อนไข")
            p_desc = st.text_area("รายละเอียด")
            
            if st.form_submit_button("🚀 Publish Now"):
                if p_name and p_price:
                    new_data = pd.DataFrame([{"username": p_name, "password": p_price, "email": p_desc, "role": "Product_Listing"}])
                    updated_df = pd.concat([df, new_data], ignore_index=True)
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    conn.update(data=updated_df)
                    st.balloons()
                    st.success(f"บันทึก '{p_name}' ลง Google Sheets เรียบร้อย!")
                    st.rerun()
    
    with tab2:
        st.write("ข้อมูลปัจจุบันใน Sheets ของบอส:")
        st.dataframe(df)
else:
    st.warning("🔄 กรุณารอสักครู่ ระบบกำลังเจรจากับ Google... หากยังไม่มา ให้กด 'Manage App' -> 'Reboot App' ครับ")
