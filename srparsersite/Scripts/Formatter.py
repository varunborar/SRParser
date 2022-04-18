import json


def formatJson(obj: str):
    return json.loads(obj)


def formatString(obj: str):
    return json.dumps(obj)
