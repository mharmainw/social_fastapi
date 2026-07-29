from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:abc123**@localhost/posts'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()


#run raw sql using postgres lib 

# while(True):
#     try:
#         conn = psycopg2.connect(host = 'localhost',database = 'posts',user = 'postgres',password = 'abc123**',cursor_factory= RealDictCursor)
#         cursor = conn.cursor()
#         print("DB Connected")
#         break
#     except Exception as error: 
#         print("DB connection failed")
#         print("Error: ", error)
#         time.sleep(2)