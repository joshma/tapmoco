import simplejson as json


def build_response(urls=[], message="Default message text"):
    d = {
        'urls': urls,
        'message': message
    }
    return json.dumps(d)
