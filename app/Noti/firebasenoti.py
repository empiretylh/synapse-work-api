import firebase_admin
from firebase_admin import credentials, messaging
import os
# Get the absolute path to the certificate file
cert_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'synapsework_firebase.json')

# Use the absolute path when creating the credentials
cred = credentials.Certificate(cert_path)
firebase_admin.initialize_app(cred)

def send_multicast_message(device_tokens, message_title, message_body, custom_data=None):
    # Create a message payload
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=message_title,
            body=message_body,
        ),
        data=custom_data,
        tokens=device_tokens,
        android=messaging.AndroidConfig(
            ttl=3600,
            priority='high'
        ),
    )

    # Send the multicast message
    response = messaging.send_multicast(message)
    print("Multicast message sent successfully:", response)
