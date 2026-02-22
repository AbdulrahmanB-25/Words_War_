# -*- coding: utf-8 -*-
"""
Words War 
"""

import random
import string
import streamlit as st
from wordfreq import top_n_list
from deep_translator import GoogleTranslator


# ---------------- Dictionary (wordfreq) ----------------
@st.cache_data(show_spinner=False)
def load_dictionary_wordfreq(n_top=10000):
    raw_words = top_n_list("en", n_top)
    return set(
        w for w in raw_words
        if w and w.isalpha() and w.islower() and all(ch in string.ascii_lowercase for ch in w)
    )


web2lowerset = load_dictionary_wordfreq(10000)

# Alphabet scoring: a=1, b=2, ..., z=26
alphabet = {letter: index + 1 for index, letter in enumerate(string.ascii_lowercase)}


# ---------------- Translation + Validation ----------------
_translation_cache = {}

def translate_to_arabic_cached(word):
    word = word.lower()
    if word in _translation_cache:
        return _translation_cache[word]
    try:
        ar = GoogleTranslator(source="en", target="ar").translate(word)
    except:
        ar = None
    _translation_cache[word] = ar
    return ar
# Arabic uniblock
def contains_arabic(text):
    return any('\u0600' <= ch <= '\u06FF' for ch in text)

def is_good_arabic_translation(word, ar_text):
    if not ar_text or ar_text.strip() == "":
        return False
    ar_text = ar_text.strip()

    # If translation returns the same English word, reject
    if ar_text.lower() == word.lower():
        return False

    # Must contain Arabic characters
    if not contains_arabic(ar_text):
        return False

    return True


# ---------------- Game Class ----------------
class Game:
    def __init__(self):
        self.total_score_p1 = 0
        self.total_score_p2 = 0

    def play_round(self, word1, word2):
        word1 = word1.lower().strip()
        word2 = word2.lower().strip()

        # No numbers or symbols allowed
        if not word1.isalpha() or not word2.isalpha():
            return {"ok": False, "msg": "No numbers or symbols are allowed"}

        # Words must be same length
        if len(word1) != len(word2):
            return {"ok": False, "msg": "Words must be same length"}

        # Must be a word, not a single letter
        if len(word1) == 1 or len(word2) == 1:
            return {"ok": False, "msg": "Enter a word, not a single letter"}

        # Words must exist in dictionary (wordfreq)
        if word1 not in web2lowerset or word2 not in web2lowerset:
            missing = []
            if word1 not in web2lowerset: missing.append(word1)
            if word2 not in web2lowerset: missing.append(word2)
            return {"ok": False, "msg": "Not in dictionary: " + ", ".join(missing)}

        # ---------- Round Scoring ----------
        round_score1 = 0
        round_score2 = 0
        log_lines = []

        for l1, l2 in zip(word1, word2):
            value1 = alphabet[l1]
            value2 = alphabet[l2]

            if value1 > value2:
                round_score1 += value1
                log_lines.append(f"{l1} ({value1}) > {l2} ({value2}) ➜ Player 1 +{value1}")
            elif value2 > value1:
                round_score2 += value2
                log_lines.append(f"{l2} ({value2}) > {l1} ({value1}) ➜ Player 2 +{value2}")
            else:
                log_lines.append(f"{l1} ({value1}) = {l2} ({value2}) ➜ No points")

        self.total_score_p1 += round_score1
        self.total_score_p2 += round_score2

        if round_score1 > round_score2:
            winner = "Player 1"
        elif round_score2 > round_score1:
            winner = "Player 2"
        else:
            winner = "Draw"

        tr1 = translate_to_arabic_cached(word1)
        tr2 = translate_to_arabic_cached(word2)

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
            "tr1": tr1 if tr1 else "Translation failed",
            "tr2": tr2 if tr2 else "Translation failed",
        }

    def AI_OR_PVP(self, word1):
        word1 = word1.lower().strip()

        # Validate input
        if not word1.isalpha():
            return {"ok": False, "msg": "No numbers or symbols are allowed"}

        if len(word1) == 1:
            return {"ok": False, "msg": "Enter a word, not a single letter"}

        if word1 not in web2lowerset:
            return {"ok": False, "msg": f"{word1} not in dictionary"}

        # Filter words that match same length
        same_length_words = [w for w in web2lowerset if len(w) == len(word1)]

        if not same_length_words:
            return {"ok": False, "msg": "No matching word length found for computer"}

        # Pick a word that has a good Arabic translation
        max_tries = 50
        ai_word = None

        for _ in range(max_tries):
            candidate = random.choice(same_length_words)
            ar = translate_to_arabic_cached(candidate)
            if is_good_arabic_translation(candidate, ar):
                ai_word = candidate
                break

        if ai_word is None:
            return {"ok": False, "msg": "AI couldn't find a word with a good Arabic translation. Try again."}

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
