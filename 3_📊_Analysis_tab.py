
#================================ /   IMPORTING LIBRARIES /   =================================#    

#Pandas Library
import pandas as pd

#MySQL and SQLAlchemy Libraries
from urllib.parse import quote
from sqlalchemy import create_engine


#UI Dashboard Libraries
import streamlit as st
import plotly.express as px


#========================= /   RE-ESTABLISHING CONNECTION WITH SQLALCHEMY   / ===========================#

db_config = {
    'host':'localhost',
    'user':'root',
    'password':'1234',
    'database':'youtube_db'
    }
encoded_password = quote(db_config['password'])

connection_url = f"mysql+mysqlconnector://{db_config['user']}:{encoded_password}@{db_config['host']}/{db_config['database']}"
engine=create_engine(connection_url)



#================================== /   DASHBOARD SETUP   / ================================#


#Drop-down box in Streamlit Dashboard
st.header(':green[Data Analysis Center]')   
st.write (':violet[Here based on the question that you select, a table format of analysed result data is displayed]')

sql_query = st.selectbox('**Questions regarding the channel**',
('1. What are the names of all the videos and their corresponding channels?',
'2. Which channels have the most number of videos, and how many videos do they have?',
'3. What are the top 10 most viewed videos and their respective channels?',
'4. How many comments were made on each video, and what are their corresponding video names?',
'5. Which videos have the highest number of likes, and what are their corresponding channel names?',
'6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
'7. What is the total number of views for each channel, and what are their corresponding channel names?',
'8. What are the names of all the channels that have published videos in the year 2022?',
'9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
'10. Which videos have the highest number of comments, and what are their corresponding channel names?'), 
key = 'question', index=None, placeholder='Choose a question')


#======================================= /   DISPLAY OF DATA   / =======================================#

#Query 1
if sql_query == '1. What are the names of all the videos and their corresponding channels?':
    query1 = ('SELECT Video_Name, Channel_Name FROM videos inner join channels ON videos.Playlist_Id = channels.Channel_Playlist_ID')
    df1 = pd.read_sql(query1, engine)
    df1.index += 1
    st.dataframe(df1)


#Query 2
elif sql_query == '2. Which channels have the most number of videos, and how many videos do they have?':       
    query2 = ('SELECT Channel_Name, Channel_Videocount AS Channel_Video_Count FROM channels ORDER BY Channel_Videocount DESC')
    df2 = pd.read_sql(query2, engine)
    df2.index += 1
    st.dataframe(df2)

    #bar plot
    fig_q2 = px.bar(df2, y='Channel_Video_Count', x='Channel_Name', text_auto=True, title="Channels with most number of videos")
    fig_q2.update_traces(textfont_size=16,marker_color='#ebc034')
    fig_q2.update_layout(title_font_color='#1308C2 ',title_font=dict(size=25))
    st.plotly_chart(fig_q2,use_container_width=True)
        

#Query 3
elif sql_query == '3. What are the top 10 most viewed videos and their respective channels?':
    query3 = ('SELECT Channel_Name, Video_Name, View_Count FROM videos \
        INNER JOIN channels ON videos.Playlist_Id = channels.Channel_Playlist_ID \
        ORDER BY View_count DESC LIMIT 10')
    df3 = pd.read_sql(query3, engine)
    df3.index += 1
    st.dataframe(df3)

    #bar plot
    fig_q3 = px.bar(df3, x='Video_Name', y='View_Count', text_auto=True, title="Top 10 most viewed videos")
    fig_q3.update_traces(textfont_size=16,marker_color='#ebc034')
    fig_q3.update_layout(title_font_color='#1308C2 ',title_font=dict(size=25))
    st.plotly_chart(fig_q3, use_container_width=True)

    
#Query 4
elif sql_query == '4. How many comments were made on each video, and what are their corresponding video names?':
    query4 = ('SELECT Video_Name, Comment_Count FROM videos ORDER BY Comment_Count DESC')
    df4 = pd.read_sql(query4,engine)
    df4.index += 1
    st.dataframe(df4)


#Query 5
elif sql_query == '5. Which videos have the highest number of likes, and what are their corresponding channel names?':
    query5 = ('SELECT Channel_Name, Video_Name, Like_Count FROM videos \
        INNER JOIN channels ON videos.Playlist_Id = channels.Channel_Playlist_ID \
        ORDER BY Like_Count DESC')
    df5 = pd.read_sql(query5,engine)
    df5.index += 1
    st.dataframe(df5)


#Query 6
elif sql_query ==  '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
    query6 = ('SELECT Video_Name, Like_Count FROM videos ORDER BY Like_Count DESC')
    df6 = pd.read_sql(query6,engine)
    df6.index += 1
    st.dataframe(df6)


#Query 7
elif sql_query == '7. What is the total number of views for each channel, and what are their corresponding channel names?':       
    query7 = ('SELECT Channel_Name, Channel_Viewcount AS View_Count FROM channels ORDER BY View_Count DESC')
    df7 = pd.read_sql(query7,engine)
    df7.index += 1
    st.dataframe(df7)

    #bar plot
    fig_q7 = px.bar(df7, x='Channel_Name', y='View_Count', text_auto=True, title="Total number of views for each channel")
    fig_q7.update_traces(textfont_size=16,marker_color='#ebc034')
    fig_q7.update_layout(title_font_color='#1308C2 ',title_font=dict(size=25))
    st.plotly_chart(fig_q7, use_container_width=True)

    
#Query 8
elif sql_query == '8. What are the names of all the channels that have published videos in the year 2022?':
    query8 = ('SELECT Channel_Name, videos.Video_Name videos, Published_date FROM channels \
        INNER JOIN videos ON videos.Playlist_Id = channels.Channel_Playlist_ID \
        WHERE EXTRACT(YEAR FROM Published_date) = 2022 ORDER BY channel_name')
    df8 = pd.read_sql(query8,engine)
    df8.index += 1
    st.dataframe(df8)


#Query 9
elif sql_query == '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?': 
    query9 = ("""SELECT Channel_Name, TIME_FORMAT(SEC_TO_TIME(AVG(TIME_TO_SEC(Duration))), '%H:%i:%s') AS Average_Duration FROM videos \
        INNER JOIN channels ON videos.Playlist_Id = channels.Channel_Playlist_ID \
        GROUP BY Channel_Name ORDER BY Average_Duration""")
    df9 = pd.read_sql(query9,engine)
    df9.index += 1
    st.dataframe(df9)


#Query 10
elif sql_query == '10. Which videos have the highest number of comments, and what are their corresponding channel names?':
    query10 = ('SELECT Channel_Name, Video_Name, Comment_Count FROM videos \
        INNER JOIN channels ON videos.Playlist_Id = channels.Channel_Playlist_ID \
        ORDER BY Comment_Count DESC')
    df10 = pd.read_sql(query10,engine)
    df10.index += 1
    st.dataframe(df10)