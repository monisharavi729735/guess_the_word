# 🎮 Guess The Word - Django Project

A Wordle-like game built with Django where players guess a random **5-letter word** within **5 attempts**.  
The app supports **two types of users**:  
- **Player** → Plays the guessing game (max 3 games per day).  
- **Admin** → Manages reports and words in the database.  

---

## 🚀 Features

### 👤 User Management
- User **registration & login** with validation:
  - Username must be **≥5 letters** (case insensitive).  
  - Password must be **≥5 characters** and include:
    - At least one **letter**  
    - At least one **number**  
    - At least one **special character** (`$`, `%`, `*`, `@`)  

- Players and Admins are assigned roles.  

### 🎲 Gameplay
- When a player starts a game:
  - A random **5-letter word** is chosen from the database.  
  - Player has **5 attempts** to guess it.  
  - Guesses are highlighted:
    - 🟩 **Green** → Correct letter, correct position.  
    - 🟧 **Orange** → Correct letter, wrong position.  
    - ⬜ **Grey** → Letter not in word.  
- Maximum **3 games per day** per user.  
- Game ends with **WIN** or **LOSE** message.  

### 📊 Reports (Admin Only)
- **Daily Report**:
  - Number of users played today  
  - Number of correct guesses (wins)  
  - Session details (player, word, status)  

- **User Report**:
  - Each user’s total games played  
  - Correct guesses count  
  - Dates when they played  

---

## 🛠️ Tech Stack
- **Backend**: Django 5.1.1
- **Database**: SQLite 
- **Frontend**: Bootstrap 5, Django Templates, HTML, CSS
- **Authentication**: Django’s built-in auth with custom `User` model