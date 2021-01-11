import sys
import os
import json
from urllib import request
from defusedxml import ElementTree

def usage():
    print("python %s URL|FILE" % __file__)
    print("Filters URL or FILE xml file to remove entries that don't match the filters on config.json")

def input(source):
    if os.path.exists(source) and os.path.isfile(source):
        with open(source) as f:
            data = f.read()
    else:
        with request.urlopen(source, timeout=10) as f:
            data = f.read().decode('utf-8')

    return data

def filter_xml(data, config):
    et = ElementTree.fromstring(data)

    channel = et.find("channel")

    for item in channel.findall("item"):
        title = item.find("title").text

        some_matches = False

        for filters in config["filters"]:
            some_matches = all(map(lambda w: w in title, tuple(filters["keys"])))

            if some_matches:
                if filters.get("category", None):
                    elem = '<qbCategory>%s</qbCategory>' % filters["category"]
                    item.append((ElementTree.fromstring(elem)))
                break

        if not some_matches:
            channel.remove(item)


    print(ElementTree.tostring(et).decode('utf-8'))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        exit(1)

    config = {}
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    source = sys.argv[1]
    data = input(source)

    filter_xml(data, config)