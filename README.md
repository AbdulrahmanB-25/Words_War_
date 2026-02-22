# ⚔️ Words War

A competitive word battle game built with **Python + Streamlit**.

Players enter words of equal length and compete letter-by-letter using alphabetical scoring (a=1 → z=26).  
The winner is determined by total letter strength.

Now powered by:

- ✅ `wordfreq` (modern English word list)
- ✅ Google Translate Arabic validation
- ✅ Streamlit UI
- ✅ Translation caching for performance
- ✅ AI word filtering with translation validation
- ✅ No external word file required

---

## 🚀 Live App

Play it here:

👉 https://wordswar-s656xzy6edrxbcbirb7pin.streamlit.app/

---

## 🎮 How It Works

### Word Validation
- Uses **wordfreq top 10,000 English words**
- Only clean `a–z` lowercase words are allowed
- No numbers or symbols
- Words must be the same length
- No single-letter words

### Letter Scoring

Each letter has a value:

```
a = 1
b = 2
...
z = 26
```

Each position is compared:

- Higher value letter wins
- Winner earns the full letter value
- Totals determine the round winner

---

## 🤖 AI Mode

When playing VS AI:

- AI selects a word of the same length
- AI word must:
  - Exist in the wordfreq dictionary
  - Have a valid Arabic translation
  - Contain actual Arabic characters
  - Not return the same English word

If translation fails, AI retries until a valid word is found.

---

## 🌍 Arabic Translation System

Each word is translated using:

```
deep-translator (Google Translate)
```

Validation rules:

- Translation must not be empty
- Must not match the original English word
- Must contain Arabic Unicode characters
- Uses caching to avoid repeated API calls

---

## 🧠 Technology Stack

- Python 3
- Streamlit
- wordfreq
- deep-translator

---


## 🔥 Features

- PVP Mode
- VS AI Mode
- Scoreboard with live totals
- Round history tracking
- Arabic translation toggle
- Clean modern UI
- Fully self-contained word dictionary
- Optimized for Streamlit Cloud deployment

---

## 🛠 Future Improvements

- Add AI difficulty levels (Easy / Hard)
- Add word definitions panel

---

## 👨‍💻 Author

[Abdulrahman B.](https://github.com/AbdulrahmanB-25)
[Mohammed](https://github.com/EngMohamed-op)
[Mohammed Alburaq](https://github.com/MohammedKQ)
[Nawaf](https://github.com/Nawaf-Alorabi)   


---


Choose your words wisely.  
Let the battle begin. ⚔️
