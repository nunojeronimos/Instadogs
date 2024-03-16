import tensorflow as tf
from PIL import Image
import os
import numpy as np
from PIL import Image

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from keras.models import load_model
from datetime import datetime


app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'

dog_model = load_model(os.path.join('models','dogidentifier.h5'))

# Hardcoded username and password
valid_username = 'username'
valid_password = 'password'

# Function to get the timestamp of a file
def get_upload_timestamp(filename):
    path = os.path.join('static', 'images', 'post', filename)
    timestamp = os.path.getmtime(path)
    return datetime.fromtimestamp(timestamp)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == valid_username and password == valid_password:
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    else:
        return "Invalid login credentials"
    
@app.route("/dashboard")
def dashboard():
    if 'logged_in' in session and session['logged_in']:
        # Get list of image files in the "post" folder
        post_images = os.listdir(os.path.join(app.static_folder, 'images', 'post'))
        # Sort images by upload timestamp
        post_images.sort(key=get_upload_timestamp, reverse=True)
        # Construct URLs for these images
        image_urls = [url_for('static', filename=f'images/post/{img}') for img in post_images]
        user_avatar_url = url_for('static', filename='images/user-avatar.png')
        return render_template("dashboard.html", user_avatar_url=user_avatar_url, image_urls=image_urls)
    else:
        return "Access denied. Please log in first."

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))      


@app.route("/upload", methods=['POST'])
def upload():
    if 'image' in request.files:
        uploaded_image = request.files['image']

        # Open and preprocess the uploaded image
        img = Image.open(uploaded_image)
        img = np.array(img)
        img = img[:, :, :3]  # Discard the alpha channel if it exists
        
        original_size = img.shape[:2]
        
        # Resize the image to fit Instagram's aspect ratio requirements
        width, height = img.shape[1], img.shape[0]
        aspect_ratio = width / height
        if aspect_ratio < 1.91 / 1 or aspect_ratio > 4 / 5:
            # Crop the image to fit the supported aspect ratio
            new_height = min(max(566, height), 1350)
            new_width = int(aspect_ratio * new_height)
            img = tf.image.resize(img, (new_width, new_height))
            img = np.array(img)

        # Resize the image to ensure its width is within 320 and 1080 pixels
        new_width = min(max(320, width), 1080)
        new_height = int(height * (new_width / width))
        img = tf.image.resize(img, (new_width, new_height))
        img = np.array(img)
        
        img = img / 255.0  # Normalize the image
        
        img_for_prediction = tf.image.resize(img, (256, 256))  # Resize as required by your model
        img_for_prediction = np.expand_dims(img_for_prediction, axis=0)

        # Make prediction using your model
        prediction = dog_model.predict(img_for_prediction)
        if prediction >= 0.5:  # Adjust threshold as needed
            print('Is a dog')
            # Resize image back to original dimensions
            original_img = tf.image.resize(img, original_size)
            original_img = np.squeeze(original_img.numpy() * 255).astype(np.uint8)

            # Save the uploaded image to a desired location
            image_path = f"static/images/post/{uploaded_image.filename}"
            Image.fromarray(original_img).save(image_path)
            
            # Get other post data
            post_text = request.form.get('post_text')  # Assuming there's a text input with name 'post_text'

            # Construct the image URL
            image_url = url_for('static', filename=f'images/post/{uploaded_image.filename}')

            return jsonify({"image_url": image_url, "post_text": post_text})
        else:
            print('Is not a dog')
            return jsonify({"error": "Uploaded image does not contain a dog"}), 400
    else:
        return jsonify({"error": "No image provided"}), 400
    
@app.route("/profile")
def profile():
   # Get list of image files in the "post" folder
    post_images = os.listdir(os.path.join(app.static_folder, 'images', 'post'))
    # Construct URLs for these images
    post_images.sort(key=get_upload_timestamp, reverse=True)
    image_urls = [url_for('static', filename=f'images/post/{img}') for img in post_images]
    return render_template("profile.html", image_urls=image_urls)

if __name__ == '__main__':
    app.run(debug=True)