import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
import datetime
from sqlalchemy import create_engine,text
import time

with st.sidebar:
    selected = option_menu("NHL Analytics Hub", ["Home", "Standings","Team Info","Player Search","Game Results","Leaderboards","SQL Query Explorer"], 
        icons=['house', 'list-ul',"people","search","controller","bar-chart","code-slash"], menu_icon="cast", default_index=0)

password = "dbms%40123"
#https://stackoverflow.com/questions/1423804/writing-a-connection-string-when-password-contains-special-characters

host = "127.0.0.1"
engine = create_engine(
    f"mysql+pymysql://root:{password}@{host}:3306/NHL_Analytics"
    #mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
)

if selected == "Home":

    st.markdown("""
    <style>

        /* ---------- Main page ---------- */

        .block-container {
            max-width: 56.25rem;
            padding-top: 8rem;
            padding-left: 0.05rem;
        }

        /* ---------- Hero ---------- */

        .hero-title {
            font-size: 3rem;
            font-weight: 700;
            color: #FFFFFF;
            margin-top: 0.05rem;
            margin-bottom: 1rem; 
        }

        .hero-line {
            border: 0;
            border-top: 0.0625rem solid #FFFFFF;
            margin: 0 0 1rem 0;
        }

        .description {
            font-size: 1.2rem;
            color: #FFFFFF;
            margin-top: 3.5rem;
            margin-bottom: 3rem;
            margin-left: -11.65rem;
        }
        /* ---------- Metric cards ---------- */

        .metric-card {
            background-color: #00000;
            font-color: #FFFFFF;
            border: 2px solid #e1e1e1;
            border-radius: 0.5rem;
            padding: 1rem 0.9rem;
            height: 6.875rem;
            box-sizing: border-box;
            align-items:center;
        }

        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            border-color: #999999;       /* subtle change on hover */
        }

        .metric-label {
            font-size: 1rem;
            color: #FFFFFF;
            margin-bottom: 8px;
        }

        .metric-value {
            font-size: 1.3rem;
            color: #FFFFFF;
            font-weight: 400;
            margin-left: 0rem;
        }


        /* ---------- Bottom divider ---------- */

        .bottom-line {
            border: 0;
            border-top: 1px solid #dddddd;
            margin-top: 1.9rem;
        }

    </style>
    """, unsafe_allow_html=True)

    hero_image, hero_content = st.columns([1.1, 4])

    with hero_image:

        st.image(
            "OIP.webp",
            width=250
        )

    with hero_content:

        st.markdown(
            '<div class="hero-title">🏒 NHL Analytics Hub</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<hr class="hero-line">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="description">API-driven hockey data pipeline with SQL analysis and Streamlit dashboard</div>',
            unsafe_allow_html=True
        )

    col1, col2, col3, col4 = st.columns(4)

    with engine.connect() as connection:
        query1 = text("""SELECT COUNT(Team_ID) from teams;""")
        team_count = connection.execute(query1).fetchall()[0][0]
        query2 = text("""SELECT COUNT(Player_id) from players;""")
        player_count = connection.execute(query2).fetchall()[0][0]
        query3 = text("""SELECT count(Game_ID) FROM games;""")
        games_count = connection.execute(query3).fetchall()[0][0]
        query4 = text("""SELECT sum(Home_Score)+sum(Away_Score) FROM games;""")
        goals_count = connection.execute(query4).fetchall()[0][0]
        query5 = text("""SELECT Team_Name from teams where team_id = (SELECT team_id FROM standings ORDER BY POINTS DESC LIMIT 1)""")
        top_team = connection.execute(query5).fetchall()[0][0]
        query6 = text("""SELECT concat(first_name," ",last_name) from players where player_id = (SELECT Player_id FROM goalie_season_stats order by save_pct desc LIMIT 1);""")
        top_goalie = connection.execute(query6).fetchall()[0][0]
        query7 = text("""SELECT concat(p.first_name," ",P.last_name) FROM Players P INNER JOIN skater_season_stats s on p.player_id = s.player_id where UCASE(p.position) IN ("R","L","C") ORDER BY S.Goals desc LIMIT 1;""")
        top_skater = connection.execute(query7).fetchall()[0][0]
        query8 = text("""SELECT concat(p.first_name," ",P.last_name) FROM Players P INNER JOIN skater_season_stats s on p.player_id = s.player_id where p.position = "D" ORDER BY S.Goals desc LIMIT 1;""")
        top_defensemen = connection.execute(query8).fetchall()[0][0]

    with col1:

        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-label">🏒 Total Teams</div>'
            f'<div class="metric-value">{team_count}</div>'
            '</div></br>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-label">🏆 Top Team</div>'
            f'<div class="metric-value">{top_team}</div>'
            '</div>',
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-label">🧑 Total Players</div>'
            f'<div class="metric-value">{player_count}</div>'
            '</div> </br>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-label">🧤 Top Goalie</div>'
            f'<div class="metric-value">{top_goalie}</div>'
            '</div>',
            unsafe_allow_html=True
        )
        
    with col3:

        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-label">🎮 Total Games</div>'
            f'<div class="metric-value">{games_count}</div>'
            '</div></br>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-label">🛼 Top Skater</div>'
            f'<div class="metric-value">{top_skater}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-label">📕 Total Goals Scored</div>'
            f'<div class="metric-value">{goals_count}</div>'
            '</div></br>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-label">🛡️ Top Defensemen</div>'
            f'<div class="metric-value">{top_defensemen}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<hr class="bottom-line">',
        unsafe_allow_html=True
    )

elif selected == "Standings":
    st.title("Standings")
    with engine.connect() as connection:
        query1_conference_list = text("""SELECT DISTINCT Conference_Name FROM teams;""")
        result = connection.execute(query1_conference_list).fetchall()
        conferences = ["All"]
        for x in result:
            conferences.append(x[0])
            
        option = st.selectbox(
            "Select Conference below",
            conferences
        )

        if option == "All":
            sql = text("""SELECT t.Logo_URL,T.Team_Name,T.Conference_Name,T.Division_Name,S.Wins,S.Losses,S.Points,S.Goals_For,S.Goals_Against FROM standings s inner join teams t on s.team_id = t.team_id ORDER BY S.POINTS DESC LIMIT 10;""")
            df = pd.read_sql(sql,connection)
        elif option == "Western":
            sql = text("""SELECT t.Logo_URL,T.Team_Name,T.Conference_Name,T.Division_Name,S.Wins,S.Losses,S.Points,S.Goals_For,S.Goals_Against FROM standings s inner join teams t on s.team_id = t.team_id where t.Conference_Name = "Western" ORDER BY S.POINTS DESC LIMIT 10;""")
            df = pd.read_sql(sql,connection)
        elif option == "Eastern":
            sql = text("""SELECT t.Logo_URL,T.Team_Name,T.Conference_Name,T.Division_Name,S.Wins,S.Losses,S.Points,S.Goals_For,S.Goals_Against FROM standings s inner join teams t on s.team_id = t.team_id where t.Conference_Name = "Eastern" ORDER BY S.POINTS DESC LIMIT 10;""")
            df = pd.read_sql(sql,connection)       

        # Create DataFrame with inline image
        df["Logo_URL"] = df["Logo_URL"].apply(
            lambda url: f'<a href="{url}" target="_blank"><img src="{url}" width="50"></a>')
    #      pd.DataFrame(
    #     [
    #         [f'<a href="{logo_url}" target="_blank"><img src="{logo_url}" width="100"></a>', 6, 7]
    #     ],
    #     columns=["Image", "Column A", "Column B"]
    # )

    df.insert(0, "No.", range(1, len(df) + 1))
    st.write(df.to_html(index=False,escape=False), unsafe_allow_html=True)

elif selected == "Team Info":
    st.title("Team Info")
    with engine.connect() as connection:
        query1_conference_list = text("""SELECT DISTINCT Team_Name FROM teams;""")
        result = connection.execute(query1_conference_list).fetchall()
        conferences = []
        for x in result:
            conferences.append(x[0])
            
        option = st.selectbox(
            "Select team below",
            conferences
        )
        print(type(option))
        q1=text(f"""select team_id,logo_url,conference_name,division_name from teams where team_name = '{option}';""")
        result_q1 = connection.execute(q1)
        answer_from_query = result_q1.fetchall()
        team_id = answer_from_query[0][0]
        logo_url = answer_from_query[0][1]
        conf_name = answer_from_query[0][2]
        division_name = answer_from_query[0][3]
        q2 = text(f"""select First_Name,Last_Name,Position,Jersey_Number,Birth_Date,Height_CM,Weight_KG from players where team_id = {team_id}""")
        df = pd.read_sql(q2,connection)

        # Create two columns
        col1, col2 = st.columns([1, 2])  # adjust ratio for sizing

        # Left column: logo
        with col1:
            st.image(logo_url, width=150)
            st.markdown(f"Conference: {conf_name}")
            st.markdown(f"Division: {division_name}")

        # Right column: table
        with col2:
            st.markdown("<h3 style='text-align: left; color: #ffffff;  font-size:26px; padding: 4px;'>Team Roaster</h3>", unsafe_allow_html=True)
            st.markdown("<hr style='border:1px solid white;'>", unsafe_allow_html=True)
            st.dataframe(df,hide_index=True)

elif selected == "Player Search":
    user_input = st.text_input("Enter player's name:", placeholder="Type here...")
    time.
    # Display the entered text
    if user_input:
        #"query"
        q1=text(f"""select First_Name,Last_Name,Position,Jersey_Number,Birth_Date,Height_CM,Weight_KG from players where first_name LIKE '%A%' AND last_name like '%B%';""")
        option = st.selectbox(
            "Select Player",
            ["t1", "t2", "t3","t4"]
        )
    logo_url = "https://assets.nhle.com/logos/nhl/svg/COL_light.svg"
    # Assume these values
    player_name = "John Carlson"
    position = "D"

    st.markdown(
    f"""
    <style>
    .player-card {{
        display: flex;
        align-items: center;
        padding: 10px 0 35px 0;
    }}

    .player-photo {{
        width: 180px;
        height: 150px;
        object-fit: contain;
        margin-right: 35px;
    }}

    .player-info {{
        display: flex;
        flex-direction: column;
    }}

    .player-name {{
        font-size: 22px;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 12px;
    }}

    .player-position {{
        font-size: 14px;
        color: #ffffff;
    }}
    </style>

    <div class="player-card">
    <img src="{logo_url}" class="player-photo">

    <div class="player-info">
    <div class="player-name">
    {player_name}
    <span style="font-size:13px;color:#aaa;">↗</span>
    </div>

    <div class="player-position">
    Position: {position}
    </div>
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )
    st.divider()
    df = pd.DataFrame(
        [[5, 6, 7]],
        columns=["Image", "Column A", "Column B"]
    )
    st.table(df)
# -----------------------------
# Player Card
# -----------------------------
    
elif selected == "Game Results":
    st.title("Game Results")
    genre = st.radio(
        "Game State",
        ["All", "OFF", "FUT"],
    )    
    today = datetime.datetime.now()
    d = st.date_input("When's your birthday", today)
    df = pd.DataFrame(
        [[5, 6, 7]],
        columns=["Image", "Column A", "Column B"]
    )
    st.table(df)
elif selected == "SQL Query Explorer":
    st.title("🔎 SQL Query Explorer")
    st.markdown("Pick a ready-made query below, or choose Custom Query to write your own")
    option = st.selectbox(
        "Choose a query",
        ["Custom Query", "Top 10 Games", "Top 10 Players"]
    )
    if option == "Custom Query":
        user_text = st.text_area("SQL Query", placeholder="Custom Query", height=150)
    st.button("▶  Run Query")
    df = pd.DataFrame(
        [[5, 6, 7]],
        columns=["Image", "Column A", "Column B"]
    )
    st.table(df)
elif selected == "Leaderboards":
    st.title("Player Metrics Selector")

    metrics = ["🥅 Goals", "🎯Assists", "🕙 Penalty Minutes", "🧤 Save %", "🏆Team Wins"]

    selected_metric = st.segmented_control("Pick a metric", metrics)
    df = pd.DataFrame(
        [
            [5, 6, 7]
        ],
        columns=["Image", "Column A", "Column B"]
    )

    # Render DataFrame with HTML enabled
    st.write(df.to_html(escape=False), unsafe_allow_html=True)


