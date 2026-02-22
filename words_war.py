# words_war.py
# Streamlit-ready version (no input(), no while True, no notebook !pip, no merge markers)

import random
import string
from typing import Optional, Tuple

import streamlit as st

# Optional deps (installed via requirements.txt)
import nltk
from nltk.corpus import words as nltk_words

try:
    from deep_translator import GoogleTranslator
except Exception:
    GoogleTranslator = None  # translation becomes optional


# ---------- Setup / Helpers ----------

ALPHABET = {letter: idx + 1 for idx, letter in enumerate(string.ascii_lowercase)}


def ensure_nltk_words() -> None:
    """Ensure NLTK 'words' corpus exists (safe for cloud)."""
    try:
        nltk.data.find("corpora/words")
    except LookupError:
        nltk.download("words")


@st.cache_data(show_spinner=False)
def get_dictionary_set() -> set:
    """Cached dictionary set for fast app reloads."""
    ensure_nltk_words()
    return set(w.lower() for w in nltk_words.words())


def translate_to_arabic(word: str) -> str:
    """Best-effort translation; never crashes the app."""
    if GoogleTranslator is None:
        return "Translation unavailable (deep-translator not installed)"
    try:
        return GoogleTranslator(source="en", target="ar").translate(word)
    except Exception:
        return "Translation failed"


def validate_words(word1: str, word2: str, dictionary_set: Optional[set], enforce_dict: bool) -> Tuple[bool, str]:
    """Validate input; returns (ok, message)."""
    if not word1 or not word2:
        return False, "Please enter both words."

    w1 = word1.strip().lower()
    w2 = word2.strip().lower()

    if not w1.isalpha() or not w2.isalpha():
        return False, "No numbers or symbols are allowed."

    if len(w1) == 1 or len(w2) == 1:
        return False, "Enter a word, not a single letter."

    if len(w1) != len(w2):
        return False, "Words must be the same length."

    if enforce_dict and dictionary_set is not None:
        if w1 not in dictionary_set:
            return False, f'"{w1}" is not in the dictionary.'
        if w2 not in dictionary_set:
            return False, f'"{w2}" is not in the dictionary.'

    return True, ""


def play_round(word1: str, word2: str) -> dict:
    """Compute round details and scores."""
    w1 = word1.lower()
    w2 = word2.lower()

    round_score1 = 0
    round_score2 = 0
    comparisons = []

    for l1, l2 in zip(w1, w2):
        v1 = ALPHABET[l1]
        v2 = ALPHABET[l2]

        if v1 > v2:
            round_score1 += v1
            winner = "P1"
            points = v1
        elif v2 > v1:
            round_score2 += v2
            winner = "P2"
            points = v2
        else:
            winner = "DRAW"
            points = 0

        comparisons.append(
            {
                "l1": l1,
                "v1": v1,
                "l2": l2,
                "v2": v2,
                "winner": winner,
                "points": points,
            }
        )

    if round_score1 > round_score2:
        round_winner = "Player 1"
    elif round_score2 > round_score1:
        round_winner = "Player 2"
    else:
        round_winner = "Draw"

    return {
        "word1": w1,
        "word2": w2,
        "round_score1": round_score1,
        "round_score2": round_score2,
        "round_winner": round_winner,
        "comparisons": comparisons,
    }


def pick_ai_word(user_word: str, dictionary_set: set) -> Optional[str]:
    """Pick a random dictionary word with same length."""
    target_len = len(user_word)
    candidates = [w for w in dictionary_set if len(w) == target_len and w.isalpha()]
    if not candidates:
        return None
    return random.choice(candidates)


def init_state():
    if "total_p1" not in st.session_state:
        st.session_state.total_p1 = 0
    if "total_p2" not in st.session_state:
        st.session_state.total_p2 = 0
    if "history" not in st.session_state:
        st.session_state.history = []


def reset_scores():
    st.session_state.total_p1 = 0
    st.session_state.total_p2 = 0
    st.session_state.history = []


# ---------- UI ----------

st.set_page_config(page_title="Words War", page_icon="⚔️", layout="centered")
init_state()

st.title("⚔️ Words War")
st.caption("Compare letters by alphabet value (a=1 … z=26). Higher letter wins points.")

with st.sidebar:
    st.header("Settings")
    mode = st.radio("Mode", ["PVP (Player vs Player)", "VS AI"], index=0)

    enforce_dict = st.toggle("Enforce English dictionary (NLTK words)", value=True)
    enable_translation = st.toggle("Show Arabic translation", value=False)

    st.divider()
    if st.button("Reset scores", use_container_width=True):
        reset_scores()
        st.success("Scores reset.")

dictionary_set = None
if enforce_dict or mode == "VS AI":
    # We need dictionary for AI and/or validation
    with st.spinner("Loading dictionary..."):
        dictionary_set = get_dictionary_set()

st.subheader("Scoreboard")
colA, colB = st.columns(2)
colA.metric("Player 1", st.session_state.total_p1)
colB.metric("Player 2", st.session_state.total_p2)

st.divider()

if mode == "PVP (Player vs Player)":
    st.subheader("PVP Round")
    c1, c2 = st.columns(2)
    word1 = c1.text_input("Player 1 word", placeholder="e.g., tiger")
    word2 = c2.text_input("Player 2 word", placeholder="e.g., zebra")

    play = st.button("Play round", type="primary", use_container_width=True)

    if play:
        ok, msg = validate_words(word1, word2, dictionary_set, enforce_dict)
        if not ok:
            st.error(msg)
        else:
            result = play_round(word1, word2)
            st.session_state.total_p1 += result["round_score1"]
            st.session_state.total_p2 += result["round_score2"]
            st.session_state.history.insert(0, result)

            st.success(f"Round winner: {result['round_winner']}")
            st.write(f"Round score → P1: **{result['round_score1']}** | P2: **{result['round_score2']}**")

            with st.expander("See letter-by-letter breakdown", expanded=True):
                for row in result["comparisons"]:
                    if row["winner"] == "P1":
                        st.write(f"**{row['l1']}** ({row['v1']}) > {row['l2']} ({row['v2']}) → Player 1 +{row['points']}")
                    elif row["winner"] == "P2":
                        st.write(f"**{row['l2']}** ({row['v2']}) > {row['l1']} ({row['v1']}) → Player 2 +{row['points']}")
                    else:
                        st.write(f"{row['l1']} ({row['v1']}) = {row['l2']} ({row['v2']}) → No points")

            if enable_translation:
                st.subheader("Arabic Translation")
                st.write(f"{result['word1']} → **{translate_to_arabic(result['word1'])}**")
                st.write(f"{result['word2']} → **{translate_to_arabic(result['word2'])}**")

else:
    st.subheader("VS AI Round")
    word1 = st.text_input("Your word", placeholder="e.g., racism")

    play = st.button("Play vs AI", type="primary", use_container_width=True)

    if play:
        if not word1 or not word1.strip():
            st.error("Please enter your word.")
        else:
            w1 = word1.strip().lower()

            # Validate user word alone first (AI word will match length)
            if not w1.isalpha():
                st.error("No numbers or symbols are allowed.")
            elif len(w1) == 1:
                st.error("Enter a word, not a single letter.")
            elif enforce_dict and dictionary_set is not None and w1 not in dictionary_set:
                st.error(f'"{w1}" is not in the dictionary.')
            else:
                ai_word = pick_ai_word(w1, dictionary_set)
                if ai_word is None:
                    st.error("No matching word length found for the computer.")
                else:
                    st.info(f"Computer chose: **{ai_word}**")
                    result = play_round(w1, ai_word)
                    st.session_state.total_p1 += result["round_score1"]
                    st.session_state.total_p2 += result["round_score2"]
                    st.session_state.history.insert(0, result)

                    st.success(f"Round winner: {result['round_winner']}")
                    st.write(f"Round score → P1: **{result['round_score1']}** | P2: **{result['round_score2']}**")

                    with st.expander("See letter-by-letter breakdown", expanded=True):
                        for row in result["comparisons"]:
                            if row["winner"] == "P1":
                                st.write(f"**{row['l1']}** ({row['v1']}) > {row['l2']} ({row['v2']}) → Player 1 +{row['points']}")
                            elif row["winner"] == "P2":
                                st.write(f"**{row['l2']}** ({row['v2']}) > {row['l1']} ({row['v1']}) → Player 2 +{row['points']}")
                            else:
                                st.write(f"{row['l1']} ({row['v1']}) = {row['l2']} ({row['v2']}) → No points")

                    if enable_translation:
                        st.subheader("Arabic Translation")
                        st.write(f"{result['word1']} → **{translate_to_arabic(result['word1'])}**")
                        st.write(f"{result['word2']} → **{translate_to_arabic(result['word2'])}**")

st.divider()
st.subheader("Recent Rounds")
if not st.session_state.history:
    st.caption("No rounds played yet.")
else:
    for i, h in enumerate(st.session_state.history[:10], start=1):
        st.write(f"{i}. **{h['word1']}** vs **{h['word2']}** → P1 {h['round_score1']} | P2 {h['round_score2']} — *{h['round_winner']}*")