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

def execute_query(query):
    with engine.connect() as connection:
        st.session_state.query_result = pd.read_sql(query, connection)

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
        st.markdown("""
        <style>
            .stMainBlockContainer {
                max-width: 75%;
                padding-left: 0rem;
                padding-right: 20px;
            }
        </style>
        """, unsafe_allow_html=True)
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
            st.table(df,hide_index=True)

elif selected == "Player Search":
    user_input = st.text_input("Enter player's name:", placeholder="Type here...")
    time.sleep(3)
    with engine.connect() as connection:
        # Display the entered text
        if user_input:
            #"query"
            q1 = text(f"""select First_Name,Last_Name from players where first_name LIKE '%{user_input}%' or last_name like '%{user_input}%';""")
            df_candidate_players = pd.read_sql(q1,connection)
            players_list = list(df_candidate_players["First_Name"]+" "+df_candidate_players["Last_Name"])
            option = st.selectbox(
                "Select Player From Available options:",
                players_list
            )   
            if option is not None:
                q2 = text(f"""select Player_ID,First_Name,Last_Name,Position,Jersey_Number,Birth_Date,Height_CM,Weight_KG,Headshot_Url from players where concat(first_name, " " ,last_name) LIKE '%{option}%' LIMIT 1;""")
                df_final_player = pd.read_sql(q2,connection)
                player_name = option
                logo_url = df_final_player["Headshot_Url"].iloc[0]
                position = df_final_player["Position"].iloc[0]
                player_id = df_final_player["Player_ID"].iloc[0]
                df_final_player["Age"] = (
                    pd.Timestamp.today().year
                    - pd.to_datetime(df_final_player["Birth_Date"]).dt.year)
                df_final_player["BMI"] = (
                    df_final_player["Weight_KG"]/((df_final_player["Height_CM"]/100))**2
                )
                st.divider()
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
                        <div class="player-info"><div class="player-name">{player_name}</div>

                        <div class="player-position">
                        Position: {position}
                        </div>
                        </div>
                        </div>
                        """,
                        unsafe_allow_html=True)
                player_data = df_final_player.loc[:, [
                    "Player_ID",
                    "First_Name",
                    "Last_Name",
                    "Jersey_Number",
                    "Age",
                    "Height_CM",
                    "Weight_KG",
                    "BMI"
                ]]
                st.table(player_data,hide_index=True)
                st.divider()
                q3 = text(f"""select player_id,Sum(Goals) as "goals",Sum(Assists) as "assists" ,Sum(Points) as "points",Count(Game_ID) as "games" from game_stats where player_id = {player_id} group by player_id;""")
                df_player_stat = pd.read_sql(q3,connection)
                if not df_player_stat.empty:
                    goals = df_player_stat["goals"].iloc[0]
                    assists = df_player_stat["assists"].iloc[0]
                    points = df_player_stat["points"].iloc[0]
                    games = df_player_stat["games"].iloc[0]
                    st.markdown("""
                        <style>
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
                        </style""",unsafe_allow_html=True)
                    col1, col2,col3,col4 = st.columns(4)

                    with col1:

                        st.markdown(
                            '<div class="metric-card">'
                            '<div class="metric-label">🏒 Goals</div>'
                            f'<div class="metric-value">{int(goals)}</div>'
                            '</div></br>',
                            unsafe_allow_html=True
                        )
                    with col2:

                        st.markdown(
                            '<div class="metric-card">'
                            '<div class="metric-label">🏆 Games</div>'
                            f'<div class="metric-value">{int(games)}</div>'
                            '</div>',
                            unsafe_allow_html=True
                        )

                    with col3:

                        st.markdown(
                            '<div class="metric-card">'
                            '<div class="metric-label">🤝Assists</div>'
                            f'<div class="metric-value">{int(assists)}</div>'
                            '</div> </br>',
                            unsafe_allow_html=True
                        )
                    with col4:
                        st.markdown(
                            '<div class="metric-card">'
                            '<div class="metric-label">🎯Points</div>'
                            f'<div class="metric-value">{int(points)}</div>'
                            '</div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.markdown("SORRY!! Stat not available")
            else:
                st.markdown("SORRY!! No Player available. Kindly retry with different name!")
            time.sleep(1.5)

elif selected == "Game Results":
    st.title("Game Results")
    with engine.connect() as connection:
        q1=text("""SELECT DISTINCT Game_State FROM Games;""")
        game_state_list = ["All"]
        for x in connection.execute(q1).fetchall():
            game_state_list.append(x[0])
        print(game_state_list)
        genre = st.radio(
            "Game State",
            game_state_list,
        )
        today = datetime.date.today()
        date = st.date_input("Filter By Date:", today)
        if genre != "All":
            q2 = text("""
                SELECT (Select Team_Name FROM Teams where Team_ID = G.Home_Team_ID) AS HomeTeam,(Select Team_Name FROM Teams where Team_ID = G.Away_Team_ID) AS AwayTeam,G.Home_Score, G.Away_Score, G.Venue_Name FROM Games G where 
                G.Game_State = :genre
                AND G.Game_Date = :date
            """)

            df = pd.read_sql(
                q2,
                connection,
                params={
                    "genre": genre,
                    "date": date
                }
            )
        else:
            q2 = text("""SELECT (Select Team_Name FROM Teams where Team_ID = G.Home_Team_ID) AS HomeTeam,(Select Team_Name FROM Teams where Team_ID = G.Away_Team_ID) AS AwayTeam,G.Home_Score, G.Away_Score, G.Venue_Name FROM Games G where G.Game_Date = :date
            """)

            df = pd.read_sql(
                q2,
                connection,
                params={
                    "date": date
                }
            )            
        time.sleep(2)
        if not df.empty:
            st.table(df)
        else:
            st.markdown("Not games found for selected state and date. Provide some other combination!")
elif selected == "SQL Query Explorer":
    with engine.connect() as connection:
        st.title("🔎 SQL Query Explorer")
        st.markdown("Pick a ready-made query below, or choose Custom Query to write your own")
        queries = {
            "Top 10 players by points": """
                SELECT
                    CONCAT(p.First_Name, ' ', p.Last_Name) AS Player,
                    s.Goals,
                    s.Assists,
                    s.Points
                FROM Skater_Season_Stats s
                JOIN Players p ON s.Player_ID = p.Player_ID
                ORDER BY s.Points DESC
                LIMIT 10;
            """,

            "Top 10 goal scorers": """
                SELECT
                    CONCAT(p.First_Name, ' ', p.Last_Name) AS Player,
                    s.Goals,
                    s.Games_Played
                FROM Skater_Season_Stats s
                JOIN Players p ON s.Player_ID = p.Player_ID
                ORDER BY s.Goals DESC
                LIMIT 10;
            """,

            "Top 10 players by assists": """
                SELECT
                    CONCAT(p.First_Name, ' ', p.Last_Name) AS Player,
                    s.Assists,
                    s.Games_Played
                FROM Skater_Season_Stats s
                JOIN Players p ON s.Player_ID = p.Player_ID
                ORDER BY s.Assists DESC
                LIMIT 10;
            """,

            "Top 10 players by plus/minus": """
                SELECT
                    CONCAT(p.First_Name, ' ', p.Last_Name) AS Player,
                    s.Plus_Minus
                FROM Skater_Season_Stats s
                JOIN Players p ON s.Player_ID = p.Player_ID
                ORDER BY s.Plus_Minus DESC
                LIMIT 10;
            """,

            "Top 10 players by shots": """
                SELECT
                    CONCAT(p.First_Name, ' ', p.Last_Name) AS Player,
                    s.Shots,
                    s.Goals
                FROM Skater_Season_Stats s
                JOIN Players p ON s.Player_ID = p.Player_ID
                ORDER BY s.Shots DESC
                LIMIT 10;
            """,

            "Top 10 teams by points": """
                SELECT
                    t.Team_Name,
                    s.Wins,
                    s.Losses,
                    s.Points
                FROM Standings s
                JOIN Teams t ON s.Team_ID = t.Team_ID
                ORDER BY s.Points DESC
                LIMIT 10;
            """,

            "Top 10 teams by goals scored": """
                SELECT
                    t.Team_Name,
                    s.Goals_For,
                    s.Games_Played
                FROM Standings s
                JOIN Teams t ON s.Team_ID = t.Team_ID
                ORDER BY s.Goals_For DESC
                LIMIT 10;
            """,

            "Top 10 goalies by save percentage": """
                SELECT
                    CONCAT(p.First_Name, ' ', p.Last_Name) AS Goalie,
                    g.Save_pct,
                    g.Wins,
                    g.Shutouts
                FROM Goalie_Season_Stats g
                JOIN Players p ON g.Player_ID = p.Player_ID
                ORDER BY g.Save_pct DESC
                LIMIT 10;
            """,

            "Top 10 goalies by shutouts": """
                SELECT
                    CONCAT(p.First_Name, ' ', p.Last_Name) AS Goalie,
                    g.Shutouts,
                    g.Save_pct,
                    g.Wins
                FROM Goalie_Season_Stats g
                JOIN Players p ON g.Player_ID = p.Player_ID
                ORDER BY g.Shutouts DESC
                LIMIT 10;
            """,

            "Top 10 games by total goals": """
                SELECT
                    Game_ID,
                    Game_Date,
                    Home_Team_ID,
                    Away_Team_ID,
                    Home_Score,
                    Away_Score,
                    (Home_Score + Away_Score) AS Total_Goals
                FROM Games
                ORDER BY Total_Goals DESC
                LIMIT 10;
            """
        }
        option = st.selectbox(
            "Choose a query",
            ["Custom Query"] + list(queries.keys())
        )
        if option == "Custom Query":
            user_text = st.text_area("SQL Query", placeholder="Custom Query", height=150)
            time.sleep(5)
        query_to_execute = queries.get(option) if option != "Custom Query" else text(user_text)
        st.button("▶ Run Query",on_click=execute_query,args=(query_to_execute,))

        if "query_result" in st.session_state:
            st.table(st.session_state.query_result)

elif selected == "Leaderboards":
    with engine.connect() as connection:
        st.title("Player Metrics Selector")

        q1=text("""SELECT (SELECT CONCAT(First_Name," ",Last_Name) from Players where Player_ID = SS.Player_ID) as Player,SS.Goals FROM skater_season_stats ss order by SS.Goals DESC LIMIT 10;""")

        q2=text("""SELECT (SELECT CONCAT(First_Name," ",Last_Name) from Players where Player_ID = SS.Player_ID) as Player,SS.Assists FROM skater_season_stats ss order by SS.Assists DESC LIMIT 10;""")

        q3=text("""SELECT (SELECT CONCAT(First_Name," ",Last_Name) from Players where Player_ID = SS.Player_ID) as Player,SS.Penalty_Min as 'Penalty Minutes' FROM skater_season_stats ss where ss.penalty_min>0 order by SS.Penalty_Min LIMIT 10;""")

        q4=text("""SELECT (SELECT CONCAT(First_Name," ",Last_Name) from Players where Player_ID = GG.Player_ID) as Player,ROUND(GG.Save_pct*100,2) AS 'Save Percentage' FROM goalie_season_stats GG order by GG.Save_pct DESC LIMIT 10;""")

        q5=text("""SELECT CONCAT(p.First_Name, ' ', p.Last_Name) AS Player,ROUND(s.Points / s.Games_Played, 2) AS Points_Per_Game FROM Skater_Season_Stats s JOIN Players p ON s.Player_ID = p.Player_ID WHERE s.Games_Played > 0 ORDER BY Points_Per_Game DESC LIMIT 10;""")

        metrics = {
            "🥅 Goals": q1,
            "🎯 Assists": q2,
            "🕙 Penalty Minutes": q3,
            "🧤 Save %": q4,
            "🏆 Team Wins": q5
        }

        selected_metric = st.segmented_control(
            "Pick a metric",
            list(metrics.keys()),default="🥅 Goals"
        )
        query = metrics.get(selected_metric)
        if query is not None:
                df = pd.read_sql(query, connection)
                st.table(df)
        else:
            st.markdown("Select a option above to see stats")
        time.sleep(2)
