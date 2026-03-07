# 🌾 Paddy Leaf Disease Identifier

The **Paddy Leaf Disease Identifier** is a deep learning-based web application designed to help farmers and agronomists identify diseases in paddy (rice) leaves quickly and accurately. This project uses a Convolutional Neural Network (CNN) to classify images and provides recommended treatments for each detected disease.

## 🚀 Key Features
- **Instant Diagnosis**: Upload an image or use a camera to identify diseases in real-time.
- **Deep Learning Powered**: Uses a trained TensorFlow/Keras model (CNN) for high-accuracy classification.
- **Multilingual Support**: Available in **English**, **Tamil**, and **Sinhala**.
- **History Tracking**: Automatically saves prediction results to a MySQL database for future reference.
- **Actionable Solutions**: Provides specific treatment recommendations for each disease.
- **Responsive UI**: Modern, glassmorphism-inspired design that works on mobile and desktop.

## 🛠️ Tech Stack
- **Backend**: Python, Flask
- **Machine Learning**: TensorFlow, Keras, NumPy, Pillow
- **Database**: MySQL (for history tracking)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)

## 📦 Prerequisites
Before running the project, ensure you have the following installed:
- [Python 3.8+](https://www.python.org/downloads/)
- [MySQL Server](https://dev.mysql.com/downloads/installer/)
- [pip](https://pip.pypa.io/en/stable/installation/)

## 🔧 Installation & Setup

1. **Navigate to the Project Directory**
   ```bash
   cd paddy_dataset
   ```

2. **Set up Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv .venv
   # Activate on Windows:
   .venv\Scripts\activate
   # Activate on macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install mysql-connector-python
   ```

4. **Database Configuration**
   - Open your MySQL terminal or Workbench.
   - Create the database:
     ```sql
     CREATE DATABASE paddy_disease_db;
     ```
   - Create the `prediction_history` table:
     ```sql
     USE paddy_disease_db;

     CREATE TABLE prediction_history (
         id INT AUTO_INCREMENT PRIMARY KEY,
         prediction VARCHAR(100),
         confidence VARCHAR(50),
         solution TEXT,
         image LONGTEXT, -- Stores base64 image data
         timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
     );
     ```
   - **Update Credentials**: If your MySQL `user` or `password` is different from the defaults in `app.py` (root/user), update lines 43-44 in `app.py`:
     ```python
     user='your_username',
     password='your_password'
     ```

## 🏃 How to Run
1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## 📖 How to Use
1. **Home**: Select your preferred language (English, Tamil, Sinhala).
2. **Upload**: Select a photo of a paddy leaf from your device or use the camera to capture a new photo.
3. **Analyze**: Click the **Analyze** button. The system will process the image and display the disease name, confidence score, and treatment recommendation.
4. **History**: Click on the **History** tab to see your past predictions. You can delete individual records or clear the entire history.
5. **About**: Learn more about the project and the specific diseases the system is trained to detect.

## 🦠 Supported Diseases
The system is trained to identify the following conditions:
1. **Bacterial Leaf Blight**
2. **Brown Spot**
3. **Leaf Blast**
4. **Leaf Scald**
5. **Narrow Brown Spot**
6. **Healthy Leaf**
7. **Not Paddy Leaf** (Detection for non-relevant images)

---
© 2024 Paddy Leaf Disease Identifier
