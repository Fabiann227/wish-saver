import mysql.connector
from mysql.connector import Error
import os

def get_db_connection():
    DB_CONFIG_EXTERNAL = {
        'host': os.getenv("DB_HOST"),
        'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASSWORD"),
        'database': os.getenv("DB_DATABASE"),
        'port': int(os.getenv("DB_PORT", 3306))
    }
    try:
        conn = mysql.connector.connect(**DB_CONFIG_EXTERNAL)
        return conn
    except Error as e:
        print(f"Error connecting to SingleStore/MySQL database: {e}")
        return None

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'wishsaver_db'
}

def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def add_user(username, password_hash):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
    cursor.execute(query, (username, password_hash))
    conn.commit()
    cursor.close()
    conn.close()

def get_wishlist_items(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM wishlist_items WHERE user_id = %s ORDER BY created_at DESC"
    cursor.execute(query, (user_id,))
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items

def add_wishlist_item(user_id, item_name, target_price, store_link, item_image_url):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO wishlist_items (user_id, item_name, target_price, store_link, item_image_url) 
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (user_id, item_name, target_price, store_link, item_image_url))
    conn.commit()
    cursor.close()
    conn.close()

def update_saved_amount(item_id, amount_to_add, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        UPDATE wishlist_items 
        SET saved_amount = saved_amount + %s 
        WHERE id = %s AND user_id = %s
    """
    cursor.execute(query, (amount_to_add, item_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    
def update_wishlist_item(item_id, item_name, target_price, store_link, item_image_url, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        UPDATE wishlist_items 
        SET item_name = %s, target_price = %s, store_link = %s, item_image_url = %s
        WHERE id = %s AND user_id = %s
    """
    cursor.execute(query, (item_name, target_price, store_link, item_image_url, item_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_wishlist_item(item_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM wishlist_items WHERE id = %s AND user_id = %s"
    cursor.execute(query, (item_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()