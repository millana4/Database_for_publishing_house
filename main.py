import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Stock, Book, Publisher, Shop, Sale

login = 'postgres'
password = '***'
host = 'localhost'
port = '5432'
database = 'book_db'

DSN = f'postgresql://{login}:{password}@{host}:{port}/{database}'
engine = sqlalchemy.create_engine(DSN)
con = engine.connect()

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

pub_id = input('Введите ID издателя: ')

data = session.query(Book.title, Shop.name, Stock.count, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale).filter(Publisher.id == pub_id).all()
print(data)

session.close()
con.close()