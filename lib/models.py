import os
import sys

sys.path.append(os.getcwd)

from sqlalchemy import (create_engine, PrimaryKeyConstraint, Column, String, Integer, ForeignKey, Table)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()
engine = create_engine('sqlite:///db/restaurants.db', echo=True)



# class Review(Base):
#     pass

association_table = Table('association', Base.metadata,
    Column('customer_id', Integer, ForeignKey('customers.id')),
    Column('review_id', Integer, ForeignKey('reviews.id'))
)

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String())
    last_name = Column(String())

    reviews = relationship("Review", secondary=association_table, back_populates="customers")
    restaurants = relationship("Restaurant", secondary="reviews", back_populates="customers")

    def __repr__(self):
        return f'Customer: {self.first_name} {self.last_name}'

    def reviews(self, session):
        """Returns a collection of all the reviews that the Customer has left"""
        return session.query(Review).join(association_table).filter(association_table.c.customer_id == self.id).all()

    def restaurants(self, session):
        """Returns a collection of all the restaurants that the Customer has reviewed"""
        return session.query(Restaurant).join(Review).join(association_table).filter(association_table.c.customer_id == self.id).distinct().all()

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    price = Column(Integer)

    customers = relationship("Customer", secondary=association_table, back_populates="restaurants")
    reviews = relationship("Review", back_populates="restaurant")

    def __repr__(self):
        return f'Restaurant: {self.name}'

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    rest_id = Column(Integer, ForeignKey('restaurants.id'))
    review_text = Column(String())
    star_rating = Column(Integer)

    restaurant = relationship("Restaurant", back_populates="reviews")
    customers = relationship("Customer", secondary=association_table, back_populates="reviews")

    def __repr__(self):
        return f'Review for {self.restaurant.name} by {", ".join([customer.first_name for customer in self.customers])}'