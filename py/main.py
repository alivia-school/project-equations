# Для событий, предупреждений
from browser import bind, alert
# Используем готовый компонент редактирования уравнений
from SimpleEquationComponent import SimpleEquation
# Используем компонент кнопка
from Controls.Button import Button
# Используем компонент Метка
from Controls.Label import Label
# Наши функции
from functions import *


# Глобальные переменные:
# Текущий этап
stage = 0


# Компонент уравнения
ce = SimpleEquation()
ce.equation.value = "2(x-1)=4" #  пока для теста


# Кнопка выполнить
button_do = Button(text="Начать")

# Метка с пояснением
note = Label()

@bind(button_do.element, "click")
def do(e):
    # Используем эти глобальные переменные
    global stage
    
    if ce.equation.value != "" and ce.equation.error != True:
        if stage == 0:
            # Пошли по шагам уравнения
            # Меняем текст кнопки
            button_do.text = "Далее"
            # Уравнение делаем только на чтение
            ce.readOnly = True
            
            
            #Проверка есть ли скобки, то нужен первый этап
            if haveParentheses(ce.equation):
                #Да есть 
                stage = 1
                note.text = "Первый этап. На этом этапе раскройте скобки, они выделены красным."
                #Пометим скобки
                markParentheses(ce.equation)
                return   


        #Второй и далее этапы, еще не сделаны, пока напишем это
        note.text = "Эти этапы еще не сделаны"
                
            
    else:
        alert("Ошибка в уравнении")
    








 