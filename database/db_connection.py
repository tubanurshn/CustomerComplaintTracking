import mysql.connector

config = {
    'user': 'root',
    'password': 'tuba3466',
    'host': 'localhost',
    'database': 'user_infos',
    'raise_on_warnings': True
}

try:
    conn = mysql.connector.connect(**config)
    if conn.is_connected():
        print("✅ Bağlantı başarılı.")

    cursor = conn.cursor()
    query = "SELECT id, full_name, student_number, password, eposta FROM ogrenciler"
    cursor.execute(query)

    rows = cursor.fetchall()
    if rows:
        for id_, full_name, student_number, password, eposta in rows:
            print(id_, full_name, student_number, password, eposta)
    else:
        print("ℹ️ Sorgu döndürmedi — tabloda kayıt olmayabilir.")

except mysql.connector.Error as err:
    print("❌ Hata:", err)

finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()


def check_student_login(student_number, password):
    try:
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "tuba3466",
            database = "user_infos"
        )
        cursor = conn.cursor()
        query = "SELECT * FROM ogrenciler WHERE student_number = %s AND password = %s"
        cursor.execute(query, (student_number, password))

        result = cursor.fetchone()
        return result is not None # Eğer kullanıcı varsa True, yoksa False

    except mysql.connector.Error as err:
        print("Database error:", err)
        return False

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


