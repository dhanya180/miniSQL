from parser.ast import Select,  Insert
from logical.logical_plan import (
    LogicalScan,
    LogicalFilter,
    LogicalProject,
    LogicalInsert
)

class LogicalPlanBuilder:
    def build(self, ast):
        if isinstance(ast, Select):
            return self._build_select(ast)
        if isinstance(ast, Insert):
            return LogicalInsert(ast.table, ast.values)
        return None

    def _build_select(self, node):
        plan = LogicalScan(node.table)

        if node.where:
            plan = LogicalFilter(node.where, plan)

        plan = LogicalProject(node.columns, plan)
        return plan
