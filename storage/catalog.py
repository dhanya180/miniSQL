class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns   # dict: col -> type


class Catalog:
    def __init__(self):
        self.tables = {}

    def create_table(self, name, columns):
        if name in self.tables:
            raise Exception(f"Table '{name}' already exists")

        col_map = {}
        for col, typ in columns:
            if col in col_map:
                raise Exception(f"Duplicate column '{col}'")
            col_map[col] = typ

        self.tables[name] = Table(name, col_map)

    def get_table(self, name):
        if name not in self.tables:
            raise Exception(f"Table '{name}' does not exist")
        return self.tables[name]
