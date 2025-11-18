# 🐷 WishSaver: Aplikasi Pengelola Wishlist & Tabungan

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](link_deployment_streamlit_anda)

WishSaver adalah sebuah aplikasi web sederhana yang dirancang untuk membantu pengguna melacak tujuan pembelian mereka (*wishlist*) dan memantau kemajuan tabungan yang telah dikumpulkan.

Dibangun dengan Python (Streamlit) sebagai *frontend* dan MySQL sebagai *backend*, aplikasi ini merupakan contoh dari proyek full-stack ringan untuk manajemen keuangan pribadi.

---

## ✨ Fitur Utama

* **Autentikasi Pengguna:** Sistem Login dan Register yang aman (menggunakan `werkzeug.security`).
* **Wishlist CRUD:** Pengelolaan penuh (Tambah, Lihat, Hapus, Edit) item impian.
* **Pelacakan Tabungan:** Fungsionalitas untuk mencatat sejumlah uang yang disimpan ke item tertentu.
* **Visualisasi Progres:** Tampilan *progress bar* yang jelas menunjukkan persentase target harga yang sudah tercapai.
* **Metrik Ringkas:** Menampilkan total tabungan dan total target harga dari semua *wishlist*.

---

## 🛠️ Stack Teknologi

| Komponen | Teknologi | Tujuan |
| :--- | :--- | :--- |
| **Frontend/App** | Streamlit | Kerangka kerja Python untuk UI/UX interaktif. |
| **Backend/Logika** | Python 3.x | Logika aplikasi inti. |
| **Database** | MySQL | Penyimpanan data pengguna dan *wishlist*. |
| **Konektor DB** | `mysql.connector` | Menghubungkan Python dengan MySQL. |

---

## 🚀 Cara Menjalankan Proyek

### Prasyarat

1.  **Python 3.x** terinstal.
2.  **MySQL Server** terinstal dan berjalan (misalnya menggunakan XAMPP/WAMP/MAMP).
3.  Install library Python yang dibutuhkan:
    ```bash
    pip install streamlit mysql-connector-python werkzeug
    ```

### Langkah-langkah Setup

1.  **Setup Database (MySQL):**
    * Buat database baru bernama `wishsaver_db`.
    * Impor skema tabel dari file `schema.sql`:
        ```sql
        -- Jalankan konten dari file schema.sql di MySQL Client Anda
        CREATE TABLE users (...);
        CREATE TABLE wishlist_items (...);
        ```

2.  **Konfigurasi Koneksi:**
    * Buka file `database.py`.
    * Ubah detail di `DB_CONFIG` sesuai dengan kredensial MySQL lokal Anda:
        ```python
        DB_CONFIG = {
            'host': 'localhost',
            'user': 'root',
            'password': 'password_anda', # Sesuaikan!
            'database': 'wishsaver_db'
        }
        ```

3.  **Jalankan Aplikasi:**
    * Buka terminal di direktori proyek.
    * Jalankan aplikasi Streamlit:
        ```bash
        streamlit run main.py
        ```

Aplikasi akan terbuka secara otomatis di *browser* Anda (biasanya di `http://localhost:8501`).
