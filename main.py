from lexer.lexer import Lexer
from parser.parser import Parser
from semantic.analyzer import SemanticAnalyzer
from storage.catalog import Catalog
from storage.data import DataStore
from logical.builder import LogicalPlanBuilder
from logical.optimizer import LogicalOptimizer
from physical.builder import PhysicalPlanBuilder
from executor.executor import InsertExec

catalog = Catalog()
datastore = DataStore()

def run(sql: str):
    lexer = Lexer(sql)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    semantic = SemanticAnalyzer(catalog)
    semantic.analyze(ast)

    logical_builder = LogicalPlanBuilder()
    logical_plan = logical_builder.build(ast)

    if logical_plan is None:
        print("DDL processed")
        return
    
    if logical_plan.__class__.__name__ != "LogicalInsert":
        optimizer = LogicalOptimizer()
        logical_plan = optimizer.optimize(logical_plan)

    physical_builder = PhysicalPlanBuilder(datastore, catalog)
    exec_plan = physical_builder.build(logical_plan)

    exec_plan.open()

    if isinstance(exec_plan, InsertExec):
        print("1 row inserted")
    else:
        print("RESULT:")
        while True:
            row = exec_plan.next()
            if row is None:
                break
            print(row)

    exec_plan.close()


def repl():
    print("MiniSQL (type Ctrl+C to exit)")
    while True:
        try:
            sql = input("minisql> ").strip()
            if not sql:
                continue
            run(sql)
        except KeyboardInterrupt:
            print("\nBye")
            break
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    repl()
