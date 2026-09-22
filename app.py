import streamlit as st
import random
import time
from datetime import datetime

# ----------------------------------------------------
# Menu Data & Pricing Configuration (all prices in ₦)
# ----------------------------------------------------
COFFEE_PRICES = {
    "Espresso": 1500,
    "Americano": 2000,
    "Cappuccino": 2500,
    "Café Latte": 3000,
    "Hot Chocolate": 2500,
}

BAR_PRICES = {
    "Hero": 2500,
    "Desperado": 2500,
    "Smirnoff ice": 2000,
    "Heineken": 3000,
    "Andrea": 30000,
}

SIZE_UPCHARGES = {
    "Small": 0,
    "Medium": 500,
    "Large": 1000
}

MILK_UPCHARGES = {
    "Whole Milk": 0,
    "Oat Milk": 750,
    "Almond Milk": 750,
    "Soy Milk": 500
}

EXTRA_PRICES = {
    "Extra Espresso Shot": 1000,
    "Whipped Cream": 500,
    "Caramel Drizzle": 500
}

PASTRY_PRICES = {
    "None": 0,
    "Butter Croissant": 3500,
    "Blueberry Muffin": 3000,
    "Chocolate Chip Cookie": 2500
}


def reset_order():
    """Clears all transient order state so the user can start fresh."""
    st.session_state.cart = []
    st.session_state.last_receipt = None
    st.session_state.order_placed = False


def validate_order(drink, drink_price, quantity, cart):
    """Returns a list of validation error strings. Empty list means valid."""
    errors = []

    if not drink or not drink.strip():
        errors.append("No drink selected.")

    if drink_price <= 0:
        errors.append("Selected drink has an invalid price.")

    if not isinstance(quantity, int) or quantity < 1:
        errors.append("Quantity must be at least 1.")
    elif quantity > 10:
        errors.append("Quantity cannot exceed 10 per item.")

    if len(cart) >= 20:
        errors.append("Cart is full — maximum 20 items per order.")

    return errors


def validate_cart(cart):
    """Returns a list of validation error strings for the cart as a whole."""
    errors = []

    if not cart:
        errors.append("Your cart is empty. Add at least one item before placing an order.")

    total = sum(item["item_total"] for item in cart)
    if total <= 0:
        errors.append("Order total must be greater than ₦0.")

    return errors


def calculate_order_total(drink_price, size, milk, selected_extras, pastry, quantity):
    """Calculates the unit price and total price of an order.

    `size` and `milk` are None for bar drinks, which contributes 0 to the total.
    """
    size_cost = SIZE_UPCHARGES.get(size, 0)
    milk_cost = MILK_UPCHARGES.get(milk, 0)

    extras_cost = sum(EXTRA_PRICES.get(extra, 0) for extra in selected_extras)
    pastry_cost = PASTRY_PRICES.get(pastry, 0)

    unit_price = drink_price + size_cost + milk_cost + extras_cost + pastry_cost
    total = unit_price * quantity
    return total, unit_price


def main():
    # Page setup
    st.set_page_config(page_title="The Daily Grind — Coffee & Bar", page_icon="☕", layout="centered")

    # ── Session state initialisation ──────────────────────────────────────────
    if "cart" not in st.session_state:
        st.session_state.cart = []          # list of order-item dicts
    if "order_placed" not in st.session_state:
        st.session_state.order_placed = False
    if "order_history" not in st.session_state:
        st.session_state.order_history = [] # list of completed order snapshots
    if "last_receipt" not in st.session_state:
        st.session_state.last_receipt = None  # most recent completed order snapshot

    # Header Section
    st.title("☕ The Daily Grind")
    st.markdown("### Coffee by Day, Cold Ones by Night")
    st.markdown(
        "Welcome to The Daily Grind's first digital ordering portal. "
        "Take your pick from the coffee or bar menu, customize it, and place your order live!"
    )

    # ── Main two-column layout ─────────────────────────────────────────────────
    col1, col2 = st.columns([2, 1])

    with col1:
        category = st.radio(
            "Choose Your Menu",
            options=["☕ Coffee", "🍺 Bar"],
            horizontal=True
        )
        is_coffee = category == "☕ Coffee"

        if is_coffee:
            st.subheader("Customize Your Drink")

            drink = st.selectbox(
                "Select Your Beverage",
                options=list(COFFEE_PRICES.keys()),
                help="Choose from our premium selected blends.",
                key="coffee_drink"
            )
            drink_price = COFFEE_PRICES[drink]

            size = st.radio(
                "Select Size",
                options=list(SIZE_UPCHARGES.keys()),
                horizontal=True,
                key="coffee_size"
            )

            milk = st.selectbox(
                "Milk Choice",
                options=list(MILK_UPCHARGES.keys()),
                key="coffee_milk"
            )

            st.subheader("Add Extras")
            selected_extras = []
            for extra, price in EXTRA_PRICES.items():
                if st.checkbox(f"{extra} (+₦{price:,.2f})", key=f"extra_{extra}"):
                    selected_extras.append(extra)
        else:
            st.subheader("Pick Your Bottle")

            drink = st.selectbox(
                "Select Your Drink",
                options=list(BAR_PRICES.keys()),
                help="Served chilled from the fridge.",
                key="bar_drink"
            )
            drink_price = BAR_PRICES[drink]

            size = None
            milk = None
            selected_extras = []

            st.caption("Bottles are served chilled — size, milk, and coffee extras are coffee-menu options.")

        st.subheader("Fresh Pastries")
        pastry = st.selectbox(
            "Select a Pastry",
            options=list(PASTRY_PRICES.keys()),
            key="pastry"
        )

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            max_value=10,
            value=1,
            step=1,
            key="quantity"
        )

        # ── Live price preview ─────────────────────────────────────────────────
        preview_total, preview_unit = calculate_order_total(
            drink_price, size, milk, selected_extras, pastry, quantity
        )
        st.markdown(
            f"**Item total:** ₦{preview_total:,.2f} "
            f"&nbsp;·&nbsp; ₦{preview_unit:,.2f} × {quantity}"
        )

        # ── Add to Cart button ─────────────────────────────────────────────────
        if st.button("🛒 Add to Cart", use_container_width=True):
            errors = validate_order(drink, drink_price, quantity, st.session_state.cart)
            if errors:
                for err in errors:
                    st.error(f"⚠️ {err}")
            else:
                item = {
                    "drink": drink,
                    "category": "coffee" if is_coffee else "bar",
                    "size": size,
                    "milk": milk,
                    "extras": list(selected_extras),
                    "pastry": pastry,
                    "quantity": quantity,
                    "unit_price": preview_unit,
                    "item_total": preview_total,
                }
                st.session_state.cart.append(item)
                st.session_state.order_placed = False
                st.toast(f"Added {drink} to your cart!")

    # ── Cart / Order summary column ────────────────────────────────────────────
    with col2:
        st.subheader("🛒 Your Cart")

        cart = st.session_state.cart

        if not cart:
            st.info("Your cart is empty.\nAdd items from the menu on the left.")
        else:
            cart_grand_total = 0
            for idx, item in enumerate(cart):
                with st.container(border=True):
                    label_parts = [item["drink"]]
                    if item["size"]:
                        label_parts.append(item["size"])
                    st.markdown(f"**{' · '.join(label_parts)}**")
                    if item["milk"]:
                        st.caption(f"Milk: {item['milk']}")
                    if item["extras"]:
                        st.caption(f"Extras: {', '.join(item['extras'])}")
                    if item["pastry"] != "None":
                        st.caption(f"Pastry: {item['pastry']}")
                    st.caption(
                        f"Qty: {item['quantity']} × ₦{item['unit_price']:,.2f} "
                        f"= ₦{item['item_total']:,.2f}"
                    )
                    if st.button("✕ Remove", key=f"remove_{idx}", use_container_width=True):
                        st.session_state.cart.pop(idx)
                        st.rerun()

                cart_grand_total += item["item_total"]

            st.markdown("---")
            st.markdown(f"### Grand Total: ₦{cart_grand_total:,.2f}")

            col_place, col_clear = st.columns(2)
            with col_place:
                place_order = st.button("🚀 Place Order", use_container_width=True)
            with col_clear:
                if st.button("🗑 Clear Cart", use_container_width=True):
                    st.session_state.cart = []
                    st.session_state.order_placed = False
                    st.rerun()

            # ── Order processing simulation ────────────────────────────────────
            if place_order:
                cart_errors = validate_cart(cart)
                if cart_errors:
                    for err in cart_errors:
                        st.error(f"⚠️ {err}")
                else:
                    has_coffee = any(i["category"] == "coffee" for i in cart)
                    has_bar    = any(i["category"] == "bar"    for i in cart)
                    has_pastry = any(i["pastry"] != "None"     for i in cart)

                    st.toast("Sending your order to the counter...")
                    with st.status("Working on your order...", expanded=True) as status:
                        if has_coffee:
                            st.write("Grinding fresh coffee beans... ☕")
                            time.sleep(1)
                            st.write("Steaming milk and crafting your drink... 🥛")
                            time.sleep(1.5)
                        if has_bar:
                            st.write("Pulling your bottle from the chiller... 🧊")
                            time.sleep(1)
                            st.write("Opening it up and getting your glass ready... 🍺")
                            time.sleep(1)
                        if has_pastry:
                            st.write("Boxing up your pastry... 🥐")
                            time.sleep(0.5)
                        status.update(label="Order ready for pickup!", state="complete", expanded=False)

                    order_num = random.randint(1000, 9999)
                    st.success(
                        f"🎉 **Order #{order_num} Placed!**\n\n"
                        f"**{len(cart)} item(s)** · Total: ₦{cart_grand_total:,.2f}\n\n"
                        f"Please collect at the counter in 5 minutes."
                    )
                    # ── Save to order history & receipt ───────────────────────────
                    receipt = {
                        "order_num": order_num,
                        "timestamp": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                        "items": list(cart),       # snapshot before clearing
                        "grand_total": cart_grand_total,
                        "item_count": len(cart),
                    }
                    st.session_state.order_history.append(receipt)
                    st.session_state.last_receipt = receipt
                    st.session_state.cart = []
                    st.session_state.order_placed = True

            # ── New Order button (shown after successful placement) ────────────
            if st.session_state.order_placed:
                st.markdown("&nbsp;")
                if st.button("🆕 Start New Order", use_container_width=True, type="primary", key="new_order_cart"):
                    reset_order()
                    st.rerun()


    # ── Receipt Card ───────────────────────────────────────────────────────────
    receipt = st.session_state.last_receipt
    if receipt:
        st.markdown("---")
        st.subheader("🧾 Your Receipt")

        receipt_md = f"""
<div style="
    background:#1e1e1e;
    border:1px solid #444;
    border-radius:12px;
    padding:24px 28px;
    font-family:'Courier New', monospace;
    color:#f0f0f0;
    max-width:480px;
    margin:auto;
">
<div style="text-align:center;margin-bottom:12px;">
  <span style="font-size:1.4rem;font-weight:bold;">☕ The Daily Grind</span><br/>
  <span style="font-size:0.85rem;color:#aaa;">Coffee by Day, Cold Ones by Night</span>
</div>
<hr style="border-color:#444;margin:10px 0;"/>
<div style="display:flex;justify-content:space-between;font-size:0.8rem;color:#aaa;">
  <span>Order #{receipt['order_num']}</span>
  <span>{receipt['timestamp']}</span>
</div>
<hr style="border-color:#444;margin:10px 0;"/>
"""
        for item in receipt["items"]:
            label = item["drink"]
            if item["size"]:
                label += f" ({item['size']})"
            receipt_md += f"""
<div style="margin-bottom:8px;">
  <div style="display:flex;justify-content:space-between;">
    <span style="font-weight:bold;">{label}</span>
    <span>₦{item['item_total']:,.2f}</span>
  </div>
"""
            sub = []
            if item["milk"]:
                sub.append(item["milk"])
            if item["extras"]:
                sub.extend(item["extras"])
            if item["pastry"] != "None":
                sub.append(item["pastry"])
            if sub:
                receipt_md += f'  <div style="font-size:0.78rem;color:#aaa;margin-left:8px;">{" · ".join(sub)}</div>\n'
            receipt_md += f'  <div style="font-size:0.78rem;color:#aaa;margin-left:8px;">Qty: {item["quantity"]} × ₦{item["unit_price"]:,.2f}</div>\n'
            receipt_md += "</div>\n"

        receipt_md += f"""
<hr style="border-color:#444;margin:10px 0;"/>
<div style="display:flex;justify-content:space-between;font-size:1.1rem;font-weight:bold;">
  <span>TOTAL</span>
  <span>₦{receipt['grand_total']:,.2f}</span>
</div>
<hr style="border-color:#444;margin:10px 0;"/>
<div style="text-align:center;font-size:0.8rem;color:#aaa;margin-top:8px;">
  Thank you for your order!<br/>Please collect at the counter.
</div>
</div>
"""
        st.markdown(receipt_md, unsafe_allow_html=True)

        st.markdown("&nbsp;")
        col_dismiss, col_new = st.columns(2)
        with col_dismiss:
            if st.button("✕ Dismiss Receipt", use_container_width=True):
                st.session_state.last_receipt = None
                st.rerun()
        with col_new:
            if st.button("🆕 Start New Order", use_container_width=True, type="primary", key="new_order_receipt"):
                reset_order()
                st.rerun()

    # ── Order History Section ──────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("📋 Order History")

    history = st.session_state.order_history

    if not history:
        st.caption("No orders placed yet this session. Your completed orders will appear here.")
    else:
        # Most recent first
        for order in reversed(history):
            with st.expander(
                f"Order #{order['order_num']}  ·  {order['timestamp']}  ·  "
                f"{order['item_count']} item(s)  ·  ₦{order['grand_total']:,.2f}",
                expanded=False
            ):
                for item in order["items"]:
                    label_parts = [item["drink"]]
                    if item["size"]:
                        label_parts.append(item["size"])
                    st.markdown(f"**{' · '.join(label_parts)}**")

                    details = []
                    if item["milk"]:
                        details.append(f"Milk: {item['milk']}")
                    if item["extras"]:
                        details.append(f"Extras: {', '.join(item['extras'])}")
                    if item["pastry"] != "None":
                        details.append(f"Pastry: {item['pastry']}")
                    if details:
                        st.caption("  ·  ".join(details))

                    st.caption(
                        f"Qty: {item['quantity']} × ₦{item['unit_price']:,.2f} "
                        f"= ₦{item['item_total']:,.2f}"
                    )
                    st.markdown("&nbsp;")

                st.markdown(f"**Order Total: ₦{order['grand_total']:,.2f}**")

        # Summary metrics
        st.markdown("---")
        total_orders = len(history)
        total_spent  = sum(o["grand_total"] for o in history)
        total_items  = sum(o["item_count"]  for o in history)

        m1, m2, m3 = st.columns(3)
        m1.metric("Orders This Session", total_orders)
        m2.metric("Items Ordered",        total_items)
        m3.metric("Total Spent",          f"₦{total_spent:,.2f}")


if __name__ == "__main__":
    main()
