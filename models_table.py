from datetime import datetime

from sqlalchemy import create_engine, Column, Float, DateTime, String, Integer
from sqlalchemy.ext.declarative import declarative_base

from config import DATABASE, USER, PASSWORD, HOST, TABLE_NAME


engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}/{DATABASE}")
Base = declarative_base()


class Expenses(Base):
    __tablename__ = TABLE_NAME
    id = Column(Integer, primary_key=True)
    rubles = Column(Float, nullable=False)
    dollars = Column(Float, nullable=False)
    date_time = Column(DateTime, default=datetime.now, nullable=False)
    waste_or_income = Column(String(15), nullable=False)
    description = Column(String(300), nullable=False)

    @property
    def serialize(self):
        return (
            self.id,
            self.rubles,
            self.dollars,
            self.date_time,
            self.waste_or_income,
            self.description,
        )


Base.metadata.create_all(engine)
