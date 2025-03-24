from flask import Flask, request, jsonify
from flask_cors import CORS  # To handle Cross-Origin Resource Sharing (CORS)
import smtplib
import ssl
from email.message import EmailMessage

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define email sender credentials
email_sender = 'extbot1.donotreply@gmail.com'
email_password = 'qjnsiwnpwvkzgoxs'

# API endpoint to send email
@app.route('/send-email', methods=['POST'])
def send_email():
    # Get the email from the request body
    data = request.json
    email_receiver = data.get('email')
    
    # Validate the email
    if not email_receiver:
        return jsonify({"error": "Email address is required"}), 400

    # Set the subject and body of the email
    subject = 'Guardian Registered'
    body = """
    You have successfully registered with our application!
    You will be updated with the results time to time.

    Please keep monitoring the subject for maximum support!
    Cheers
    """

    # Create the email message
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
            return jsonify({"message": f"Email sent to {email_receiver}"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to send email: {e}"}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)