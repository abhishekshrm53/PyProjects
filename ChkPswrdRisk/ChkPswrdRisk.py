import hashlib
import requests
import sys


def get_api_data(query):
    url = 'http://api.pwnedpasswords.com/range/' + query
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, try again')
    return res


def get_leak_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(pswrd):
    sha1pswrd = hashlib.sha1(pswrd.encode('utf-8')).hexdigest().upper()
    hashstart, hashrest = sha1pswrd[:5], sha1pswrd[5:]
    response = get_api_data(hashstart)
    return get_leak_count(response, hashrest)


def main(args):
    for arg in args:
        with open(arg, mode='r') as file:
            pswrds = file.read()
            pswrds = pswrds.splitlines()
            for pswrd in pswrds:
                count = pwned_api_check(pswrd)
                if count:
                    print(f'{pswrd} was found {count} times. Weak password.')
                else:
                    print(f'{pswrd} was NOT found. Password seems to be good.')
    print('Done!')
    return 0


main(sys.argv[1:])
