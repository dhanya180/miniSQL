class DataStore:
    def __init__(self):
        self.tables = {}

    def insert_table(self, name, rows):
        self.tables[name] = rows

    def get_rows(self, name):
        return self.tables.get(name, [])
