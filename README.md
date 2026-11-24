<img width="512" height="512" alt="image" src="https://github.com/user-attachments/assets/b32f9026-75be-41ca-9b16-04cf7aaa8968" /># 🛡️ CyberSentinel AI – Intelligent Scam Detection System

An AI-powered SMS scam detection application built using Machine Learning, NLP, and an Embedding-Based Text Representation System.

## 🚀 Project Overview

CyberSentinel AI is designed to detect suspicious SMS messages using Natural Language Processing (NLP), text embeddings, and Machine Learning.

The system converts message text into meaningful numerical vector representations using an embedding system. These representations help the model understand textual patterns and classify messages as legitimate or suspicious.

## ✨ Key Features

- **AI-Powered Detection:** Uses a trained Machine Learning model to classify SMS messages.
- **Embedding-Based Text Representation:** Converts text into numerical vector representations.
- **Spam Classification:** Identifies spam and legitimate messages.
- **Scam Risk Analysis:** Highlights suspicious words and message patterns.
- **Risk Score:** Displays the predicted risk level.
- **Interactive Dashboard:** User-friendly Streamlit interface.
- **Example Messages:** Test the application using sample messages.
- **Real-Time Prediction:** Analyze messages instantly.
- **Batch Analysis:** Supports analyzing multiple messages if enabled in the application.
## ⚙️ Tools Used
Python 3.11 | VS Code | Scikit-learn | Pandas | NumPy | Embeddings| LogisticRegresssion Joblib | Streamlit | GitHub

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Machine Learning | Message classification |
| Natural Language Processing | Text processing |
| Text Embeddings | Semantic text representation |
| Scikit-learn | Machine Learning |
| Pandas | Data processing |
| NumPy | Numerical operations |
| Joblib | Model serialization |
| Streamlit | Web application interface |

## 📂 Project Structure

```text
CyberSentinel-AI/
│
├── streamlit_app.py
├── predict.py
├── train_model.py
├── prepare_data.py
├── requirements.txt
├── README.md
│
├── data/
│   └── cleaned_messages.csv
│
└── models/
    ├── spam_model.pkl
    └── embedding_model.pkl
```

*Adjust model filenames to match the actual files used by your application.*

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/aswinichalla12/CyberSentinel-AI.git
```

### 2. Navigate to the project folder

```bash
cd CyberSentinel-AI
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit application

```bash
streamlit run streamlit_app.py
```

### 5. Open the application

```text
http://localhost:8501
```

## 🧠 Machine Learning Workflow

1. Collect the SMS Spam Collection dataset.
2. Clean and preprocess SMS messages.
3. Generate numerical text embeddings.
4. Use the embedding representations as input features for the classification model.
5. Train the Machine Learning model.
6. Evaluate model performance.
7. Save the trained model and required embedding components.
8. Load the saved components into the Streamlit application.
9. Predict whether incoming messages are suspicious or legitimate.

## 📊 Model Performance

The trained model achieved approximately **97% accuracy** on the reported test dataset.

*Performance may vary depending on the dataset and evaluation conditions.*

## 🎯 Project Objective

The main objective of CyberSentinel AI is to help users identify potentially fraudulent and suspicious SMS messages using AI-powered text analysis and classification.

## 🔮 Future Enhancements

- URL and phishing link detection.
- Advanced Deep Learning models.
- Multilingual scam message detection.
- Email scam detection.
- Explainable AI integration.
- Improved fraud pattern identification.

## ⚠️ Disclaimer

CyberSentinel AI is an educational and demonstration project. Its predictions are not guaranteed to identify every scam. Always verify suspicious messages independently and never share OTPs, passwords, or banking information.

## 👩‍💻 Author

**Challa Aswini**

GitHub: https://github.com/aswinichalla12

---

⭐
