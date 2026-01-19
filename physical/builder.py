from logical.logical_plan import LogicalScan, LogicalFilter, LogicalProject, LogicalInsert
from executor.executor import SeqScanExec, FilterExec, ProjectExec, InsertExec

class PhysicalPlanBuilder:
    def __init__(self, datastore, catalog):
        self.datastore = datastore
        self.catalog = catalog

    def build(self, plan):
        if isinstance(plan, LogicalScan):
            return SeqScanExec(plan.table, self.datastore)

        if isinstance(plan, LogicalFilter):
            child = self.build(plan.child)
            return FilterExec(plan.predicate, child)

        if isinstance(plan, LogicalProject):
            child = self.build(plan.child)
            return ProjectExec(plan.columns, child)
        
        if isinstance(plan, LogicalInsert):
            return InsertExec(
                plan.table,
                plan.values,
                self.datastore,
                self.catalog
            )

        raise Exception("Unknown logical plan")