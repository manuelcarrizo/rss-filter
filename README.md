# Bittorrent RSS filter

This two scripts help filtering content from RSS torrent feeds

## filter.py

`python filter.py config.json`

Reads a RSS feed obtained from the json config file. Source can be a file, an url or stdin (if source is not present in json file).

Then removes all the items in the RSS that doesn't match a key on the filters list of json file.

A new RSS is generated and printed to stdout, containing only matching items.

## upload.py

`python upload.py config.json [input]`

Reads a RSS feed that can be a file, an url or stdin if `input` parameter is ommited.
Tries to find the corresponding category from the config json and adds the torrents to the download queue from qBittorent. qBittorent authentication is obtained from config
