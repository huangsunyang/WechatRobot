import sqlite3

CREATE_TABLE_TEXT = "create table Message " \
                    "(id varchar(20) primary key, from_name varchar(20), time varchar(20))"


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("data.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('')

    def AddText(self, msg):
        self.cursor.execute()

    def __del__(self):
        self.conn.close()


if __name__ == '__main__':

    # cursor.execute('')

    cursor.execute('insert into TextMessage (id, name) values (\'1\', \'Michael1\')')
    cursor.execute('insert into TextMessage (id, name) values (\'2\', \'Michael2\')')
    cursor.execute('insert into TextMessage (id, name) values (\'3\', \'Michael3\')')

    cursor.close()
    conn.commit()
    conn.close()