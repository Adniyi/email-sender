# This server is used to recive email data and send it to an email account.
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

CORS(app)
# Mail configuration from environment variables
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 465))
app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL", "true").lower() == "true"
app.config["MAIL_USERNAME"] = os.getenv("EMAIL_ADDRESS")
app.config["MAIL_PASSWORD"] = os.getenv("EMAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("EMAIL_ADDRESS")
CORS(app, resources={r"/send-email": {"origins": "http://127.0.0.1:5500"}})
mail = Mail(app)

@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    name = data.get("name", "Anonymous")
    sender_email = data.get("email", "unknown@example.com")
    subject = data.get("subject", "No Subject")
    message = data.get("message", "")

    recipient = os.getenv("TO_EMAIL")
    print("pass")
    try:
        msg = Message(subject, recipients=[recipient]) # type: ignore
        msg.body = (
            f"From: {name} <{sender_email}>\n\n{message}"
            f"Name: {name}\n"
            f"Email: {sender_email}\n"
            f"Subject: {subject}\n"
            f"Message: {message}\n"
        )

        msg.reply_to = sender_email
        mail.send(msg)
        return jsonify({"message": "Email sent successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=False)