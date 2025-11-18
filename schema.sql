-- Tabel untuk menyimpan data user
CREATE TABLE users (
   id INT AUTO_INCREMENT PRIMARY KEY,
   username VARCHAR(80) UNIQUE NOT NULL,
   password_hash VARCHAR(255) NOT NULL,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Tabel untuk menyimpan item-item wishlist
CREATE TABLE wishlist_items (
   id INT AUTO_INCREMENT PRIMARY KEY,
   user_id INT NOT NULL,
   item_name VARCHAR(255) NOT NULL,
   target_price DECIMAL(10, 2) NOT NULL,
   saved_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
   item_image_url VARCHAR(2048),
   store_link VARCHAR(2048),
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   -- Menambahkan foreign key untuk menghubungkan ke tabel users
   FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
