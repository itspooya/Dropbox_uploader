import requests
import re
from requests.exceptions import RequestException
import urllib
import shutil

class ERROR_FILE_SIZE(Exception):
    print("ERROR Getting File Size")

class ERROR_DOWNLOADING_FILE(Exception):
    print("Problem Downloading File")



def get_file_size(url):
    req = urllib.request.Request(url, method="HEAD")
    fil = urllib.request.urlopen(req)
    if fil.status == 200:
        if fil.headers['Content-Length']:
            return fil.headers['Content-Length']
        else:
            raise ERROR_FILE_SIZE
    else:
        raise ERROR_FILE_SIZE

    return len(fil.content)


def download(url):
    try:
        with requests.get(url, stream=True) as r:
            fname = ''
            if "Content-Disposition" in r.headers.keys():
                fname = re.findall("filename=(.+)", r.headers["Content-Disposition"])[0]
            else:
                fname = url.split("/")[-1]
            with open("{}".format(fname), "wb") as f:
                shutil.copyfileobj(r.raw, f)
    except RequestException:
        raise ERROR_DOWNLOADING_FILE
    return fname