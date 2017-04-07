import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, Date

username = 'asmo'
word = 'allahakbar'
db_name = 'hh'


def connect(user=username, password=word,
            db=db_name, host='localhost', port=5432):
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)
    con = sqlalchemy.create_engine(url, client_encoding='utf8')
    print(url)
    meta = sqlalchemy.MetaData(bind=con, reflect=True)
    return meta, con


def add_column(con, table_name, col):
    column_name = col.compile(dialect=con.dialect)
    column_type = col.type.compile(con.dialect)
    con.execute('ALTER TABLE {} ADD COLUMN {} {}'.
                format(table_name, column_name, column_type))
metadata, connection = connect()

vacancy_fields = ['job_type', 'company_name',
                  'pub_date', 'vacancy_description',
                  'work_hours', 'address', 'key_skills',
                  ['salary', 'town', 'experience'],
                  ]


def create_table(meta, con):
    meta.create_all(con)


hh_vacancies = Table('vacancies', metadata,
                     Column('job_type', String(64)),
                     Column('company_name', String(64)),
                     Column('pub_date', Date),
                     Column('vacancy_description', String),
                     Column('work_hours', String),
                     Column('address', String(100)),
                     Column('key_skills', String),
                     Column('salary', String(32)),
                     Column('town', String(64)),
                     Column('experience', String(64)),
                     extend_existing=True)

column = Column('url', String())