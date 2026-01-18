# from lexer.lexer import Lexer
# from parser.parser import Parser

# def run(sql):
#     lexer = Lexer(sql)
#     tokens = lexer.tokenize()
#     print("TOKENS:", tokens)

#     parser = Parser(tokens)
#     ast = parser.parse()
#     print("AST:", ast)

# if __name__ == "__main__":
#     while True:
#         try:
#             sql = input("minisql> ")
#             run(sql)
#         except Exception as e:
#             print("Error:", e)


# from lexer.lexer import Lexer
# from parser.parser import Parser
# from semantic.analyzer import SemanticAnalyzer
# from storage.catalog import Catalog

# catalog = Catalog()

# def run(sql):
#     lexer = Lexer(sql)
#     tokens = lexer.tokenize()

#     parser = Parser(tokens)
#     ast = parser.parse()

#     semantic = SemanticAnalyzer(catalog)
#     semantic.analyze(ast)

#     print("✔ Semantic analysis passed")
#     print("AST:", ast)

# if __name__ == "__main__":
#     while True:
#         try:
#             sql = input("minisql> ")
#             run(sql)
#         except Exception as e:
#             print("❌ Error:", e)


# from lexer.lexer import Lexer
# from parser.parser import Parser
# from semantic.analyzer import SemanticAnalyzer
# from storage.catalog import Catalog
# from logical.builder import LogicalPlanBuilder

# catalog = Catalog()

# def run(sql):
#     lexer = Lexer(sql)
#     tokens = lexer.tokenize()

#     parser = Parser(tokens)
#     ast = parser.parse()

#     semantic = SemanticAnalyzer(catalog)
#     semantic.analyze(ast)

#     builder = LogicalPlanBuilder()
#     logical_plan = builder.build(ast)

#     if logical_plan:
#         print("LOGICAL PLAN:")
#         print(logical_plan)
#     else:
#         print("✔ DDL processed")

# if __name__ == "__main__":
#     while True:
#         try:
#             sql = input("minisql> ")
#             run(sql)
#         except Exception as e:
#             print("❌ Error:", e)


# from lexer.lexer import Lexer
# from parser.parser import Parser
# from semantic.analyzer import SemanticAnalyzer
# from storage.catalog import Catalog
# from logical.builder import LogicalPlanBuilder
# from logical.optimizer import LogicalOptimizer

# catalog = Catalog()

# def run(sql):
#     lexer = Lexer(sql)
#     tokens = lexer.tokenize()

#     parser = Parser(tokens)
#     ast = parser.parse()

#     semantic = SemanticAnalyzer(catalog)
#     semantic.analyze(ast)

#     builder = LogicalPlanBuilder()
#     logical_plan = builder.build(ast)

#     if logical_plan:
#         print("ORIGINAL LOGICAL PLAN:")
#         print(logical_plan)

#         optimizer = LogicalOptimizer()
#         optimized = optimizer.optimize(logical_plan)

#         print("\nOPTIMIZED LOGICAL PLAN:")
#         print(optimized)
#     else:
#         print("✔ DDL processed")

# if __name__ == "__main__":
#     while True:
#         try:
#             sql = input("minisql> ")
#             run(sql)
#         except Exception as e:
#             print("❌ Error:", e)


# from lexer.lexer import Lexer
# from parser.parser import Parser
# from semantic.analyzer import SemanticAnalyzer
# from storage.catalog import Catalog
# from logical.builder import LogicalPlanBuilder
# from logical.optimizer import LogicalOptimizer
# from physical.builder import PhysicalPlanBuilder

# catalog = Catalog()

# def run(sql):
#     lexer = Lexer(sql)
#     tokens = lexer.tokenize()

#     parser = Parser(tokens)
#     ast = parser.parse()

#     semantic = SemanticAnalyzer(catalog)
#     semantic.analyze(ast)

#     builder = LogicalPlanBuilder()
#     logical_plan = builder.build(ast)

#     if logical_plan:
#         print("LOGICAL PLAN:")
#         print(logical_plan)

#         optimizer = LogicalOptimizer()
#         optimized = optimizer.optimize(logical_plan)

#         print("\nOPTIMIZED LOGICAL PLAN:")
#         print(optimized)

#         physical_builder = PhysicalPlanBuilder()
#         physical_plan = physical_builder.build(optimized)

#         print("\nPHYSICAL PLAN:")
#         print(physical_plan)
#     else:
#         print("✔ DDL processed")

# if __name__ == "__main__":
#     while True:
#         try:
#             sql = input("minisql> ")
#             run(sql)
#         except Exception as e:
#             print("❌ Error:", e)


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
            print("❌ Error:", e)
