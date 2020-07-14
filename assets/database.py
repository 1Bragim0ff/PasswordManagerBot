import sqlite3

class Database:
    conn = sqlite3.connect('data.sqlite', check_same_thread=False)
    cursor = conn.cursor()
    
    def create(self, user_id):
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {user_id} (
        url VARCHAR(32),
        login VARCHAR(32),
        password VARCHAR(32)
        )""")

        self.conn.commit()

    def add(self, user_id, url, login, password):
        if self.cursor.execute(f" SELECT url FROM {user_id} WHERE url = '{url}' \
        AND login = '{login}' AND password = '{password}' ").fetchone() is None:

            self.cursor.execute(f"INSERT INTO {user_id} VALUES (?,?,?)", (url, login, password))
            self.conn.commit()

    def get(self, user_id, url):
        try:
            return self.cursor.execute(f"SELECT * FROM {user_id} WHERE url = '{url}' ").fetchone()
        except sqlite3.OperationalError:
            return None

    def geta(self, user_id):
        try:
            return self.cursor.execute(f'SELECT * FROM {user_id}').fetchall()
        except sqlite3.OperationalError:
            return None
            
    def delete(self, user_id, url, login):
        if not self.cursor.execute(f" SELECT url FROM {user_id} WHERE url = '{url}' AND login = '{login}' ").fetchone() is None:
            self.cursor.execute(f"DELETE FROM {user_id} WHERE url = '{url}' AND login = '{login}' ")
            self.conn.commit()
            return 1

if __name__ == '__main__':
    db = Database()
    db.create('user0123456789')
    db.add('user0123456789', 'test.ru', 'testlogin', 'testpassword')
    info = db.get('user0123456789', 'test.ru')
    print(info)
    db.conn.close()