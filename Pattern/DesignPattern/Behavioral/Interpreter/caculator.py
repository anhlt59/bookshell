import re


class ExpressionProcessor:
    expression_compiler = re.compile(r"([a-zA-Z]\w*)")

    def __init__(self):
        self.variables = {}

    def calculate(self, expression):
        try:
            return eval(
                self.expression_compiler.sub(r"self.variables['\1']", expression)
            )
        except KeyError as e:
            raise KeyError(f"Variable {e} is not defined")


ep = ExpressionProcessor()
ep.variables['x'] = 5
ep.variables['y'] = 2
print(ep.calculate('1+2'))
print(ep.calculate('1+x*y'))
print(ep.calculate('1+x+z'))
