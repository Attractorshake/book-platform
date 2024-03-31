## API Documentation

- used a virtual python environment to build flask local web hosted app
- book_exchange_platform is the main directory for the flask app
-  Pros of Flask include lightweight framework that offers hassle-free development
    - Provide flexibility to the developer to experiment with their modules or architecture
    - Offers a built-in development server and fast debugger
    - Easily scalable for the applications
    - Support for secure cookies
    - Uses Ninja2 Template engine
    - integrated support for unit testing
    - APIs are coherent and neat
    - Provide strong WSGI support

### User Registration
- URL: `/register`
- Method: `POST`
- Description: Registers a new user.
- Request Body:
  - `username` (string, required): Username of the user.
  - `password` (string, required): Password of the user.
- Response:
  - `message`: Indicates whether the registration was successful.

### User Login
- URL: `/login`
- Method: `POST`
- Description: Logs in an existing user.
- Request Body:
  - `username` (string, required): Username of the user.
  - `password` (string, required): Password of the user.
- Response:
  - `token`: JWT token for authentication.

### User Profile
- URL: `/users/<user_id>`
- Method: `GET`, `PUT`
- Description: Retrieves or updates user profile.
- Request Body (PUT):
  - `username` (string): New username.
  - `email` (string): New email address.

### Book Listing
- URL: `/books`
- Method: `POST`, `GET`
- Description: Adds a new book or searches for books.
- Request Body (POST):
  - `title` (string, required): Title of the book.
  - `author` (string, required): Author of the book.
  - `owner_id` (integer, required): ID of the book owner.
- Query Parameters (GET):
  - `title` (string): Title of the book to search for.
  - `author` (string): Author of the book to search for.
  - `page` (integer): Page number for pagination (default: 1).
  - `per_page` (integer): Number of items per page (default: 10).
- Response (GET):
  - `books`: List of books matching the search criteria.
  - `total_pages`: Total number of pages for pagination.


### Exchange History
- URL: `/exchanges/history/<user_id>`
- Method: `GET`
- Description: Retrieves exchange history for a user.
- Path Parameters:
  - `user_id` (integer, required): ID of the user.
- Response:
  - List of exchange history entries, each containing:
    - `exchange_id`: ID of the exchange.
    - `book_title`: Title of the exchanged book.
    - `status`: Status of the exchange (requested, accepted, completed, etc.).

### Book Rating
- URL: `/books/<book_id>/rate`
- Method: `POST`
- Description: Rates and leaves a review for a book.
- Path Parameters:
  - `book_id` (integer, required): ID of the book.
- Request Body:
  - `user_id` (integer, required): ID of the user.
  - `rating` (integer, required): Rating for the book (1-5).
  - `comment` (string): Review comment.
- Response:
  - `message`: Indicates whether the rating was successful.


### Future Extensions and Milestones:

- Define a roadmap for future development and identify potential features to add. Set milestones for each feature along with estimated timelines for implementation.

## Future Extensions

### Mobile App Development
- Develop mobile apps for iOS and Android platforms to provide a seamless user experience on mobile devices.

### Social Sharing Integrations
- Integrate with social media platforms to allow users to share their exchange activities and recommendations with friends.

### Advanced Search Filters
- Implement advanced search filters such as genre, publication year, and language to enhance the book search functionality.

### Chat Integration
- Add chat functionality to facilitate communication between users during the exchange process.

## Milestones

### Milestone 1: User Authentication and Basic Functionality
- Implement user registration, login, and basic book listing functionality.
- Estimated Timeline: 2 weeks

### Milestone 2: Exchange Mechanism and Community Engagement
- Add endpoints for requesting and accepting exchanges.
- Implement features for users to leave ratings and reviews for exchanged books.
- Estimated Timeline: 3 weeks

### Milestone 3: User Profile and Advanced Features
- Implement user profile functionality including viewing and updating user details.
- Add pagination support for book listings and enhance security features.
- Estimated Timeline: 4 weeks
"# book-platform" 
"# book-platform" 
