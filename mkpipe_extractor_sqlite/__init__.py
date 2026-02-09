import os

from mkpipe.spark import JdbcExtractor


class SqliteExtractor(JdbcExtractor, variant='sqlite'):
    driver_name = 'sqlite'
    driver_jdbc = 'org.sqlite.JDBC'

    def build_jdbc_url(self):
        db_path = self.connection.extra.get('db_path', self.database or 'data.db')
        db_path = os.path.abspath(db_path)
        return f'jdbc:sqlite:{db_path}'
