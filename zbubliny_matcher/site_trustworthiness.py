import requests


class WOT_API:

    api_key = "e404cccc3b85ad275f20d719a8065e6d77ac8ee6"

    @staticmethod
    def get_rating(host):
        link = "http://api.mywot.com/0.4/public_link_json2?hosts=" + host + "/&key=" + WOT_API.api_key
        r = requests.get(link)
        # print (r.content.decode())
        return r.json()

    @staticmethod
    def get_trustworthiness(host):
        """Returns number between 0 - 100, meaning the site trustworthyness in percent, returns -1 if site unknown"""
        try:
            response = WOT_API.get_rating(host)
            return response[list(response.keys())[0]]["0"][0]
        except:
            return -1

    @staticmethod
    def get_flags(host):
        """Returns dictionary in format 'Condition':How confident I am"""
        """For example: {'Other': 6, 'Online tracking': 48, 'Good site': 99} (This is for google)"""
        response = WOT_API.get_rating(host)
        hazards = response[list(response.keys())[0]]["categories"]

        flags = {}

        flag_database = {101: "Malware or viruses", 102: "Poor costumer experience", 103:"Phishing", 104:"Scam", 105:"Potentially illegal", 201:"Misleading or unethical", 202: "Privacy risks", 203:"Suspicious", 204:"Hate", 205:"Spam", 206:"Potentially unwanted programs", 207:"Ads / pop-ups", 301:"Online tracking", 302:"Alternative or controversial medicine", 303: "Opinions, religion, politics", 304: "Other", 501:"Good site", 401:"Adult content", 402:"Nudity", 403:"Gruesome"}

        for key in hazards:
            flags[flag_database[int(key)]] = hazards[key]

        return flags


if __name__ == "__main__":
    print (WOT_API.get_flags("www.google.com"))