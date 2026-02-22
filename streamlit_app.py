{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "execution_count": 19,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "d1NzgOzBuCk8",
        "outputId": "d90a7415-fa79-41ac-999b-5fd373a8938b"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: streamlit in /usr/local/lib/python3.12/dist-packages (1.54.0)\n",
            "Requirement already satisfied: pyngrok in /usr/local/lib/python3.12/dist-packages (7.5.0)\n",
            "Requirement already satisfied: deep-translator in /usr/local/lib/python3.12/dist-packages (1.11.4)\n",
            "Requirement already satisfied: nltk in /usr/local/lib/python3.12/dist-packages (3.9.1)\n",
            "Requirement already satisfied: altair!=5.4.0,!=5.4.1,<7,>=4.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (5.5.0)\n",
            "Requirement already satisfied: blinker<2,>=1.5.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (1.9.0)\n",
            "Requirement already satisfied: cachetools<7,>=5.5 in /usr/local/lib/python3.12/dist-packages (from streamlit) (6.2.6)\n",
            "Requirement already satisfied: click<9,>=7.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (8.3.1)\n",
            "Requirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in /usr/local/lib/python3.12/dist-packages (from streamlit) (3.1.46)\n",
            "Requirement already satisfied: numpy<3,>=1.23 in /usr/local/lib/python3.12/dist-packages (from streamlit) (2.0.2)\n",
            "Requirement already satisfied: packaging>=20 in /usr/local/lib/python3.12/dist-packages (from streamlit) (26.0)\n",
            "Requirement already satisfied: pandas<3,>=1.4.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (2.2.2)\n",
            "Requirement already satisfied: pillow<13,>=7.1.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (11.3.0)\n",
            "Requirement already satisfied: pydeck<1,>=0.8.0b4 in /usr/local/lib/python3.12/dist-packages (from streamlit) (0.9.1)\n",
            "Requirement already satisfied: protobuf<7,>=3.20 in /usr/local/lib/python3.12/dist-packages (from streamlit) (5.29.6)\n",
            "Requirement already satisfied: pyarrow>=7.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (18.1.0)\n",
            "Requirement already satisfied: requests<3,>=2.27 in /usr/local/lib/python3.12/dist-packages (from streamlit) (2.32.4)\n",
            "Requirement already satisfied: tenacity<10,>=8.1.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (9.1.4)\n",
            "Requirement already satisfied: toml<2,>=0.10.1 in /usr/local/lib/python3.12/dist-packages (from streamlit) (0.10.2)\n",
            "Requirement already satisfied: tornado!=6.5.0,<7,>=6.0.3 in /usr/local/lib/python3.12/dist-packages (from streamlit) (6.5.1)\n",
            "Requirement already satisfied: typing-extensions<5,>=4.10.0 in /usr/local/lib/python3.12/dist-packages (from streamlit) (4.15.0)\n",
            "Requirement already satisfied: watchdog<7,>=2.1.5 in /usr/local/lib/python3.12/dist-packages (from streamlit) (6.0.0)\n",
            "Requirement already satisfied: PyYAML>=5.1 in /usr/local/lib/python3.12/dist-packages (from pyngrok) (6.0.3)\n",
            "Requirement already satisfied: beautifulsoup4<5.0.0,>=4.9.1 in /usr/local/lib/python3.12/dist-packages (from deep-translator) (4.13.5)\n",
            "Requirement already satisfied: joblib in /usr/local/lib/python3.12/dist-packages (from nltk) (1.5.3)\n",
            "Requirement already satisfied: regex>=2021.8.3 in /usr/local/lib/python3.12/dist-packages (from nltk) (2025.11.3)\n",
            "Requirement already satisfied: tqdm in /usr/local/lib/python3.12/dist-packages (from nltk) (4.67.3)\n",
            "Requirement already satisfied: jinja2 in /usr/local/lib/python3.12/dist-packages (from altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (3.1.6)\n",
            "Requirement already satisfied: jsonschema>=3.0 in /usr/local/lib/python3.12/dist-packages (from altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (4.26.0)\n",
            "Requirement already satisfied: narwhals>=1.14.2 in /usr/local/lib/python3.12/dist-packages (from altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (2.16.0)\n",
            "Requirement already satisfied: soupsieve>1.2 in /usr/local/lib/python3.12/dist-packages (from beautifulsoup4<5.0.0,>=4.9.1->deep-translator) (2.8.3)\n",
            "Requirement already satisfied: gitdb<5,>=4.0.1 in /usr/local/lib/python3.12/dist-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit) (4.0.12)\n",
            "Requirement already satisfied: python-dateutil>=2.8.2 in /usr/local/lib/python3.12/dist-packages (from pandas<3,>=1.4.0->streamlit) (2.9.0.post0)\n",
            "Requirement already satisfied: pytz>=2020.1 in /usr/local/lib/python3.12/dist-packages (from pandas<3,>=1.4.0->streamlit) (2025.2)\n",
            "Requirement already satisfied: tzdata>=2022.7 in /usr/local/lib/python3.12/dist-packages (from pandas<3,>=1.4.0->streamlit) (2025.3)\n",
            "Requirement already satisfied: charset_normalizer<4,>=2 in /usr/local/lib/python3.12/dist-packages (from requests<3,>=2.27->streamlit) (3.4.4)\n",
            "Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.12/dist-packages (from requests<3,>=2.27->streamlit) (3.11)\n",
            "Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.12/dist-packages (from requests<3,>=2.27->streamlit) (2.5.0)\n",
            "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.12/dist-packages (from requests<3,>=2.27->streamlit) (2026.1.4)\n",
            "Requirement already satisfied: smmap<6,>=3.0.1 in /usr/local/lib/python3.12/dist-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit) (5.0.2)\n",
            "Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.12/dist-packages (from jinja2->altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (3.0.3)\n",
            "Requirement already satisfied: attrs>=22.2.0 in /usr/local/lib/python3.12/dist-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (25.4.0)\n",
            "Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /usr/local/lib/python3.12/dist-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (2025.9.1)\n",
            "Requirement already satisfied: referencing>=0.28.4 in /usr/local/lib/python3.12/dist-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (0.37.0)\n",
            "Requirement already satisfied: rpds-py>=0.25.0 in /usr/local/lib/python3.12/dist-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<7,>=4.0->streamlit) (0.30.0)\n",
            "Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.12/dist-packages (from python-dateutil>=2.8.2->pandas<3,>=1.4.0->streamlit) (1.17.0)\n"
          ]
        }
      ],
      "source": [
        "!pip install streamlit pyngrok deep-translator nltk"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from pyngrok import ngrok\n",
        "\n",
        "ngrok.set_auth_token(\"39wLzKc2JFm7cxxyRSneVAm47Hz_3Nb8Xgie2zVLRMveGFeSG\")"
      ],
      "metadata": {
        "id": "5EBSzF0uuq-p"
      },
      "execution_count": 20,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "%%writefile app.py\n",
        "import streamlit as st\n",
        "import random\n",
        "import string\n",
        "import nltk\n",
        "from nltk.corpus import words\n",
        "from deep_translator import GoogleTranslator\n",
        "\n",
        "@st.cache_resource\n",
        "def load_dictionary():\n",
        "    nltk.download('words')\n",
        "    return set(w.lower() for w in words.words())\n",
        "\n",
        "web2lowerset = load_dictionary()\n",
        "\n",
        "alphabet = {letter: index+1 for index, letter in enumerate(string.ascii_lowercase)}\n",
        "\n",
        "def translate_to_arabic(word):\n",
        "    try:\n",
        "        return GoogleTranslator(source='en', target='ar').translate(word)\n",
        "    except:\n",
        "        return \"Translation failed\"\n",
        "\n",
        "class Game():\n",
        "    def __init__(self):\n",
        "        self.total_score_p1 = 0\n",
        "        self.total_score_p2 = 0\n",
        "\n",
        "    def play_round(self, word1, word2):\n",
        "        word1 = word1.lower()\n",
        "        word2 = word2.lower()\n",
        "\n",
        "        if len(word1) == 1 or len(word2) == 1:\n",
        "            st.error(\"Single letter is not allowed\")\n",
        "            return\n",
        "\n",
        "        if len(word1) != len(word2):\n",
        "            st.error(\"Words must be same length\")\n",
        "            return\n",
        "\n",
        "        if word1 not in web2lowerset or word2 not in web2lowerset:\n",
        "            st.error(\"Word not in dictionary\")\n",
        "            return\n",
        "\n",
        "        round_score1 = 0\n",
        "        round_score2 = 0\n",
        "\n",
        "        st.subheader(f\"{word1} VS {word2}\")\n",
        "\n",
        "        for l1, l2 in zip(word1, word2):\n",
        "            value1 = alphabet[l1]\n",
        "            value2 = alphabet[l2]\n",
        "\n",
        "            if value1 > value2:\n",
        "                round_score1 += value1\n",
        "                st.write(f\"{l1}({value1}) > {l2}({value2}) ➜ Player 1 +{value1}\")\n",
        "\n",
        "            elif value2 > value1:\n",
        "                round_score2 += value2\n",
        "                st.write(f\"{l2}({value2}) > {l1}({value1}) ➜ Player 2 +{value2}\")\n",
        "\n",
        "            else:\n",
        "                st.write(f\"{l1}({value1}) = {l2}({value2}) ➜ No points\")\n",
        "\n",
        "        self.total_score_p1 += round_score1\n",
        "        self.total_score_p2 += round_score2\n",
        "\n",
        "        st.divider()\n",
        "        st.write(f\"Round Score → P1: {round_score1} | P2: {round_score2}\")\n",
        "\n",
        "        if round_score1 > round_score2:\n",
        "            st.success(\"Round Winner: Player 1\")\n",
        "        elif round_score2 > round_score1:\n",
        "            st.success(\"Round Winner: Player 2\")\n",
        "        else:\n",
        "            st.info(\"Round Draw\")\n",
        "\n",
        "        st.write(\"### TOTAL SCORE\")\n",
        "        st.write(f\"Player 1: {self.total_score_p1}\")\n",
        "        st.write(f\"Player 2: {self.total_score_p2}\")\n",
        "\n",
        "        st.write(\"### Arabic Translation\")\n",
        "        st.write(f\"{word1} → {translate_to_arabic(word1)}\")\n",
        "        st.write(f\"{word2} → {translate_to_arabic(word2)}\")\n",
        "\n",
        "st.title(\"🔥 Words War Game\")\n",
        "\n",
        "if \"game\" not in st.session_state:\n",
        "    st.session_state.game = Game()\n",
        "\n",
        "mode = st.radio(\n",
        "    \"Choose Game Mode\",\n",
        "    [\"Player vs Player\", \"Player vs Computer\"]\n",
        ")\n",
        "\n",
        "word1 = st.text_input(\"Enter first Word\")\n",
        "\n",
        "if mode == \"Player vs Player\":\n",
        "    word2 = st.text_input(\"Enter second Word\")\n",
        "else:\n",
        "    word2 = \"\"\n",
        "\n",
        "col1, col2 = st.columns(2)\n",
        "\n",
        "with col1:\n",
        "    play = st.button(\"▶️ Play Round\")\n",
        "\n",
        "with col2:\n",
        "    new_game = st.button(\"🔄 New Game (Reset Score)\")\n",
        "\n",
        "if new_game:\n",
        "    st.session_state.game = Game()\n",
        "    st.success(\"Game Reset! Scores cleared.\")\n",
        "\n",
        "if play:\n",
        "    if not word1:\n",
        "        st.warning(\"Enter your word first\")\n",
        "    else:\n",
        "        if mode == \"Player vs Computer\":\n",
        "            same_length_words = [w for w in web2lowerset if len(w) == len(word1)]\n",
        "            if same_length_words:\n",
        "                word2 = random.choice(same_length_words)\n",
        "                st.info(f\"Computer chose: {word2}\")\n",
        "            else:\n",
        "                st.error(\"No words found with same length\")\n",
        "                st.stop()\n",
        "\n",
        "        if word1 and word2:\n",
        "            st.session_state.game.play_round(word1, word2)\n",
        "\n",
        "st.divider()\n",
        "st.write(\"## 🏆 Current Total Score\")\n",
        "st.write(f\"Player 1: {st.session_state.game.total_score_p1}\")\n",
        "st.write(f\"Player 2: {st.session_state.game.total_score_p2}\")"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "xhdWe_6VuKlv",
        "outputId": "6bd86f29-a4d6-4c59-a920-08559ac02115"
      },
      "execution_count": 21,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Overwriting app.py\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import subprocess, time\n",
        "from pyngrok import ngrok\n",
        "\n",
        "process = subprocess.Popen([\"streamlit\", \"run\", \"app.py\"])\n",
        "\n",
        "time.sleep(10)\n",
        "\n",
        "public_url = ngrok.connect(8501)\n",
        "print(\"🔗open the link\", public_url)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "XmU2Ccv5vrb8",
        "outputId": "4e43284a-dd41-47c0-edeb-1d2772eaf000"
      },
      "execution_count": 22,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "🔗open the link NgrokTunnel: \"https://farinose-muriel-flickeringly.ngrok-free.dev\" -> \"http://localhost:8501\"\n"
          ]
        }
      ]
    }
  ]
}