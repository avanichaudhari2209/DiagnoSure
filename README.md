# DiagnoSure 

A symptom-based disease prediction web application built with **Django REST Framework** (backend) and **vanilla HTML/CSS/JS** (frontend). Users enter their symptoms in plain text, and DiagnoSure uses keyword-matching logic to predict the most likely disease — along with precautions, risk level, and dietary recommendations.

---

## Features

- **Symptom Analysis** — Enter symptoms in natural language; the backend intelligently matches them to a disease database
- **Disease Prediction** — Returns the best-matched disease with description, severity, precautions, and diet advice
- **User Authentication** — Register and login with hashed password storage
- **Family Member Management** — Add, view, and delete family members associated with an account
- **Medical History** — Track past assessments with timestamps, symptoms, and predicted diseases
- **Report Storage** — All analysis results are saved per user and retrievable anytime
- **Chatbot** — Basic symptom-guidance chatbot for common queries

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6.x, Django REST Framework |
| Database | SQLite3 |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Auth | Django's `make_password` / `check_password` |
| CORS | `django-cors-headers` |

---

## Project Structure

```
DiagnoSure-main/
├── diagnosure/               # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── api/                      # Core Django app
│   ├── models.py             # User, Disease, Report, FamilyMember, etc.
│   ├── views.py              # API logic + disease prediction engine
│   ├── serializers.py        # DRF serializers
│   ├── urls.py               # API routes
│   ├── admin.py
│   ├── diseases.json         # Disease seed data
│   ├── diet.json             # Diet recommendation seed data
│   ├── load_diseases.py      # Management script to populate diseases
│   └── load_diets.py         # Management script to populate diets
├── final1/                   # Frontend (static HTML pages)
│   ├── diagnosure_final.html # Main landing / assessment page
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── account.html
│   ├── family.html
│   ├── history.html
│   ├── lifestyle.html
│   ├── member_assessment.html
│   └── script.js             # Frontend API calls
├── manage.py
└── db.sqlite3
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/DiagnoSure.git
   cd DiagnoSure
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate         # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework django-cors-headers
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Seed the database with disease and diet data**
   ```bash
   python manage.py shell < api/load_diseases.py
   python manage.py shell < api/load_diets.py
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`.

Open any HTML file in the `final1/` folder directly in your browser to use the frontend.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/user/` | Register a new user |
| `POST` | `/api/login/` | Login with email and password |
| `POST` | `/api/analyze/` | Submit symptoms and get disease prediction |
| `POST` | `/api/chatbot/` | Send a message to the chatbot |
| `GET` | `/api/reports/<user_id>/` | Get all past reports for a user |
| `GET` | `/api/family/` | Get family members for a user |
| `POST` | `/api/family/` | Add a new family member |
| `DELETE` | `/api/family/` | Remove a family member |

### Example: Symptom Analysis

**Request**
```http
POST /api/analyze/
Content-Type: application/json

{
  "user_id": 1,
  "symptoms": ["fever", "headache", "body ache"]
}
```

**Response**
```json
[
  {
    "disease": "Influenza",
    "score": 85,
    "risk": "High",
    "precautions": ["Rest", "Stay hydrated", "Avoid contact"],
    "description": "A contagious respiratory illness...",
    "symptoms": ["fever", "headache", "body ache", "fatigue"],
    "diet": "Warm soups, fluids, vitamin C-rich foods"
  }
]
```

---

## Data Models

- **User** — Name, age, gender, email, hashed password
- **Disease** — Name, description, category, severity, symptoms (JSON), precautions (JSON), risk factors, diet, contagious flag
- **Report** — Links a User to a Disease prediction with risk level and timestamp
- **FamilyMember** — Linked to a User with name, relation, and age
- **MedicalHistory** — Stores per-assessment records with predicted diseases, symptom severity, and diet advice
- **ChatbotMessage** — Stores chatbot conversation history per user

---

## How the Prediction Works

The prediction engine in `api/views.py` uses a keyword-scoring approach:

1. The user's symptom input is lowercased and tokenized, with common stop words removed.
2. Each disease in the database is scored by matching its symptom list against the user's input.
3. Exact phrase matches score **3 points**; partial keyword overlaps score **1 point per shared word**.
4. The disease with the highest score (minimum 1 point) is returned as the result.

---

## Configuration Notes

- `CORS_ALLOW_ALL_ORIGINS = True` is set for development. Restrict this in production.
- `DEBUG = True` — change to `False` and configure `ALLOWED_HOSTS` before deploying.
- The `SECRET_KEY` in `settings.py` must be replaced with a secure value in production (use environment variables).

---

## Future Improvements

- Replace keyword matching with an ML-based classifier (e.g., scikit-learn or a trained model)
- Add JWT-based authentication
- Upgrade from SQLite to PostgreSQL for production
- Build a proper chatbot with NLP capabilities
- Add email verification on registration
- Deploy frontend and backend together (e.g., via Docker or a cloud platform)

---

## License

This project is for educational purposes. Feel free to fork and extend it.

