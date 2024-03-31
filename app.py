# app.py

from flask import Flask, request, jsonify, render_template
from models import db, User, Book, Exchange
from models import Review, Wishlist
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta

#user authentication using JWT (JSON Web Tokens) in Flask. This involves creating endpoints for user registration, login, logout, and password reset.

#app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book_exchange.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)


# Route to serve the HTML template
@app.route('/')
def index():
    return render_template('index.html')

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 409
    
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    token = jwt.encode({'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)}, app.config['SECRET_KEY'])
    return jsonify({'token': token.decode('UTF-8')}), 200

if __name__ == '__main__':
    app.run(debug=True)

#endpoints for users to list their books for exchange and search for books based on various criteria.
    
# Book Listing
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    title = data.get('title')
    author = data.get('author')
    owner_id = data.get('owner_id')
    if not title or not author or not owner_id:
        return jsonify({'message': 'Title, author, and owner ID are required'}), 400
    
    new_book = Book(title=title, author=author, owner_id=owner_id)
    db.session.add(new_book)
    db.session.commit()
    
    return jsonify({'message': 'Book added successfully'}), 201



# Book Search
#Adding Pagination to Book Listings:
#To handle large numbers of books, we'll add pagination support to the book listing endpoint.

@app.route('/books', methods=['GET'])
def search_books():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    title = request.args.get('title')
    author = request.args.get('author')
    if not title and not author:
        return jsonify({'message': 'At least one search parameter is required (title or author)'}), 400
    
    books = Book.query
    if title:
        books = books.filter_by(title=title)
    if author:
        books = books.filter_by(author=author)
    
    paginated_books = books.paginate(page=page, per_page=per_page)
    result = [{'id': book.id, 'title': book.title, 'author': book.author} for book in paginated_books.items]
    return jsonify({'books': result, 'total_pages': paginated_books.pages}), 200


# Exchange Mechanism
@app.route('/exchanges/request', methods=['POST'])
def request_exchange():
    data = request.json
    requester_id = data.get('requester_id')
    accepter_id = data.get('accepter_id')
    book_id = data.get('book_id')
    if not requester_id or not book_id:
        return jsonify({'message': 'Requester ID and book ID are required'}), 400
    
    exchange = Exchange(requester_id=requester_id, accepter_id=accepter_id, book_id=book_id)
    db.session.add(exchange)
    db.session.commit()
    
    return jsonify({'message': 'Exchange requested successfully'}), 201

 #endpoints for requesting and accepting exchanges, and handle the updating of book ownership and exchange status in the database.

@app.route('/exchanges/accept', methods=['POST'])
def accept_exchange():
    data = request.json
    exchange_id = data.get('exchange_id')
    if not exchange_id:
        return jsonify({'message': 'Exchange ID is required'}), 400
    
    exchange = Exchange.query.get(exchange_id)
    if not exchange:
        return jsonify({'message': 'Exchange not found'}), 404
    
    exchange.accepter_id = exchange.requester_id
    exchange.status = 'accepted'
    db.session.commit()
    
    return jsonify({'message': 'Exchange accepted successfully'}), 200

#Implementing Book Exchange History:
# endpoints for users to view their exchange history, including past and ongoing exchanges.


@app.route('/exchanges/history/<int:user_id>', methods=['GET'])
def get_exchange_history(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    exchanges = Exchange.query.filter((Exchange.requester_id == user_id) | (Exchange.accepter_id == user_id))
    exchange_history = [{
        'exchange_id': exchange.id,
        'book_title': exchange.book.title,
        'status': exchange.status
    } for exchange in exchanges]
    
    return jsonify(exchange_history), 200



# Community Engagement
#features for users to leave reviews and ratings for exchanged books.

@app.route('/books/<int:book_id>/reviews', methods=['POST'])
def add_review(book_id):
    data = request.json
    user_id = data.get('user_id')
    rating = data.get('rating')
    comment = data.get('comment')
    if not user_id or not rating:
        return jsonify({'message': 'User ID and rating are required'}), 400
    
    # Save review to the database
    # Implement your logic here
    
    return jsonify({'message': 'Review added successfully'}), 201

#Implementing Book Rating and Reviews:
#Users can rate and leave reviews for books they've exchanged.  add endpoints to handle this functionality.

@app.route('/books/<int:book_id>/rate', methods=['POST'])
def rate_book(book_id):
    data = request.json
    user_id = data.get('user_id')
    rating = data.get('rating')
    comment = data.get('comment')
    if not user_id or not rating:
        return jsonify({'message': 'User ID and rating are required'}), 400
    
    # Save rating and review to the database
    # Assuming there's a Review model with book_id, user_id, rating, and comment fields
    new_review = Review(book_id=book_id, user_id=user_id, rating=rating, comment=comment)
    db.session.add(new_review)
    db.session.commit()
    
    return jsonify({'message': 'Book rated successfully'}), 201


#Implementing User Profile:
# add endpoints for users to view and update their profiles, including details such as name, email, and profile picture.


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    profile_data = {
        'username': user.username,
        'email': user.email,  # Assuming 'email' is a field in the User model
        # Add other profile details as needed
    }
    return jsonify(profile_data), 200

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    data = request.json
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    # Update other profile details as needed
    db.session.commit()
    
    return jsonify({'message': 'User profile updated successfully'}), 200




#Adding Email Notifications:
#Implementing email notifications to notify users about exchange requests, acceptances, and other important updates.

from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'

mail = Mail(app)

def send_email(subject, recipients, body):
    msg = Message(subject, recipients=recipients)
    msg.body = body
    mail.send(msg)







#Implementing Book Wishlist:
# endpoints for users to create and manage their book wishlists, allowing them to keep track of books they're interested in exchanging for.

@app.route('/wishlist', methods=['POST'])
def add_to_wishlist():
    data = request.json
    user_id = data.get('user_id')
    book_id = data.get('book_id')
    if not user_id or not book_id:
        return jsonify({'message': 'User ID and book ID are required'}), 400
    
    # Add book to user's wishlist in the database
    # Assuming there's a Wishlist model with user_id and book_id fields
    new_wishlist_item = Wishlist(user_id=user_id, book_id=book_id)
    db.session.add(new_wishlist_item)
    db.session.commit()
    
    return jsonify({'message': 'Book added to wishlist successfully'}), 201

@app.route('/wishlist/<int:user_id>', methods=['GET'])
def get_wishlist(user_id):
    # Retrieve user's wishlist from the database
    wishlist_items = Wishlist.query.filter_by(user_id=user_id).all()
    wishlist_data = [{'book_id': item.book_id} for item in wishlist_items]
    
    return jsonify(wishlist_data), 200



# Implementing Book Recommendation System:
#Introduce a recommendation system to suggest books to users based on their reading history, preferences, and community ratings.

# Import necessary libraries
from collections import defaultdict
from sqlalchemy import func

# Define a function to calculate book recommendations for a user
def get_recommendations(user_id):
    # Get the list of books already read by the user
    user_read_books = [exchange.book_id for exchange in Exchange.query.filter_by(requester_id=user_id).all()]

    # Calculate the average rating for each book in the system
    average_ratings = defaultdict(int)
    total_ratings = defaultdict(int)
    for review in Review.query.all():
        average_ratings[review.book_id] += review.rating
        total_ratings[review.book_id] += 1

    for book_id in average_ratings:
        average_ratings[book_id] /= total_ratings[book_id]

    # Find users with similar reading preferences
    similar_users = []
    for exchange in Exchange.query.filter(Exchange.requester_id != user_id).all():
        if exchange.book_id in user_read_books:
            similar_users.append(exchange.requester_id)

    # Get the books read by similar users and calculate their ratings
    similar_books_ratings = defaultdict(list)
    for similar_user in similar_users:
        similar_user_read_books = [exchange.book_id for exchange in Exchange.query.filter_by(requester_id=similar_user).all()]
        for book_id in similar_user_read_books:
            if book_id not in user_read_books:
                similar_books_ratings[book_id].append(average_ratings[book_id])

    # Calculate the average rating of each book by similar users
    similar_books_average_ratings = {}
    for book_id in similar_books_ratings:
        similar_books_average_ratings[book_id] = sum(similar_books_ratings[book_id]) / len(similar_books_ratings[book_id])

    # Sort the books by their average ratings
    recommended_books = sorted(similar_books_average_ratings.items(), key=lambda x: x[1], reverse=True)

    # Return the recommended books
    return recommended_books


@app.route('/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    # Implement recommendation logic based on user's preferences and history
    # Return a list of recommended books
    recommended_books = get_recommendations(user_id)
    return jsonify(recommended_books[:10]), 200  # Return top 10 recommended books



#Enhancing Security:
#Implementing rate limiting to prevent abuse and adding input validation to endpoints to mitigate against potential security risks.

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address)

# Rate limiting
@app.route('/api/endpoint', methods=['POST'])
@limiter.limit("5 per minute")

def some_endpoint():
    # Endpoint implementation
    # Check if request data is valid JSON
    try:
        data = request.json
    except ValueError:
        return jsonify({'error': 'Invalid JSON'}), 400

    # Ensure required fields are present
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400

    # Validate username and password
    username = data['username']
    password = data['password']

    # Implement your authentication logic here (e.g., check against database)
    if username == 'admin' and password == 'password':
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


# Input validation
from cerberus import Validator

book_schema = {
    'title': {'type': 'string', 'required': True},
    'author': {'type': 'string', 'required': True},
    'owner_id': {'type': 'integer', 'required': True}
}

@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    validator = Validator(book_schema)
    if not validator.validate(data):
        return jsonify({'message': 'Invalid input data', 'errors': validator.errors}), 400
 


#Adding Error Handling:
#Implementing error handling to provide meaningful responses for various error scenarios.
    

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'message': 'Resource not found', 'error': str(error)}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'message': 'Internal server error', 'error': str(error)}), 500



if __name__ == '__main__':
    app.run(debug=True)