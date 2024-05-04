
#========================================= /   IMPORTING LIBRARIES /   ==========================================#    

#Pandas Library
import pandas as pd

#MySQL and SQLAlchemy Libraries
from mysql.connector import connect
from urllib.parse import quote
from sqlalchemy import create_engine
import sqlalchemy

#UI Dashboard Libraries
import streamlit as st


#========================================== /   DASHBOARD SETUP   / =============================================#


st.header(':green[Data Migration center]')
st.write ('Here the collected data is migrated to SQL. Please click the button below to **Migrate Data**')
migrate_data = st.button('**Migrate Data**', type = 'primary',
    help = 'Clicking this button will migrate the Youtube channel data to SQL')

# Define Session state to Migrate to MySQL button
if 'migrate_data' not in st.session_state:
    st.session_state.migrate_data = False
if migrate_data:
    st.session_state.migrate_data = True

    #Shared variables
    channel_id = st.session_state.channel_id
    channel = st.session_state.channel
    video = st.session_state.video


    #========================== /   CONVERTING DICTIONARY DATA TO PANDAS DATAFRAME   / ==========================#


    #DataFrame of channels
    df_c = pd.DataFrame(channel[f"{channel_id}"],index=[0])


    #DataFrame of videos
    df_v = pd.concat([pd.DataFrame(dict,columns=['Video_Id','Playlist_Id','Video_Name','Video_Description','Published_Date','View_Count',
        'Like_Count','Fav_Count','Comment_Count','Duration','Thumbnail','Caption_Status'], index=[range(0,len(video))]) for dict in video.values()],
        ignore_index=True)

    #DataFrame of Comments
    df_com = pd.concat([pd.DataFrame.from_dict(item['Comments'],orient='index') for item in video.values()], ignore_index=True)



    #============================= /   ESTABLISHING SQL AND SQLALCHEMY CONNECTIONs   / ============================#

    #Configuring
    db_config = {
        'host':'localhost',
        'user':'root',
        'password':'1234',
        'database':'youtube_db'
        }
    encoded_password = quote(db_config['password'])


    #Connecting to MySQL Workbench
    connection = connect(user=db_config['user'], password=encoded_password, host=db_config['host'])
    cursor = connection.cursor(buffered=True)


    #Creating and Using "youtube_db" database
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
    cursor.execute(f"USE {db_config['database']}")


    #Closing the cursor and database connection
    cursor.close()
    connection.close()


    #Connection for SQLAlchemy
    connection_url = f"mysql+mysqlconnector://{db_config['user']}:{encoded_password}@{db_config['host']}/{db_config['database']}"
    engine=create_engine(connection_url)



    #====================================== /   MIGRATING DATA TO MYSQL TABLES   / ===================================#

    #Creating ChannelS table in SQL
    table_name1 = 'channels'
    df_c.to_sql(name=table_name1, con=engine, if_exists='append',index=False,
        dtype = {
            'Channel_Id': sqlalchemy.types.VARCHAR(length=225),
            'Channel_Name': sqlalchemy.types.VARCHAR(length=225),
            'Channel_Description': sqlalchemy.types.TEXT,
            'Channel_Subcount': sqlalchemy.types.BIGINT,
            'Channel_Viewcount': sqlalchemy.types.BIGINT,
            'Channel_Playlist_Id': sqlalchemy.types.VARCHAR(length=225)
        }
    )


    #Creating Videos table in SQL
    table_name2 = 'videos'
    df_v.to_sql(name=table_name2, con=engine, if_exists='append',index=False,
        dtype = {
            'Playlist_Id': sqlalchemy.types.VARCHAR(length=225),
            'Video_Id': sqlalchemy.types.VARCHAR(length=225),
            'Video_Name': sqlalchemy.types.VARCHAR(length=225),
            'Video_Description': sqlalchemy.types.TEXT,
            'Published_Date': sqlalchemy.types.VARCHAR(length=50),
            'View_Count': sqlalchemy.types.BIGINT,
            'Like_Count': sqlalchemy.types.BIGINT,
            'Fav_Count': sqlalchemy.types.INT,
            'Comment_Count': sqlalchemy.types.INT,
            'Duration': sqlalchemy.types.VARCHAR(length=1024),
            'Thumbnail': sqlalchemy.types.VARCHAR(length=225),
            'Caption_Status': sqlalchemy.types.VARCHAR(length=225)
        }
    )


    #Creating Comment table in SQL
    table_name3 = 'comments'
    df_com.to_sql(name=table_name3, con=engine, if_exists='append',index=False,
        dtype = {
            'Video_Id': sqlalchemy.types.VARCHAR(length=225),
            'Comment_Id': sqlalchemy.types.VARCHAR(length=225),
            'Comment_Text': sqlalchemy.types.TEXT,
            'Comment_Author': sqlalchemy.types.VARCHAR(length=225),
            'Comment_PublishedAt': sqlalchemy.types.VARCHAR(length=50)
        }
    )

    st.write("Data successfully migrate to SQL")
    st.write(":violet[To enter another Channel ID move to Collection Tab **or else** move to Analysis Tab]")