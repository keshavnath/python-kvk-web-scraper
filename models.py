from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True)
    kvk_number = Column(String(8), unique=True)
    company_name = Column(String(255))
    street = Column(String(255))
    house_number = Column(String(10))
    postcode = Column(String(6))
    city = Column(String(255))
    is_main_establishment = Column(Boolean)
    establishment_number = Column(String(12))
    is_branch = Column(Boolean)

engine = create_engine('sqlite:///companies.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
