## Nhl_Analytics

Hi, 

This project aims to display National Hockey League data in Multipage STREAM Dashboard for quick and easy visulization and summary.

The data is ingested from APIs except for the game_stats, skater_season_stats and goalie_season_stats json files which can be found in this repo.

The complete data ingestion and data insertion in DB is handled in notebook and streamlit dashboard is created under app.py file.

Appropriate mark downs are provided prior to coding of in each cell of the notebook to provide a quick summary.

We just need to replace the password to our MYSQL local host password. The other steps from calling APIs, storing it's result, creation of DB, tables and insertion of data will be done thereafter automatically. Please make sure to include the 3 json files present in this repo in the project folder prior to running the cells of notebook.

<img width="1273" height="595" alt="Screenshot 2026-09-25 224601" src="https://github.com/user-attachments/assets/0bf79c69-7ba0-450e-a4f8-2ccf406c6d07" />

When we have ingested data in all the seven tables, and then we move on to creation of STREAMLIT dashboard. 

The streamlit dashboard consists of 7 pages which can be accessed using the sidebar. The functionality of each of these sidebars is in alignment with their name and pretty intutive.

<img width="301" height="561" alt="image" src="https://github.com/user-attachments/assets/1e0bc55e-8156-4a2b-ab9c-4a531b7b9ac9" />


There are SQLs written in app.py file which connects to the DB and provides the result in the corresponding dashboard. The user can navigate at their will and edge scenarios like no input or data not found are also handled so things work as expected as well for such cases.
