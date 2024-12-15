# Для событий, предупреждений, взаимодействия с браузером
from browser import bind, alert, window, confirm, console
# Используем готовый компонент редактирования уравнений
from SimpleEquationComponent import SimpleEquation
# Используем компонент кнопка
from Controls.Button import Button
# Используем компонент Метка
from Controls.Label import Label
# Наши функции
from functions import *
# Пояснения
from tips import *


# Глобальные переменные:
# Текущий этап
stage = 0
# Результат для проверки на каждом шаге
result = True

# Компонент уравнения
ce = SimpleEquation()

# Кнопка выполнить
button_do = Button(text="Начать")
# Кнопка заново
button_reset = Button(text="Заново")


# Метка с пояснением
note = Label()

@bind(button_do.element, "click")
def do(e):
    # Используем эти глобальные переменные
    global stage, ce, result
    
    # Текущее уравнение
    eq = ce.equation
    
    # Проверяем текущее уравнение
    if eq.value == "" or eq.error == True:
        alert("Ошибка в уравнении")
        return
            
    if result != True:
        # Нужно проверить результат
        if not eq.isSame(result):
            # Неверно
            alert("Неверно. Попробуйте еще раз")   
            # Не переходим на следующий уровень
            return
            
    # Переходим на следующую стадию
    stage += 1  
    
    # Уравнение делаем только на чтение
    ce.readOnly = True 
    
        
    # Первая стадия
    if stage == 1:
        
        # Меняем текст кнопки
        button_do.text = "Далее"
        
        # Пояснение
        note.text = "Первый этап. На этом этапе раскройте скобки."
        
        #Проверка есть ли скобки, то нужен первый этап
        if haveParentheses(eq):
            # Да есть 

            # Создадим второе поле для уравнения - ответа
            ce = SimpleEquation()
            ce.before(button_do.element)
            ce.placeholder = "Введите ответ"   
        
            # Дополним пояснение
            note.text += tip_stage_one
            
            # Пометим скобки
            markParentheses(eq)
            
            # Раскроем скобки, чтобы проверить ответ введенный пользователем и сохраним результат
            result = expandParentheses(eq)
            
        else:
            # Нет скобок
            note.text += "В этом уравнении скобок нет. Нажмите далее для перехода к следующему этапу"
            result = True
    
    # Вторая стадия    
    elif stage == 2:
        
        # Пояснение
        note.text = "Второй этап. На этом этапе перенесите части с неизвестным влево а числа вправо."
        
        #Проверка нужно ли переносить
        if needMove(eq):
            # Да нужно
            
            # Создадим еще одно поле для уравнения - ответа
            ce = SimpleEquation()
            ce.before(button_do.element)
            ce.placeholder = "Введите ответ"   
        
            # Дополним пояснение
            note.text += tip_stage_two
            
            # Пометим что переносить
            markMoveElements(eq)
            
            # Выполним перенос, чтобы проверить ответ введенный пользователем и сохраним результат
            result = moveElements(eq)
            
        else:
            # Не нужно переносить
            note.text += "В данном случае перенос не требуется. Нажмите далее для перехода к следующему этапу"
            result = True
            
    # Третья стадия    
    elif stage == 3:
        
        # Пояснение
        note.text = "Третий этап. На этом этапе упростите уравнение."
        
        #Проверка нужно ли упрощать
        if needSimplification(eq):
            # Да нужно
            
            # Создадим еще одно поле для уравнения - ответа
            ce = SimpleEquation()
            ce.before(button_do.element)
            ce.placeholder = "Введите ответ"   
        
            # Дополним пояснение
            note.text += tip_stage_three
            
            # Пометим что упрощать
            markSimplificationElements(eq)
            
            # Выполним упрощение, чтобы проверить ответ введенный пользователем и сохраним результат
            result = simplificationElements(eq)
            
        else:
            # Не нужно упрощать
            note.text += "В данном случае упрощение не требуется. Нажмите далее для перехода к следующему этапу"
            result = True
       
    # Четвертая стадия    
    elif stage == 4:
        
        # Пояснение
        note.text = "Четвертый этап. На этом этапе вычислите неизвестное."
        
        #Проверка нужно ли вычислять неизвестное
        if needCalcUnknown(eq):
            # Да нужно
            
            # Создадим еще одно поле для уравнения - ответа
            ce = SimpleEquation()
            ce.isResult = True
            ce.before(button_do.element)
            ce.placeholder = "Введите ответ"   
        
            # Дополним пояснение
            note.text += tip_stage_four
            
            
            # Выполним вычисление, чтобы проверить ответ введенный пользователем и сохраним результат
            result = calcUnknown(eq)
            
        else:
            # Не нужно упрощать
            note.text += "В данном случае упрощение не требуется. Нажмите далее для перехода к следующему этапу"
            result = True
            
    # Конец    
    elif stage == 5: 
        # Пояснение
        note.text = "Молодец! Уравнение решено"
        
        # Кнопка "Далее" не нужна более
        button_do.hide()      
            
            
            
@bind(button_reset.element, "click")
def reset(e):  
    if confirm("Вы хотите завершить работу с текущим уравнением?") == True:
        window.location.reload();



 