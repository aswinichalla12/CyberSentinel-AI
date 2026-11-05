
import joblib

model = joblib.load("models/spam_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

message = input("Enter an SMS message: ")

message_vector = vectorizer.transform([message])
prediction = model.predict(message_vector)[0]

if prediction == "spam":
    print("Warning: This message may be SPAM!")
else:
    print("This message is classified as NORMAL.")
