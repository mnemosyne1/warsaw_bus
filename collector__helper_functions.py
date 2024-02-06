import argparse
import requests
import sys


def get_from_link(link):
    """Takes the link and repeats trying to receive
    data from it until it succeeds or gets a fatal error"""
    wrong_string = "Błędna metoda lub parametry wywołania"
    while True:
        try:
            __ans = requests.get(link)
            if __ans.status_code == 200 and __ans.json()['result'] == 'false':
                exit(__ans.json()['error'])
            while (__ans.status_code != 200 or
                   __ans.json()['result'] == wrong_string):
                __ans = requests.get(link)
                if (__ans.status_code == 200 and
                        __ans.json()['result'] == 'false'):
                    exit(__ans.json()['error'])
            return __ans
        except Exception:
            print('Exception in get_from_link', file=sys.stderr)
            continue


def get_key():
    """Returns apikey, link to file with which should be given
        as an argument when calling the script"""
    __parser = argparse.ArgumentParser()
    __parser.add_argument('keyfile', help='name of file with API key')
    args = __parser.parse_args()
    try:
        with open(args.keyfile, 'r') as keyfile:
            return keyfile.read()
    except Exception:
        exit('Error: apikey not found')


def create_link(url: str, apikey: str, other):
    """Creates link using a form common for requests to this API"""
    return url + '&apikey=' + apikey + '&' + other
