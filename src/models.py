from sqlalchemy import Column, Integer, String, Boolean

from database import Base


class Pokemon(Base):
    __tablename__ = "pokemon"

    id = Column(Integer, primary_key=True, index=True)
    dex = Column(Integer)
    name = Column(String)
    types = Column(String)
    released = Column(Boolean)