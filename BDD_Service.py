import mysql.connector
import hashlib

def hash(query):
    hasher = hashlib.sha256()

    hasher.update(query.encode('utf-8'))

    hash_output = hasher.hexdigest()

    return hash_output

class DatabaseConnection:
    def __init__(self, host_name, user_name, user_password, db_name):
        self.connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        self.cursor = self.connection.cursor()

    def auth(self, username, password):
        try:
            hashPassword = hash(password)
            values= (username, hashPassword)
            self.cursor.execute("Select * from user where username=%s and password=%s", values)
            result = self.connection.fetchall()
            if len(result) == 1:
                return result[0]
            elif len(result) > 1 : 
                return False
            else:
                return False
        except Exception as e:
            print(f"The error '{e}' occurred")

    def close_connection(self):
        self.connection.close()
        print("Connection closed")

