class ExecNode:
    def open(self): pass
    def next(self): pass
    def close(self): pass


class SeqScanExec(ExecNode):
    def __init__(self, table, datastore):
        self.table = table
        self.datastore = datastore
        self.rows = None
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

    def next(self):
        row = self.child.next()
        if row is None:
            return None

        # project only requested columns
        return {c: row[c] for c in self.columns}
