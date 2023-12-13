import streamlit as st
import pandas as pd
import numpy as np
import chess
import chess.svg
import chess.pgn
import matplotlib.pyplot as plt
from stockfish import Stockfish
from load_chessmatch import open_match

import random
from PIL import Image
from io import BytesIO

st.title('Chess Upsets - Pawn to Power')
engine = chess.engine.SimpleEngine.popen_uci(r"C:/Users/Jhon/stockfish/stockfish-windows-x86-64-avx2")

RAW_DATA_URL = 'chess_df.csv'
UPSET_DATA = 'upset_dataset.csv'


@st.cache_data
def load_data(DATA, nrows):
    data = pd.read_csv(DATA, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data


# gets both datasets
raw_df = load_data(RAW_DATA_URL, 20000)  # dataset has ~20000
upset_df = load_data(UPSET_DATA, 10000)


# Intro
top_white = None
top_black = None

st.header("Let us start off, ***THESE ARE THE SPARTANS!***")

col1, col2 = st.columns(2)
with col1:
    white = upset_df.query("(winner == 'white' and white_rating < black_rating)")
    most_upsets = white["white_id"].value_counts()
    st.header("White Players")
    top_white = most_upsets[:5]
    st.write(top_white)

with col2:
    black = upset_df.query("(winner == 'black' and white_rating > black_rating)")
    most_upsets1 = black["black_id"].value_counts()
    st.header("Black Players")
    top_black = most_upsets1[:5]
    st.write(top_black)

my_expander = st.expander(label='A little more details on the top 4 players')
with my_expander:
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    with col1:
        name = top_white.index[0]
        st.write(f"{name}:")
        openings = upset_df.query(f"white_id == '{name}' or black_id == '{name}'")
        st.write(openings["opening_name"])
        st.write(openings["victory_status"])
    with col2:
        name = top_white.index[1]
        st.write(f"{name}:")
        openings = upset_df.query(f"white_id == '{name}' or black_id == '{name}'")
        st.write(openings["opening_name"])
        st.write(openings["victory_status"])
    with col3:
        name = top_black.index[0]
        st.write(f"{name}:")
        openings = upset_df.query(f"white_id == '{name}' or black_id == '{name}'")
        st.write(openings["opening_name"])
        st.write(openings["victory_status"])
    with col4:
        name = top_black.index[1]
        st.write(f"{name}:")
        openings = upset_df.query(f"white_id == '{name}' or black_id == '{name}'")
        st.write(openings["opening_name"])
        st.write(openings["victory_status"])

st.header("Some context")
st.subheader("Chess ratings are given to chess players to estimate the *strength of the player* based on"
             " previous matches against other players")
text = """
2700+	sometimes informally called super grandmasters\n
2500–2700	most Grandmasters (GM)\n
2400–2500	most International Masters (IM) and some Grandmasters (GM)\n
2300–2400	most FIDE Masters (FM) and some International Masters (IM)\n
2200–2300	FIDE Candidate Masters (CM), most national masters (NM)\n
2000–2200	Candidate masters (CM)\n
1800–2000	Class A, category 1\n
1600–1800	Class B, category 2\n
1400–1600	Class C, category 3\n
1200–1400	Class D, category 4\n
1000–1200	Class E, category 5\n
Below 1000	Novices
"""
st.write(text)

st.image("category.PNG")

st.header("What are upsets?")
st.markdown("From Wikipedia: An upset occurs in a competition, frequently in electoral politics or sports, "
            "when the **party expected to win is defeated by an underdog whom the majority expects to lose**, "
            "defying the conventional wisdom. It is often used in reference to beating the betting odds in sports, "
            "or beating the opinion polls in electoral politics.")

st.subheader("Overall, very rare for upsets to happen, as shown in the normal distribution")
st.image("normal_dist.png")

st.subheader(f"In this dataset, there are {len(raw_df)} matches....   *{len(upset_df)}* of them are upsets *(elo difference of 400+)*")
st.markdown("An estimated ***1%*** of the matches do the underdogs come out on top")

st.subheader("The graph below are the outliers.")
st.image("outskirt_dist.png")


st.header("Now why might they be winning?")
st.subheader("They got awsome openings?")
st.image("upset_freq_moves.PNG")

if st.checkbox('Scotch Game'):
    col1, col2 = st.columns(2)
    text = """
    Pros: \n
    White virtually guarantees himself a space advantage \n
    Black is unable to maintain the e5 point \n
    Avoids the well-analyzed Ruy Lopez \n
    Cons: \n
    Releases the tension very early \n
    Recapturing the d4 pawn will require a second move by the white knight \n
    The e4 pawn can later come under attack -Quoted From Lichess \n
    """
    with col1:
        st.image("scotch_opening.png")
    with col2:
        st.write(text)

if st.checkbox("Van't Kruijs Opening"):
    col1, col2 = st.columns(2)
    text = """
    This is often used when White has much knowledge of the opening when playing as Black. Therefore, this can be used to 
    ensnare a few opponents into traps. However, since this gives the first move advantage to Black straight away, this is not recommended." -Wikipedia\n
    Pros: \n
    Allows for the Queen and the white square Bishop to move freely\n
    Cons: \n
    Gives the first move advantage to Black straight away. It allows them to take control of the center faster. \n
    """
    with col1:
        st.image("vant_opening.png")
    with col2:
        st.write(text)


if st.checkbox('Ruy Lopez: Berlin Defense'):
    col1, col2 = st.columns(2)
    text = """
    The Berlin Defense is a natural, classical way of meeting the Ruy Lopez. Black develops the knight to a 
    good square and attacks the e4-pawn. The Berlin Defense contains a common variation beginning with 4.O-O Nxe4 
    which leads to a well-known queen-less middlegame \n
    Pros: \n
    Black fights for equality in a natural way \n
    Black leaves the bishop on b5, where it can come under attack\n
    The 4.0-0 Nxe4 line usually leads to a complicated, unusual endgame\n
    Cons:\n
    White has many ways to force a drawish position\n
    The opening is not ideal for attacking players\n
    White makes most of the decisions about what kind of game will result\n
    """
    with col1:
        st.image("lopez_opening.png")
    with col2:
        st.write(text)

st.subheader("Or maybe their opponents were frustrated that they lost to lower rated player")
st.image("upset_victory_status.PNG")

# Searches a player
#players_upset = pd.concat([upset_df['white_id'], upset_df['black_id']]).drop_duplicates()
#st.subheader("Below are the usernames that are within the dataset. \n Specifically the 'interesting' players")
#st.write(players_upset)

st.subheader("Search a match!")
user_input = st.text_input("Enter in a number ranging from 0 - 545 or a player_id:", "crazyscientist1")
if user_input:
    st.subheader('Match Information')

    try:
        match_history = upset_df.iloc[[int(user_input)]]
        test = ""
        st.text(f"Let's see match {user_input}!")
        st.write(match_history)
        open(match_history["moves"])

    except:
        st.text(f"Let's see '{user_input}' match history!")
        result = upset_df.query(f'((white_id == "{user_input}") or (black_id == "{user_input}"))')
        st.write(result)

        get_index = st.text_input("Let's take a look at the match", 0)
        if get_index:
            match_history = upset_df.iloc[[int(get_index)]]
            st.write(match_history)
            #open_match(match_history["moves"]) #uncomment


# displays 2 datasets
if st.checkbox('Show raw chess data'):
    st.subheader('Raw data')
    st.write(raw_df)

if st.checkbox('Show processed upsets'):
    st.subheader('Processed data - This is what we will be using')
    st.write(upset_df)
