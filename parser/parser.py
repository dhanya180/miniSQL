from lexer.tokens import TokenType
from parser.ast import CreateTable, Select, Where

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def eat(self, token_type):
        if self.current().type == token_type:
            self.pos += 1
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current()}")

    def parse(self):
        if self.current().type == TokenType.CREATE:
            return self.parse_create()
        elif self.current().type == TokenType.SELECT:
            return self.parse_select()
        else:
            raise SyntaxError("Unknown statement")

    def parse_create(self):
        self.eat(TokenType.CREATE)
        self.eat(TokenType.TABLE)
        name = self.current().value
        self.eat(TokenType.IDENT)

        self.eat(TokenType.LPAREN)
        columns = []
        while self.current().type != TokenType.RPAREN:
            col_name = self.current().value
            self.eat(TokenType.IDENT)
            col_type = self.current().type
            self.eat(col_type)
            columns.append((col_name, col_type.name))
            if self.current().type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.SEMICOLON)
        return CreateTable(name, columns)

    def parse_select(self):
        self.eat(TokenType.SELECT)
        columns = []
        while self.current().type != TokenType.FROM:
            columns.append(self.current().value)
            self.eat(TokenType.IDENT)
            if self.current().type == TokenType.COMMA:
                self.eat(TokenType.COMMA)

        self.eat(TokenType.FROM)
        table = self.current().value
        self.eat(TokenType.IDENT)

        where = None
        if self.current().type == TokenType.WHERE:
            self.eat(TokenType.WHERE)
            col = self.current().value
            self.eat(TokenType.IDENT)
            op = self.current().value
            self.eat(self.current().type)
            val = self.current().value
            self.eat(TokenType.NUMBER)
            where = Where(col, op, val)

        self.eat(TokenType.SEMICOLON)
        return Select(columns, table, where)
