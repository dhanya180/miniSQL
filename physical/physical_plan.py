class PhysicalPlan:
    pass


class SeqScanExec(PhysicalPlan):
    def __init__(self, table):
        self.table = table

    def __repr__(self):
        return f"SeqScanExec(table={self.table})"


class FilterExec(PhysicalPlan):
    def __init__(self, predicate, child):
        self.predicate = predicate
        self.child = child

    def __repr__(self):
        return f"FilterExec({self.predicate}, child={self.child})"


class ProjectExec(PhysicalPlan):
    def __init__(self, columns, child):
        self.columns = columns
        self.child = child

    def __repr__(self):
        return f"ProjectExec({self.columns}, child={self.child})"
