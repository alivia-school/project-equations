from Equation import EquationComponentType

# Проверка есть ли в уравнении скобки
def haveParentheses(equation):
    for c in equation.components:
        if c.type == EquationComponentType.Parentheses: 
            # Есть скобки
            return True
    
    # Нет скобок
    return False



# Выделить в уравнении скобки красным
def markParentheses(equation):
    for c in equation.components:
        if c.type == EquationComponentType.Parentheses: 
            # Выделяем
            c.color = "red"



 