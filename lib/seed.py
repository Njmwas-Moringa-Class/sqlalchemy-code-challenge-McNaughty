from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Customer, Restaurant, Review

def seed_database():
    try:
        engine = create_engine('sqlite:///db/restaurants.db')  
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Add seed data to the session
        session.add_all(seed_data)
        session.commit()

    except Exception as e:
        print(f"Error occurred: {e}")
        session.rollback()  # Rollback changes in case of error

    finally:
        session.close()  # Close the session

if __name__ == "__main__":
    seed_data = [
        Customer(first_name='John', last_name='Doe'),
        Customer(first_name='Jane', last_name='Smith'),
        Restaurant(name='Restaurant A', price=3),
        Restaurant(name='Restaurant B', price=2),
        Review(rest_id=1, cust_id=1, review_text='Good food', star_rating=5),
        Review(rest_id=2, cust_id=2, review_text='Average food', star_rating=3),
    ]

    seed_database()
