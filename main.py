import json
from urllib import request
from defusedxml import ElementTree

config = {}

with open("config.json", "r") as config_file:
    config = json.load(config_file)

for feed in config["feeds"]:
    print(feed["url"])

    with request.urlopen(feed["url"], timeout=10) as f:
        data = f.read().decode('utf-8')

        et = ElementTree.fromstring(data)

        channel = et.find("channel")

        for item in channel.findall("item"):
            title = item.find("title").text

            some_matches = False

            for filters in feed["filters"]:
                some_matches = all(map(lambda w: w in title, tuple(filters["keys"])))

                if some_matches:
                    break

            if not some_matches:
                channel.remove(item)

        with open(feed["output"], "w") as f:
            f.write(ElementTree.tostring(et).decode('utf-8'))

