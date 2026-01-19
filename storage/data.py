class DataStore:
    def __init__(self):
        self.tables = {}

    def get_rows(self, name):
        rows = self.tables.get(name)
        if rows is None:
            return []
        return rows

    def insert_row(self, table, row):
        if table not in self.tables:
            self.tables[table] = []
        self.tables[table].append(row)
