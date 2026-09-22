import streamlit as st
import random
import time
from datetime import datetime

# ----------------------------------------------------
# Menu Data & Pricing Configuration (all prices in ₦)
# ----------------------------------------------------
COFFEE_PRICES = {
    "Espresso":      1500,
    "Americano":     2000,
    "Cappuccino":    2500,
    "Café Latte":    3000,
    "Hot Chocolate": 2500,
}

COFFEE_ICONS = {
    "Espresso":      "☕",
    "Americano":     "☕",
    "Cappuccino":    "☕",
    "Café Latte":    "🥛",
    "Hot Chocolate": "🍫",
}

BAR_PRICES = {
    "Hero":         2500,
    "Desperado":    2500,
    "Smirnoff Ice": 2000,
    "Heineken":     3000,
    "Andrea":       30000,
}

BAR_ICONS = {
    "Hero":         "🍺",
    "Desperado":    "🍺",
    "Smirnoff Ice": "🍹",
    "Heineken":     "🍺",
    "Andrea":       "🍾",
}

SIZE_UPCHARGES = {
    "Small":  0,
    "Medium": 500,
    "Large":  1000,
}

MILK_UPCHARGES = {
    "Whole Milk":   0,
    "Oat Milk":     750,
    "Almond Milk":  750,
    "Soy Milk":     500,
}

EXTRA_PRICES = {
    "Extra Espresso Shot": 1000,
    "Whipped Cream":        500,
    "Caramel Drizzle":      500,
}

PASTRY_PRICES = {
    "None":                    0,
    "Butter Croissant":     3500,
    "Blueberry Muffin":     3000,
    "Chocolate Chip Cookie": 2500,
}

PASTRY_ICONS = {
    "None":                    "",
    "Butter Croissant":     "🥐",
    "Blueberry Muffin":     "🧁",
    "Chocolate Chip Cookie": "🍪",
}

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* hide default streamlit header/footer */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #2c1a0e 0%, #4a2c17 50%, #6b3a1f 100%);
    border-radius: 16px;
    padding: 48px 40px 36px;
    margin-bottom: 32px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}
.hero-badge {
    display: inline-block;
    background: rgba(212,163,115,0.2);
    color: #d4a373;
    border: 1px solid rgba(212,163,115,0.35);
    border-radius: 50px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 4px 14px;
    margin-bottom: 14px;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    color: #f5e6d3;
    margin: 0 0 8px;
    line-height: 1.15;
}
.hero p {
    color: #c4a882;
    font-size: 1rem;
    font-weight: 300;
    margin: 0;
    letter-spacing: 0.3px;
}

/* ── Section headings ── */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    font-weight: 600;
    color: #2c1a0e;
    margin: 24px 0 12px;
    padding-bottom: 6px;
    border-bottom: 2px solid #e8d5c0;
}

/* ── Menu toggle pills ── */
.menu-toggle {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

/* ── Drink cards ── */
.drink-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
    gap: 10px;
    margin-bottom: 16px;
}
.drink-card {
    background: #fdf8f3;
    border: 2px solid #e8d5c0;
    border-radius: 12px;
    padding: 14px 10px;
    text-align: center;
    cursor: pointer;
    transition: all 0.18s ease;
}
.drink-card:hover {
    border-color: #c17d3c;
    background: #fef3e8;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(193,125,60,0.15);
}
.drink-card.selected {
    border-color: #8b4513;
    background: #fef3e8;
    box-shadow: 0 0 0 3px rgba(139,69,19,0.12);
}
.drink-card .icon { font-size: 1.6rem; margin-bottom: 6px; }
.drink-card .name { font-size: 0.78rem; font-weight: 600; color: #3d2008; line-height: 1.3; }
.drink-card .price { font-size: 0.72rem; color: #8b5e3c; margin-top: 3px; }

/* ── Customisation panel ── */
.custom-panel {
    background: #fdf8f3;
    border: 1px solid #e8d5c0;
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 16px;
}

/* ── Price preview pill ── */
.price-pill {
    background: linear-gradient(90deg, #2c1a0e, #5a3010);
    color: #f5e6d3;
    border-radius: 50px;
    padding: 10px 20px;
    font-size: 0.95rem;
    font-weight: 600;
    text-align: center;
    margin: 12px 0;
    letter-spacing: 0.3px;
}

/* ── Cart panel ── */
.cart-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    font-weight: 600;
    color: #2c1a0e;
    padding-bottom: 8px;
    border-bottom: 2px solid #e8d5c0;
    margin-bottom: 14px;
}
.cart-empty {
    background: #fdf8f3;
    border: 1.5px dashed #d4b896;
    border-radius: 12px;
    padding: 28px 16px;
    text-align: center;
    color: #9e7a55;
    font-size: 0.88rem;
}
.cart-item {
    background: #fdf8f3;
    border: 1px solid #e8d5c0;
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 8px;
}
.cart-item-name {
    font-weight: 600;
    font-size: 0.9rem;
    color: #2c1a0e;
}
.cart-item-detail {
    font-size: 0.75rem;
    color: #9e7a55;
    margin-top: 2px;
}
.cart-item-price {
    font-size: 0.82rem;
    font-weight: 600;
    color: #5a3010;
    margin-top: 4px;
}
.cart-total {
    background: linear-gradient(90deg, #2c1a0e, #5a3010);
    color: #f5e6d3;
    border-radius: 10px;
    padding: 14px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 12px 0;
    font-weight: 600;
    font-size: 1rem;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    border-radius: 8px;
    transition: all 0.18s ease;
}

/* ── Receipt ── */
.receipt-wrap {
    background: #1a1008;
    border: 1px solid #3d2b18;
    border-radius: 16px;
    padding: 28px 32px;
    max-width: 500px;
    margin: 0 auto;
    font-family: 'Courier New', monospace;
    color: #f0e0c8;
}
.receipt-shop {
    text-align: center;
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    color: #d4a373;
    margin-bottom: 4px;
}
.receipt-tagline {
    text-align: center;
    font-size: 0.75rem;
    color: #7a5c3a;
    margin-bottom: 14px;
}
.receipt-divider { border-color: #3d2b18; margin: 10px 0; }
.receipt-meta {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    color: #7a5c3a;
    margin-bottom: 14px;
}
.receipt-item {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    font-weight: bold;
    margin-bottom: 2px;
}
.receipt-sub {
    font-size: 0.72rem;
    color: #7a5c3a;
    margin-left: 8px;
    margin-bottom: 8px;
}
.receipt-total {
    display: flex;
    justify-content: space-between;
    font-size: 1.05rem;
    font-weight: bold;
    color: #d4a373;
    margin-top: 4px;
}
.receipt-thanks {
    text-align: center;
    font-size: 0.75rem;
    color: #7a5c3a;
    margin-top: 14px;
}

/* ── History ── */
.history-empty {
    background: #fdf8f3;
    border: 1.5px dashed #d4b896;
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    color: #9e7a55;
    font-size: 0.88rem;
}
.metrics-row {
    background: linear-gradient(135deg, #2c1a0e, #5a3010);
    border-radius: 14px;
    padding: 20px 24px;
    color: #f5e6d3;
    margin-top: 16px;
}

/* ── Streamlit overrides ── */
div[data-testid="stRadio"] label {
    font-size: 0.88rem !important;
}
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label {
    font-weight: 500;
    color: #3d2008;
    font-size: 0.88rem;
}
</style>
"""


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def reset_order():
    st.session_state.cart = []
    st.session_state.last_receipt = None
    st.session_state.order_placed = False


def validate_order(drink, drink_price, quantity, cart):
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
    errors = []
    if not cart:
        errors.append("Your cart is empty. Add at least one item before placing an order.")
    if sum(i["item_total"] for i in cart) <= 0:
        errors.append("Order total must be greater than ₦0.")
    return errors


def calculate_order_total(drink_price, size, milk, selected_extras, pastry, quantity):
    size_cost   = SIZE_UPCHARGES.get(size, 0)
    milk_cost   = MILK_UPCHARGES.get(milk, 0)
    extras_cost = sum(EXTRA_PRICES.get(e, 0) for e in selected_extras)
    pastry_cost = PASTRY_PRICES.get(pastry, 0)
    unit_price  = drink_price + size_cost + milk_cost + extras_cost + pastry_cost
    return unit_price * quantity, unit_price


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="The Daily Grind — Coffee & Bar",
        page_icon="☕",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Inject CSS
    st.markdown(CSS, unsafe_allow_html=True)

    # Session state
    for key, default in [
        ("cart", []),
        ("order_placed", False),
        ("order_history", []),
        ("last_receipt", None),
        ("selected_drink", None),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">✦ Now Taking Live Orders ✦</div>
        <h1>☕ The Daily Grind</h1>
        <p>Coffee by Day &nbsp;·&nbsp; Cold Ones by Night &nbsp;·&nbsp; Lagos, NG</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Two-column layout ─────────────────────────────────────────────────────
    col1, col2 = st.columns([3, 2], gap="large")

    # ════════════════════════════════════════════════════════════════════
    # LEFT — Menu & customisation
    # ════════════════════════════════════════════════════════════════════
    with col1:

        # Menu toggle
        st.markdown('<div class="section-title">Choose Your Menu</div>', unsafe_allow_html=True)
        category = st.radio(
            "",
            options=["☕  Coffee", "🍺  Bar"],
            horizontal=True,
            label_visibility="collapsed",
            key="category",
        )
        is_coffee = category == "☕  Coffee"

        # ── Drink selection ───────────────────────────────────────────────
        st.markdown('<div class="section-title">Select Your Drink</div>', unsafe_allow_html=True)

        if is_coffee:
            prices = COFFEE_PRICES
            icons  = COFFEE_ICONS
        else:
            prices = BAR_PRICES
            icons  = BAR_ICONS

        drink_names = list(prices.keys())

        # Card grid via columns
        cols_per_row = 5
        rows = [drink_names[i:i+cols_per_row] for i in range(0, len(drink_names), cols_per_row)]

        if st.session_state.selected_drink not in drink_names:
            st.session_state.selected_drink = drink_names[0]

        for row in rows:
            row_cols = st.columns(len(row))
            for col, name in zip(row_cols, row):
                with col:
                    is_selected = st.session_state.selected_drink == name
                    border_color = "#8b4513" if is_selected else "#e8d5c0"
                    bg_color     = "#fef3e8" if is_selected else "#fdf8f3"
                    shadow       = "box-shadow: 0 0 0 3px rgba(139,69,19,0.15);" if is_selected else ""
                    st.markdown(f"""
                    <div style="
                        background:{bg_color};
                        border:2px solid {border_color};
                        border-radius:12px;
                        padding:14px 8px;
                        text-align:center;
                        {shadow}
                    ">
                        <div style="font-size:1.5rem">{icons[name]}</div>
                        <div style="font-size:0.78rem;font-weight:600;color:#3d2008;margin-top:4px;line-height:1.3">{name}</div>
                        <div style="font-size:0.7rem;color:#8b5e3c;margin-top:2px">₦{prices[name]:,}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Select", key=f"sel_{name}", use_container_width=True):
                        st.session_state.selected_drink = name
                        st.rerun()

        drink       = st.session_state.selected_drink
        drink_price = prices[drink]

        # ── Customisation ─────────────────────────────────────────────────
        if is_coffee:
            st.markdown('<div class="section-title">Customise Your Order</div>', unsafe_allow_html=True)
            with st.container():
                c_size, c_milk = st.columns(2)
                with c_size:
                    size = st.radio(
                        "Size",
                        options=list(SIZE_UPCHARGES.keys()),
                        key="coffee_size",
                        help="Medium +₦500 · Large +₦1,000",
                    )
                with c_milk:
                    milk = st.selectbox(
                        "Milk",
                        options=list(MILK_UPCHARGES.keys()),
                        key="coffee_milk",
                    )

            st.markdown("**Extras**")
            extra_cols = st.columns(len(EXTRA_PRICES))
            selected_extras = []
            for ec, (extra, price) in zip(extra_cols, EXTRA_PRICES.items()):
                with ec:
                    if st.checkbox(f"{extra}\n+₦{price:,}", key=f"extra_{extra}"):
                        selected_extras.append(extra)
        else:
            size           = None
            milk           = None
            selected_extras = []
            st.markdown(
                '<p style="color:#9e7a55;font-size:0.85rem;margin-top:8px">'
                '🧊 Served chilled straight from the fridge. No customisation needed.</p>',
                unsafe_allow_html=True,
            )

        # ── Pastries ──────────────────────────────────────────────────────
        st.markdown('<div class="section-title">Add a Pastry</div>', unsafe_allow_html=True)
        pastry_names = list(PASTRY_PRICES.keys())
        pastry_cols  = st.columns(len(pastry_names))
        for pc, name in zip(pastry_cols, pastry_names):
            with pc:
                icon = PASTRY_ICONS[name]
                price_str = f"₦{PASTRY_PRICES[name]:,}" if PASTRY_PRICES[name] else "Free"
                st.markdown(f"""
                <div style="
                    background:#fdf8f3;border:1px solid #e8d5c0;border-radius:10px;
                    padding:10px 6px;text-align:center;
                ">
                    <div style="font-size:1.3rem">{icon if icon else "✕"}</div>
                    <div style="font-size:0.72rem;font-weight:600;color:#3d2008;margin-top:3px;line-height:1.3">{name}</div>
                    <div style="font-size:0.68rem;color:#8b5e3c">{price_str}</div>
                </div>
                """, unsafe_allow_html=True)

        pastry = st.selectbox(
            "Choose pastry",
            options=pastry_names,
            key="pastry",
            label_visibility="collapsed",
        )

        # ── Quantity & price preview ───────────────────────────────────────
        st.markdown('<div class="section-title">Quantity</div>', unsafe_allow_html=True)
        quantity = st.number_input(
            "",
            min_value=1, max_value=10, value=1, step=1,
            key="quantity",
            label_visibility="collapsed",
        )

        preview_total, preview_unit = calculate_order_total(
            drink_price, size, milk, selected_extras, pastry, quantity
        )

        drink_icon  = icons.get(drink, "🍹")
        size_label  = f" · {size}" if size else ""
        pill_html = (
            f'<div class="price-pill">'
            f'{drink_icon} {drink}{size_label}'
            f' &nbsp;|&nbsp; '
            f'&#8358;{preview_unit:,.0f} &times; {quantity}'
            f' &nbsp;= &nbsp;'
            f'<span style="font-size:1.15rem;font-weight:700">'
            f'&#8358;{preview_total:,.0f}'
            f'</span></div>'
        )
        st.markdown(pill_html, unsafe_allow_html=True)

        # ── Add to cart ───────────────────────────────────────────────────
        if st.button("🛒  Add to Cart", use_container_width=True, type="primary"):
            errors = validate_order(drink, drink_price, quantity, st.session_state.cart)
            if errors:
                for err in errors:
                    st.error(f"⚠️ {err}")
            else:
                st.session_state.cart.append({
                    "drink":      drink,
                    "category":   "coffee" if is_coffee else "bar",
                    "icon":       icons.get(drink, "🍹"),
                    "size":       size,
                    "milk":       milk,
                    "extras":     list(selected_extras),
                    "pastry":     pastry,
                    "quantity":   quantity,
                    "unit_price": preview_unit,
                    "item_total": preview_total,
                })
                st.session_state.order_placed = False
                st.toast(f"✅ {drink} added to your cart!")

    # ════════════════════════════════════════════════════════════════════
    # RIGHT — Cart
    # ════════════════════════════════════════════════════════════════════
    with col2:
        cart_count = len(st.session_state.cart)
        st.markdown(
            f'<div class="cart-header">🛒 Your Cart'
            f'{"" if cart_count == 0 else f" &nbsp;<span style=\'background:#8b4513;color:#fff;border-radius:50px;padding:1px 9px;font-size:0.75rem\'>{cart_count}</span>"}'
            f'</div>',
            unsafe_allow_html=True,
        )

        cart = st.session_state.cart

        if not cart:
            st.markdown("""
            <div class="cart-empty">
                <div style="font-size:2rem;margin-bottom:8px">🛒</div>
                <div style="font-weight:600;color:#5a3010;margin-bottom:4px">Your cart is empty</div>
                <div>Pick something from the menu and add it here.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            cart_grand_total = 0
            for idx, item in enumerate(cart):
                label = item["drink"]
                if item["size"]:
                    label += f" · {item['size']}"

                details = []
                if item["milk"]:
                    details.append(item["milk"])
                if item["extras"]:
                    details.extend(item["extras"])
                if item["pastry"] != "None":
                    details.append(item["pastry"])

                st.markdown(f"""
                <div class="cart-item">
                    <div class="cart-item-name">{item.get('icon','🍹')} {label}</div>
                    {f'<div class="cart-item-detail">{" · ".join(details)}</div>' if details else ''}
                    <div class="cart-item-price">
                        Qty {item['quantity']} × ₦{item['unit_price']:,.0f}
                        &nbsp;=&nbsp; ₦{item['item_total']:,.0f}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button("✕ Remove", key=f"remove_{idx}", use_container_width=True):
                    st.session_state.cart.pop(idx)
                    st.rerun()

                cart_grand_total += item["item_total"]

            st.markdown(f"""
            <div class="cart-total">
                <span>Grand Total</span>
                <span>₦{cart_grand_total:,.0f}</span>
            </div>
            """, unsafe_allow_html=True)

            btn_place, btn_clear = st.columns(2)
            with btn_place:
                place_order = st.button("🚀  Place Order", use_container_width=True, type="primary")
            with btn_clear:
                if st.button("🗑  Clear Cart", use_container_width=True):
                    st.session_state.cart = []
                    st.session_state.order_placed = False
                    st.rerun()

            # ── Order processing ───────────────────────────────────────────
            if place_order:
                errs = validate_cart(cart)
                if errs:
                    for e in errs:
                        st.error(f"⚠️ {e}")
                else:
                    has_coffee = any(i["category"] == "coffee" for i in cart)
                    has_bar    = any(i["category"] == "bar"    for i in cart)
                    has_pastry = any(i["pastry"]   != "None"   for i in cart)

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
                        f"**{len(cart)} item(s)** · Total: ₦{cart_grand_total:,.0f}\n\n"
                        f"Please collect at the counter in 5 minutes."
                    )
                    receipt = {
                        "order_num":  order_num,
                        "timestamp":  datetime.now().strftime("%d %b %Y, %I:%M %p"),
                        "items":      list(cart),
                        "grand_total": cart_grand_total,
                        "item_count": len(cart),
                    }
                    st.session_state.order_history.append(receipt)
                    st.session_state.last_receipt = receipt
                    st.session_state.cart         = []
                    st.session_state.order_placed = True

            if st.session_state.order_placed:
                st.markdown("&nbsp;")
                if st.button("🆕  Start New Order", use_container_width=True, type="primary", key="new_order_cart"):
                    reset_order()
                    st.rerun()

    # ── Receipt ───────────────────────────────────────────────────────────────
    receipt = st.session_state.last_receipt
    if receipt:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title" style="text-align:center">🧾 Your Receipt</div>', unsafe_allow_html=True)

        lines = ""
        for item in receipt["items"]:
            label = item["drink"]
            if item["size"]:
                label += f" ({item['size']})"
            sub = []
            if item["milk"]:    sub.append(item["milk"])
            if item["extras"]:  sub.extend(item["extras"])
            if item["pastry"] != "None": sub.append(item["pastry"])
            lines += f"""
            <div class="receipt-item">
                <span>{item.get('icon','')}&nbsp;{label}</span>
                <span>₦{item['item_total']:,.0f}</span>
            </div>
            <div class="receipt-sub">
                {(" · ".join(sub) + " &nbsp;·&nbsp; ") if sub else ""}
                Qty {item['quantity']} × ₦{item['unit_price']:,.0f}
            </div>
            """

        st.markdown(f"""
        <div class="receipt-wrap">
            <div class="receipt-shop">☕ The Daily Grind</div>
            <div class="receipt-tagline">Coffee by Day, Cold Ones by Night</div>
            <hr class="receipt-divider"/>
            <div class="receipt-meta">
                <span>Order #{receipt['order_num']}</span>
                <span>{receipt['timestamp']}</span>
            </div>
            <hr class="receipt-divider"/>
            {lines}
            <hr class="receipt-divider"/>
            <div class="receipt-total">
                <span>TOTAL</span>
                <span>₦{receipt['grand_total']:,.0f}</span>
            </div>
            <div class="receipt-thanks">Thank you for your order!<br/>Please collect at the counter.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("&nbsp;")
        rc1, rc2, rc3 = st.columns([1, 1, 1])
        with rc2:
            if st.button("✕  Dismiss Receipt", use_container_width=True):
                st.session_state.last_receipt = None
                st.rerun()
        with rc3:
            if st.button("🆕  Start New Order", use_container_width=True, type="primary", key="new_order_receipt"):
                reset_order()
                st.rerun()

    # ── Order History ─────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 Order History</div>', unsafe_allow_html=True)

    history = st.session_state.order_history

    if not history:
        st.markdown("""
        <div class="history-empty">
            <div style="font-size:1.5rem;margin-bottom:6px">📋</div>
            <div style="font-weight:600;color:#5a3010;margin-bottom:4px">No orders yet</div>
            <div>Completed orders will appear here.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for order in reversed(history):
            with st.expander(
                f"Order #{order['order_num']}  ·  {order['timestamp']}  ·  "
                f"{order['item_count']} item(s)  ·  ₦{order['grand_total']:,.0f}",
                expanded=False,
            ):
                for item in order["items"]:
                    label = item["drink"]
                    if item["size"]:
                        label += f" · {item['size']}"
                    st.markdown(f"**{item.get('icon','🍹')} {label}**")
                    details = []
                    if item["milk"]:   details.append(f"Milk: {item['milk']}")
                    if item["extras"]: details.append(f"Extras: {', '.join(item['extras'])}")
                    if item["pastry"] != "None": details.append(f"Pastry: {item['pastry']}")
                    if details:
                        st.caption("  ·  ".join(details))
                    st.caption(f"Qty {item['quantity']} × ₦{item['unit_price']:,.0f} = ₦{item['item_total']:,.0f}")
                    st.markdown("&nbsp;")
                st.markdown(f"**Order Total: ₦{order['grand_total']:,.0f}**")

        total_orders = len(history)
        total_spent  = sum(o["grand_total"] for o in history)
        total_items  = sum(o["item_count"]  for o in history)

        m1, m2, m3 = st.columns(3)
        m1.metric("Orders This Session", total_orders)
        m2.metric("Items Ordered",       total_items)
        m3.metric("Total Spent",         f"₦{total_spent:,.0f}")

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="
        text-align:center;
        padding: 20px;
        border-top: 1px solid #e8d5c0;
        color: #9e7a55;
        font-size: 0.8rem;
    ">
        ☕ The Daily Grind &nbsp;·&nbsp; Lagos, NG &nbsp;·&nbsp;
        Built with Streamlit &nbsp;·&nbsp; © 2026
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
