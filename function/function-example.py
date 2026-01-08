# below is the format of a function
# `def` is the keyword used to declare a function
# `function_name` is the name you want to give it
# the `function_name` has to be followed by parentheses 
# arguments can be passed in as needed

def function_name(parameters):

    """Docstring explaining the function"""
    # Code block (indented)
    return # Optional   

# Examples

def greet(name):
    print(f"Hi {name}!")

def add(a: int, b: int) -> int:
    return a+b


greet("santosh")
print(add(1,2))