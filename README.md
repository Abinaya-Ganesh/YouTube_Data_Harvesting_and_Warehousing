# YouTube_Data_Harvesting_and_Warehousing
User can extract a YouTube Channel's Data by providing the Channel's ID and can analyze the data using a set of questions provided.

**Introduction**
	
YouTube is a huge Video Streaming Platform where lot of people post their creative videos which are either to the likes of audience or of use to the target audience. It also generates a lot of data with all the videos that are being posted by content creators and data is also generated when people interact through comments. 

Through this project, we will see how to extract data from Youtube using YouTube API in Python, then store them in suitable format in MySQL for the end user to analyze the data using a set of questions provided to them on the Streamlit User Interface.

![cap1](https://github.com/Abinaya-Ganesh/YouTube_Data_Harvesting_and_Warehousing/assets/162968618/891be83c-f1cd-47f7-91cb-e433b3fb1a14)


**User Guide**

1. **Data Collection Tab**

      a. Open a YouTube channel's Homepage. Click on About ---> Share channel ---> Copy channel ID. This is how you get a YouTube Channel's ID
   
      b. Enter the Channel Id and click the **Get data** button

3. **Data Migration Tab**

      To Migrate the channel date to MySQL and store it, click the **Migrate data** button

4. This project can collect upto 10 YouTube channels' data unless and until the user doesn't exhaust the daily YouTube API quota

5. **Data Analysis Tab**

      Users are put forward with 10 questions where they can choose one to get a resultant analysed data
   

**Developer Guide**

1. **Tools required**
         
      •	 Python
   
      •	 Visual Studio Code
    
      •	 MySQL workbench
   
      •	 YouTube API key from Google Developers console


2. **Python libraries to install**
   
      •	google-api-python-client
   
      •	pandas
   
      •	mysql-connector-python
   
      •	SQLAlchemy
   
      •	streamlit

      •	plotly-express

      •	isodate

3. **Modules to import**
   
      a. Google API Library
   
          •	import googleapiclient.discovery

      b. ISO Date Library to convert ISO time string into a time object
   
          •	import isodate

      c. Pandas Library
   
          •	import pandas as pd

      d. MySQL and SQLAlchemy Libraries
   
          •	from mysql.connector import connect
   
          •	from urllib.parse import quote
   
          •	from sqlalchemy import create_engine
   
          •	import sqlalchemy

      e. UI Dashboard Libraries
   
          •	import streamlit as st
   
          •	import plotly.express as px

4. **Process**
   
       •	With the help of YouTube API developer console, extract the required channel, video and comments data of a YouTube channel

       •	Store the extracted data temporarily in a pandas DataFrame

       •	Migrate the data and store it in a SQL database

       •	Use SQLAlchemy tool to query from the database as per the question the user selects

       •	Create a Streamlit dashboard where the user can input channel ID and get the data

       •	Display the analysed data also using Streamlit data visualization tools

**NOTE:**

	I have created a multipage Streamlit app. Except the main.py, other files should be in a folder named 
 	"pages" under the directory where main.py is saved.

   	










