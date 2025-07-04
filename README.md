# 🧪 TinkerLab Equipment Booking System

A Streamlit-based web application to manage equipment booking in a college TinkerLab.  
It allows students to browse, request, and track equipment while enabling admins to approve bookings, update inventory, and monitor usage.

---
DEPLOYED LINK:- https://tinkerlab-booking-gr7xncd6hytdymmaiebwpn.streamlit.app

## Features

### 👨‍🎓 For Students
- Browse and filter lab equipment
- Watch training videos for each equipment
- Book equipment in 3-day time slots
- View personal booking history
- See only your bookings without scrolling

### 🛠️ For Admins
- Approve or reject student booking requests
- Add, edit, or delete equipment entries
- View booking request statuses (pending, accepted, in-use, returned)
- Track check-ins and returns
- Monitor inventory usage with quantity tracking

---

##  Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: Firebase Realtime Database
- **Auth & Config**: Firebase Admin SDK
- **Data Handling**: Python & JSON
- **Version Control**: Git + GitHub

---

## Requirements-mentioned in requirements.txt
You can just do pip install -r requirements.txt


Install Python 3.11 or higher and clone the repo:


git clone https://github.com/Aayushya-paswan/tinkerlab-booking.git
cd tinkerlab-booking
Install the dependencies:

bash
Copy
Edit
pip install -r requirements.txt
🔐 Firebase Setup
Go to Firebase Console

Create a new project named tinker-lab-manager

Enable Realtime Database and set the rules to allow read/write access during testing

Add a service account:

Go to Project Settings > Service Accounts > Generate new private key

Download the JSON file

🔒 Adding Secrets (Locally)
Create a folder .streamlit/ and inside it a file named secrets.toml.
Paste your Firebase credentials in this format (escape all \n in private_key):

toml
Copy
Edit
[firebase]
type = "service_account"
project_id = "tinker-lab-manager"
private_key_id = "YOUR_KEY_ID"
private_key = "-----BEGIN PRIVATE KEY-----\\nMIIEvAIBADANBg...\\n-----END PRIVATE KEY-----\\n"
client_email = "firebase-adminsdk-xxx@tinker-lab-manager.iam.gserviceaccount.com"
client_id = "YOUR_CLIENT_ID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxx%40tinker-lab-manager.iam.gserviceaccount.com"
universe_domain = "googleapis.com"
▶Running the App Locally
bash
Copy
Edit
streamlit run main.py
The app will open in your browser at http://localhost:8501.

Deploying to Streamlit Cloud
Push your project to a public GitHub repo

Go to Streamlit Cloud

Click New App and select your repo

Set Python version to 3.11

In Secrets, paste the same [firebase] TOML block from above

Click Deploy

Your app will be live and accessible from any device.

🧑‍💻 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you’d like to change.

🛡️ License
This project is licensed under the MIT License.

🙏 Credits
Built with ❤️ by Aayush Paswan
Thanks to Streamlit and Firebase for the tools!

yaml
Copy
Edit
