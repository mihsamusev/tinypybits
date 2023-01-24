import ast
import inspect
# add subscript t to lambda expression
# convert:
# x <= 100
# lambda t: x[t] <= 100 
expression = lambda: x <= 100
expression_str = inspect.getsource(expression)
expression_str = expression_str.split(" = ")[-1].strip()

result= ast.parse(expression_str)
print(ast.dump(result, indent=4))

result = compile(result, '<string>', mode='exec')

