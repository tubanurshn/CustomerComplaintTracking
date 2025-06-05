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
        conn = mysql.connector.connect(**config)
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
        conn = mysql.connector.connect(**config)
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


def addComplaintToDatabase(ogrenci_id, student_number, status, compliment, privacy, answer, category):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        sql = (
            "INSERT INTO complaints (ogrenci_id,student_number, status, compliment, privacy, answer, category) "
            "VALUES (%s,%s, %s, %s, %s, %s, %s)"
        )
        vals = (ogrenci_id,student_number, status, compliment, privacy, answer, category)
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
        conn = mysql.connector.connect(**config)
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
        conn = mysql.connector.connect(**config)
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
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        query = """
            SELECT student_number, status, compliment, privacy, answer, category
            FROM complaints
            WHERE ogrenci_id = %s
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
        conn = mysql.connector.connect(**config)
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




def get_complaints_by_category_and_status(email, status="Process"):
    try:
        if email is None:
            print("Uyarı: E-mail None geldi!")
            return []

        conn = mysql.connector.connect(**config)

        cursor = conn.cursor()

        query_admin = "SELECT category FROM adminler WHERE email = %s"
        cursor.execute(query_admin, (email.strip(),))
        admin_category = cursor.fetchone()

        if not admin_category:
            print(f"E-mail '{email}' ile eşleşen admin kategorisi bulunamadı.")
            return []

        category = admin_category[0]

        query_complaints = """
            SELECT complaint_id,student_number, status, compliment, privacy, answer, category
            FROM complaints
            WHERE category = %s AND status = %s
        """
        cursor.execute(query_complaints, (category, status))
        results = cursor.fetchall()

        conn.close()
        return results

    except mysql.connector.Error as err:
        print("Veritabanı hatası:", err)
        return []



def get_user_id_by_email(email, role):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        if role == 'student':
            query = "SELECT id FROM ogrenciler WHERE eposta = %s"
        elif role == 'admin':
            query = "SELECT id FROM adminler WHERE email = %s"
        else:
            raise ValueError("Rol sadece 'student' veya 'admin' olabilir.")

        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            return result[0]  # sadece ID
        else:
            return None

    except mysql.connector.Error as err:
        print("Veritabanı hatası:", err)
        return None

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def isAdminExist(email):
    try:
        conn = mysql.connector.connect(**config)
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

def get_student_by_login(student_no, password):# bu ogrenciler tablosundaki idye erişmek için yazıldı
    try:
        conn = mysql.connector.connect(**config)
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

def update_complaint_answer_and_status(complaint_id, answer_text, new_status):
    try:
        connection = mysql.connector.connect(**config)

        cursor = connection.cursor()
        sql = "UPDATE complaints SET answer = %s, status = %s WHERE complaint_id = %s"
        cursor.execute(sql, (answer_text, new_status, complaint_id))
        connection.commit()
        return cursor.rowcount  # kaç satır güncellendi
    except mysql.connector.Error as err:
        print("Veritabanı hatası:", err)
        return -1
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



def get_all_complaints_by_category(email):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Adminin kategorisini bul
        cursor.execute("SELECT category FROM adminler WHERE email = %s", (email,))
        category_result = cursor.fetchone()

        if not category_result:
            return []

        category = category_result[0]

        # Kategoriye ait tüm şikayetleri çek
        sql = """
            SELECT student_number, status, compliment, privacy, answer, category
            FROM complaints
            WHERE category = %s
        """
        cursor.execute(sql, (category,))
        result = cursor.fetchall()
        return result

    except mysql.connector.Error as err:
        print("Veritabanı hatası:", err)
        return []

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
