from parser.ast import CreateTable, Select

class SemanticAnalyzer:
    def __init__(self, catalog):
        self.catalog = catalog

    def analyze(self, ast):
        if isinstance(ast, CreateTable):
            self._analyze_create(ast)
        elif isinstance(ast, Select):
            self._analyze_select(ast)
        else:
            raise Exception("Unknown AST node")

    def _analyze_create(self, node):
        self.catalog.create_table(node.name, node.columns)

    def _analyze_select(self, node):
        table = self.catalog.get_table(node.table)

        # Check SELECT columns
        for col in node.columns:
            if col != "*" and col not in table.columns:
                raise Exception(f"Column '{col}' does not exist in '{table.name}'")

        # Check WHERE clause
        if node.where:
            if node.where.column not in table.columns:
                raise Exception(
                    f"Column '{node.where.column}' does not exist in '{table.name}'"
                )
