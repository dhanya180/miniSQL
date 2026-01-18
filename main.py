from lexer.lexer import Lexer
from parser.parser import Parser
from semantic.analyzer import SemanticAnalyzer
from storage.catalog import Catalog
from storage.data import DataStore
from logical.builder import LogicalPlanBuilder
from logical.optimizer import LogicalOptimizer
from physical.builder import PhysicalPlanBuilder

catalog = Catalog()
datastore = DataStore()

# sample data
datastore.insert_table("users", [
    {"id": 1, "name": "Alice", "age": 22},
    {"id": 2, "name": "Bob", "age": 17},
    {"id": 3, "name": "Carol", "age": 30},
])

def run(sql):
    tokens = Lexer(sql).tokenize()
    ast = Parser(tokens).parse()
    SemanticAnalyzer(catalog).analyze(ast)

    logical = LogicalPlanBuilder().build(ast)
    if logical is None:
        print("✔ DDL processed")
        return

    optimized = LogicalOptimizer().optimize(logical)
    exec_plan = PhysicalPlanBuilder(datastore).build(optimized)

    exec_plan.open()
    print("\nRESULT:")
    while True:
        row = exec_plan.next()
        if row is None:
            break
        print(row)
    exec_plan.close()

if __name__ == "__main__":
    while True:
        try:
            run(input("minisql> "))
        except Exception as e:
            print("Error:", e)
