# -*- coding: utf-8 -*-
"""
Words War - Streamlit version (minimal changes from original code)
"""

import random
import nltk
from nltk.corpus import words
from deep_translator import GoogleTranslator
import string
import streamlit as st


# ---------- Ensure NLTK words corpus is available ----------
def ensure_words_corpus():
    try:
        nltk.data.find("corpora/words")
    except LookupError:
        nltk.download("words")


@st.cache_data(show_spinner=False)
def load_dictionary():
    ensure_words_corpus()
    return set(w.lower() for w in words.words())


web2lowerset = load_dictionary()

# Alphabet scoring: a=1, b=2, ..., z=26
alphabet = {letter: index + 1 for index, letter in enumerate(string.ascii_lowercase)}


# Translate English word to Arabic
def translate_to_arabic(word):
    try:
        return GoogleTranslator(source="en", target="ar").translate(word)
    except:
        return "Translation failed"


# ---------------- Game Class ----------------
class Game:
    def __init__(self):
        # Store cumulative scores
        self.total_score_p1 = 0
        self.total_score_p2 = 0

    def play_round(self, word1, word2):
        # Normalize input to lowercase
        word1 = word1.lower()
        word2 = word2.lower()

        # ---------- Validation Rules ----------

        # No numbers or symbols allowed
        if not word1.isalpha() or not word2.isalpha():
            return {"ok": False, "msg": "No numbers or symbols are allowed"}

        # Words must be same length
        if len(word1) != len(word2):
            return {"ok": False, "msg": "Words must be same length"}

        # Words must exist in dictionary
        if word1 not in web2lowerset or word2 not in web2lowerset:
            return {"ok": False, "msg": f"{word1} not in dictionary"}

        # Must be a word, not a single letter
        if len(word1) == 1 or len(word2) == 1:
            return {"ok": False, "msg": "Enter a word, not a single letter"}

        # ---------- Round Scoring ----------
        round_score1 = 0
        round_score2 = 0
        log_lines = []

        # Compare letters position by position
        for l1, l2 in zip(word1, word2):
            value1 = alphabet[l1]
            value2 = alphabet[l2]

            if value1 > value2:
                round_score1 += value1
                log_lines.append(
                    f"{l1} ({value1}) > {l2} ({value2}) ➜ Player 1 +{value1}"
                )

            elif value2 > value1:
                round_score2 += value2
                log_lines.append(
                    f"{l2} ({value2}) > {l1} ({value1}) ➜ Player 2 +{value2}"
                )

            else:
                log_lines.append(
                    f"{l1} ({value1}) = {l2} ({value2}) ➜ No points"
                )

        # Update total scores
        self.total_score_p1 += round_score1
        self.total_score_p2 += round_score2

        # Determine round winner
        if round_score1 > round_score2:
            winner = "Player 1"
        elif round_score2 > round_score1:
            winner = "Player 2"
        else:
            winner = "Draw"

        return {
            "ok": True,
            "word1": word1,
            "word2": word2,
            "round_score1": round_score1,
            "round_score2": round_score2,
            "winner": winner,
            "total_p1": self.total_score_p1,
            "total_p2": self.total_score_p2,
            "log": log_lines,
            "tr1": translate_to_arabic(word1),
            "tr2": translate_to_arabic(word2),
        }

    # Play against computer
    def AI_OR_PVP(self, word1):
        word1 = word1.lower()

        # Filter words that match the same length
        same_length_words = list(
            filter(lambda w: len(w) == len(word1), web2lowerset)
        )

        if not same_length_words:
            return {"ok": False, "msg": "No matching word length found for computer"}

        ai_word = random.choice(same_length_words)
        result = self.play_round(word1, ai_word)

        if result.get("ok"):
            result["ai_word"] = ai_word

        return result


# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Words War", page_icon="⚔️", layout="centered")
st.title("⚔️ Words War")
st.markdown(
    """
**Welcome to Words War!**  
A fun and interactive game where players battle using words.  
Compare letters, score points, and learn new words with translations!  
""",
    unsafe_allow_html=True
)

# Store game object in session state
if "game" not in st.session_state:
    st.session_state.game = Game()

game = st.session_state.game

# Choose mode
mode = st.radio("Choose mode:", ["PVP", "VS AI"], horizontal=True)

# Display total scores
col1, col2 = st.columns(2)
col1.metric("Player 1 Total", game.total_score_p1)
col2.metric("Player 2 Total", game.total_score_p2)

st.divider()

show_translation = st.toggle("Show Arabic translation", value=True)

if mode == "PVP":
    w1 = st.text_input("Enter Word 1 (Player 1)")
    w2 = st.text_input("Enter Word 2 (Player 2)")

    if st.button("Play Round", type="primary"):
        result = game.play_round(w1.strip(), w2.strip())

        if not result["ok"]:
            st.error(result["msg"])
        else:
            st.success(f"Round Winner: {result['winner']}")
            st.write(
                f"Round Score → P1: **{result['round_score1']}** | "
                f"P2: **{result['round_score2']}**"
            )
            st.write(
                f"TOTAL SCORE → P1: **{result['total_p1']}** | "
                f"P2: **{result['total_p2']}**"
            )

            with st.expander("Letter-by-letter details", expanded=True):
                for line in result["log"]:
                    st.write(line)

            if show_translation:
                st.subheader("Arabic Translation")
                st.write(f"{result['word1']} → **{result['tr1']}**")
                st.write(f"{result['word2']} → **{result['tr2']}**")

else:
    w1 = st.text_input("Enter Word (You)")

    if st.button("Play VS AI", type="primary"):
        result = game.AI_OR_PVP(w1.strip())

        if not result["ok"]:
            st.error(result["msg"])
        else:
            st.info(f"Computer chose: **{result['ai_word']}**")
            st.success(f"Round Winner: {result['winner']}")
            st.write(
                f"Round Score → P1: **{result['round_score1']}** | "
                f"P2: **{result['round_score2']}**"
            )
            st.write(
                f"TOTAL SCORE → P1: **{result['total_p1']}** | "
                f"P2: **{result['total_p2']}**"
            )

            with st.expander("Letter-by-letter details", expanded=True):
                for line in result["log"]:
                    st.write(line)

            if show_translation:
                st.subheader("Arabic Translation")
                st.write(f"{result['word1']} → **{result['tr1']}**")
                st.write(f"{result['word2']} → **{result['tr2']}**")

st.divider()

# Reset game
if st.button("Reset Game"):
    st.session_state.game = Game()
    st.rerun()
