from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import your models (Restaurant, Customer, Review) here
from your_module import Customer, Restaurant, Review

# Create an engine to connect to your database
engine = create_engine('sqlite:///example.db')

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Sample data to insert into the database
# Let's assume we have a few customers and restaurants and some reviews associated with them

# Insert some customers
customer1 = Customer(first_name='John', last_name='Doe')
customer2 = Customer(first_name='Jane', last_name='Smith')
session.add_all([customer1, customer2])
session.commit()

# Insert some restaurants
restaurant1 = Restaurant(name='Restaurant A', price=3)
restaurant2 = Restaurant(name='Restaurant B', price=2)
session.add_all([restaurant1, restaurant2])
session.commit()

# Insert some reviews
review1 = Review(rest_id=restaurant1.id, review_text='Good food', star_rating=5)
review2 = Review(rest_id=restaurant2.id, review_text='Average food', star_rating=3)
review1.customer = customer1
review2.customer = customer2
session.add_all([review1, review2])
session.commit()

# Now let's check the methods as requested

# Check if the restaurants method works for the first customer
first_customer = session.query(Customer).first()
print("Restaurants for the first customer:")
print(first_customer.restaurants)

# Check if the customer method works for the first review
first_review = session.query(Review).first()
print("\nCustomer for the first review:")
print(first_review.customer)

# Close the session
session.close()
