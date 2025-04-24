import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from datetime import datetime
import time
import sqlite3
from Database.database_logic import add_menu_item

# Initialize session state for notifications and dark mode
if 'notifications' not in st.session_state:
    st.session_state.notifications = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

def show_notification(message):
    st.session_state.notifications.append(message)

def display_notifications():
    for notification in st.session_state.notifications:
        st.info(notification)
    st.session_state.notifications = []

def main():
    st.set_page_config(page_title="Pub & Restaurant Automation", layout="wide")

    # Apply dark mode styling
    if st.session_state.dark_mode:
        st.markdown(
            """<style>
            body { background-color: #121212; color: #ffffff; }
            .stButton>button { background-color: #333333; color: #ffffff; }
            </style>""",
            unsafe_allow_html=True
        )

    st.title("🍽️ Pub & Restaurant Automation")

    # Sidebar navigation
    menu = ["Take New Order", "Add Menu Item", "Update Menu Item", "Delete Menu Item", "View Order History", "Sales Summary", "Power BI Dashboard", "ML Insights"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Dark mode toggle
    if st.sidebar.button("Toggle Dark Mode"):
        toggle_dark_mode()

    # Notifications
    display_notifications()

    if choice == "Take New Order":
        st.header("Take New Order")
        table_number = st.number_input("Table Number", min_value=1, step=1)
        waiter_name = st.text_input("Waiter/Robot Name")
        item_id = st.number_input("Item ID", min_value=1, step=1)
        quantity = st.number_input("Quantity", min_value=1, step=1)

        if st.button("Place Order"):
            show_notification(f"Order placed for Table {table_number} by {waiter_name}.")

    elif choice == "Add Menu Item":
        st.header("Add Menu Item")
        item_name = st.text_input("Item Name")
        category = st.text_input("Category")
        price = st.number_input("Price (₹)", min_value=0.0, step=0.1)
        description = st.text_area("Description")
        is_available = st.selectbox("Available", ["Yes", "No"])

        if st.button("Add Item"):
            try:
                add_menu_item(item_name, category, price, description, is_available)
                show_notification(f"Menu item '{item_name}' added successfully.")
            except Exception as e:
                st.error(f"Failed to add menu item: {e}")

    elif choice == "Update Menu Item":
        st.header("Update Menu Item")
        item_id = st.number_input("Item ID", min_value=1, step=1)
        field = st.selectbox("Update Field", ["Name", "Price", "Availability", "Description"])
        new_value = st.text_input("New Value")

        if st.button("Update Item"):
            show_notification(f"Menu item {item_id} updated successfully.")

    elif choice == "Delete Menu Item":
        st.header("Delete Menu Item")
        item_id = st.number_input("Item ID", min_value=1, step=1)

        if st.button("Delete Item"):
            show_notification(f"Menu item {item_id} deleted successfully.")

    elif choice == "View Order History":
        st.header("View Order History")
        date_filter = st.date_input("Filter by date")
        st.write(f"Showing orders for {date_filter}.")

    elif choice == "Sales Summary":
        st.header("Sales Summary")
        summary_date = st.date_input("Enter date")
        st.write(f"Showing sales summary for {summary_date}.")

    elif choice == "Power BI Dashboard":
        st.header("Power BI Dashboard")
        st.write("Embed Power BI dashboard here.")

    elif choice == "ML Insights":
        st.header("ML Insights")
        st.write("Show machine learning insights here.")

    # Real-time clock
    st.sidebar.markdown(f"**Current Time:** {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()