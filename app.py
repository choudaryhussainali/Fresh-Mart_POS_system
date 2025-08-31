import streamlit as st
import datetime

# ----------------- Grocery Items -----------------
grocery_items = {
    "Grains": {
        "Rice (1kg)": 200,
        "Wheat (1kg)": 180,
        "Oats (500g)": 120
    },
    "Dairy": {
        "Milk (1L)": 60,
        "Cheese (200g)": 150,
        "Butter (500g)": 250
    },
    "Bakery": {
        "Bread (1 loaf)": 50,
        "Eggs (6 pcs)": 90,
        "Cake (500g)": 400
    },
    "Beverages": {
        "Tea (250g)": 180,
        "Coffee (200g)": 250,
        "Juice (1L)": 120
    },
    "Snacks": {
        "Chips (200g)": 80,
        "Biscuits (300g)": 90,
        "Chocolate (100g)": 150
    }
}

# ----------------- Functions -----------------
def calculate_bill(order):
    total = 0
    lines = []

    for item, details in order.items():
        cost = details["price"] * details["qty"]
        total += cost
        lines.append(f"{item} x {details['qty']} = ₹{cost}")

    discount = 0
    if total > 1000:
        discount = total * 0.10
        lines.append(f"✅ Discount Applied: -₹{discount:.2f}")

    after_discount = total - discount
    tax = after_discount * 0.05
    final_total = after_discount + tax

    lines.append(f"GST (5%): ₹{tax:.2f}")
    lines.append(f"💰 Final Amount to Pay: ₹{final_total:.2f}")

    return lines, total, discount, tax, final_total

def save_invoice(name, phone, lines, total, discount, tax, final_total):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("invoice.txt", "a", encoding="utf-8") as f:
        f.write(f"\n🧾 INVOICE - {timestamp}\n")
        f.write(f"Customer: {name}\nPhone: {phone}\n\n")
        for line in lines:
            f.write(line + "\n")
        f.write(f"\nSubtotal: ₹{total}")
        f.write(f"\nDiscount: ₹{discount:.2f}")
        f.write(f"\nGST: ₹{tax:.2f}")
        f.write(f"\nFinal Amount: ₹{final_total:.2f}")
        f.write("\n" + "-"*50 + "\n")

# ----------------- Streamlit UI -----------------
def main():
    st.set_page_config(page_title="Fresh-Mart Grocery Store", page_icon="🛒", layout="wide")
    st.title("🛒 Fresh-Mart | Grocery")
    st.write("Welcome to the **Professional POS Billing System** ")

    # Sidebar - Customer Info
    st.sidebar.header("👤 Customer Details")
    name = st.sidebar.text_input("Enter Customer Name")
    phone = st.sidebar.text_input("Enter Phone Number")

    st.sidebar.write("---")
    st.sidebar.info("Fill customer details and select items from the menu")

    # Main - Menu Selection
    st.header("📂 Grocery Menu")
    order = {}

    for category, items in grocery_items.items():
        with st.expander(category, expanded=False):
            for item, price in items.items():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    selected = st.checkbox(f"{item} (₹{price})", key=item)
                with col2:
                    qty = st.number_input("Qty", min_value=1, value=1, step=1, key=f"{item}_qty")
                with col3:
                    st.write(" ")
                if selected:
                    order[item] = {"price": price, "qty": qty}

    # Billing Section
    if st.button("🧾 Generate Invoice"):
        if not name or not phone:
            st.error("⚠️ Please enter customer details before generating invoice.")
        elif not order:
            st.warning("⚠️ No items selected. Please add some items.")
        else:
            lines, total, discount, tax, final_total = calculate_bill(order)

            st.success("✅ Invoice Generated Successfully!")
            st.subheader("🧾 Customer Invoice")
            st.text(f"Customer: {name}\nPhone: {phone}")
            st.write("---")
            for line in lines:
                st.write(line)
            st.write("---")
            st.write(f"**Subtotal:** ₹{total}")
            st.write(f"**Discount:** ₹{discount:.2f}")
            st.write(f"**GST (5%):** ₹{tax:.2f}")
            st.write(f"**Final Amount:** ₹{final_total:.2f}")

            # Save Invoice
            save_invoice(name, phone, lines, total, discount, tax, final_total)
            st.info("📂 Invoice saved to `invoice.txt`")

if __name__ == "__main__":
    main()

