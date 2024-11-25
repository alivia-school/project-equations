from Equation import EquationComponentType, EquationComponent

# Перевести число в строку со знаком "+" если число >= 0 и плюс нужен
# Также не печатаем "1" перед неизвестным (1x = x)
def str_plus(number, ignore_plus, isUnknown=False):
    if isUnknown and number == -1:
        return "-"
        
    if isUnknown and number == 1:
        return "" if ignore_plus else "+"
        
    if ignore_plus or number < 0:
        return str(number)
        
    return  '+' + str(number)
    


# Проверка есть ли в уравнении скобки
def haveParentheses(equation):
    # Обходим все компоненты уравнения
    for c in equation.components:
        if c.type == EquationComponentType.Parentheses: 
            # Есть скобки
            return True
    
    # Нет скобок
    return False


# Выделить в уравнении скобки красным
def markParentheses(equation):
    # Обходим все компоненты уравнения
    for c in equation.components:
        if c.type == EquationComponentType.Parentheses: 
            # Выделяем
            c.color = "red"


# Раскрыть скобки
def expandParentheses(equation): 
    ## Переменные: ##
    # Результат
    r = ""
    # Знак
    s = 1
    # Компонент перед скобкой
    a = EquationComponent(1)
    # Флаг: Внутри скобок или нет
    b = False
    # Флаг: Начало выражения
    start = True
    
    # Обходим все компоненты уравнения
    for c in equation.components:       
    
        # Проверяем скобки    
        if c.value == '(':
            b = True
            
            # К следующему компоненту уравнения
            continue
            
        if c.value == ')':
            b = False
            
            # Сбросим компонент
            a = EquationComponent(1)
            
            # К следующему компоненту уравнения
            continue
            
            
        
        # Мы внутри скобок?
        if b == True:
            # Да, внутри скобок
            
            if c.type == EquationComponentType.Unknown: 
                # Текущая компонента - неизвестное (типо "x" или "2x" и т.д.)
                
                # Перемножим с тем что за скобкой и добавим в результат    
                r += str_plus(a.value * c.factor_value * s, start, True) + c.value
                
            elif c.type == EquationComponentType.Number: 
                # Текущая компонента - число
                
                # Перемножим с тем что за скобкой и добавим в результат  
                if a.type == EquationComponentType.Unknown:                 
                    r += str_plus(a.factor_value * c.value * s, start, True) + a.value
                elif c.type == EquationComponentType.Number:                    
                    r += str_plus(a.value * c.value * s, start)  
                    
        else:
            # Мы вне скобок
            
            if c.type == EquationComponentType.Unknown or c.type == EquationComponentType.Number: 
                # Тип компоненты неизвестное или число
                
                # Проверим нет ли скобки после компонента
                if c.as_factor == True:
                
                    # Сохраним компонент, на него что будем умножать внутри скобок
                    a = EquationComponent(c)
                    # Добавим знак 
                    if a.type == EquationComponentType.Unknown: 
                        a.factor_value *= s                      
                    elif a.type == EquationComponentType.Number: 
                        a.value *= s
                    # Сбросим знак на плюс
                    s = 1
                    
                else:    
                    # Добавим компонент в результат    
                    
                    if c.type == EquationComponentType.Unknown: 
                        # Текущая компонента - неизвестное (типо "x" или "2x" и т.д.)
                        
                        r += str_plus(c.factor_value * s, start, True) + c.value
                        
                    elif c.type == EquationComponentType.Number: 
                        # Текущая компонента - число
                        
                        r += str_plus(c.value * s, start)


        if c.type == EquationComponentType.Operation:
        
            # Сохраняем знак
            if c.value == '-': 
                s = -1
            else:
                s = 1 
                
            # После любого действия это уже не начало выражения
            start = False
            
            
        if c.value == '=':
        
            # После "=" Вновь начало выражения
            start = True  
            
            # После "=" сбрасываем знак в "+"
            s = 1 
            
            # Добавим "=" в результат
            r += "="
    
    
    # Вернем результат
    return r



# Проверка нужен ли перенос элементов в уравнении
def needMove(equation):
    # Проверим левую чась
    for c in equation.left():        
        if c.type == EquationComponentType.Number:
            # Если есть числа слева, то перенос нужен
            return True   
            
    # Проверим правую чась
    for c in equation.rigth():
        if c.type == EquationComponentType.Unknown:
            # Если есть неизвестное справа, то перенос нужен
            return True    
    
    return False
    
    
# Пометить элементы для переноса
def markMoveElements(equation):
    a = EquationComponent(0)
    # Для левой части
    for c in equation.left():
        if c.type == EquationComponentType.Number:
            a.color = "red"
            c.color = "red"
            a = EquationComponent(0)
        elif c.type == EquationComponentType.Operation:        
            a = c
            
    # Для правой части
    for c in equation.rigth():
        if c.type == EquationComponentType.Unknown:
            a.color = "blue"
            c.color = "blue"
            a = EquationComponent(0)
        elif c.type == EquationComponentType.Operation:        
            a = c
        

# Выполнить перенос
def moveElements(equation):
    ## Переменные: ##
    # Результат левой части
    rl = ""
    # Результат правой части
    rr = ""
    
    # Знак
    s = 1
        
    # Оставим неизвесные слева
    for c in equation.left():        
            
        # Оставим неизвестное слева    
        if c.type == EquationComponentType.Unknown:
            # Текущая компонента - неизвестное                
            rl += str_plus(c.factor_value * s, rl=="", True) + c.value
          
                
        # Сохраняем знак
        if c.type == EquationComponentType.Operation:                
            if c.value == '-': 
                s = -1
            else:
                s = 1 
                
            
    # Сбросим знак
    s = 1             
    
    # Оставим числа справа и перенесем неизвестное влево
    for c in equation.rigth():

        # Перенесем неизвестное влево с противоположным знаком
        if c.type == EquationComponentType.Unknown:
            # Текущая компонента - неизвестное                
            rl += str_plus(c.factor_value * -s, rl=="", True) + c.value
          
        # Оставим числа справа
        if c.type == EquationComponentType.Number:
            # Текущая компонента - число                
            rr += str_plus(c.value * s, rr=="")            
            
        # Сохраняем знак
        if c.type == EquationComponentType.Operation:                
            if c.value == '-': 
                s = -1
            else:
                s = 1             

    # Сбросим знак
    s = 1             
    
    # Перенесем числа вправо
    for c in equation.left():        
        # Перенесем числа вправо с противоположным знаком
        if c.type == EquationComponentType.Number:
            # Текущая компонента - число                
            rr += str_plus(c.value * -s, rr=="")            


    return rl + "=" + rr
    