import simplejson as json


def build_response(urls=[], message="", icon="48.png"):
    d = {
        'urls': urls,
        'message': message,
        'icon': icon
    }
    return json.dumps(d)
