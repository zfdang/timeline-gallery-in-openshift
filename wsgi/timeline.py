# -*- coding:UTF-8 -*-
# timelineJS: http://timeline.verite.co/
import json


class Timeline(object):
    """docstring for Timeline"""
    def __init__(self, headline, text, startDate, type='default'):
        super(Timeline, self).__init__()
        self.content = {}
        self.content['timeline'] = {}
        self.content['timeline']["headline"] = headline
        self.content['timeline']['type'] = type
        self.content['timeline']['text'] = text
        self.content['timeline']['startDate'] = startDate
        self.content['timeline']['date'] = []

    def add_date(self, startDate, headline, asset_media, endDate="", text="", asset_credit="", asset_caption=""):
        ############################################
        # date format
        ############################################
        # "startDate":"2012,1,26",
        # "endDate":"2012,1,27",
        # "headline":"Sh*t Politicians Say",
        # "text":"<p>In true political fashion, his character rattles off common jargon heard from people running for office.</p>",
        # "asset":
        # {
        #     "media":"http://youtu.be/u4XpeU9erbg",
        #     "credit":"",
        #     "caption":""
        # }
        _date = {}
        _date['startDate'] = startDate
        _date['endDate'] = endDate
        _date['headline'] = headline
        _date['text'] = text
        _date['asset'] = {}
        _date['asset']['media'] = asset_media
        _date['asset']['credit'] = asset_credit
        _date['asset']['caption'] = asset_caption
        self.content['timeline']['date'].append(_date)

    def get_json(self):
        result = json.dumps(self.content)
        return result


def get_sample_json():
    tr = Timeline("Chinese PRC", "this is the text", '2011,9,30')
    tr.add_date('2011,10,1', 'baidu home', 'http://www.baidu.com', '2011,10,5',)
    tr.add_date('2011,12,1', 'google home', 'http://www.google.com', '2011,12,5')
    tr.add_date('2012,15,1', 'zfdang blog', 'http://blog.zfdang.com')
    return tr.get_json()


if __name__ == "__main__":

    print get_sample_json()
