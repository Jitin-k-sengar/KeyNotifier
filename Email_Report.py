from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(receiver_email, subject, body):
    """
    This function sends an email using SMTP protocol.

    Parameters:
    receiver_email (str): The email address of the recipient.
    subject (str): The subject line of the email.
    body (str): The content of the email.

    Returns:
    None

    This function attempts to send an email to the specified recipient using the provided subject and body.
    It uses the SMTP protocol to connect to smtp.gmail.com on port 587, starts a TLS session, logs in using
    the sender's email address and password, and sends the email. If any exception occurs during the process,
    it prints an error message. Finally, it quits the SMTP server.
    """
    try:
        sender_email = "tstark.squad"
        password = "mzzc bjpr qijj ohxe"
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server = SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        try:
            server.quit()
        except Exception as e:
            print(f"Error quitting server: {e}")
