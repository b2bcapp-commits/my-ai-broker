import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Global Trade Hub", layout="wide")

# --- การเชื่อมต่อแบบ Real-time ---
def get_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn.read(ttl=0)

st.title("🌍 BethofenPro Command Center")

try:
    df = get_data()
    st.success("✅ เชื่อมต่อฐานข้อมูลสำเร็จ!")
    
    tab1, tab2 = st.tabs(["📤 Post Product", "📊 Database View"])
    
    with tab1:
        st.subheader("เพิ่มสินค้าใหม่เข้าสู่ระบบ")
        with st.form("product_form", clear_on_submit=True):
            p_name = st.text_input("ชื่อสินค้า (เช่น Sugar ICUMSA 45)")
            p_price = st.text_input("ราคา/เงื่อนไข (เช่น 480 per ton)")
            p_desc = st.text_area("รายละเอียด (เช่น FOB Brazil)")
            
            if st.form_submit_button("🚀 Publish Product Now"):
                if p_name and p_price:
                    # สร้างข้อมูลใหม่
                    new_row = pd.DataFrame([{
                        "username": p_name, 
                        "password": p_price, 
                        "email": p_desc, 
                        "role": "Product_Listing"
                    }])
                    # อัปเดตลง Sheets
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    conn.update(data=updated_df)
                    st.balloons()
                    st.success(f"บันทึกสินค้า '{p_name}' เรียบร้อยแล้ว!")
                    st.rerun()
    
    with tab2:
        st.write("ข้อมูลปัจจุบันในฐานข้อมูล:")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"กำลังรอการเชื่อมต่อ... (หากรอนานเกิน 1 นาที ให้กด Reboot App)")
