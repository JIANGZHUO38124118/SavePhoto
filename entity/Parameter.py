# entity/Parameter.py

class Parameter:

    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def getKey(self) -> str:
        return self.key

    def getValue(self) -> str:
        return self.value