# FAQ-Assistant

## 📌 Project Overview

### This is an FAQ assistant that provides answers to user queries. It can function in two modes:

1. Using OpenAI API: If an API key is provided, it fetches dynamic responses from OpenAI.

2. Using faq.json (Fallback Mode): If no API key is available, it retrieves pre-defined answers from faq.json.

## 🔧 Installation & Setup
### 1️⃣ Clone the Repository (If Required)

If you need to clone the repository from GitHub:

```
git clone https://github.com/Rakshit11111/FAQ-Assistant.git
```
```
cd FAQ-Assistant
```
## 2️⃣ Create & Activate Virtual Environment
```
python -m venv venv  # Create a virtual environment
source venv/bin/activate  # Activate on macOS/Linux
venv\Scripts\activate  # Activate on Windows
```

## 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```
## 🌍 Environment Variables

Edit a .env file in the project root with the following content:

```
OPENAI_API_KEY=Your_api_key
MONGO_URI=mongodb://your_mongo_uri  # Replace with actual URI or local host
```

#### > If using MongoDB locally, set:
```
MONGO_URI=mongodb://localhost:27017
```
#### >If using a remote MongoDB cluster, set:
```
MONGO_URI=mongodb+srv://your_user:your_password@your_cluster.mongodb.net/
```

## 🚀 Running the Project
1. Ensure your virtual environment is activated.

2. Run the Flask app:
```
python app.py
```
3. Open your browser and go to:
```
http://127.0.0.1:5000/
```

## 📜 Notes
> venv folder are not uploaded to GitHub for security reasons.

> Ensure MongoDB is running if using a local database.

> If OpenAI API key is not provided, the system will default to faq.json for responses.




