#Импортируем os
import os
#Импортируем класс корабля и класс Sprite из objects
from objects import*
#Импортируем константы
from constants import*
#Создаем функцию создания карты
def create_map(self_list_map_player,list_map):
    #Создаем Индексы координат Х и У
    index_x = 0
    index_y = 0
    #Перебираем матрицу по строкам
    for string in self_list_map_player:
        #Перебираем строку по столбцам
        for column in string:
            #Если Корабль на клетке
            #Если пустая клетка
            if column == '0':
                #Создаем пустую клетку
                empty_cell = Sprite(
                            x = index_x*cell,y = index_y*cell,
                            width = cell,height = cell,
                            path_img = None
                            )
                #Добавляем клетку в список
                list_map.append(empty_cell)
            if column == 's':
                #Создаем пустую клетку
                empty_cell = Sprite(
                            x = index_x*cell,y = index_y*cell,
                            width = cell,height = cell,
                            path_img = None
                            )
                #Добавляем клетку в список
                list_map.append(empty_cell)
            #Изменяем индекс по Х
            index_x+=1
        #Обнуляем индекс по Х
        index_x = 0
        #Изменяем индекс по У
        index_y += 1
#Функция движения силуэта корабля
def move_shadow_ship(ship_rotate_map,list_rect,direction,check_x_y,x,y):
    #Проверяем направление корабля
    if ship_rotate_map.DIRECTION_SHIP == direction:
        #Проверяем координаты корабля
        if check_x_y:
            #Перебираем список с Rect
            for rect in list_rect:
                #Задаем цвет силуэта на красный
                list_rect[list_rect.index(rect)][1] = 'red'
            #Возвращаем True    
            return True
        #Иначе
        else:
            #Создаем Rect корабля
            rect_ship = pygame.Rect(x,y,cell,cell)
            #Добавляем в список с зелёным цветом
            list_rect.append([rect_ship,'green'])
#Функция меняет корабли матрицы с числами на корабли матрицы с попаданиями
def list_map_enemy(list_map):
    #Цкил перебора переданного списка по индекс У
    for index_y in range(len(list_map)):
        #Цикл перебора переданного списка индекса У по индексу Х
        for index_x in range(len(list_map[index_y])):
            #Если клетка равняеться одному из кораблей
            if list_map[index_y][index_x] in ['1','2','3','4','b']:
                #Меняем клетку корабля цифры на S
                list_map[index_y][index_x] = 's'
    #Возвращаем изменённый переданный список
    return list_map