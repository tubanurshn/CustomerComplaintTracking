import mysql.connector

config = {
    'user': 'root',
    'password': 'Bk.25122512',
    'host': 'localhost',
    'database': 'proje',
    'raise_on_warnings': True
}

try:
    conn = mysql.connector.connect(**config)
    if conn.is_connected():
        print("✅ ,Bağlantı başarılı.")

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
            host="localhost",
            user="root",
            password="Bk.25122512",
            database="proje"
        )
        cursor = conn.cursor()
        query = "SELECT * FROM ogrenciler WHERE student_number = %s AND password = %s"
        cursor.execute(query, (student_number, password))
        result = cursor.fetchone()
        return result is not None

    except mysql.connector.Error as err:
        print("Database error:", err)
        return False

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def addUserToDatabase(full_name, student_number, password, email):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Bk.25122512",
            database="proje"
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


def addComplaintToDatabase(student_number, status, compliment, privacy, answer, category):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Bk.25122512",
            database="proje"
        )
        cursor = conn.cursor()

        sql = (
            "INSERT INTO complaints (student_number, status, compliment, privacy, answer, category) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        vals = (student_number, status, compliment, privacy, answer, category)
        cursor.execute(sql, vals)
        conn.commit()
        print("✅ Şikayet kaydı başarılı.")
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
            password="Bk.25122512",
            database="proje"
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


def addAdminToDatabase(full_name, email, password, category):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Bk.25122512",
            database="proje"
        )
        cursor = conn.cursor()
        sql = "INSERT INTO adminler (full_name, email, password, category) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (full_name, email, password, category))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print("❌ Hata:", err)
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
# db_connection.py içinde
import mysql.connector

def get_complaints_by_student(student_number):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Bk.25122512",
            database="proje"
        )
        cursor = conn.cursor()
        query = """
            SELECT student_number, status, compliment, privacy, answer, category
            FROM complaints
            WHERE student_number = %s
        """
        cursor.execute(query, (student_number,))
        results = cursor.fetchall()
        conn.close()
        return results
    except mysql.connector.Error as err:
        print("Database error:", err)
        return []


def get_all_public_complaints():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Bk.25122512",
            database="proje"
        )
        cursor = conn.cursor()
        query = """
            SELECT student_number, status, compliment, privacy, answer, category
            FROM complaints
            WHERE privacy = 'public'
        """
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except mysql.connector.Error as err:
        print("Database error:", err)
        return []


def isAdminExist(email):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Bk.25122512",
            database="proje"
        )
        cursor = conn.cursor()
        sql = "SELECT * FROM adminler WHERE email = %s"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        return result is not None
    except mysql.connector.Error as err:
        print("❌ Hata:", err)
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
