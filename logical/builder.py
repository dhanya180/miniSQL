from parser.ast import Select
from logical.logical_plan import (
    LogicalScan,
    LogicalFilter,
    LogicalProject,
)

class LogicalPlanBuilder:
    def build(self, ast):
        if isinstance(ast, Select):
            return self._build_select(ast)
        else:
            # CREATE TABLE has no logical plan
            return None

    def _build_select(self, node):
        plan = LogicalScan(node.table)

        if node.where:
            plan = LogicalFilter(node.where, plan)

        plan = LogicalProject(node.columns, plan)
        return plan
