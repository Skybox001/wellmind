# WellMind (Mental Health Support AI)

A Flask-based web application that combines machine learning and AI chatbot technology to provide mental health support and assessment.

## Features

- **Mental Health Assessment**: SVM-based prediction model to assess mental health status based on demographic, socioeconomic, and symptom data
- **AI Chatbot**: PyTorch neural network-powered conversational bot trained on mental health topics
- **User Authentication**: Secure login/signup system with MySQL database
- **Professional Support Integration**: WhatsApp integration for connecting with mental health professionals

## Tech Stack

- **Backend**: Flask (Python)
- **Machine Learning**: scikit-learn (SVM), PyTorch (Neural Network)
- **NLP**: NLTK for tokenization and stemming
- **Database**: MySQL
- **Frontend**: HTML/CSS/JavaScript with particles.js

---

## Local Development Setup

### Prerequisites
- Python 3.11+
- MySQL Server running on `localhost` (default port `3306`)

### 1) Create a virtual environment + install dependencies

**Windows PowerShell:**
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2) Configure environment variables
Copy `.env.example` to `.env` and fill in your values:
```bash
cp .env.example .env
```

Edit `.env`:
```env
FLASK_SECRET_KEY=your-secret-key-here
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your-password
DB_NAME=chatbot
```

### 3) Initialize the database
Run the SQL script in your MySQL client:
```bash
mysql -u root -p < init_db.sql
```

Or manually:
```sql
CREATE DATABASE IF NOT EXISTS chatbot;
USE chatbot;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_username (username)
);
```

### 4) Download NLTK data
```python
python -c "import nltk; nltk.download('punkt')"
```

### 5) Run the application
```bash
python app.py
```

Open: http://127.0.0.1:5000

---

## Deployment on Render

### Quick Deploy (Recommended)

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/wellmind.git
   git push -u origin main
   ```

2. **Create a Render account**
   - Go to [render.com](https://render.com) and sign up

3. **Deploy using render.yaml**
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml` and create:
     - Web service (Flask app)
     - MySQL database
   - Click "Apply"

4. **Initialize the database**
   - Once deployed, go to your database dashboard on Render
   - Click "Connect" → "External Connection"
   - Use the provided credentials to connect with a MySQL client
   - Run the `init_db.sql` script:
     ```bash
     mysql -h <hostname> -u <username> -p --ssl-mode=REQUIRED < init_db.sql
     ```

5. **Access your app**
   - Your app will be available at: `https://wellmind.onrender.com`

### Manual Deploy (Alternative)

If you prefer manual setup:

1. **Create a new Web Service**
   - Go to Render Dashboard → "New +" → "Web Service"
   - Connect your GitHub repo
   - Configure:
     - **Name**: wellmind
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt && python -c 'import nltk; nltk.download("punkt")'`
     - **Start Command**: `gunicorn app:app`

2. **Create a MySQL Database**
   - Go to Render Dashboard → "New +" → "MySQL"
   - **Name**: wellmind-db
   - **Database**: chatbot
   - **User**: wellmind_user

3. **Set Environment Variables**
   In your web service settings, add:
   - `FLASK_SECRET_KEY`: (auto-generate a secure key)
   - `DB_HOST`: (from database connection info)
   - `DB_PORT`: (from database connection info)
   - `DB_USER`: (from database connection info)
   - `DB_PASSWORD`: (from database connection info)
   - `DB_NAME`: chatbot

4. **Initialize database** (see step 4 above)

### Important Notes for Render Deployment

- **Free tier limitations**: 
  - Web service spins down after 15 minutes of inactivity
  - First request after spin-down takes ~30 seconds
  - Database limited to 1GB storage
  
- **Model files**: Ensure `svm_model.pkl` and `data.pth` are committed to your repo

- **NLTK data**: The build command automatically downloads required NLTK data

- **Database connection**: Uses SSL by default on Render's managed MySQL

---

## Usage

### For Users

1. **Sign Up / Login**
   - Create an account or login with existing credentials

2. **Mental Health Self-Assessment**
   - Fill out the comprehensive form with demographic and symptom information
   - Get instant ML-based prediction
   - Receive personalized guidance

3. **Chat with AI Bot**
   - Navigate to chatbot section
   - Ask about mental health symptoms, coping strategies, or general wellness
   - Get instant, empathetic responses

### Default Test Account
If you've inserted the test data:
- **Username**: `admin`
- **Password**: `123456`

---

## Project Structure

```
wellmind/
├── app.py                 # Main Flask application
├── chat.py                # Chatbot inference logic
├── model.py               # PyTorch neural network definition
├── nltk_utils.py          # NLP preprocessing utilities
├── train.py               # Chatbot training script
├── training.py            # SVM model training script
├── intents.json           # Chatbot training data
├── data.pth               # Trained chatbot model
├── svm_model.pkl          # Trained SVM model
├── Cleaned Data.xlsx      # SVM training dataset
├── requirements.txt       # Python dependencies
├── runtime.txt            # Python version for Render
├── render.yaml            # Render deployment configuration
├── init_db.sql            # Database initialization script
├── .env.example           # Environment variables template
├── templates/             # HTML templates
│   ├── index.html         # Mental health assessment form
│   ├── chatbot.html       # Chatbot interface
│   ├── login.html         # Login page
│   ├── signup.html        # Signup page
│   └── self_check.html    # Landing page
└── static/                # Static assets (images)
```

---

## Security Considerations

⚠️ **Current Implementation Limitations**:
- Passwords are stored in plain text (not hashed)
- No CSRF protection
- No rate limiting on API endpoints

**Recommended Improvements for Production**:
1. Implement password hashing (bcrypt/Argon2)
2. Add Flask-WTF for CSRF protection
3. Implement rate limiting with Flask-Limiter
4. Use HTTPS (Render provides this automatically)
5. Add input validation and sanitization
6. Implement session timeout

---

## Model Information

### SVM Model (Mental Health Prediction)
- **Algorithm**: Support Vector Machine (Linear Kernel)
- **Features**: 16 (demographic, socioeconomic, symptoms)
- **Target**: Binary classification (mentally ill: 0/1)
- **Training**: 80/20 split on cleaned dataset

### Chatbot Neural Network
- **Architecture**: 3-layer feedforward network
- **Input**: Bag-of-words vector (NLTK tokenized + stemmed)
- **Output**: Intent classification (20 intents)
- **Training**: 10,000 epochs, Adam optimizer
- **Confidence threshold**: 75%

---

## Contributing

Contributions are welcome! Please consider:
- Adding password hashing for security
- Implementing unit tests
- Expanding the chatbot's intent dataset
- Adding more mental health assessment features

---

## License

This project is for educational and research purposes.

---

## Support

For mental health emergencies, please contact:
- **Emergency Services**: 911
- **Suicide Prevention Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741

---

## Credits

Developed by Shresth Gautam © 2025
