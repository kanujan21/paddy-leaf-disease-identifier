# 🎓 Viva Preparation Guide: Paddy Leaf Disease Identifier

This guide will help you prepare for the questions the examiners might ask during your viva session.

## Potential Technical Questions

1.  **"Why did you choose a Convolutional Neural Network (CNN) for this project?"**
    *   **Answer:** CNNs are the state-of-the-art for image classification because they can automatically learn spatial hierarchies of features (like edges, textures, and shapes) from images, which is essential for identifying subtle differences in leaf disease patterns.

2.  **"What is the input size of your model, and how do you preprocess the images?"**
    *   **Answer:** The images are resized to **180x180 pixels**. Preprocessing includes converting the image to a NumPy array and ensuring it has 3 channels (RGB). We also use **Softmax activation** on the output layer to get probability scores.

3.  **"How does your system handle images that are NOT paddy leaves?"**
    *   **Answer:** We implemented a two-step robustness check:
        1. We trained a specific class called `not_paddy_leaf`.
        2. We have a **confidence threshold logic**: If the model is less than **60% confident**, or if the `not_paddy_leaf` category probability exceeds **30%**, we classify it as an invalid image.

4.  **"How do you store the prediction history?"**
    *   **Answer:** We use a **MySQL database**. The image itself is converted into a **Base64 string** (LongText) so it can be stored directly in the database without needing a separate file server for images.

5.  **"Which framework did you use for the Backend and why?"**
    *   **Answer:** I used **Flask (Python)** because it is lightweight, easy to integrate with deep learning libraries like TensorFlow, and perfect for building the RESTful APIs used by the frontend.

## Vital Viva Tips

*   **Know Your Dataset:** If asked, be ready to mention where you got your training data (e.g., Kaggle, UCI, or field collection).
*   **Demonstrate the History Feature:** Examiners love seeing CRUD operations. Showing how you can view and delete past predictions in the "History" tab proves your full-stack development skills.
*   **Mention the Multilingual Support:** This shows that you considered the "End User" (local farmers) during development, which is a big plus for "social impact" evaluation.
*   **Be Honest about Limitations:** If asked about accuracy, mention that while it's high, it could be further improved with a larger, more diverse dataset or by using transfer learning (e.g., ResNet or MobileNet).

Good luck with your viva! You have built a solid, useful project.
