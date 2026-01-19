from lexer.tokens import TokenType

class ExecNode:
    def open(self):
        pass

    def next(self):
        pass

    def close(self):
        pass

class SeqScanExec(ExecNode):
    def __init__(self, table, datastore):
        self.table = table
        self.datastore = datastore
        self.rows = []
        self.idx = 0

    def open(self):
        self.rows = self.datastore.get_rows(self.table)
        self.idx = 0

    def next(self):
        if self.idx >= len(self.rows):
            return None
        row = self.rows[self.idx]
        self.idx += 1
        return row

    def close(self):
        pass

class FilterExec(ExecNode):
    def __init__(self, predicate, child):
        self.predicate = predicate
        self.child = child

    def open(self):
        self.child.open()

    def next(self):
        while True:
            row = self.child.next()
            if row is None:
                return None

            lhs = row[self.predicate.column]
            rhs = int(self.predicate.value)

            if self.predicate.op == ">" and lhs > rhs:
                return row
            if self.predicate.op == "<" and lhs < rhs:
                return row
            if self.predicate.op == "=" and lhs == rhs:
                return row

    def close(self):
        self.child.close()

class ProjectExec(ExecNode):
    def __init__(self, columns, child):
        self.columns = columns
        self.child = child

    def open(self):
        self.child.open()

    def next(self):
        row = self.child.next()
        if row is None:
            return None
        return {c: row[c] for c in self.columns}

    def close(self):
        self.child.close()

from lexer.tokens import TokenType

class InsertExec(ExecNode):
    def __init__(self, table, values, datastore, catalog):
        self.table = table
        self.values = values
        self.datastore = datastore
        self.catalog = catalog

    def open(self):
        table = self.catalog.get_table(self.table)
        row = {}

        for (col, col_type), value in zip(table.columns.items(), self.values):
            if col_type == TokenType.INT:
                row[col] = int(value)
            else:
                row[col] = value

        self.datastore.insert_row(self.table, row)

    def next(self):
        return None

    def close(self):
        pass
