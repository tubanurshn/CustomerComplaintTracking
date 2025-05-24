import mysql.connector

config = {
    'user': 'root',
    'password': 'Root23',
    'host': 'localhost',
    'database': 'user_infos',
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
            password="Root23",
            database="user_infos"
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
            password="Root23",
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


# def addComplaintToDatabase(student_number, status, compliment, privacy, answer, category):
#     try:
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="Root23",
#             database="user_infos"
#         )
#         cursor = conn.cursor()
#
#         sql = (
#             "INSERT INTO complaints (student_number, status, compliment, privacy, answer, category) "
#             "VALUES (%s, %s, %s, %s, %s, %s)"
#         )
#         vals = (student_number, status, compliment, privacy, answer, category)
#         cursor.execute(sql, vals)
#         conn.commit()
#         print("✅ Şikayet kaydı başarılı.")
#         return True
#
#     except mysql.connector.Error as err:
#         print("❌ Hata:", err)
#         return False
#
#     finally:
#         if conn.is_connected():
#             cursor.close()
#             conn.close()

def addComplaintToDatabase(ogrenci_id, student_number, status, compliment, privacy, answer, category):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Root23",
            database="user_infos"
        )
        cursor = conn.cursor()

        sql = (
            "INSERT INTO complaints (ogrenci_id, student_number, status, compliment, privacy, answer, category) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )
        vals = (ogrenci_id, student_number, status, compliment, privacy, answer, category)
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
            password="Root23",
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

def get_student_by_login(student_no, password):# bu ogrenciler tablosundaki idye erişmek için yazıldı
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Root23",
            database="user_infos"
        )
        cursor = conn.cursor()
        query = """
            SELECT id, student_number 
            FROM ogrenciler 
            WHERE student_number = %s AND password = %s
        """
        cursor.execute(query, (student_no, password))
        result = cursor.fetchone()
        #Eğer eşleşen bir öğrenci varsa, örneğin (id,stunum) gibi bir tuple döner. yoksa None döner
        return result
    except mysql.connector.Error as err:
        print("❌ Giriş hatası:", err)
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def addAdminToDatabase(full_name, email, password, category):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Root23",
            database="user_infos"
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

def get_complaints_by_student(ogrenci_id):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Root23",
            database="user_infos"
        )
        cursor = conn.cursor()
        query = """
            SELECT student_number, status, compliment, privacy, answer, category
            FROM complaints
            WHERE ogrenci_id = %s
        """
        cursor.execute(query, (ogrenci_id,))
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
            password="Root23",
            database="user_infos"
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
            password="Root23",
            database="user_infos"
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
