import streamlit as st
import json
import os
import pandas as pd
from fpdf import FPDF
import io

# --- Configuration & File Handling ---
DB_FILE = "data.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Purchase Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    
    # Table Header
    pdf.cell(80, 10, "Item", border=1)
    pdf.cell(30, 10, "Price", border=1)
    pdf.cell(20, 10, "Qty", border=1)
    pdf.cell(40, 10, "Total", border=1)
    pdf.ln()

    # Table Rows
    total_sum = 0
    for item in data:
        pdf.cell(80, 10, str(item['Item']), border=1)
        pdf.cell(30, 10, f"${item['Unit Price']:.2f}", border=1)
        pdf.cell(20, 10, str(item['Qty']), border=1)
        pdf.cell(40, 10, f"${item['Total']:.2f}", border=1)
        pdf.ln()
        total_sum += item['Total']
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(130, 10, "Grand Total", border=1)
    pdf.cell(40, 10, f"${total_sum:.2f}", border=1)
    
    return pdf.output(dest='S').encode('latin-1')

st.set_page_config(page_title="SpendStack Pro", page_icon="🛍️", layout="wide")

# --- Session State ---
if 'shopping_list' not in st.session_state:
    st.session_state.shopping_list = load_data()
if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

st.title("🛍️ SpendStack Pro")

# --- Import/Export Sidebar ---
with st.sidebar:
    st.header("Import / Export")
    uploaded_file = st.file_uploader("Upload previous CSV", type="csv")
    if uploaded_file is not None:
        if st.button("Merge CSV with Current List"):
            uploaded_df = pd.read_csv(uploaded_file)
            # Standardize columns to match our JSON structure
            new_items = uploaded_df.to_dict('records')
            st.session_state.shopping_list.extend(new_items)
            save_data(st.session_state.shopping_list)
            st.success("CSV Imported & Merged!")
            st.rerun()

# --- Input/Edit Section ---
with st.expander("📝 Item Details", expanded=True):
    edit_idx = st.session_state.edit_index
    is_editing = edit_idx is not None
    
    curr = st.session_state.shopping_list
    d_name = curr[edit_idx]['Item'] if is_editing else ""
    d_price = curr[edit_idx]['Unit Price'] if is_editing else 0.0
    d_qty = curr[edit_idx]['Qty'] if is_editing else 1

    col1, col2, col3 = st.columns([3, 1, 1])
    item_name = col1.text_input("Item Name", value=d_name)
    price = col2.number_input("Price ($)", min_value=0.0, value=d_price, format="%.2f")
    quantity = col3.number_input("Qty", min_value=1, value=d_qty, step=1)

    if st.button("Update Item" if is_editing else "Add to List", type="primary"):
        if item_name:
            new_item = {"Item": item_name, "Unit Price": price, "Qty": quantity, "Total": price * quantity}
            if is_editing:
                st.session_state.shopping_list[edit_idx] = new_item
                st.session_state.edit_index = None
            else:
                st.session_state.shopping_list.append(new_item)
            save_data(st.session_state.shopping_list)
            st.rerun()

# --- List Display ---
if st.session_state.shopping_list:
    st.subheader("Current List")
    for idx, item in enumerate(st.session_state.shopping_list):
        c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 1])
        c1.write(item['Item'])
        c2.write(f"${item['Unit Price']:.2f}")
        c3.write(str(item['Qty']))
        c4.write(f"${item['Total']:.2f}")
        
        btn_c1, btn_c2 = c5.columns(2)
        if btn_c1.button("✏️", key=f"e_{idx}"):
            st.session_state.edit_index = idx
            st.rerun()
        if btn_c2.button("🗑️", key=f"d_{idx}"):
            st.session_state.shopping_list.pop(idx)
            save_data(st.session_state.shopping_list)
            st.rerun()

    # --- Totals & Downloads ---
    st.divider()
    total_val = sum(i['Total'] for i in st.session_state.shopping_list)
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Grand Total", f"${total_val:.2f}")
    
    # CSV Download
    df = pd.DataFrame(st.session_state.shopping_list)
    csv_data = df.to_csv(index=False).encode('utf-8')
    col_b.download_button("📥 Download CSV", csv_data, "list.csv", "text/csv")
    
    # PDF Download
    pdf_data = generate_pdf(st.session_state.shopping_list)
    col_c.download_button("📄 Download PDF", pdf_data, "report.pdf", "application/pdf")

else:
    st.info("List is empty. Use the form above or upload a CSV.")