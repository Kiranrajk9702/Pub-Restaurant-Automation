import os
import sqlite3
from datetime import datetime

# Ensure the database and tables are created when this file is imported

def initialize_database():
    connection = sqlite3.connect('pub_restaurant.db')
    cursor = connection.cursor()

    # Create the menu table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL,
            is_available TEXT DEFAULT 'Yes',
            description TEXT
        )
    ''')

    # Create other necessary tables if needed
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_time TEXT NOT NULL,
            table_number INTEGER,
            waiter_Robot_name TEXT,
            total_amount REAL NOT NULL,
            payment_method TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            item_id INTEGER,
            quantity INTEGER,
            price_per_item REAL,
            FOREIGN KEY(order_id) REFERENCES orders(order_id),
            FOREIGN KEY(item_id) REFERENCES menu(id)
        )
    ''')

    connection.commit()
    connection.close()

# Call the function to ensure tables are created
initialize_database()

# --- Connect to SQLite DB ---
conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'pub_restaurant.db'))
cursor = conn.cursor()

# --- Insert Menu Items ---
def add_menu_items():
    print("\n--- MENU ENTRY ---")
    while True:
        try:
            print("\nEnter new menu item details:")

            item_name = input("Item name: ").strip()
            category = input("Category (Drinks/Snacks/etc): ").strip()
            price = float(input("Price: ₹").strip())
            description = input("Description: ").strip()
            is_available = input("Available? (Yes/No): ").strip().capitalize()

            cursor.execute("""
                INSERT INTO menu (item_name, category, price, is_available, description)
                VALUES (?, ?, ?, ?, ?)
            """, (item_name, category, price, is_available, description))
            conn.commit()
            print("✅ Item added to menu.")
        except ValueError:
            print("❌ Error: Price must be a number.")
        except Exception as e:
            print(f"❌ Error: {e}")

        choice = input("Add another item? (y/n): ").strip().lower()
        if choice != 'y':
            break

def add_menu_item(item_name, category, price, description, is_available):
    connection = sqlite3.connect('pub_restaurant.db')
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO menu (item_name, category, price, description, is_available)
        VALUES (?, ?, ?, ?, ?)
    ''', (item_name, category, price, description, is_available))

    connection.commit()
    connection.close()

# --- Update Menu Item ---
def update_menu_item():
    print("\n--- UPDATE MENU ITEM ---")
    try:
        item_id = int(input("Enter Item ID to update: "))
        print("1. Update Name")
        print("2. Update Price")
        print("3. Update Availability")
        print("4. Update Description")
        choice = input("What would you like to update? (1/2/3/4): ")

        if choice == '1':
            new_name = input("Enter new item name: ")
            cursor.execute("UPDATE menu SET item_name = ? WHERE id = ?", (new_name, item_id))
        elif choice == '2':
            new_price = float(input("Enter new price: ₹"))
            cursor.execute("UPDATE menu SET price = ? WHERE id = ?", (new_price, item_id))
        elif choice == '3':
            new_availability = input("Enter new availability (Yes/No): ")
            cursor.execute("UPDATE menu SET is_available = ? WHERE id = ?", (new_availability, item_id))
        elif choice == '4':
            new_description = input("Enter new description: ")
            cursor.execute("UPDATE menu SET description = ? WHERE id = ?", (new_description, item_id))
        else:
            print("❌ Invalid choice!")
            return

        conn.commit()
        print("✅ Item updated successfully!")
    except ValueError:
        print("❌ Invalid input. Please enter correct values.")
    except Exception as e:
        print(f"❌ Error: {e}")

# --- Delete Menu Item ---
def delete_menu_item():
    print("\n--- DELETE MENU ITEM ---")
    try:
        item_id = int(input("Enter Item ID to delete: "))
        cursor.execute("DELETE FROM menu WHERE id = ?", (item_id,))
        conn.commit()
        print("✅ Item deleted successfully!")
    except ValueError:
        print("❌ Please enter a valid Item ID.")
    except Exception as e:
        print(f"❌ Error: {e}")

# --- View Order History ---
def view_order_history():
    print("\n--- ORDER HISTORY ---")
    try:
        date_filter = input("Filter by date? (Y/N): ").strip().lower()
        if date_filter == 'y':
            date = input("Enter date (YYYY-MM-DD): ")
            cursor.execute("SELECT * FROM orders WHERE date_time LIKE ?", (f"{date}%",))
        else:
            cursor.execute("SELECT * FROM orders")

        orders = cursor.fetchall()
        if orders:
            for order in orders:
                print(f"Order ID: {order[0]} | Table: {order[2]} | Waiter: {order[3]} | Total: ₹{order[4]} | Date: {order[1]}")
        else:
            print("❌ No orders found.")
    except Exception as e:
        print(f"❌ Error: {e}")

# --- Sales Summary ---
def daily_sales_summary():
    print("\n--- DAILY SALES SUMMARY ---")
    try:
        date = input("Enter the date for summary (YYYY-MM-DD): ")
        cursor.execute("""
            SELECT SUM(total_amount), COUNT(order_id), payment_method FROM orders
            WHERE date_time LIKE ?
            GROUP BY payment_method
        """, (f"{date}%",))
        sales_data = cursor.fetchall()

        total_sales = 0
        total_orders = 0
        for data in sales_data:
            total_sales += data[0]
            total_orders += data[1]
            print(f"Payment Method: {data[2]} | Orders: {data[1]} | Total: ₹{data[0]}")

        print(f"\nTotal Sales for {date}: ₹{total_sales}")
        print(f"Total Orders for {date}: {total_orders}")
    except Exception as e:
        print(f"❌ Error: {e}")

# --- Take Order ---
def take_order():
    try:
        print("\n📋 Current Menu:")
        cursor.execute("SELECT id, item_name, price, is_available FROM menu WHERE is_available = 'Yes'")
        menu_items = cursor.fetchall()

        for item in menu_items:
            print(f"ID: {item[0]} | {item[1]} - ₹{item[2]}")

        table_number = int(input("\nEnter Table Number: "))
        waiter_name = input("Enter Waiter Name: ")

        order_items = []
        total_amount = 0

        while True:
            try:
                item_id = int(input("Enter Item ID to add to order (0 to finish): "))
                if item_id == 0:
                    break
                quantity = int(input("Enter Quantity: "))

                cursor.execute("SELECT item_name, price FROM menu WHERE id = ?", (item_id,))
                result = cursor.fetchone()

                if result:
                    item_name, price = result
                    item_total = price * quantity
                    order_items.append((item_id, quantity, price))
                    total_amount += item_total
                    print(f"✅ Added {quantity} x {item_name} = ₹{item_total}")
                else:
                    print("❌ Invalid item ID. Try again.")
            except ValueError:
                print("❌ Invalid input. Please enter numeric values.")

        tax = round(total_amount * 0.10, 2)
        final_amount = round(total_amount + tax, 2)

        print("\n🧾 --- BILL SUMMARY ---")
        print(f"Table: {table_number} | Waiter: {waiter_name}")
        print(f"Subtotal: ₹{total_amount}")
        print(f"Tax (10%): ₹{tax}")
        print(f"Total Bill: ₹{final_amount}")

        payment_method = input("Enter Payment Method (Cash/Card/UPI): ")
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO orders (date_time, table_number, waiter_name, total_amount, payment_method)
            VALUES (?, ?, ?, ?, ?)
        """, (date_time, table_number, waiter_name, final_amount, payment_method))
        conn.commit()

        order_id = cursor.lastrowid
        for item in order_items:
            item_id, quantity, price = item
            cursor.execute("""
                INSERT INTO order_items (order_id, item_id, quantity, price_per_item)
                VALUES (?, ?, ?, ?)
            """, (order_id, item_id, quantity, price))
        conn.commit()
        print("💾 Order saved successfully!\n")
    except Exception as e:
        print(f"❌ Error taking order: {e}")

# --- Main Menu ---
def main():
    while True:
        print("\n========= AutoBite 🍽️ =========")
        print("1. Take New Order")
        print("2. Add Menu Item")
        print("3. Update Menu Item")
        print("4. Delete Menu Item")
        print("5. View Order History")
        print("6. Sales Summary")
        print("7. Exit")

        choice = input("Choose an option: ")
        if choice == '1':
            take_order()
        elif choice == '2':
            add_menu_items()
        elif choice == '3':
            update_menu_item()
        elif choice == '4':
            delete_menu_item()
        elif choice == '5':
            view_order_history()
        elif choice == '6':
            daily_sales_summary()
        elif choice == '7':
            print("👋 Exiting AutoBite System. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

# Start the program
if __name__ == "__main__":
    main()

# Close DB connection
conn.close()
