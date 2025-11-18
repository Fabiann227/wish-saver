import streamlit as st
from werkzeug.security import generate_password_hash, check_password_hash
import database as db

st.set_page_config(
    page_title="WishSaver",
    page_icon="🐷",
    layout="wide",
    initial_sidebar_state="auto"
)

def login_page():
    st.title("Selamat Datang di WishSaver 🐷")
    st.write("Silahkan login atau daftar untuk melanjutkan.")

    choice = st.selectbox("Pilih Aksi", ["Login", "Register"])

    if choice == "Login":
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

            if submitted:
                user = db.get_user_by_username(username)
                if user and check_password_hash(user['password_hash'], password):
                    st.session_state['logged_in'] = True
                    st.session_state['user_id'] = user['id']
                    st.session_state['username'] = user['username']
                    st.success("Login berhasil!")
                    st.rerun()
                else:
                    st.error("Username atau password salah.")

    elif choice == "Register":
        with st.form("register_form"):
            username = st.text_input("Username Baru")
            password = st.text_input("Password Baru", type="password")
            submitted = st.form_submit_button("Register")

            if submitted:
                if db.get_user_by_username(username):
                    st.warning("Username sudah digunakan.")
                else:
                    password_hash = generate_password_hash(password)
                    db.add_user(username, password_hash)
                    st.success("Registrasi berhasil! Silakan login.")

def main_dashboard():
    with st.sidebar:
        st.title(f"Halo, {st.session_state['username']}!")
        if st.button("Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        st.divider()

        with st.form("add_item_form", clear_on_submit=True):
            st.header("Tambah Wish Baru")
            item_name = st.text_input("Nama Barang", placeholder="iPhone 17 Pro")
            target_price = st.number_input("Target Harga (Rp)", min_value=0, step=1000)
            store_link = st.text_input("Link Toko (Opsional)", placeholder="https://tokopedia.com/...")
            item_image_url = st.text_input("URL Gambar (Opsional)", placeholder="https://gambar.com/iphone.jpg")
            submitted = st.form_submit_button("Tambah Wish")

            if submitted and item_name and target_price > 0:
                db.add_wishlist_item(st.session_state['user_id'], item_name, target_price, store_link, item_image_url)
                st.success(f"{item_name} berhasil ditambahkan!")

    st.title("Dashboard Wishlist Anda ✨")

    items = db.get_wishlist_items(st.session_state['user_id'])
    total_saved = sum(item['saved_amount'] for item in items)
    total_target = sum(item['target_price'] for item in items)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Tabungan", f"Rp {total_saved:,.0f}".replace(',', '.'))
    with col2:
        st.metric("Total Target", f"Rp {total_target:,.0f}".replace(',', '.'))
    
    st.divider()

    if not items:
        st.info("Wishlist Anda masih kosong! Tambahkan impian pertamamu melalui form di sidebar.")
    else:
        cols = st.columns(3) # Membuat 3 kolom
        for i, item in enumerate(items):
            with cols[i % 3]: # Menempatkan setiap item ke kolom secara bergiliran
                with st.container(border=True):
                    # Gambar
                    default_image = 'https://placehold.co/600x400/262730/FFFFFF?text=Wish'
                    st.image(item['item_image_url'] if item['item_image_url'] else default_image, use_container_width=True)
                    
                    # Detail
                    st.subheader(item['item_name'])
                    if item['store_link']:
                        st.markdown(f"[Lihat Produk]({item['store_link']}) ↗️")
                    
                    # Progress Bar
                    percentage = 0
                    if item['target_price'] > 0:
                        percentage = int((item['saved_amount'] / item['target_price']) * 100)
                    
                    st.progress(percentage / 100, text=f"{percentage}% Tercapai")
                    st.caption(f"Terkumpul Rp {item['saved_amount']:,.0f} dari Rp {item['target_price']:,.0f}".replace(',', '.'))

                    # Aksi
                    with st.expander("Kelola Item"):
                        # Tambah Tabungan
                        with st.form(f"save_form_{item['id']}", clear_on_submit=True):
                            amount_to_add = st.number_input("Tambah Tabungan", min_value=0, step=1000, key=f"add_{item['id']}")
                            if st.form_submit_button("Simpan"):
                                db.update_saved_amount(item['id'], amount_to_add, st.session_state['user_id'])
                                st.rerun()

                        # Hapus Item
                        if st.button("Hapus Item", key=f"delete_{item['id']}", use_container_width=True, type="primary"):
                            db.delete_wishlist_item(item['id'], st.session_state['user_id'])
                            st.rerun()


# --- Logika Utama Aplikasi ---

# Inisialisasi session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Router sederhana
if st.session_state['logged_in']:
    main_dashboard()
else:
    login_page()

