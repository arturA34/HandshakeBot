from src.database.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, BigInteger
from sqlalchemy import JSON


class Users(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=False)
    role = Column(String)
    region = Column(String)
    name = Column(String)

    __mapper_args__ = {
        'polymorphic_on': role,
        'polymorphic_identity': 'user'
    }


class Customers(Users):
    __tablename__ = 'customers'

    id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'customer'
    }


class Executors(Users):
    __tablename__ = 'executors'

    id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)

    # description = Column(String)
    categories = Column(JSON)
    rating = Column(Integer, default=None)

    __mapper_args__ = {
        'polymorphic_identity': 'executor'
    }


class Ads(Base):
    __tablename__ = 'ads'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    complete = Column(Boolean, default=False)
    customer_id = Column(BigInteger, ForeignKey("users.id"))
    executor_id = Column(BigInteger, ForeignKey("users.id"))
