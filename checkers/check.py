import json

class Checker:
    def __init__(self, path):
        self.path = path
        self.type = "Generic"
        self.result = None
        self.score = None

    @property
    def dict(self):
        return {"result": self.result, "score": self.score, "file": self.path, "type": self.type}

    def __str__(self):
        return "{} checker for file: {}" % (self.type, self.path)

    def to_json(self):
        return json.dumps(self.dict)

