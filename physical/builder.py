# from logical.logical_plan import (
#     LogicalScan,
#     LogicalFilter,
#     LogicalProject,
# )
# from physical.physical_plan import (
#     SeqScanExec,
#     FilterExec,
#     ProjectExec,
# )

# class PhysicalPlanBuilder:
#     def build(self, logical_plan):
#         if isinstance(logical_plan, LogicalScan):
#             return SeqScanExec(logical_plan.table)

#         if isinstance(logical_plan, LogicalFilter):
#             child = self.build(logical_plan.child)
#             return FilterExec(logical_plan.predicate, child)

#         if isinstance(logical_plan, LogicalProject):
#             child = self.build(logical_plan.child)
#             return ProjectExec(logical_plan.columns, child)

#         raise Exception("Unknown logical operator")


from logical.logical_plan import LogicalScan, LogicalFilter, LogicalProject
from executor.executor import SeqScanExec, FilterExec, ProjectExec

class PhysicalPlanBuilder:
    def __init__(self, datastore):
        self.datastore = datastore

    def build(self, plan):
        if isinstance(plan, LogicalScan):
            return SeqScanExec(plan.table, self.datastore)

        if isinstance(plan, LogicalFilter):
            child = self.build(plan.child)
            return FilterExec(plan.predicate, child)

        if isinstance(plan, LogicalProject):
            child = self.build(plan.child)
            return ProjectExec(plan.columns, child)

        raise Exception("Unknown logical plan")
