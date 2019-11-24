import os
import requests
import json

class CGTNVideoParser:
    """Class to parse the CGTN online video"""

    def __init__(self, url):
        self.url = url
        pass

    def get_videos_json(self):
        try:
            r = requests.get(self.url)
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:", errh)
            return None
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:", errc)
            return None
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt)
            return None
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else", err)
            return None

        # with open(os.path.join("resources", "data", "video.json")) as json_videos:
        #     return json.load(json_videos)
        
        return r.json()
    
    def get_videos(self):
        videos = []

        for video in self.get_videos_json()['data']:
            video_url = video['coverVideo'][0]['video']['url']
            poster_url = video['coverVideo'][0]['poster']['url']
            detail_url = video['detailUrl']
            share_url = video['shareUrl']
            headline = video['longHeadline']
            publish_time = video['publishTime']
            editor = video['editorName']

            videos.append(CGTNVideo(video_url=video_url,
                                    poster_url=poster_url,
                                    detail_url=detail_url,
                                    share_url=share_url,
                                    headline=headline,
                                    publish_time=publish_time,
                                    editor=editor))
        return videos

class CGTNVideo:
    """Class to contain CGTN video metadata"""

    def __init__(self, video_url=None, poster_url=None, detail_url=None, share_url=None,
                    headline=None, publish_time=None, editor=None):
        self.video_url = video_url
        self.poster_url = poster_url
        self.detail_url = detail_url
        self.share_url = share_url
        self.headline = headline
        self.publish_time = publish_time
        self.editor = editor
        pass

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
