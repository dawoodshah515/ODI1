import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


st.set_page_config(page_title="Cricket Matches Dashboard", layout="wide")
st.title("ODI Cricket Insights")
st.write("## 2002-2023")

# Load dataset
df = pd.read_csv(".myvenv\ODI_Match_info.csv")
df = df[["team1", "team2", "toss_winner", "winner"]]

# Sidebar team selection
with st.sidebar:
    teams = ["Pakistan", "India", "Australia", "Sri Lanka", "Bangladesh","England", "South Africa", "West Indies"]

st.sidebar.title("SELECT TWO TEAMS")
with st.sidebar:
    team1 = st.radio("**Select Team 1**", teams)
    available_team2 = [t for t in teams if t != team1]
    team2 = st.radio("**Select Team 2**", available_team2)

    st.title("Note:")
    st.write("## These are ODI Matches \n ## Data From 2002 to 2023")

st.write(f"## **{team1} VS {team2} Matches**")  

# Insert a photo (local file or URL)
#st.image("download.jpeg", caption="Cricket ODI Matches", width=80)
# Dictionary of team logos (use small PNG/JPG files)
team_logos = {
    "Pakistan": ".myvenv\Logos\Pakistan.logo.png",
    "India": ".myvenv\Logos\India.logo.png",
    "Australia": ".myvenv\Logos\Australia.logo.jpeg",
    "Sri Lanka": ".myvenv\Logos\Srilanka.logo.jpeg",
    "Bangladesh": ".myvenv\Logos\Bangladesh.logo.png",
    "England": ".myvenv\Logos\England.logo.jpeg",
    "South Africa": ".myvenv\Logos\southafrica.logo.png",
    "West Indies": ".myvenv\Logos\westindies.logo.jpeg"
}

# Show both team logos (small size)
st.image([team_logos[team1], team_logos[team2]], 
         caption=[team1, team2], 
         width=80)   # 👈 small size like a logo

# -----------------------------
# Filter dataset for only selected two teams
# -----------------------------
subset = df[
    ((df["team1"] == team1) & (df["team2"] == team2)) |
    ((df["team1"] == team2) & (df["team2"] == team1))
]

if subset.empty:
    st.warning("No matches found between these teams.")
else:
    # Toss Winner Stats
    toss_counts = subset["toss_winner"].value_counts()
    toss_colors = ["blue" if team == toss_counts.idxmax() else "gray" for team in toss_counts.index]

    fig_toss = px.bar(
        toss_counts,
        x=toss_counts.index,
        y=toss_counts.values,
        labels={"x": "Team", "y": "Toss Wins"},
        title="Toss Wins",
        color=toss_counts.index,
        color_discrete_sequence=toss_colors
    )
    st.plotly_chart(fig_toss)

    # Match Winner Stats
    winner_counts = subset["winner"].value_counts()
    match_colors = ["blue" if team == winner_counts.idxmax() else "gray" for team in winner_counts.index]

    fig_match = px.bar(
        winner_counts,
        x=winner_counts.index,
        y=winner_counts.values,
        labels={"x": "Team", "y": "Match Wins"},
        title="Match Wins",
        color=winner_counts.index,
        color_discrete_sequence=match_colors
    )
    st.plotly_chart(fig_match)

    # Summary
    st.title("Summary")
    st.write(f"- Total matches **played**: **{len(subset)}**")
    st.write(f"- Toss winner most often: **{toss_counts.idxmax()}** ({toss_counts.max()} times)")
    st.write(f"- Match winner most often: **{winner_counts.idxmax()}** ({winner_counts.max()} times)")