# 🛍️ SpendStack Pro

**SpendStack Pro** is a lightweight, persistent purchase calculator built with Python and Streamlit. It helps users manage shopping lists, calculate totals in real-time, and export data for record-keeping.



## ✨ Features

* **Real-time Calculations:** Automatically calculates totals as you add or edit items.
* **Persistence:** Saves your list to a local `data.json` file so you don't lose data on refresh.
* **Modify & Delete:** Easily update existing items or remove them from your list.
* **Data Import:** Upload previous CSV exports to merge them into your current list.
* **Professional Exports:** Download your shopping list as a formatted **PDF** or a **CSV** for Excel.
* **Responsive UI:** A clean, wide-layout interface that works on mobile and desktop.

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have Python installed. You will also need to install the following libraries:

pip install streamlit pandas fpdf

1. Run the App
Clone this repository or download the files, then run:

Bash

streamlit run app.py
📂 File Structure
app.py: The main application code.

requirements.txt: List of dependencies for cloud deployment.

data.json: Local database (created automatically upon first use).

README.md: Project documentation.

🛠️ Built With
Streamlit - The fastest way to build and share data apps.

Pandas - For data manipulation and CSV handling.

FPDF - For PDF report generation.

📝 How to Use
Add Items: Use the "Item Details" form at the top.

Edit/Delete: Use the ✏️ and 🗑️ buttons next to each row in the table.

Manage Data: Use the sidebar to upload old CSVs or the download buttons at the bottom to save your work.
