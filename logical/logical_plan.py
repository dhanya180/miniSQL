class LogicalPlan:
    pass


class LogicalScan(LogicalPlan):
    def __init__(self, table):
        self.table = table

    def __repr__(self):
        return f"LogicalScan(table={self.table})"


class LogicalFilter(LogicalPlan):
    def __init__(self, predicate, child):
        self.predicate = predicate
        self.child = child

    def __repr__(self):
        return f"LogicalFilter({self.predicate}, child={self.child})"


class LogicalProject(LogicalPlan):
    def __init__(self, columns, child, required=None):
        self.columns = columns
        self.required = required or set(columns)
        self.child = child

    def __repr__(self):
        return f"LogicalProject({self.columns}, child={self.child})"
