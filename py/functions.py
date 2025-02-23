# Используем компоненты для работы с уравнением
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
    # Знак перед числом
    s = 1
    # Знак перед скобками
    sp = 1    
    # Флаг: Внутри скобок или нет
    b = False
    # Флаг: Начало выражения
    start = True
    #Элемент перед скобкой. По умолчанию = 1
    a = EquationComponent(1)
    
    # Обходим все компоненты уравнения
    for c in equation.components:       
        
        # Проверяем скобки    
        if c.value == '(':
            # Выставим флаг, что мы внутри скобки
            b = True
            # Сохраним знак перед скобками
            sp = s
            # Сбросим текущий знак на +
            s = 1
            # К следующему компоненту уравнения
            continue
            
        if c.value == ')':
            # Снимем флаг что мы внутри скобок
            b = False
            #Сбросим элемент перед скобкой. По умолчанию = 1
            a = EquationComponent(1)
            # К следующему компоненту уравнения
            continue
            

        # Мы внутри скобок?
        if b == True:
            # Да, внутри скобок
            
            if c.type == EquationComponentType.Unknown: 
                # Текущая компонента - неизвестное (типо "x" или "2x" и т.д.)
                
                # Перемножим с тем что за скобкой и добавим в результат    
                r += str_plus(a.value * c.factor_value * s * sp, start, True) + c.value
                
            elif c.type == EquationComponentType.Number: 
                # Текущая компонента - число
                # Перемножим с тем что за скобкой и добавим в результат  
                if a.type == EquationComponentType.Unknown:                 
                    r += str_plus(a.factor_value * c.value * s * sp, start, True) + a.value
                elif a.type == EquationComponentType.Number:                    
                    r += str_plus(a.value * c.value * s * sp, start)  
                    
        else:
            # Мы вне скобок
            
            if c.type == EquationComponentType.Unknown or c.type == EquationComponentType.Number: 
                # Тип компоненты неизвестное или число
                            
                # Проверим нет ли скобки после компонента
                if c.as_factor == True:
                    # Сохраним компонент, на него что будем умножать внутри скобок
                    a = c
                    
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
         
        elif (c.type == EquationComponentType.Unknown or c.type == EquationComponentType.Number) \
              and c.as_factor == False:            
            # После числа или неизвестного, которое стоит не перед скобкой, уже не начало выражения
            start = False
          
        elif c.value == '=':
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
    # Проверим левую часть
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
    
    # В 'a' будем помещать компонент для знака перед числом, по умолчанию присвоим пустой компонент
    a = EquationComponent(0)
    # Для левой части
    for c in equation.left():
        if c.type == EquationComponentType.Number:
            a.color = "red"
            c.color = "red"
            a = EquationComponent(0)
        elif c.type == EquationComponentType.Operation:        
            a = c
            
    # В 'a' будем помещать компонент для знака перед числом, по умолчанию присвоим пустой компонент
    a = EquationComponent(0)            
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
        
    # Оставим неизвестные слева
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
            
        # Сохраняем знак
        if c.type == EquationComponentType.Operation:                
            if c.value == '-': 
                s = -1
            else:
                s = 1             

    # Вернем полученное уравнение, соединив левую и правую часть
    return rl + "=" + rr
    
    
# Проверка нужно ли упрощение 
def needSimplification(equation):
    # Проверим левую часть
    if len(equation.left()) >= 3:        
        return True   
            
    # Проверим правую часть
    if len(equation.rigth()) >= 3:
        return True    
    
    return False
    
    
# Пометить элементы для упрощения
def markSimplificationElements(equation):
    # Обходим все компоненты уравнения
    for c in equation.components:
        if c.type == EquationComponentType.Operation: 
            c.color = "red"
            
        

# Выполнить упрощения
def simplificationElements(equation):
    ## Переменные: ##
    # Результат левой части
    rl = 0
    # Результат правой части
    rr = 0
    
    # Знак
    s = 1
        
    # Упрощаем левую часть
    for c in equation.left():        
                     
        if c.type == EquationComponentType.Operation:
            # Сохраняем знак
            if c.value == '-': 
                s = -1
            else:
                s = 1 
        else:
            rl += c.factor_value * s

    # Сбросим знак
    s = 1
         
    # Упрощаем правую часть
    for c in equation.rigth():        
            
        if c.type == EquationComponentType.Operation:
            # Сохраняем знак
            if c.value == '-': 
                s = -1
            else:
                s = 1 
        else:
            rr += c.value * s 

    if rl == 0:
        # Уравнение не имеет корней
        return False
   
    # Вернем полученное уравнение, соединив левую и правую часть
    return str_plus(rl, True, True) + equation.unknown + "=" + str_plus(rr, True, False)
        
    

# Проверка нужно ли вычислять неизвестное
def needCalcUnknown(equation):
    
    # Возьмем левую часть
    l = equation.left()
    
    if l[0].value == '-':
        # Если есть минус, то нужно вычислять, так как -x это -1 * x
        return True  
        
    if l[0].factor_value > 1:
        # Если фактор (то что мы умножаем на неизвестное) больше 1, то вычисление тоже нужно            
        return True
        
    # В других случаях вычисление не нужно
    return False        
    
    
# Вычисление неизвестного
def calcUnknown(equation):
    
    # Определим левую часть
    a = equation.left()       
    if a[0].value == '-':
        l = -a[1].factor_value
    else:
        l = a[0].factor_value   

    # Определим правую часть
    a = equation.rigth()       
    if a[0].value == '-':
        r = -int(a[1].value)
    else:
        r = int(a[0].value)  
        
    # Проверим делится ли нацело (нет остатка)
    if r % l == 0:
        return equation.unknown + "=" + str(int(r/l))
    else:
        #Знак перед дробью
        s = "-" if r/l<0 else ""
        return equation.unknown + "=" + s + str(abs(r)) + "/" + str(abs(l))
        
        
        