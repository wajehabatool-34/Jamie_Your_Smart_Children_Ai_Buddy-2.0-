# Jamie – Children's AI Buddy

A simple educational AI chatbot experience designed for children and managed by parents. This project combines a Flask-based web frontend with a FastAPI backend to deliver safe chat, learning prompts, mini-games, and video recommendations.

## Project Overview

- `flask_app.py`: Main web application for parent login, account creation, chat session access, logout, and admin panel.
- `fastapi_app.py`: Chat API that receives child messages, validates content, and returns friendly responses, games, and learning video links.
- `templates/`: HTML templates used by Flask for the landing page, login flow, chat interface, and admin panel.
- `static/`: CSS and JavaScript assets for UI styling, chat behavior, and interactive animations.
- `users.json`: Local user database storing parent accounts, child settings, passwords, and stars.

## Key Features

- Parent-managed login and account creation.
- Child-friendly chat UI with custom voice responses.
- Safe language filtering via a built-in bad word blocklist.
- Learning topics including Math, English, Science, Manners, Poems, Islamic stories, and Technology.
- Mini-games: Rock-Paper-Scissors and Guess the Number.
- Interactive frontend features: emoji picker, clear chat, help modal, and speech synthesis.
- Simple admin panel with hardcoded credentials for viewing user accounts.

## File Structure

- `fastapi_app.py`
- `flask_app.py`
- `users.json`
- `templates/`
  - `land.html`
  - `login.html`
  - `index.html`
  - `admin.html`
- `static/`
  - `chat.js`
  - `chat.css`
  - `land.css`
  - `audio/`
  - `piano/`

## Running the Project

### 1. Install dependencies

Install Python dependencies in your environment.

```powershell
pip install fastapi uvicorn flask pydantic
```

### 2. Start the FastAPI chat backend

```powershell
cd c:\Jamie_Your_Smart_Children_Ai_Buddy
uvicorn fastapi_app:app --reload --host 127.0.0.1 --port 8000
```

### 3. Start the Flask frontend

In a second terminal:

```powershell
cd c:\Jamie_Your_Smart_Children_Ai_Buddy
python flask_app.py
```

### 4. Open the app

Visit:

- Parent site and chat landing: `http://127.0.0.1:5000/`
- Chat interface after login: `http://127.0.0.1:5000/chat`
- Admin panel: `http://127.0.0.1:5000/admin`

## Usage Notes

- The frontend uses `http://127.0.0.1:8000/chat` to reach the FastAPI backend.
- Parent credentials and child profiles are stored in `users.json`.
- The admin login is hardcoded as:
  - Email: `admin@gmail.com`
  - Password: `admin123`
- Game sessions are tracked in memory within the FastAPI app, so restarting the backend resets ongoing games.

## Chat API Behavior

`fastapi_app.py` accepts POST requests to `/chat` with JSON payload:

```json
{
  "message": "hello",
  "age": 8,
  "email": "parent@example.com"
}
```

Response includes conversation replies and may also include a video link for learning topics.

## Recommended Improvements

- Add password hashing for user security.
- Persist game progress and conversation history per user.
- Use environment variables for secret keys and admin credentials.
- Expand topic detection and add more content categories.
- Add proper validation and error handling for frontend forms.

## Contact

For further improvements or support, update the project files directly and adjust the Flask/ FastAPI routes as needed.
