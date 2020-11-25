from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from apikey import apikey


class YoutubeBot:

    CLIENT_SECRET_FILE = 'client_secret.json'
    SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    credentials = flow.run_console()
    youtube = build('youtube', 'v3', credentials=credentials)

    def getVids(self):
        searchString = "kagaya john"  # search paramter
        numOfResults = 10
        ids = [] #stores the video ids
        
        youtube = build('youtube', 'v3', developerKey=apikey)
        req = youtube.search().list(q=searchString, part='snippet', type='video', maxResults=numOfResults)
        res = req.execute()
        print("You will be like/commenting on the following videos: ")
        for item in res['items']:
            print(item['snippet']['title'])
            ids.append((item['id']['videoId'], item['snippet']['channelId']))

        
        return ids

    def likeVids(self):
        print("---------------------------------------------")
        print("Startings LikeVids")
        ids = self.getVids()
        for videoId in ids:
            self.youtube.videos().rate(rating='like', id=videoId[0]).execute()

        print("---------------------------------------------")
        print("End of likeVids")
        print("---------------------------------------------")
    def commentVids(self):
        print("---------------------------------------------")
        print("Startings CommentVideos")
        ids = self.getVids()
        message = "nice videos"
        for id in ids:
            self.insert_comment(id[1], id[0], message)
        print("---------------------------------------------")
        print("End CommentVideos")
        print("---------------------------------------------")
        
    def insert_comment(self, channel_id, video_id, text):
        self.youtube.commentThreads().insert(
            part="snippet",
            body=dict(
                snippet=dict(
                    channelId=channel_id,
                    videoId=video_id,
                    topLevelComment=dict(
                        snippet=dict(
                            textOriginal=text
                        )
                    )
                )
            )
        ).execute()


bot = YoutubeBot()
bot.commentVids()
