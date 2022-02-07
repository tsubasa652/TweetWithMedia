import os
from requests_oauthlib import OAuth1Session

twitter_base_url = 'https://api.twitter.com'
twitter_upload_media_url = "https://upload.twitter.com/1.1/media/upload.json"


def tweetWithMedia(tweet, filePath):
    try:
        
        twitter = OAuth1Session(
            os.environ["API_KEY"],
            os.environ["API_SECRET_KEY"],
            os.environ["ACCESS_TOKEN"],
            os.environ["ACCESS_TOKEN_SECRET"]
        )
        
        f = open(filePath, 'rb')
        files = {'media': f.read()}
        res = twitter.post(twitter_upload_media_url, files=files)

        f.close()
       
        if res.status_code != 200:
            print ("画像アップロード失敗: ", res.text, res.status_code)
            exit()
            
        res = res.json()
        
        if(not "media_id_string" in res):
            raise Exception("Can't upload file")
        
        params = {
            "status": tweet,
            "media_ids": res["media_id_string"]
        }
        res = twitter.post("https://api.twitter.com/1.1/statuses/update.json", params = params)
        
        if res.status_code != 200:
            print("ツイート失敗：", res.text, res.status_code)
        else:
            print("ツイートしました")
    except Exception as e:
        print(e)