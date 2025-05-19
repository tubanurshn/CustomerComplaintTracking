import mysql.connector

config = {
    'user': 'root',
    'password': 'tuba3466',
    'host': 'localhost',
    'database': 'user_infos',
    'raise_on_warnings': True
}

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='tuba3466',
        database='user_infos',
        raise_on_warnings=True
    )
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


# registerdan alınan verileri databaase yüklemek için
def addUserToDatabase(full_name, student_number, password, email):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="tuba3466",
            database="user_infos"
        )
        cursor = conn.cursor()

        sql = (
            "INSERT INTO ogrenciler (full_name, student_number, password, eposta) "
            "VALUES (%s, %s, %s, %s)"
        )
        vals = (full_name, student_number, password, email)
        cursor.execute(sql, vals)
        conn.commit()
        print("✅ Kayıt başarılı.")
        return True

    except mysql.connector.Error as err:
        print("❌ Hata:", err)
        return False

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()



def isUserExist(student_number, email):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="tuba3466",
            database="user_infos"
        )
        cursor = conn.cursor()

        sql = "SELECT * FROM ogrenciler WHERE student_number = %s OR eposta = %s"
        vals = (student_number, email)
        cursor.execute(sql, vals)
        result = cursor.fetchone()
        return result is not None

    except mysql.connector.Error as err:
        print("❌ Hata:", err)
        return False

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()