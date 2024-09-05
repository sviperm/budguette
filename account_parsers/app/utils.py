import json


def save_cookies(context, path):
    cookies = context.cookies()
    with open(path, 'w') as file:
        json.dump(cookies, file)


def load_cookies(context, path):
    with open(path, 'r') as file:
        cookies = json.load(file)
        context.add_cookies(cookies)
