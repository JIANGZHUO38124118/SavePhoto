# entity/Parameter.py

class Parameter:

    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def getKey(self) -> str:
        return self.key

    def getValue(self) -> str:
        return self.value
    
    def updateParameter(self, photoid, key, new_value):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                UPDATE parameter 
                SET value = ? 
                WHERE photoid = ? AND key = ?
            """, (new_value, photoid, key))
            self.conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()