import psycopg2

class Database(object):

    def __init__(self, database, host, user, password):
        self._conn = None
        if database:
            self._connect(database, host, user, password)

    def _connect(self, db_name, db_host, db_user, db_password):
        self._conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host)
        self._conn.autocommit = True

    def _cursor(self):
        return self._conn.cursor()



if __name__ == '__main__':
    pass

