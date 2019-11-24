import sys
import logging
import unittest

from resources.lib.cgtnschedule import CGTNScheduleParser, CGTNLiveScheduleItem, CGTNLiveScheduleState

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout)) 

class CGTNScheduleParserTest(unittest.TestCase):

    schedule_url = "https://api.cgtn.com/website/api/live/channel/epg/list?channelId=1"

    def setUp(self):
        self.parser = CGTNScheduleParser(CGTNScheduleParserTest.schedule_url)

    def test_get_schedule(self):
        schedule = self.parser.get_schedule()
        logger.debug("Number of schedule items parsed: " + str(len(schedule)))
        self.assertNotEqual(len(schedule), 0)

        for item in schedule:
            self.assertIsInstance(item, CGTNLiveScheduleItem)
            logger.debug(" Schedule item: " + str(item)) 
    
    def test_get_play_item(self):
        self.parser.get_schedule()
        play_item = self.parser.get_play_item()
        self.assertIsNotNone(play_item)
        self.assertIsInstance(play_item, CGTNLiveScheduleItem)
        logger.debug("Item currently playing: " + str(play_item))


if __name__ == '__main__':
    unittest.main()