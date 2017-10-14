import requests
import json

class WOT_API:

    api_key = "e404cccc3b85ad275f20d719a8065e6d77ac8ee6"

    @staticmethod
    def getRating(host):
        link = "http://api.mywot.com/0.4/public_link_json2?hosts=" + host + "/&key=" + WOT_API.api_key
        r = requests.get(link)
        print (r.content.decode())
        return r.json()

    @staticmethod
    def getTrustworthyness(host):
        response = WOT_API.getRating(host)
        try:
            return response[list(response.keys())[0]]["0"][0]
        except:
            return -1

print (WOT_API.getTrustworthyness("www.awillum.com"))