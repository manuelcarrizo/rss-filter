import sys
import os
import json
from urllib import request
from defusedxml import ElementTree
import qbittorrentapi

def usage():
    print("python %s CONFIG_FILE [URL|FILE|stdin]" % __file__)
    print("Reads an torrent RSS feed and add items to qBittorrent. Gets categories and qBittorrent auth from json file")

def input(source):
    if source is None:
        data = sys.stdin.read()
    elif os.path.exists(source) and os.path.isfile(source):
        with open(source) as f:
            data = f.read()
    else:
        with request.urlopen(source, timeout=10) as f:
            data = f.read().decode('utf-8')

    return data

def client(config):
    qbt = config["qbittorrent"]

    qbt_client = qbittorrentapi.Client(host=qbt["host"], port=qbt["port"], username=qbt["username"], password=qbt["password"])

    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    return qbt_client

def add_items(data, config, client):
    et = ElementTree.fromstring(data)

    channel = et.find("channel")

    for item in channel.findall("item"):
        title = item.find("title").text
        link = item.find("link").text
        category = None

        some_matches = False
        
        for filters in config["filters"]:
            some_matches = all(map(lambda w: w in title, tuple(filters["keys"])))

            if some_matches:
                category = filters.get("category", None)
                break
        
        print("adding %s - %s" % (link, category))
        client.torrents.add(urls=link, category=category)

if __name__ == "__main__":
    config = {}

    if len(sys.argv) not in [2, 3]:
        usage()
        exit(1)


    config = {}
    with open(sys.argv[1], "r") as config_file:
        config = json.load(config_file)
    
    source = None
    try:
        source = sys.argv[2]
    except IndexError:
        pass

    data = input(source)
    client = client(config)

    add_items(data, config, client)
