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

    reviews = relationship("Review", back_populates="restaurant")
    customers = relationship("Customer", secondary="reviews", back_populates="restaurants")

    def __repr__(self):
        return f'Restaurant: {self.name}'

    @classmethod
    def fanciest(cls, session):
        """Class method to return the restaurant instance with the highest price"""
        return session.query(cls).order_by(cls.price.desc()).first()

    def all_reviews(self):
        """Return a list of strings with all the reviews for this restaurant formatted as specified"""
        formatted_reviews = []
        for review in self.reviews:
            formatted_review = f'Review for {self.name} by {review.customer.full_name()}: {review.star_rating} stars.'
            formatted_reviews.append(formatted_review)
        return formatted_reviews



class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    rest_id = Column(Integer, ForeignKey('restaurants.id'))
    cust_id = Column(Integer, ForeignKey('customers.id'))
    review_text = Column(String())
    star_rating = Column(Integer)

    restaurant = relationship("Restaurant", back_populates="reviews")
    customer = relationship("Customer", back_populates="reviews")

    def __repr__(self):
        return f'Review for {self.restaurant.name} by {self.customer.first_name}'

    def full_review(self, session):
        """Returns a string formatted as 'Review for {restaurant name} by {customer's full name}: {review star_rating} stars'"""
        restaurant_name = self.restaurant.name
        customer_full_name = self.customer.full_name()
        star_rating = self.star_rating
        return f'Review for {restaurant_name} by {customer_full_name}: {star_rating} stars.'
