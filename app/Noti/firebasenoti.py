import firebase_admin
from firebase_admin import credentials, messaging

# Initialize Firebase Admin SDK
cred = credentials.Certificate("synapsework_firebase.json")
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

    )

    # Send the multicast message
    response = messaging.send_multicast(message)
    print("Multicast message sent successfully:", response)
