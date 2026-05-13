from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import json
import os
import re  # For regex parsing

# ------------------- FastAPI app -------------------
app = FastAPI(
    title="Jamie – Children's AI Buddy",
    description="Safe & Friendly AI API for Children",
    version="1.3"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- Users File -------------------
USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except json.JSONDecodeError:
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

# ------------------- Bad words -------------------
BAD_WORDS = ["stupid", "dumb", "idiot", "fool", "lazy", "nonsense", "silly", "crazy", "ugly", "weird", "noob"]

def is_safe(msg):
    for word in BAD_WORDS:
        if word in msg:
            return False
    return True

# ------------------- Chat Request -------------------
class ChatRequest(BaseModel):
    message: str
    age: int
    email: str  # 👈 Email from frontend

# ------------------- YouTube Links -------------------
MATH_LINKS = [
    "https://youtu.be/zDqnWRmG2SI?si=rIrOwO2sJMsLUBzJ",
    "https://youtu.be/4ce6s_eHFKo?si=SrwB4ukqGD7EVt39",
    "https://youtu.be/S9N9Sly9DFw?si=GutIPoekiJG9nLnP",
    "https://youtu.be/vPPDu23aibw?si=bXuWDNMGnS3RO2nd",
    "https://youtu.be/c8zwOreeACU?si=0qoH4XIzuGp7xsuy",
    "https://youtu.be/ickBvCbYpCE?si=t1m2p_z5BMfkpaRS",
    "https://youtu.be/JHrgYLv8DV8?si=x5LNgX19I6qEfTFR",
    "https://youtu.be/pi3L8bw_t5Q?si=l8DTNh9vZu51KYw",
    "https://youtu.be/rr2n6BJYmos?si=EBYn9D1UewTW7Ar8",
    "https://youtu.be/iqkAVUDdygM?si=-rhNxRLxsEr1r3pz",
    "https://youtu.be/BveGX9MsW-c?si=LfXKJT9F5BHCRJYM",
    "https://youtu.be/7D4K9oi7oBM?si=EVTYDDkOQwtk-dp6",
    "https://youtu.be/jlzX8jt0Now?si=gKuBhHUMF8dlAz7_"
]
English = [
    "https://youtu.be/hq3yfQnllfQ?si=mO_pcJmnSgwf8ksI",
    "https://youtu.be/I_3mbra4dHU?si=tcrtwpNQlU3310Qe",
    "https://youtu.be/LAqLBOh3Ric?si=6-pfMq-kqAppPlBG",
    "https://youtu.be/tRj1AKjdmHs?si=6uprNZEJu_P7mFcP",
    "https://youtu.be/4ncLB3JPy_w?si=iXK4UFEpw9jiWw63",
    "https://youtu.be/gAy54zq7fck?si=dIHe9q6ZrFzh3meY",
    "https://youtu.be/KJem0WLap5c?si=E6X5QntgCBLb-_SS",
    "https://youtu.be/l4dCByK0TN4?si=AAFdbQ7aMgzjLU2z"
]
Science = [
    "https://youtu.be/q1xNuU7gaAQ?si=ksBXHjqUAG--rP8m",
    "https://youtu.be/ndDpjT0_IM0?si=4e2BDUZZg33HDoDJ",
    "https://youtu.be/d7yTlp4gBTI?si=Vsw_l8WlJjVG9_lh",
    "https://youtu.be/BEdfwxKCSPc?si=va_h7pNK02FafdPJ",
    "https://youtu.be/n1jC9BGzKfk?si=v0NAaHdRqIXfAqIy",
    "https://youtu.be/ErUZVWUP0c4?si=brfWCOGG-uvgNnho"
]
Manners = [
    "https://youtu.be/TPhabSkn3sM?si=M1VvqObCjDUVpSTY",
    "https://youtu.be/TPhabSkn3sM?si=rWKCnRyvUaAwDW6Z",
    "https://youtu.be/41VMA4rp9bs?si=JPiA3ZyFEdkdlUoe",
    "https://youtu.be/UgLrsqlGA3U?si=PiJms9f0EH0kTpgW",
    "https://youtu.be/o1gJXpzoMqY?si=JJlMAYwgKc0aa3X6",
    "https://youtu.be/ZbSZCBYKfHk?si=BtdHl3mjETtRmv1g"
]
Poem = [
    "https://youtu.be/ygcN65SlLFg?si=czZ3X2kRVMtjPKSF",
    "https://youtu.be/q84zMUrvOiQ?si=0bGnhoAWQm2kOaQl",
    "https://youtu.be/hqzvHfy-Ij0?si=1XxDiH8X7VVm5Imo",
    "https://youtu.be/Zu6o23Pu0Do?si=iAHUNJq8-XWEa-Qo",
    "https://youtu.be/ygcN65SlLFg?si=FzjpHROBt9sh97KH",
    "https://youtu.be/e_04ZrNroTo?si=GuAUh1-1sp7Dbssa",
    "https://youtu.be/i7ygKQunfmE?si=0zvmh58ZitsFjw9a"
]
Computer = [
    "https://youtu.be/67TNabOXBc8?si=JUFS1C5sRDm4OG1A",
    "https://youtu.be/QtDAzhiTXC4?si=xYLE_YhtpU7JdP9i",
    "https://youtu.be/HFMtfBbJxjI?si=73JZ3VqDy27Tvtzc",
    "https://youtu.be/Wchru8alhaE?si=D1PUvYp9I5WdvdwO",
    "https://youtu.be/UXsomnDkntI?si=5ea6ECV0UBXjZdTl"
]
Isl = [
    "https://youtu.be/d2D6WuKlymM?si=3hHwy8O6hb8BeO_T",
    "https://youtu.be/xxnZuAHCAjY?si=tYspHmHP3q9JmZJW",
    "https://youtu.be/WEEORXFj-lo?si=O9Ikq9c9fArF9jfi",
    "https://youtu.be/a_DYze3dnk4?si=ih-khnk-vtBc42ff",
    "https://youtu.be/_TAQylisi5M?si=Fr0boaViAbm4U3sj",
]  # Islamic story placeholder
Fav = [
    "https://youtu.be/g3yG6rU9Uys?si=gqh8mchnDQ7gIXA5",
    "https://youtu.be/uv3VXLVK6FQ?si=H03rfUrkoPqh8khj",
    "https://youtu.be/u7Ny0Scq9_w?si=UgGZ3FT39LoRKcMw",
    "https://youtu.be/BRp2IalJzNQ?si=aRLW7sIBxLlJ8T6D",
    "https://youtu.be/COH6McIjZlA?si=AD_ZLOp-WfQv3xPG",
    "https://youtu.be/Dai9lZ4Sne0?si=ofjXU4xPwotfxsDM"
]
# ----------- Games tracking for single user -----------
ONGOING_RPS = False
ONGOING_GUESS = None  # number to guess

# ------------------- Chat Endpoint -------------------
@app.post("/chat")
def chat(req: ChatRequest):
    global ONGOING_RPS, ONGOING_GUESS

    msg = req.message.lower()
    user_age = req.age
    email = req.email
    reply_prefix = "Hey little buddy" if user_age < 8 else "Hi there!"

    # Load users
    users = load_users()

    # Initialize user if new
    if email in users:
        stars = users[email].get("stars", 0)
        users[email]["age"] = user_age
    else:
        users[email] = {"name": "Unknown", "age": user_age, "stars": 0}
        stars = 0

    # Bad words check
    if not is_safe(msg):
        return {"reply": "Let's use kind words! We learn better when we are respectful.", "stars": stars}

    # ---------- Stop command ----------
    if msg == "stop":
        ONGOING_RPS = False
        ONGOING_GUESS = None
        return {"reply": "Game stopped. Let's continue learning!", "stars": stars}

    # ---------- Rock-Paper-Scissors ----------
    RPS_OPTIONS = ["rock", "paper", "scissors"]
    if "rock-paper-scissors" in msg or "rps" in msg:
        ONGOING_RPS = True
        return {"reply": reply_prefix + " You want to play Rock-Paper-Scissors game! Type rock, paper, or scissors to play.", "stars": stars}

    if ONGOING_RPS and msg in RPS_OPTIONS:
        ai_choice = random.choice(RPS_OPTIONS)
        if msg == ai_choice:
            result = "It's a tie! Every tie teaches balance—sometimes learning is more important than winning."
        elif (msg == "rock" and ai_choice == "scissors") or \
             (msg == "paper" and ai_choice == "rock") or \
             (msg == "scissors" and ai_choice == "paper"):
            result = "You win! Remember, every success is a lesson—celebrate it and keep growing."
        else:
            result = "I won! But true growth is in playing the game, not just winning"

        ONGOING_RPS = False
        return {"reply": reply_prefix + f" I chose {ai_choice}. {result}"}

    # ---------- Guess the Number ----------
    if "guess the number" in msg or "gtn" in msg:
        ONGOING_GUESS = random.randint(1, 20)
        return {"reply": reply_prefix + " Let's play Guess the Number! I picked a number between 1 and 20, try to guess it!", "stars": stars}

    if ONGOING_GUESS is not None:
        if msg.isdigit():
            guess = int(msg)
            if guess < ONGOING_GUESS:
                return {"reply": reply_prefix + " Too low! Keep trying."}
            elif guess > ONGOING_GUESS:
                return {"reply": reply_prefix + " Too high! Keep trying."}
            else:
                ONGOING_GUESS = None
                return {"reply": reply_prefix + f" Correct! The number was {guess}."}
        else:
            return {"reply": reply_prefix + " Please enter a number between 1 and 20."}

    # ---------- Addition check ----------
    addition_match = re.match(r"^\s*(\d+)\s*\+\s*(\d+)\s*$", msg)
    if addition_match:
        a = int(addition_match.group(1))
        b = int(addition_match.group(2))
        result = a + b
        return {"reply": f"{reply_prefix} Lets calculate! {a} apple + {b} apple = {result} apple", "calculated": True}

    # ---------- Learning Topics ----------
    if "hello" in msg or "hi" in msg:
        return {"reply": reply_prefix + " I'm Jamie. I'm proud of you for learning today!"}
    elif "math" in msg:
        return {"reply": reply_prefix + " Math is fun! Let's learn together.", "video_link": random.choice(MATH_LINKS)}
    elif "computer" in msg or "technology" in msg:
        return {"reply": reply_prefix + " Computer is fun! Let's learn together about Computers and Technology.", "video_link": random.choice(Computer)}
    elif "english" in msg:
        return {"reply": reply_prefix + " English is fun! Let's learn together.", "video_link": random.choice(English)}
    elif "science" in msg:
        return {"reply": reply_prefix + " Science is awesome! Let's explore together.", "video_link": random.choice(Science)}
    elif "manners" in msg or "manner" in msg:
        return {"reply": reply_prefix + " Let's learn manners! Important for everyone.", "video_link": random.choice(Manners)}
    elif "poem" in msg or "poems" in msg:
        return {"reply": reply_prefix + " Let's enjoy some poems together.", "video_link": random.choice(Poem)}
    elif "islamic story" in msg or "holy story" in msg or "story" in msg:
        return {"reply": reply_prefix + " I have an interesting story for you!", "video_link": random.choice(Isl)}
    elif "islamic" in msg or "holy" in msg or "dua" in msg or "surah" in msg:
        return {"reply": reply_prefix + " Let's gain some Islamic knowledge, because the real wealth is knowledge of Allah and His guidance!", "video_link": random.choice(Fav)}
    elif "happy" in msg or "excited" in msg:
        return {"reply": reply_prefix + " I'm happy to know that you're feeling good and you're happy."}
    elif "sad" in msg:
        return {"reply": reply_prefix + " I'm sorry you're feeling sad. You're not alone."}
    elif "angry" in msg:
        return {"reply": reply_prefix + " It's okay to feel angry sometimes. Let's take a deep breath together."}
    elif "abc" in msg or "abcd" in msg or "alphabet" in msg:
        return {
            "reply": reply_prefix + " Let's learn alphabets",
        }
    elif "123" in msg or "count" in msg or "counting" in msg:
        return {
            "reply": reply_prefix + " Let's learn counting",
        }
    elif "piano" in msg or "PIANO" in msg:
        return {
            "reply": reply_prefix + " Let's play piano",
        }
    # ------------------- Multiplication / Table -------------------
    table_match = re.search(r"\btable of (\d+)\b", msg)  # "table of 2"
    mul_match = re.search(r"\b(\d+)\s*[\*xX]\s*\d+\b", msg)  # "2 x 1", "2 * 1"

    if table_match:
        table_num = int(table_match.group(1))
        return {
            "reply": f"{reply_prefix} Let's learn the table of {table_num}!"
        }

    elif mul_match:
        table_num = int(mul_match.group(1))
        return {
            "reply": f"{reply_prefix} Let's learn the table of {table_num}!"
        }

    else:
        return {"reply": reply_prefix + " Great thinking! Can you tell me more?"}

