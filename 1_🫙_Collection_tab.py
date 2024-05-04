
#====================================== /   IMPORTING LIBRARIES /   =======================================#    

#Google API Library
import googleapiclient.discovery

#ISO Date Library to convert ISO time string into a time object
import isodate

#UI Dashboard Libraries
import streamlit as st


#======================================== /   DASHBOARD SETUP   / ===========================================#



st.header(':green[Data Collection Center]')
st.write (':violet[**Here data is collected from Youtube by using Channel ID that you enter**]')
channel_id = st.text_input('**Enter a YouTube Channel ID**', placeholder="Eg: UCA6qYhjwHGsiErCRzDLqL8Q")
get_data = st.button('**Get data**', type = 'primary',
    help ='Clicking this button collects the Data of the YouTube channel ID given')

# Define Session state to Get data button
if "get_data" not in st.session_state:
    st.session_state.get_data = False
if get_data:
    st.session_state.get_data = True


    #====================================== /   YOUTUBE VARIABLE   / ========================================#

    api_service_name = "youtube"
    api_version = "v3"
    api_key = "use your API key"
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)



    #==================================== /   FUNCTION DEFINITIONS   / =====================================#

    #Function to get Channel Data
    def get_channel_data(c_id):
        channel_request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=c_id
        )
        channel_response = channel_request.execute()

        if 'items' not in channel_response:
            st.write(f"Invalid channel id: {c_id}")
            st.error("Enter the correct **channel_id**")
            return None
        return channel_response

                

    #Function to get Playlist Items
    def get_playlist_data(p_id,page_Token=''):
        playlist_request = youtube.playlistItems().list(
        part="snippet",
        maxResults=50,
        playlistId=p_id,
        pageToken = page_Token
        )
        playlist_response = playlist_request.execute()
                    
        return playlist_response


    #Function to get Video data
    def get_video_data(v_id):
        video_request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=v_id
        )
        video_response = video_request.execute()
        
        return video_response


    #Function to get Comments data
    def get_comments_data(v_id):
        comments_request = youtube.commentThreads().list(
        part="snippet",
        maxResults=100,
        videoId=v_id
        )
        comments_response = comments_request.execute()
        
        return comments_response




    #======================================= /   FUNCTION CALLS   / =====================================#


    #Getting Channels data
    channel_data = get_channel_data(channel_id)

    channel={}

    channel_information = {
        "Channel_Id": channel_id,
        "Channel_Name":channel_data['items'][0]['snippet']['title'],
        "Channel_Description":channel_data['items'][0]['snippet']['description'] if channel_data['items'][0]['snippet']['description'] != '' else "Not Available",
        "Channel_Playlist_Id":channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
        "Channel_Videocount": int(channel_data['items'][0]['statistics']['videoCount']),
        "Channel_Subcount":int(channel_data['items'][0]['statistics']['subscriberCount']),
        "Channel_Viewcount":int(channel_data['items'][0]['statistics']['viewCount'])
        }

    channel[f"{channel_id}"] = channel_information

    #Getting Videos data
    video={}

    p_id = channel[f"{channel_id}"]['Channel_Playlist_Id']
    playlist_response = get_playlist_data(p_id)
    playlist_items = playlist_response['items']

    while('nextPageToken' in playlist_response):
        playlist_response = get_playlist_data(p_id,playlist_response['nextPageToken'])
        playlist_items.extend(playlist_response['items'])

    for i in range(len(playlist_items)):
        v_id = playlist_items[i]['snippet']['resourceId']['videoId']
        video_data = get_video_data(v_id)

        if video_data['items']:
            video_information = {
            "Video_Id": v_id,
            "Playlist_Id": p_id,
            "Video_Name": video_data['items'][0]['snippet']['title'] if 'title' in video_data['items'][0]['snippet'] else "Not Available",
            "Video_Description":video_data['items'][0]['snippet']['description'] if 'description' in video_data['items'][0]['snippet'] else "Not Available",
            "Published_Date":video_data['items'][0]['snippet']['publishedAt'],
            "View_Count":int(video_data['items'][0]['statistics']['viewCount']) if 'viewCount' in video_data['items'][0]['statistics'] else 0,
            "Like_Count":int(video_data['items'][0]['statistics']['likeCount']) if 'likeCount' in video_data['items'][0]['statistics'] else 0,
            "Fav_Count":int(video_data['items'][0]['statistics']['favoriteCount']) if 'favoriteCount' in video_data['items'][0]['statistics'] else 0 ,
            "Comment_Count":int(video_data['items'][0]['statistics']['commentCount']) if 'commentCount' in video_data['items'][0]['statistics'] else 0,
            "Duration":str(isodate.parse_duration(video_data['items'][0]['contentDetails']['duration'])),
            "Thumbnail":video_data['items'][0]['snippet']['thumbnails']['default']['url'],
            "Caption_Status": "Available" if video_data['items'][0]['contentDetails']['caption'] == 'true' else "Not Available",
            "Comments": {}
            }

            #Getting Comments data of the video and inserting them into the Video's dictionary
            comments_response = get_comments_data(v_id)
            comments_data = comments_response['items']
            
            for j in range(len(comments_data)):
                comment_information = {
                "Comment_Id": comments_data[j]['snippet']['topLevelComment']['id'],
                "Video_Id": comments_data[j]['snippet']['topLevelComment']['snippet']['videoId'],
                "Comment_Text": comments_data[j]['snippet']['topLevelComment']['snippet']['textDisplay'],
                "Comment_Author": comments_data[j]['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                "Comment_PublishedAt": comments_data[j]['snippet']['topLevelComment']['snippet']['publishedAt']
                }
                video_information['Comments']['Comment_Id_'+str(j+1)] = comment_information
        
            video["Video_Id_"+str(i+1)] = video_information


    #Dashboard
    st.header(":red[Channel Details]")
    for keys,values in channel_information.items():
        st.write(f"**{keys}** : {values}")

    st.write(f":orange[If you want to migrate the data of {channel_information['Channel_Name']} channel, go to **Migrate Tab**!]")

    #Sharing variables to other page
    st.session_state.channel_id = channel_id
    st.session_state.channel = channel
    st.session_state.video = video
