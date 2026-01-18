from logical.logical_plan import (
    LogicalScan,
    LogicalFilter,
    LogicalProject,
)

class LogicalOptimizer:
    def optimize(self, plan):
        return self._optimize_node(plan)

    def _optimize_node(self, node):
        if isinstance(node, LogicalFilter):
            node.child = self._optimize_node(node.child)
            return node

        if isinstance(node, LogicalProject):
            node.child = self._optimize_node(node.child)
            return self._safe_pushdown(node)

        return node

    def _safe_pushdown(self, project):
        if isinstance(project.child, LogicalFilter):
            filter_node = project.child

            # 🔑 KEEP predicate column
            required = set(project.columns)
            required.add(filter_node.predicate.column)

            new_project = LogicalProject(
                columns=list(required),
                child=filter_node.child,
            )

            return LogicalFilter(filter_node.predicate, new_project)

        return project
