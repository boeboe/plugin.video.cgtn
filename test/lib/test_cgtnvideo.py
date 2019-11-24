import sys
import logging
import unittest

from resources.lib.cgtnvideo import CGTNVideoParser, CGTNVideo

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout)) 

class CGTNVideoParserTest(unittest.TestCase):

    video_url = "https://api.cgtn.com/website/api/program/getList"

    def setUp(self):
        self.parser = CGTNVideoParser(CGTNVideoParserTest.video_url)

    def test_get_videos(self):
        videos = self.parser.get_videos()
        self.assertNotEqual(len(videos), 0)
        logger.debug("Number of videos parsed: " + str(len(videos)))
        for video in videos:
            self.assertIsNotNone(video.video_url)
            self.assertIsNotNone(video.poster_url)
            self.assertIsNotNone(video.detail_url)
            self.assertIsNotNone(video.share_url)
            self.assertIsNotNone(video.headline)
            self.assertIsNotNone(video.publish_time)
            self.assertIsNotNone(video.editor)


if __name__ == '__main__':
    unittest.main()