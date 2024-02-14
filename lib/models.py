import os
import sys

from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///db/restaurants.db', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

association_table = Table('association', Base.metadata,
    Column('customer_id', Integer, ForeignKey('customers.id')),
    Column('review_id', Integer, ForeignKey('reviews.id'))
)

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


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String())
    last_name = Column(String())

    reviews = relationship("Review", secondary=association_table, back_populates="customer")
    restaurants = relationship("Restaurant", secondary="reviews", back_populates="customers")

    def __repr__(self):
        return f'Customer: {self.first_name} {self.last_name}'

    def full_name(self):
        """Returns the full name of the customer, with the first name and the last name concatenated."""
        return f"{self.first_name} {self.last_name}"

    def reviews(self):
        """Returns a collection of all the reviews that the Customer has left."""
        return self.reviews

    def restaurants(self):
        """Returns a collection of all the restaurants that the Customer has reviewed."""
        return [review.restaurant for review in self.reviews]

    def favorite_restaurant(self):
        """Returns the restaurant instance that has the highest star rating from this customer."""
        if not self.reviews:
            return None
        return max(self.reviews, key=lambda review: review.star_rating).restaurant

    def add_review(self, restaurant, rating):
        """Creates a new review for the restaurant with the given restaurant_id."""
        new_review = Review(restaurant=restaurant, customer=self, star_rating=rating)
        session.add(new_review)
        session.commit()

    def delete_reviews(self, restaurant):
        """Removes all reviews for the given restaurant."""
        reviews_to_delete = [review for review in self.reviews if review.restaurant == restaurant]
        for review in reviews_to_delete:
            session.delete(review)
        session.commit()



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
