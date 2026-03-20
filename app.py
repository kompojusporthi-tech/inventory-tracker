import streamlit as st
import pandas as pd

if 'user_role' not in st.session_state:
    st.session_state.user_role = None
    st.session_state.user_email = None
    st.session_state.orders = []
    st.session_state.inventory = None
    st.session_state.notifications = []
    st.session_state.sales = []

st.title("🏭 **Warehouse Management System**")


# COMPLETE SAMPLE DATA - 26 grocery items with SKUs
SAMPLE_DATA = {
    'sku': ['BASM5K-001', 'WHFL10-002', 'SFOI1L-003', 'SUGR5K-004', 'MILK1K-005',
            'DALDG5-006', 'TEA225-007', 'COFF2G-008', 'SALT1K-009', 'CHIL100-010',
            'TURM100-011', 'CORR200-012', 'TOOR1K-013', 'CHAN1K-014', 'MOON500-015',
            'RBOL5L-016', 'MUST1L-017', 'PALM15-018', 'MAID5K-019', 'RAVA1K-020',
            'BESN1K-021', 'IDLI1K-022', 'SUJI500-023', 'OATS1K-024', 'MAGG12P-025', 'BING50P-026'],
    'item_name': [
        'Basmati Rice 5kg', 'Wheat Flour 10kg', 'Sunflower Oil 1L', 'Sugar 5kg', 'Milk Powder 1kg',
        'Dalda Ghee 500g', 'Tea Leaves 250g', 'Coffee Powder 200g', 'Salt 1kg', 'Chilli Powder 100g',
        'Turmeric Powder 100g', 'Coriander Powder 200g', 'Toor Dal 1kg', 'Chana Dal 1kg', 'Moong Dal 500g',
        'Rice Bran Oil 5L', 'Mustard Oil 1L', 'Palm Oil 15kg', 'Maida Flour 5kg', 'Rava 1kg',
        'Besan Flour 1kg', 'Idli Rava 1kg', 'Suji 500g', 'Oats 1kg', 'Maggi Noodles 12pk', 'Bingo Chips 50pk'
    ],
    'quantity': [150, 80, 200, 120, 60, 45, 120, 80, 300, 75, 90, 110, 95, 70, 40, 12, 180, 8, 65, 85, 55, 75, 60, 110, 24, 36],
    'reorder_level': [50, 30, 75, 40, 25, 20, 50, 30, 100, 30, 40, 50, 40, 30, 20, 5, 75, 3, 25, 40, 25, 30, 25, 50, 12, 15],
    'last_30_days_usage': [20, 15, 25, 18, 12, 8, 10, 7, 20, 12, 15, 14, 16, 12, 8, 2, 22, 3, 12, 14, 10, 13, 11, 16, 4, 6],
    'price': [1200, 650, 180, 380, 750, 950, 450, 720, 60, 280, 220, 190, 220, 180, 250, 1400, 280, 1850, 420, 140, 160, 150, 130, 420, 350, 280],
    'category': ['Grains', 'Grains', 'Oils', 'Sweeteners', 'Dairy', 'Fats', 'Beverages', 'Beverages', 'Spices', 'Spices', 'Spices', 'Spices', 'Pulses', 'Pulses', 'Pulses', 'Oils', 'Oils', 'Oils', 'Grains', 'Grains', 'Grains', 'Grains', 'Grains', 'Grains', 'Snacks', 'Snacks']
}

def load_inventory():
    if st.session_state.inventory is None:
        df = pd.DataFrame(SAMPLE_DATA)
        st.session_state.inventory = df
        st.session_state.inventory.to_csv('warehouse_data.csv', index=False)

# SIDE-BY-SIDE LOGIN (Owner LEFT, Customer RIGHT)
col1, col2 = st.columns(2)
st.markdown("---")

with col1:
    st.markdown("### 👑 **Owner Portal**")
    st.markdown("***Full warehouse control***")
    owner_email = st.text_input("**Owner Email**", placeholder="admin@warehouse.com")
    owner_pass = st.text_input("**Owner Password**", type="password")
    
    if st.button("**🚀 ENTER OWNER DASHBOARD**", use_container_width=True):
        if (owner_email == "admin@warehouse.com" and owner_pass == "admin2026") or \
           (owner_email == "owner@warehouse.com" and owner_pass == "owner2026"):
            st.session_state.user_role = "owner"
            st.session_state.user_email = owner_email
            load_inventory()
            st.success("✅ **Owner Dashboard Unlocked!**")
            st.rerun()
        else:
            st.error("❌ **Wrong credentials!**")

with col2:
    st.markdown("### 🛒 **Customer Portal**")
    st.markdown("***Place orders & view stock***")
    customer_email = st.text_input("**Your Email**", placeholder="john@gmail.com")
    customer_pass = st.text_input("**Password**", type="password")
    
    if st.button("**🛒 START SHOPPING**", use_container_width=True):
        if customer_pass == customer_email.split('@')[0]:  # Simple password = username before @
            st.session_state.user_role = "customer"
            st.session_state.user_email = customer_email
            load_inventory()
            st.success("✅ **Welcome Customer!**")
            st.rerun()
        else:
            st.error("❌ **Password = username before @!**")

# MAIN DASHBOARD - ALL 8 TABS
if st.session_state.user_role and st.session_state.inventory is not None:
    df = st.session_state.inventory.copy()
    df['days_left'] = (df['quantity'] / df['last_30_days_usage'] * 30).round(1)
    df['inventory_value'] = df['quantity'] * df['price']
    
    # SIDEBAR
    st.sidebar.success(f"👤 **{st.session_state.user_role.upper()}**")
    st.sidebar.info(f"📧 {st.session_state.user_email}")
    st.sidebar.markdown("### 🔔 **Notifications**")
    if st.session_state.notifications:
        for msg in st.session_state.notifications[-5:]:
            st.sidebar.warning(msg)
    
    # 8 PROFESSIONAL TABS
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📊 Dashboard", "🔍 Search", "🛒 Orders", "📦 Replenish", 
        "💰 Sales", "📱 Scanner", "💰 Value", "📈 Reports"
    ])
    
    with tab1:
        st.header("📊 **Dashboard**")
        low_stock = df[df['quantity'] < df['reorder_level']]
        if not low_stock.empty:
            st.error(f"🚨 **{len(low_stock)} LOW STOCK ITEMS!**")
            st.dataframe(low_stock[['sku', 'item_name', 'quantity', 'reorder_level']], use_container_width=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("⚠️ Critical (<7 days)", len(df[df['days_left'] < 7]))
        with col2:
            st.metric("🔴 Low Stock", len(low_stock))
        with col3:
            st.metric("🛒 Orders", len(st.session_state.orders))
        with col4:
            total_revenue = sum(sale.get('total', 0) for sale in st.session_state.sales)
            st.metric("💰 Revenue", f"₹{total_revenue:,.0f}")
        with col5:
            total_value = df['inventory_value'].sum()
            st.metric("🏭 Inventory Value", f"₹{total_value:,.0f}")
        
        st.markdown("**Days Left Chart:**")
        st.bar_chart(df.set_index('item_name')['days_left'])
    
    with tab2:
        st.header("🔍 **Smart Search**")
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search SKU/Name")
        with col2:
            min_stock = st.number_input("Min Stock", value=0)
        with col3:
            category = st.selectbox("Category", ["All"] + sorted(df['category'].unique().tolist()))
        
        filtered_df = df[
            (df['item_name'].str.contains(search_term, case=False, na=False) | 
             df['sku'].str.contains(search_term, case=False, na=False) if search_term else True) &
            (df['quantity'] >= min_stock) &
            (df['category'] == category if category != "All" else True)
        ]
        st.dataframe(filtered_df, use_container_width=True)
    
    with tab3:
        st.header("🛒 **Orders**")
        if st.session_state.user_role == "customer":
            st.info(f"👤 **{st.session_state.user_email}** - Place your order!")
            col1, col2 = st.columns(2)
            with col1:
                item = st.selectbox("Select Item", df['item_name'])
                item_sku = df[df['item_name'] == item]['sku'].iloc[0]
                item_price = df[df['item_name'] == item]['price'].iloc[0]
            with col2:
                qty = st.number_input("Quantity", min_value=1, max_value=100, value=1)
            
            st.info(f"🆔 **SKU: {item_sku} | ₹{item_price} | Total: ₹{item_price * qty:,.0f}")
            delivery_date = st.date_input("📅 Delivery Date")
            
            if st.button("🛒 **PLACE ORDER**", use_container_width=True, type="primary"):
                order = {
                    "id": len(st.session_state.orders) + 1,
                    "customer": st.session_state.user_email,
                    "sku": item_sku,
                    "item": item, "quantity": qty, 
                    "date": str(delivery_date),
                    "status": "Pending", "price": item_price
                }
                st.session_state.orders.append(order)
                st.session_state.notifications.append(f"✅ Order #{order['id']} placed by {st.session_state.user_email}")
                st.success("✅ **Order placed successfully!**")
                st.rerun()
        else:
            if st.session_state.orders:
                orders_df = pd.DataFrame(st.session_state.orders)
                st.dataframe(orders_df, use_container_width=True)
                
                order_id = st.selectbox("Select Order to Manage", orders_df['id'].tolist())
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ **APPROVE**", use_container_width=True):
                        for order in st.session_state.orders:
                            if order['id'] == order_id:
                                order['status'] = "Approved"
                                st.session_state.notifications.append(f"✅ Order #{order_id} approved!")
                        st.rerun()
                with col2:
                    if st.button("❌ **REJECT**", use_container_width=True):
                        for order in st.session_state.orders:
                            if order['id'] == order_id:
                                order['status'] = "Rejected"
                                st.session_state.notifications.append(f"❌ Order #{order_id} rejected!")
                        st.rerun()
            else:
                st.info("👑 **No orders yet. Wait for customers!**")
    
    with tab4:
        st.header("📦 **Auto-Replenish**")
        if st.session_state.user_role == "owner":
            critical_items = df[df['days_left'] < 7]
            if not critical_items.empty:
                st.warning(f"🚨 **{len(critical_items)} CRITICAL ITEMS!**")
                st.dataframe(critical_items[['sku', 'item_name', 'quantity', 'days_left']], use_container_width=True)
                
                if st.button("🤖 **AUTO-ORDER ALL CRITICAL**", use_container_width=True, type="primary"):
                    for idx, row in critical_items.iterrows():
                        order = {
                            "id": len(st.session_state.orders) + 1 + idx,
                            "customer": "AUTO-SYSTEM",
                            "sku": row['sku'],
                            "item": row['item_name'],
                            "quantity": 100,
                            "date": "2026-04-01",
                            "status": "Auto-Ordered"
                        }
                        st.session_state.orders.append(order)
                        st.session_state.notifications.append(f"🤖 Auto-ordered {row['sku']}")
                    st.success("✅ **All critical items auto-ordered!**")
                    st.rerun()
            else:
                st.success("✅ **All stock levels good!**")
    
    with tab5:
        st.header("💰 **Sales Dashboard**")
        if st.session_state.user_role == "owner":
            # Auto-convert approved orders to sales
            completed_orders = [o for o in st.session_state.orders if o['status'] == 'Approved']
            for order in completed_orders:
                if 'price' in order and order['id'] not in [s.get('order_id', 0) for s in st.session_state.sales]:
                    sale = {
                        'order_id': order['id'],
                        'customer': order['customer'],
                        'sku': order['sku'],
                        'item': order['item'],
                        'quantity': order['quantity'],
                        'price': order['price'],
                        'total': order['quantity'] * order['price'],
                        'date': order['date']
                    }
                    st.session_state.sales.append(sale)
            
            if st.session_state.sales:
                sales_df = pd.DataFrame(st.session_state.sales)
                st.dataframe(sales_df, use_container_width=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("📊 Total Sales", len(st.session_state.sales))
                with col2:
                    total_revenue = sales_df['total'].sum()
                    st.metric("💵 Total Revenue", f"₹{total_revenue:,.0f}")
                
                st.markdown("**Sales by Item:**")
                st.bar_chart(sales_df.set_index('item')['total'])
            else:
                st.info("👑 **No sales yet! Approve some orders.**")
    
    with tab6:
        st.header("📱 **Barcode Scanner**")
        barcode_input = st.text_input("📷 **Scan SKU or Type**", placeholder="BASM5K-001")
        
        if barcode_input:
            item_match = df[df['sku'] == barcode_input]
            if not item_match.empty:
                item_data = item_match.iloc[0]
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.success(f"✅ **{item_data['item_name']}**")
                with col2:
                    st.metric("📦 Stock", item_data['quantity'])
                with col3:
                    st.metric("💰 Price", f"₹{item_data['price']:,.0f}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("➕ **ADD 10**", use_container_width=True):
                        st.session_state.inventory.loc[st.session_state.inventory['sku'] == barcode_input, 'quantity'] += 10
                        st.session_state.notifications.append(f"📦 +10 {item_data['item_name']}")
                        st.success("✅ **Stock added!**")
                        st.rerun()
                with col2:
                    if st.button("➖ **REMOVE 1**", use_container_width=True):
                        if item_data['quantity'] > 0:
                            st.session_state.inventory.loc[st.session_state.inventory['sku'] == barcode_input, 'quantity'] -= 1
                            st.session_state.notifications.append(f"📦 -1 {item_data['item_name']}")
                            st.success("✅ **Stock removed!**")
                            st.rerun()
                        else:
                            st.warning("⚠️ **Out of stock!**")
            else:
                st.error("❌ **SKU not found!**")
    
    with tab7:
        st.header("💰 **Inventory Value**")
        value_df = df[['sku', 'item_name', 'quantity', 'price', 'inventory_value']].sort_values('inventory_value', ascending=False)
        st.dataframe(value_df, use_container_width=True)
        st.metric("🏭 **TOTAL INVENTORY VALUE**", f"₹{df['inventory_value'].sum():,.0f}")
        st.caption(f"📊 **{len(df)} items | ₹{df['price'].mean():.0f} avg price**")
    
    with tab8:
        st.header("📈 **Reports & Analytics**")
        st.markdown("**Stock Levels:**")
        st.line_chart(df.set_index('item_name')['quantity'])
        st.markdown("**Statistical Summary:**")
        st.dataframe(df.describe())
    
    # QUICK EDIT (Owner Only)
    if st.session_state.user_role == "owner":
        st.markdown("---")
        st.subheader("✏️ **Quick Stock Edit**")
        col1, col2 = st.columns(2)
        with col1:
            item_sku = st.selectbox("Select SKU", df['sku'])
        with col2:
            new_qty = st.number_input("New Quantity", min_value=0, value=10)
        
        if st.button("💾 **UPDATE STOCK**", use_container_width=True):
            st.session_state.inventory.loc[st.session_state.inventory['sku'] == item_sku, 'quantity'] = new_qty
            st.session_state.inventory.to_csv('warehouse_data.csv', index=False)
            item_name = df[df['sku'] == item_sku]['item_name'].iloc[0]
            st.session_state.notifications.append(f"📦 {item_name} updated to {new_qty}")
            st.success("✅ **Stock updated & saved!**")
            st.rerun()
    
    # DOWNLOAD REPORT
    st.markdown("---")
    st.download_button(
        "📥 **Download Full Report (CSV)**", 
        df.to_csv(index=False), 
        "hyderabad-warehouse-report.csv",
        "text/csv"
    )
    
    # LOGOUT
    st.markdown("---")
    if st.button("🚪 **LOGOUT**", use_container_width=True, type="secondary"):
        st.session_state.clear()
        st.rerun()

st.markdown("---")
st.caption("✅ **Customer Password = username before @ (john@gmail.com → john)**")