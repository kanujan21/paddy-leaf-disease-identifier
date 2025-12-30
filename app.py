import os
from flask import Flask, request, jsonify, render_template
from PIL import Image
import numpy as np
import tensorflow as tf
from keras.models import load_model
from flask_cors import CORS
import base64
from io import BytesIO
import mysql.connector
from mysql.connector import Error

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)  # To allow frontend to connect

# Load your trained model
try:
    model = load_model('paddyleaf_model.h5')
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Define the class names
paddyleaf_names = ['bacterial_leaf_blight', 'brown_spot', 'healthy', 'leaf_blast', 'leaf_scald', 'narrow_brown_spot', 'not_paddy_leaf']

solutions = {
    'bacterial_leaf_blight': "Apply copper-based fungicides and remove infected leaves.",
    'brown_spot': "Use resistant varieties and practice crop rotation.",
    'healthy': "No action needed, the leaf is healthy.",
    'leaf_blast': "Use fungicides and practice proper irrigation.",
    'leaf_scald': "Reduce leaf wetness and use fungicides.",
    'narrow_brown_spot': "Apply fungicides and remove infected plant debris.",
    'not_paddy_leaf': "The uploaded image is not a paddy leaf. Please try again."
}

# Database Connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='paddy_disease_db',
            user='root',      # Adjust if necessary
            password='user'       # Adjust if necessary
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    return None

# Function to convert image to base64 string
def convert_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Prediction function
def classify_image(image):
    if model is None:
        return "Model not loaded", 0, "No model"
        
    input_image = image.resize((180, 180))
    input_image_array = np.array(input_image)

    # Ensure image has 3 channels (RGB)
    if input_image_array.shape[-1] != 3:
        input_image_array = input_image_array[..., :3]

    input_image_exp_dim = np.expand_dims(input_image_array, axis=0)

    predictions = model.predict(input_image_exp_dim)
    result = tf.nn.softmax(predictions[0])

    predicted_class = paddyleaf_names[np.argmax(result)]
    prediction_score = np.max(result) * 100
    
    # Confidence threshold check - if confidence is below 60%, classify as not_paddy_leaf
    # Also check if the not_paddy_leaf class has significant probability
    not_paddy_index = paddyleaf_names.index('not_paddy_leaf')
    not_paddy_score = result[not_paddy_index].numpy() * 100
    
    # If the predicted class is not 'not_paddy_leaf' BUT confidence is low OR not_paddy has decent probability
    if predicted_class != 'not_paddy_leaf':
        if prediction_score < 60 or not_paddy_score > 30:
            predicted_class = 'not_paddy_leaf'
            prediction_score = max(prediction_score, not_paddy_score)
    
    solution = solutions.get(predicted_class, "No solution available.")
    
    return predicted_class, prediction_score, solution

# --- Page Routes ---

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/upload_page')
def upload_page():
    return render_template('upload.html')

@app.route('/about_page')
def about_page():
    return render_template('about.html')

@app.route('/history_page')
def history_page():
    return render_template('history.html')

# --- API Routes ---

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded!"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected!"}), 400

    try:
        image = Image.open(file)
        predicted_class, prediction_score, solution = classify_image(image)

        # Convert image to base64
        image_base64 = convert_image_to_base64(image)
        confidence_str = f"{prediction_score:.2f}%"

        # Save prediction to MySQL Database
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            query = "INSERT INTO prediction_history (prediction, confidence, solution, image) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (predicted_class, confidence_str, solution, image_base64))
            conn.commit()
            cursor.close()
            conn.close()
        else:
            print("Failed to save history: No DB connection")

        return jsonify({
            'prediction': predicted_class,
            'confidence': confidence_str,
            'solution': solution,
            'image': image_base64
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    history_list = []
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            # Fetch history sorted by newest first
            cursor.execute("SELECT * FROM prediction_history ORDER BY timestamp DESC")
            rows = cursor.fetchall()
            
            for row in rows:
                history_list.append({
                    'id': row['id'],
                    'prediction': row['prediction'],
                    'confidence': row['confidence'],
                    'solution': row['solution'],
                    'image': row['image']
                })
                
            cursor.close()
            conn.close()
    except Exception as e:
        print(f"Error fetching history: {e}")
        
    return jsonify({'history': history_list})

@app.route('/delete_history/<int:id>', methods=['POST'])
def delete_history_item(id):
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM prediction_history WHERE id = %s", (id,))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'message': 'History item deleted successfully!'}), 200
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear_history', methods=['POST'])
def clear_history():
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM prediction_history") 
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'message': 'History cleared successfully!'}), 200
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
