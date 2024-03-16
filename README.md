# Instadogs

Welcome to InstaDogs, a web application where users can share pictures of their beloved dogs with the world! InstaDogs allows users to upload images, view their profiles, and interact with other users' posts.

## Features

User Authentication: InstaDogs implements user authentication to ensure secure access to user profiles. Users can log in using their username and password.

Dashboard: Upon logging in, users are directed to their dashboard, where they can view a feed of uploaded dog images from themselves and other users. The dashboard displays images in chronological order, allowing users to see the most recent posts first.

Profile: Users have their own profile page where they can view all the images they've uploaded. This page provides a personalized space for users to showcase their favorite dog photos.

Upload: InstaDogs enables users to upload images of their dogs directly from their devices. The application automatically adjusts the size and aspect ratio of the uploaded images to ensure they fit Instagram's requirements.

Image Classification: InstaDogs includes a machine learning model that can classify uploaded images to determine if they contain dogs. This feature helps maintain the theme of the application and ensures that only relevant content is shared.

## FILE STRUCTURE

- `main.py`: This file contains the main Flask application code, including routes for login, dashboard, profile, image upload, and logout. It also includes functions for image preprocessing and classification using a pre-trained model.

- `templates`: This directory contains HTML templates for different pages of the application, including index.html (login page), dashboard.html, and profile.html.

- `static`: This directory contains static files such as CSS stylesheets, JavaScript files, and image assets used by the application.

- `models`: This directory holds the pre-trained machine learning model for dog classification.

## SETUP INSTRUCTIONS

1. Clone the Repository: Clone the InstaDogs repository to your local machine.
   git clone <repository_url>

2. Install Dependencies: Navigate to the project directory and install the required dependencies using pip.
   pip install -r requirements.txt

3. Run the Application: Start the Flask application by running the main.py file.
   python main.py

4. Access the Application: Open a web browser and go to http://localhost:5000 to access InstaDogs. You can now log in, upload images, and explore dog pictures!

## Technologies Used

- Python: Flask web framework is used for backend development.
- HTML/CSS/JavaScript: Frontend interfaces and interactivity are implemented using these web technologies.
- TensorFlow/Keras: Deep learning model for dog image classification.
- PIL (Python Imaging Library): Image processing and manipulation.
- SQLite: Lightweight SQL database for user authentication and session management.

## CONTRIBUTORS

- Nuno Jeronimo: https://github.com/nunojeronimos
