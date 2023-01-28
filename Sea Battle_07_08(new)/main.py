#Импортируем pygame
import pygame
#Импортируем os
import os 
#Импортируем все константы
from constants import *
#Импортируем все нужные функции
from modules import *
#Импортируем объекты
from objects import *
#
import socket
#Инициализруем настройки pygame
pygame.init()
#Переменная игрового цикла
game = True


#Матрица с кораблями игрока
self_list_map_player1 = [
                        list('0000000000'),
                        list('0000000000'),
                        list('0000000000'),
                        list('0000000000'),
                        list('0000000000'),
                        list('0000000000'),
                        list('0000000000'),
                        list('0000000000'),
                        list('0000000000'),
                        list('0000000000')
] 
self_list_objects = list()
def send_data(index_y,index_x,flag_move):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((IP,PORT))
    client.send((str([index_y,index_x,flag_move])).encode('utf-8'))
    client.close()
def receive_data():

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((IP,PORT))
    data = eval(client.recv(1024).decode('utf-8'))
    client.close()
    return data
#Вызываем функцию наполнения карты
create_map(self_list_map_player1,list_map)
#
flag_move = True
list_rect = []
#Оснвной игровой цикл
while game:
    #Заливаем экран цветом 
    screen.fill(color_background)
    #Создаем координаты мыши 
    mouse_cor = pygame.mouse.get_pos()
    
    if scene == "win":
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and button_back.click_on_rect(mouse_cor):
                game = False
        bg_win.show_image()
        button_back.show_image()

    if scene == "defeat":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and button_back.click_on_rect(mouse_cor):
                game = False
        bg_defeat.show_image()
        button_back.show_image()
    if scene == 'developers':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and button_menu.click_on_rect(mouse_cor):
                scene = 'menu'
        bg_developers.show_image()
        names.show_image()
        button_menu.show_image()
    if scene == 'menu':
        bg_menu.show_image()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_start_play.click_on_rect(mouse_cor):
                    scene = 'choiceclient'
                if button_developer.click_on_rect(mouse_cor):
                    scene = 'developers'
                if button_exit.click_on_rect(mouse_cor):
                    game = False
        button_start_play.show_image()
        button_exit.show_image()
        button_developer.show_image()
    if scene == 'choiceclient':
        bg_menu.show_image()
        client1.show_image()
        client2.show_image()
        button_menu.show_image()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if  button_menu.click_on_rect(mouse_cor):
                    scene = 'menu'
                if client1.click_on_rect(mouse_cor):
                    PORT = 12345
                    scene = 'prepare'
                    SCREEN_WIDTH = 700
                    SCREEN_HEIGHT = 500
                    flag_move = True
                    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
                if client2.click_on_rect(mouse_cor):
                    PORT = 54321
                    scene = 'prepare'
                    flag_move = False
                    SCREEN_WIDTH = 700
                    SCREEN_HEIGHT = 500
                    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
                    
    if scene == 'prepare':
        #Отрисовка изображения поля
        background.show_image()
        #Показываем карту с вращением
        map_rotate.show_image()
        #Отрисовывем картинку кнопки
        button_rotate.show_image()
        #Флаг для отрисовки кнопки
        flag_number_ship = False
        #Перебираем список с кораблями в меню
        for ship in list_ships_menu:
            #Если количество кораблей 0
            if ship.NUMBER_SHIP == 0:
                #Разрешаем отрисовку кнопки
                flag_number_ship = True
            #Иначе
            else:
                #Запрещаем отрисовку кнопки
                flag_number_ship = False
                #Выходим из цикла
                break
        #Если флаг отрисовки кнопки = True
        if flag_number_ship:
            #Отрисовываем кнопку
            button_end_set.show_image()
        #Перебираем события pygame
        for event in pygame.event.get():
            #Условия закрытия игрового окна
            if event.type == pygame.QUIT:
                #Закрытия игрового окна
                game = False
            #Проверяем нажатие левой кнопки мыши 
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #Перебираем список с картой
                for obj in list_map:
                    #Проверяем нажатие мыши на ячейку
                    if obj.click_on_rect(mouse_cor):
                        #Задаем индекс клеточки по матрице по вертикали
                        index_x = obj.X//cell
                        #Задаем индекс клеточки по матрице по горизонтали
                        index_y = obj.Y//cell
                        #Если ячейка на которую нажали - корабль
                        if self_list_map_player1[index_y][index_x] == 'b' or self_list_map_player1[index_y][index_x] in ['1','2','3','4']:
                            #Флаг для удаления корабля
                            flag_del_ship = False
                            #Если индекс корабля по У не выходит за матрицу
                            if index_y >= 0:
                                #Если в выбранном индексе блок, а индекс сверху это корабль
                                if self_list_map_player1[index_y-1][index_x]  in ['2','3','4'] and self_list_map_player1[index_y][index_x] == 'b':
                                    #Изменяем индекс по У на один вверх
                                    index_y = index_y-1
                                    #Разрешаем удалить корабль
                                    flag_del_ship = True
                                #Если сверху по У есть блок
                                elif self_list_map_player1[index_y-1][index_x] == 'b':
                                    #Создаем переменную счётчика для индекса по У
                                    index_count = index_y-1
                                    #Цикл пока не встретим 0 или корабль
                                    while 1:
                                        #Изменяем счётчик индекса по У
                                        index_count -= 1 
                                        #Если индекс У не выходит за матрицу 
                                        if index_count >= 0:
                                            #Если встречаем пустую ячейку
                                            if self_list_map_player1[index_count][index_x] == '0':
                                                #Выходим из цикла
                                                break
                                            #Если встречаем корабль 
                                            elif self_list_map_player1[index_count][index_x] in ['2','3','4']:
                                                #Меняем индекс по У на значение счётчика
                                                index_y = index_count
                                                #Разрешаем удалить корабль
                                                flag_del_ship = True
                                                #Выходим из цикла
                                                break
                                        #Если вышел за матрицу
                                        else:
                                            #Выходим из цикла
                                            break
                            #Условие если не вышли за край по правой стороне
                            if index_x+1 <= WIDTH_MAP-1:
                                #Если в выбранном индексе блок, а индекс справа это корабль
                                if self_list_map_player1[index_y][index_x+1]  in ['2','3','4'] and self_list_map_player1[index_y][index_x] == 'b':
                                    #Изменяем индекс по Х на один вправо
                                    index_x = index_x+1
                                    #Разрешаем удалить корабль
                                    flag_del_ship = True
                                #Если справа по Х есть блок
                                elif self_list_map_player1[index_y][index_x+1] == 'b':
                                    #Создаем переменную счётчика для индекса по Х
                                    index_count = index_x+1
                                    #Цикл пока не встретим 0 или корабль
                                    while 1:
                                        #Изменяем счётчик индекса по Х
                                        index_count += 1 
                                        #Если индекс Х не выходит за матрицу 
                                        if index_count+1 <= WIDTH_MAP-1:
                                            #Если встречаем пустую ячейку
                                            if self_list_map_player1[index_y][index_count] == '0':
                                                #Выходим из цикла
                                                break
                                            #Если встречаем корабль 
                                            elif self_list_map_player1[index_y][index_count] in ['2','3','4']:
                                                #Меняем индекс по Х на значение счётчика
                                                index_x = index_count
                                                #Разрешаем удалить корабль
                                                flag_del_ship = True
                                                #Выходим из цикла
                                                break
                                        #Если вышел за матрицу
                                        else:
                                            #Выходим из цикла
                                            break
                            #Условие если не вышли за край по нижней стороне
                            if index_y+1 <= HEIGHT_MAP-1:
                                #Если в выбранном индексе блок, а индекс снизу это корабль
                                if self_list_map_player1[index_y+1][index_x]  in ['2','3','4'] and self_list_map_player1[index_y][index_x] == 'b':
                                    #Изменяем индекс по У на один вниз
                                    index_y = index_y+1
                                    #Разрешаем удалить корабль
                                    flag_del_ship = True
                                #Если справа по У есть блок
                                elif self_list_map_player1[index_y+1][index_x] == 'b':
                                    #Изменяем счётчик индекса по У
                                    index_count = index_y+1
                                    #Если индекс У не выходит за матрицу 
                                    while 1:
                                        #Изменяем счётчик индекса по У
                                        index_count += 1 
                                        #Если индекс У не выходит за матрицу 
                                        if index_count+1 <= HEIGHT_MAP-1:
                                            #Если встречаем пустую ячейку
                                            if self_list_map_player1[index_count][index_x] == '0':
                                                #Выходим из цикла
                                                break
                                            #Если встречаем корабль 
                                            elif self_list_map_player1[index_count][index_x] in ['2','3','4']:
                                                #Меняем индекс по У на значение счётчика
                                                index_y = index_count
                                                #Разрешаем удалить корабль
                                                flag_del_ship = True
                                                #Если вышел за матрицу
                                                break
                                        #Если вышел за матрицу
                                        else:
                                            #Выходим из цикла
                                            break
                            #Условие если не вышли за край по верхней стороне
                            if index_x >= 0:
                                #Если в выбранном индексе блок, а индекс снизу это корабль
                                if self_list_map_player1[index_y][index_x-1]  in ['2','3','4'] and self_list_map_player1[index_y][index_x] == 'b':
                                    #Изменяем индекс по Х на один влево
                                    index_x = index_x-1
                                    #Разрешаем удалить корабль
                                    flag_del_ship = True
                                #Если слева по Х есть блок
                                elif self_list_map_player1[index_y][index_x-1] == 'b':
                                    #Изменяем счётчик индекса по Х
                                    index_count = index_x-1
                                    #Если индекс Х не выходит за матрицу 
                                    while 1:
                                        #Изменяем счётчик индекса по Х
                                        index_count -= 1 
                                        #Если индекс Х не выходит за матрицу 
                                        if index_count >= 0:
                                            #Если встречаем пустую ячейку
                                            if self_list_map_player1[index_y][index_count] == '0':
                                                #Выходим из цикла
                                                break
                                            #Если встречаем корабль 
                                            elif self_list_map_player1[index_y][index_count] in ['2','3','4']:
                                                #Меняем индекс по Х на значение счётчика
                                                index_x = index_count
                                                #Разрешаем удалить корабль
                                                flag_del_ship = True
                                                #Если вышел за матрицу
                                                break   
                                        #Если вышел за матрицу
                                        else:
                                            #Если вышел за матрицу
                                            break
                            #Если нажали на корабль
                            if self_list_map_player1[index_y][index_x] in ['1','2','3','4']:
                                #Разрешаем удалить корабль
                                flag_del_ship = True
                            #Если разрешили удалять корабль 
                            if flag_del_ship:
                                #Записываем кораблик на который нажали, исходя из индексов нажатой клетки
                                ship_list_map = list_map[index_y*10+index_x]
                                #Перебираем в длину корабля
                                for i in range(ship_list_map.LEN_SHIP-1):
                                    #Если направление корабля вниз
                                    if ship_list_map.DIRECTION_SHIP == 'down':
                                        #Записываем индекс вниз
                                        index = i+1
                                        #Если под кораблем есть b
                                        if self_list_map_player1[index_y+index][index_x] == 'b':
                                            #Меняем b на 0
                                            self_list_map_player1[index_y+index][index_x] = '0'
                                        #Если проверка вышла за длину корабля
                                        else:
                                            #Выходим из цикла
                                            break
                                    #Если направление корабля вправо
                                    elif ship_list_map.DIRECTION_SHIP == 'right':
                                        #Записываем индекс вправо
                                        index = i+1
                                        #Если справа от корабля b
                                        if self_list_map_player1[index_y][index_x+index] == 'b':
                                            #Меняем b на 0
                                            self_list_map_player1[index_y][index_x+index] = '0'
                                        #Если проверка вышла за длину корабля
                                        else:
                                            #Выходим из цикла
                                            break
                                    #Если направление корабля вверх
                                    elif ship_list_map.DIRECTION_SHIP == 'up':
                                        #Записываем индекс вверх
                                        index = i+1
                                        #Если сверху от корабля b
                                        if self_list_map_player1[index_y-index][index_x] == 'b':
                                            #Меняем b на 0
                                            self_list_map_player1[index_y-index][index_x] = '0'
                                        #Если проверка вышла за длину корабля
                                        else:
                                            #Выходим из цикла
                                            break
                                    #Если направление корабля влево
                                    elif ship_list_map.DIRECTION_SHIP == 'left':
                                        #Записываем индекс вверх
                                        index = i+1
                                        #Если слева от корабля b
                                        if self_list_map_player1[index_y][index_x-index] == 'b':
                                            #Меняем b на 0
                                            self_list_map_player1[index_y][index_x-index] = '0'
                                        #Если проверка вышла за длину корабля
                                        else:
                                            #Выходим из цикла
                                            break
                                #Меняем корабль на который нажали, на Sprite
                                list_map[index_y*10+index_x] = Sprite(
                                                                        x = index_x*cell,y = index_y*cell,
                                                                        width = cell,height = cell,
                                                                        path_img = None
                                                                    )
                                #Изменяем по матрице корабль на 0
                                list_ships_menu[int(self_list_map_player1[index_y][index_x])-1].NUMBER_SHIP += 1
                                list_ships_menu[int(self_list_map_player1[index_y][index_x])-1].TEXT_NUMBER_SHIP.CONTENT = str(list_ships_menu[int(self_list_map_player1[index_y][index_x])-1].NUMBER_SHIP)
                                self_list_map_player1[index_y][index_x] = '0'
                        #Если выбран корабль (Если корабль на карте вращения по Х не равняется нулю)
                        if ship_rotate_map.X != 0  and len(list_rect) != 0:
                            #Способность поставить корабль
                            flag_can_set_ship = True
                            #Цикл проверки силуэта корабля
                            for rect in list_rect:
                                #Если хоть одна красная
                                if rect[1] == 'red':
                                    #Нельзя поставить корабль
                                    flag_can_set_ship = False
                                    #Выходим из цикла
                                    break
                            #Условие если можно ставить корабль
                            if flag_can_set_ship :
                                #Создаем корабль по индексу на карте
                                list_map[index_y*10+index_x] = Ship(
                                                                ship_rotate_map.LEN_SHIP,
                                                                x=index_x*cell,
                                                                y=index_y*cell,
                                                                width=cell,
                                                                height=cell,
                                                                path_img=ship_rotate_map.PATH_IMG
                                                                )
                                #Если направление корабля на карте вращения вниз
                                if ship_rotate_map.DIRECTION_SHIP == 'down':
                                    #Меняем 0 на число длины корабля 
                                    self_list_map_player1[index_y][index_x] = str(ship_rotate_map.LEN_SHIP)
                                    #Задаем направление кораблю на карте
                                    list_map[index_y*10+index_x].DIRECTION_SHIP = 'down'
                                    #Цикл в длину корабля 
                                    for i in range(ship_rotate_map.LEN_SHIP-1):
                                        #Задаем индекс
                                        index = i+1
                                        #В матрице ставим букву b исходя из направления корабля
                                        self_list_map_player1[index_y+index][index_x] = 'b'
                                #Если направление корабля на карте вращения вверх
                                if ship_rotate_map.DIRECTION_SHIP == 'up':
                                    #Меняем 0 на число длины корабля 
                                    self_list_map_player1[index_y][index_x] = str(ship_rotate_map.LEN_SHIP)
                                    #Задаем направление кораблю на карте
                                    list_map[index_y*10+index_x].DIRECTION_SHIP = 'up'
                                    #Цикл в длину корабля 
                                    for i in range(ship_rotate_map.LEN_SHIP-1):
                                        #Задаем индекс
                                        index = i+1
                                        #В матрице ставим букву b исходя из направления корабля
                                        self_list_map_player1[index_y-index][index_x] = 'b'
                                #Если направление корабля на карте вращения вправо
                                if ship_rotate_map.DIRECTION_SHIP == 'right':
                                    #Меняем 0 на число длины корабля 
                                    self_list_map_player1[index_y][index_x] = str(ship_rotate_map.LEN_SHIP)
                                    #Задаем направление кораблю на карте
                                    list_map[index_y*10+index_x].DIRECTION_SHIP = 'right'
                                    #Цикл в длину корабля 
                                    for i in range(ship_rotate_map.LEN_SHIP-1):
                                        #Задаем индекс
                                        index = i+1
                                        #В матрице ставим букву b исходя из направления корабля
                                        self_list_map_player1[index_y][index_x+index] = 'b'
                                #Если направление корабля на карте вращения влево
                                if ship_rotate_map.DIRECTION_SHIP == 'left':
                                    #Меняем 0 на число длины корабля 
                                    self_list_map_player1[index_y][index_x] = str(ship_rotate_map.LEN_SHIP)
                                    #Цикл в длину корабля 
                                    list_map[index_y*10+index_x].DIRECTION_SHIP = 'left'
                                    #Задаем индекс
                                    for i in range(ship_rotate_map.LEN_SHIP-1):
                                        #Задаем индекс
                                        index = i+1
                                        #В матрице ставим букву b исходя из направления корабля
                                        self_list_map_player1[index_y][index_x-index] = 'b'
                                #Создаем корабль по индексу корабля на карте вращения из меню
                                ship = list_ships_menu[ship_rotate_map.INDEX_SHIP]
                                #Изменяем количество кораблей
                                ship.NUMBER_SHIP -=1
                                #Изменяем текст количества кораблей
                                ship.TEXT_NUMBER_SHIP.CONTENT = str(ship.NUMBER_SHIP)
                                #Корабль для карты вращения пересоздаем
                                ship_rotate_map = Ship()
                                #Пересоздаем обводку
                                select = Sprite(
                                                path_img='images/select.png'
                                )
                                #
                                list_rect = list()    
                                #Проверяем что ячейка корабль
                                for ship in list_map: 
                                    index_ship = list_map.index(ship)
                                    #Задаем индекс клеточки по матрице по вертикали
                                    index_x = ship.X//cell
                                    #Задаем индекс клеточки по матрице по горизонтали
                                    index_y = ship.Y//cell
                                    if self_list_map_player1[index_y][index_x] in '1' or self_list_map_player1[index_y][index_x] in '2' or self_list_map_player1[index_y][index_x] in '3' or self_list_map_player1[index_y][index_x] in '4':                                        
                                        #Проверка на то что кораблик не вылазит за карту вниз
                                        if index_y <= HEIGHT_MAP-1:
                                            #Проверяем что корабль смотрит вниз
                                            if list_map[index_ship].DIRECTION_SHIP == 'down':
                                                #Изменяем ширину(высоту из-за поворота кораблика)
                                                list_map[index_ship].WIDTH = cell*list_map[index_ship].LEN_SHIP
                                                #Загружаем изображение
                                                list_map[index_ship].load_image()
                                                #Меняем направление
                                                list_map[index_ship].change_direction()
                                        #Проверяем что корабль смотрит вверх
                                        if index_y >= 0:
                                            #Проверяем что корабль смотрит вверх
                                            if list_map[index_ship].DIRECTION_SHIP == 'up':
                                                #Изменяем Y двигая вверх кораблик
                                                list_map[index_ship].Y = list_map[index_ship].Y-(list_map[index_ship].LEN_SHIP-1)*cell
                                                #Изменяем ширину(высоту из-за поворота кораблика)
                                                list_map[index_ship].WIDTH = cell*list_map[index_ship].LEN_SHIP
                                                #Загружаем изображение
                                                list_map[index_ship].load_image()
                                                #Меняем направление
                                                list_map[index_ship].change_direction(-270)
                                        #Проверяем что корабль смотрит вправо
                                        if index_x <= WIDTH_MAP-1:
                                            #Проверяем что корабль смотрит вправо
                                            if list_map[index_ship].DIRECTION_SHIP == 'right':
                                                #Изменяем ширину
                                                list_map[index_ship].WIDTH = cell*list_map[index_ship].LEN_SHIP
                                                #Загружаем изображение
                                                list_map[index_ship].load_image()
                                        #Проверяем что корабль смотрит влево
                                        if index_x >= 0:
                                            #Проверяем что корабль смотрит влево
                                            if list_map[index_ship].DIRECTION_SHIP == 'left':
                                                #Изменяем Х двигая влево кораблик
                                                list_map[index_ship].X = list_map[index_ship].X-cell*(list_map[index_ship].LEN_SHIP-1)
                                                #Изменяем ширину
                                                list_map[index_ship].WIDTH = cell*list_map[index_ship].LEN_SHIP
                                                #Загружаем изображение
                                                list_map[index_ship].load_image()
                                                #Меняем направление
                                                list_map[index_ship].change_direction(-180)  
                #Если нажали на кнопку, то вращаем кораблик
                if button_rotate.click_on_rect(mouse_cor) and ship_rotate_map.X > 0:
                    #Вращаем кораблик
                    ship_rotate_map.change_direction()
                    #Вызываем проверку направления для кораблика на карте вращения
                    ship_rotate_map.check_index_direction()
                
                if button_end_set.click_on_rect(mouse_cor) and flag_number_ship:
                    scene = 'fight'
                    
                #Перебираем список корабликов в меню
                for ship in list_ships_menu:
                    #Если нажали на корабль
                    if ship.click_on_rect(mouse_cor) and ship.NUMBER_SHIP > 0:
                        #Изменяем размер обводки корабля
                        select.X = ship.X - 5
                        select.Y = ship.Y - 5
                        select.WIDTH = ship.WIDTH + 10 
                        select.HEIGHT = ship.HEIGHT + 10
                        #Вызываем метод проверки направления для корабля в меню
                        ship.check_index_direction()
                        #Меняем длину корабля на карте вращения на длину выбраного корабля
                        ship_rotate_map.LEN_SHIP = ship.LEN_SHIP
                        #Изменяем направление корабля на карте вращения на направление выбраного корабля
                        ship_rotate_map.DIRECTION_SHIP = ship.DIRECTION_SHIP
                        #Изменяем индекс направления корабля на карте вращения на индекс выбраного корабля
                        ship_rotate_map.INDEX_DIRECTION = ship.INDEX_DIRECTION
                        #Изменяем индекс на индекс выбраного корабля
                        ship_rotate_map.INDEX_SHIP = list_ships_menu.index(ship)
                        #Загружаем картинку выбраного кораблика
                        select.load_image()
                        #Изменяем размеры кораблика на карте вращения
                        ship_rotate_map.WIDTH = cell*ship.LEN_SHIP
                        ship_rotate_map.HEIGHT = cell
                        ship_rotate_map.PATH_IMG = ship.PATH_IMG
                        #Условие выбора координат корабля для 3 и 4 на карте вращения 
                        if ship.LEN_SHIP == 3 or ship.LEN_SHIP == 4:
                            ship_rotate_map.X  = 500
                            ship_rotate_map.Y  = 200
                        #Условие выбора координат корабля для 1 и 2 на карте вращения 
                        if ship.LEN_SHIP == 1 or ship.LEN_SHIP == 2:
                            ship_rotate_map.X  = 500+cell
                            ship_rotate_map.Y  = 200+cell
                        #Загружаем изображение кораблика на карте вращения
                        ship_rotate_map.load_image()
        #Показываем кораблик на карте вращения
        ship_rotate_map.show_image()
        #Показываем картинку обводки
        select.show_image()
        #Перебираем список с кораблями меню
        for ship in list_ships_menu:
            if ship.NUMBER_SHIP > 0:
                #Показываем корабль
                ship.show_image()
                #Показываем количество кораблей
                ship.TEXT_NUMBER_SHIP.show_text()
        #Перебираем карту
        for ship in list_map:
            #Задаем индекс клеточки по матрице по вертикали
            index_x = ship.X//cell
            #Задаем индекс клеточки по матрице по горизонтали
            index_y = ship.Y//cell
            #Отрисовываем кораблик
            ship.show_image()
            #Если водим мышкой по полю 
            if ship.click_on_rect(mouse_cor):
                #Обновляем список с Rect силуэта корабля
                list_rect = list()
                #Цикл направления корабля
                for i in range(ship_rotate_map.LEN_SHIP):
                    #Если направление силуэта корабля вверх и вышло за верхнюю часть экрана, тогда выходим из цикла
                    if move_shadow_ship(ship_rotate_map,list_rect,'up',(ship.Y-cell*(i-1) <= 0),ship.X,ship.Y-cell*i):
                        break
                    #Если направление силуэта корабля вниз и вышло за нижнюю часть экрана, тогда выходим из цикла
                    if move_shadow_ship(ship_rotate_map,list_rect,'down',(ship.Y+cell*i >= 500),ship.X,ship.Y+cell*i):
                        break
                    #Если направление силуэта корабля вправо и вышло за правую часть экрана, тогда выходим из цикла
                    if move_shadow_ship(ship_rotate_map,list_rect,'right',(ship.X+cell*i >= 500),ship.X+cell*i,ship.Y):
                        break
                    #Если направление силуэта корабля влево и вышло за левую часть экрана, тогда выходим из цикла
                    if move_shadow_ship(ship_rotate_map,list_rect,'left',(ship.X-cell*(i-1) <= 0),ship.X-cell*i,ship.Y):
                        break
                #Цикл перебора клеток силуэта корабля
                for i in range(len(list_rect)):
                    #Список с проверяемыми индексами
                    list_index_ship = [
                                        [index_y,index_x],[index_y+1,index_x],[index_y-1,index_x],
                                        [index_y,index_x-1],[index_y+1,index_x-1],[index_y-1,index_x-1],
                                        [index_y,index_x+1],[index_y+1,index_x+1],[index_y-1,index_x+1],
                                        ]
                    #Исходя из направления изменяем индекс Х или У
                    if ship_rotate_map.DIRECTION_SHIP == 'down':
                        index_y+=1
                    if ship_rotate_map.DIRECTION_SHIP == 'up':
                        index_y-=1
                    if ship_rotate_map.DIRECTION_SHIP == 'right':
                        index_x+=1
                    if ship_rotate_map.DIRECTION_SHIP == 'left':
                        index_x-=1
                    #Перебираем  список с индексами
                    for list_index in list_index_ship:
                        #Если не выходит за карту
                        if not list_index[0] > HEIGHT_MAP-1 and not list_index[0] < 0 and not list_index[1] > WIDTH_MAP-1 and not list_index[1] < 0:
                            #Если на клетке что то есть 
                            if not self_list_map_player1[list_index[0]][list_index[1]] == '0':
                                #Делаем клетку силуэта корабля красной
                                list_rect[i][1] = 'red'
                                #Выходим из цикла
                                break
                        
            #Цикл отрисовки силуэта корабля
            for rect in list_rect:
                pygame.draw.rect(screen,rect[1],rect[0])
        #Если сцена атаки, которая находится в сцене подгатовки 
        if scene == 'fight':
            #Меняем размеры экрана
            SCREEN_WIDTH = 1200
            SCREEN_HEIGHT = 550
            #Двигаем карту с кораблями по У
            background.Y = 50
            #Пересоздаем экран
            screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
            #Возвращаем числа кораблям из меню, и двигаем их
            for i in range(len(list_ships_menu)):
                list_ships_menu[i].Y += 100
                list_ships_menu[i].X += 50
                list_ships_menu[i].TEXT_NUMBER_SHIP.CONTENT = str(4-i)
                list_ships_menu[i].TEXT_NUMBER_SHIP.X += 50
                list_ships_menu[i].TEXT_NUMBER_SHIP.Y += 100
                list_ships_menu[i].NUMBER_SHIP = 4-i
            client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

            client.connect((IP,PORT))
            client.send(str(self_list_map_player1).encode('utf-8')) 
            data = client.recv(1024).decode('utf-8')
            data = eval(data)
            client.close()
            #Создаем вражескую карту(с числами)
            enemy_list_map_player1 = data
            #Создаем вражескую карту(с попаданиями)
            list_cross_point_enemy = []
            list_enemy_objects = list()
            #Гениальный цикл записи вражеской карты с с попаданиями
            for obj2 in range(len(enemy_list_map_player1)):
                #Добавляем пустой список
                list_cross_point_enemy.append([])
                #Перебираем список вражеской карты с числами 
                for obj in range(len(enemy_list_map_player1[obj2])):
                    #Добавляем в созданный список элементы
                    list_cross_point_enemy[obj2].append(enemy_list_map_player1[obj2][obj])
            #Функция меняет корабли матрицы с числами на корабли матрицы с попаданиями
            list_cross_point_enemy = list_map_enemy(list_cross_point_enemy)
            create_map(list_cross_point_enemy,list_enemy_objects)

            #Создаем список с объектами вражеской карты
            list_cross_point_self = []
            for obj2 in range(len(self_list_map_player1)):
                #Добавляем пустой список
                list_cross_point_self.append([])
                #Перебираем список вражеской карты с числами 
                for obj in range(len(self_list_map_player1[obj2])):
                    #Добавляем в созданный список элементы
                    list_cross_point_self[obj2].append(self_list_map_player1[obj2][obj])
            list_cross_point_self = list_map_enemy(list_cross_point_self)
            self_list_objects = list()
            #Наполяем вражескую карту 
            create_map(list_cross_point_self,self_list_objects)
            
            #Двигаем союзные корабли под размер экрана
            for obj in self_list_objects:
                obj.Y += 50
            for obj in list_map:
                obj.Y += 50
            #Двигаем вражеские корабли под размер экрана
            for obj in list_enemy_objects:
                obj.Y += 50
                obj.X += 700
                obj.RECT.y = obj.Y
                obj.RECT.x = obj.X

    #Если сцена бой
    if scene == 'fight':
        #Двигаем карту к своей изначальной координате по Х и отрисовываем
        background.X = background.START_X
        background.show_image()
        #Изменяем Х для отрисовки карты (отрисовка карты второй раз)
        background.X = 700
        background.show_image()
        #Отрисовываем текст надписи над картой
        enemy_text_map.show_text()
        self_text_map.show_text()
        #Отрисовываем кнопку атаки
        button_fight.show_image()
        if flag_move == False:
            wait.show_image()
            pygame.display.flip()
            try:
                data = receive_data()
            except:
                game = False
                break
            
            if list_cross_point_self[data[0]][data[1]] == 's':
                self_list_objects[data[0]*10+data[1]].PATH_IMG = 'images/cross.png'
                self_list_objects[data[0]*10+data[1]].load_image()
                list_cross_point_self[data[0]][data[1]] = '1'
                flag_move = False
                index_y = data[0]
                index_x = data[1]
                if self_list_map_player1[index_y][index_x] in ['1','2','3','4']:
                    #Изначальное направление
                    direction = 'right'
                    #Создаем список с индексами
                    list_index_cross = list()
                    #Если изначальное направления есть и если не однопалубный корабль
                    if direction == 'right' and not self_list_map_player1[index_y][index_x] == '1':
                        #Задаем направление корабля
                        if index_y+1 <= HEIGHT_MAP-1:
                            if self_list_map_player1[index_y+1][index_x] == 'b':
                                direction = 'down'
                        if index_y-1 >= 0:
                            if self_list_map_player1[index_y-1][index_x] == 'b':
                                direction = 'up'
                        if index_x+1 <= WIDTH_MAP-1:
                            if self_list_map_player1[index_y][index_x+1] == 'b':
                                direction = 'right'
                        if index_x-1 >= 0:
                            if self_list_map_player1[index_y][index_x-1] == 'b':
                                direction = 'left'
                    #Добавление в список индексов, индексы клеток корабля(b)
                    for i in range(int(self_list_map_player1[index_y][index_x])-1):
                        if direction == 'down':
                            list_index_cross.append([index_y+i+1,index_x])                                       
                        if direction == 'up':
                            list_index_cross.append([index_y-(i+1),index_x])
                        if direction == 'left':    
                            list_index_cross.append([index_y,index_x-(i+1)])
                        if direction == 'right':
                            list_index_cross.append([index_y,index_x+i+1])
                    #Добавляем индексы цифры корабля
                    list_index_cross.append([index_y,index_x])
                    #Условие разрешение разрушения корабля
                    for index in list_index_cross:
                        if list_cross_point_self[index[0]][index[1]] != '1':
                            flag_destroy = False
                            break
                        else:
                            flag_destroy = True
                #Если нажали на часть корабля(не на цифру)
                if self_list_map_player1[index_y][index_x] == 'b':
                    #Создаем список с индексами
                    list_index = list()
                    #Создаем список индексов попаданий(крестиков)
                    list_index_cross = list()
                    #Переменная направления
                    direction = 'right'
                    #Цикл вправо
                    while True:
                        #Условие выхода за пределы карты(если не вышли)
                        if index_x+1 < WIDTH_MAP:
                            #Двигаемся вправо
                            index_x += 1
                            #Условие при котором зададуться координаты цифры корабля
                            if self_list_map_player1[index_y][index_x] in ['2','3','4']:
                                #Записываем координта в список 
                                list_index = [index_y,index_x]
                                #Возвращаем индекс Х к изначальному значению
                                index_x = data[1]
                                #Выходим из цикла
                                break
                            #Если неправильное направление или вышли за длину корабля
                            elif self_list_map_player1[index_y][index_x] == '0':
                                #Возвращаем индекс Х к изначальному значению
                                index_x = data[1]
                                #Выходим из цикла
                                break
                        #Иначе
                        else:
                            #Возвращаем индекс Х к изначальному значению
                            index_x = data[1]
                            #Выходим из цикла
                            break
                    #Тоже самое, но влево
                    if not list_index:
                        while True:
                            if index_x-1 >= 0:
                                index_x -= 1
                                if self_list_map_player1[index_y][index_x] in ['2','3','4']:
                                    list_index = [index_y,index_x]
                                    index_x = data[1]
                                    break
                                elif self_list_map_player1[index_y][index_x] == '0':
                                    index_x = data[1]
                                    break
                            else:
                                index_x = data[1]
                                break
                    #Тоже самое, но вниз
                    if not list_index:
                        while True:
                            if index_y+1 <= HEIGHT_MAP-1:
                                index_y += 1
                                if self_list_map_player1[index_y][index_x] in ['2','3','4']:
                                    list_index = [index_y,index_x]
                                    index_y = data[0]
                                    break
                                elif self_list_map_player1[index_y][index_x] == '0':
                                    index_y = data[0]
                                    break
                            else:
                                index_y = data[0]
                                break
                    #Тоже самое, но вверх
                    if not list_index:
                        while True:
                            if index_y-1 >= 0:
                                index_y -= 1
                                if self_list_map_player1[index_y][index_x] in ['2','3','4']:
                                    list_index = [index_y,index_x]
                                    index_y = data[0]
                                    break
                                elif self_list_map_player1[index_y][index_x] == '0':
                                    index_y = data[0]
                                    break
                            else:
                                index_y = data[0]
                                break
                    #Определяем направление корабля 
                    if list_index[1]+1 <= WIDTH_MAP-1:
                        if self_list_map_player1[list_index[0]][list_index[1]+1] == 'b':
                            direction = 'right'
                    if list_index[1]-1 >= 0:
                        if self_list_map_player1[list_index[0]][list_index[1]-1] == 'b':
                            direction = 'left'
                    if list_index[0]-1 >= 0:
                        if self_list_map_player1[list_index[0]-1][list_index[1]] == 'b':
                            direction = 'up'
                    if list_index[0]+1 <= HEIGHT_MAP-1:
                        if self_list_map_player1[list_index[0]+1][list_index[1]] == 'b':
                            direction = 'down'
                    #Записываем координаты клеток корабля
                    for i in range(int(self_list_map_player1[list_index[0]][list_index[1]])-1):
                        if direction == 'right':
                            list_index_cross.append([list_index[0],list_index[1]+1+i])
                        if direction == 'left':
                            list_index_cross.append([list_index[0],list_index[1]-1-i])
                        if direction == 'up':
                            list_index_cross.append([list_index[0]-1-i,list_index[1]])
                        if direction == 'down':
                            list_index_cross.append([list_index[0]+1+i,list_index[1]])
                    #Записываем координату цифры корабля
                    list_index_cross.append([list_index[0],list_index[1]])
                    #Условие уничтожение корабля
                    for index in list_index_cross:
                        #Проверяем что на всех клетках корабля крестики(попадания)
                        if list_cross_point_self[index[0]][index[1]] != '1':
                            flag_destroy = False
                            break
                        else:
                            flag_destroy = True
                            index_y = list_index[0]
                            index_x = list_index[1]
                #Условие разрушение корабля
                if flag_destroy:
                    #Перебираем список с частями корабля(индексы)
                    for element in list_index_cross:
                        #Меняем текущую клетку на клетку корабля
                        index_y_miss = element[0]
                        index_x_miss = element[1]
                        #Перебираем ряды(У)
                        for a in range(3):
                            #Перебираем клетки в ряду
                            for b in range(3):
                                #Условие не выхода за карту
                                if index_y_miss-1 >= 0 and index_x_miss+b-1 >= 0 and index_y_miss-1 < HEIGHT_MAP and index_x_miss+b-1 < WIDTH_MAP:
                                    #Меняем клетки перебора на промахи
                                    list_cross_point_self[index_y_miss-1][index_x_miss+b-1 ] = '2'
                                    #Меняем картинку клетки на промах
                                    self_list_objects[(index_y_miss-1)*10+index_x_miss+b-1].PATH_IMG = 'images/point.png'
                                    self_list_objects[(index_y_miss-1)*10+index_x_miss+b-1].load_image()
                            #Переходим на след. ряд
                            index_y_miss+=1
                    #Перебираем список с индесами букв b(частей корабля)
                    for i in list_index_cross:
                        #Задаем в перменную все клетки корабля
                        sprite = self_list_objects[i[0]*10+i[1]]
                        #Удаляем изображениеr
                        sprite.PATH_IMG = None
                        sprite.IMG = None
                    #Меняем сам объект на уничтоженный корабль
                    list_map[index_y*10+index_x] = Ship(
                                                                len_ship=int(self_list_map_player1[index_y][index_x]),
                                                                direction_ship=direction,
                                                                x = (index_x)*cell, y = (index_y+1)*cell,
                                                                width = cell*int(self_list_map_player1[index_y][index_x]),
                                                                height = cell,
                                                                path_img = 'images/ship'+self_list_map_player1[index_y][index_x]+'_d.png'
                                                                )
                    #Проверяем что корабль смотрит вниз
                    if direction == 'down':
                        #Загружаем изображение
                        list_map[index_y*10+index_x].load_image()
                        #Меняем направление
                        list_map[index_y*10+index_x].change_direction()
                    #Проверяем что корабль смотрит вверх
                    if direction == 'up':
                        list_map[index_y*10+index_x].Y = list_map[index_y*10+index_x].Y-(list_map[index_y*10+index_x].LEN_SHIP-1)*cell
                        #Загружаем изображение
                        list_map[index_y*10+index_x].load_image()
                        #Меняем направление
                        list_map[index_y*10+index_x].change_direction(-270)
                    #Проверяем что корабль смотрит вправо
                    if direction == 'right':
                        #Загружаем изображение
                        list_map[index_y*10+index_x].load_image()
                    #Проверяем что корабль смотрит влево
                    if direction == 'left':
                        list_map[index_y*10+index_x].X = list_map[index_y*10+index_x].X-cell*(list_map[index_y*10+index_x].LEN_SHIP-1)
                        #Загружаем изображение
                        list_map[index_y*10+index_x].load_image()
                        #Меняем направление
                        list_map[index_y*10+index_x].change_direction(-180)  
            else:
                flag_move = True
                list_cross_point_self[data[0]][data[1]] = '2'
                self_list_objects[data[0]*10+data[1]].PATH_IMG = 'images/point.png'
                self_list_objects[data[0]*10+data[1]].load_image()
        
        #Перебираем события 
        for event in pygame.event.get():
            #Если нажат крестик 
            if event.type == pygame.QUIT:
                #Выходим из главного цикра игры
                game = False
                client1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                client1.connect((IP,PORT))
                client1.send('WIN'.encode('utf-8'))
                client1.close()
            #Если нажата левая кнопка мыши
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and flag_move:
                index_y = None
                index_x = None
                #Перебираем список объектов карты врага
                for obj in list_enemy_objects:
                    #Записываем индексы объекта
                    index_x = obj.X//cell-14
                    index_y = obj.Y//cell-1
                    #Если мы нажали на объект
                    if obj.click_on_rect(mouse_cor):

                        #Проверяем на нажатие по кораблю или пустой клетке
                        if list_cross_point_enemy[index_y][index_x] == 's' or list_cross_point_enemy[index_y][index_x] == '0':
                            #Если у выбранного объекта есть картинка и выбранная какая то клетка
                            if flag_select and obj.PATH_IMG != None:
                                #Путь для объекта Ноне
                                obj.PATH_IMG = None
                                #Убираем картинку
                                obj.IMG = None
                                #Флаг выбранной клетке фалсе
                                flag_select = False
                            #Если не выбранна клетка, выбираем её
                            elif not flag_select:
                                #Меняем путь картинке
                                obj.PATH_IMG = 'images/select.png'
                                #Задаем выбранную клетку
                                flag_select = True
                                #Загружаем имаге 
                                obj.load_image()
                    #Если нажали на кнопку атаковать и есть выбранная клетка
                    if button_fight.click_on_rect(mouse_cor) and obj.PATH_IMG != None:
                        #Если эта клетка корабль
                        if list_cross_point_enemy[index_y][index_x] == 's':
                            
                            send_data(index_y,index_x,flag_move)
                            
                            # flag_move = True
                            #Локальные константы
                            flag_destroy = False
                            obj.PATH_IMG = 'images/cross.png'
                            flag_select = False
                            #Загружаем имаге на выбранную клетку
                            obj.load_image()
                            #Заменяем в матрице по попаданием на крестик(1)
                            list_cross_point_enemy[index_y][index_x] = '1'
                            #Если попали по цифре корабля
                            if enemy_list_map_player1[index_y][index_x] in ['1','2','3','4']:
                                
                                #Изначальное направление
                                direction = 'right'
                                #Создаем список с индексами
                                list_index_cross = list()
                                #Если изначальное направления есть и если не однопалубный корабль
                                if direction == 'right' and not enemy_list_map_player1[index_y][index_x] == '1':
                                    #Задаем направление корабля
                                    if index_y+1 <= HEIGHT_MAP-1:
                                        if enemy_list_map_player1[index_y+1][index_x] == 'b':
                                            direction = 'down'
                                    if index_y-1 >= 0:
                                        if enemy_list_map_player1[index_y-1][index_x] == 'b':
                                            direction = 'up'
                                    if index_x+1 <= WIDTH_MAP-1:
                                        if enemy_list_map_player1[index_y][index_x+1] == 'b':
                                            direction = 'right'
                                    if index_x-1 >= 0:
                                        if enemy_list_map_player1[index_y][index_x-1] == 'b':
                                            direction = 'left'
                                #Добавление в список индексов, индексы клеток корабля(b)
                                for i in range(int(enemy_list_map_player1[index_y][index_x])-1):
                                    if direction == 'down':
                                        list_index_cross.append([index_y+i+1,index_x])                                       
                                    if direction == 'up':
                                        list_index_cross.append([index_y-(i+1),index_x])
                                    if direction == 'left':    
                                        list_index_cross.append([index_y,index_x-(i+1)])
                                    if direction == 'right':
                                        list_index_cross.append([index_y,index_x+i+1])
                                #Добавляем индексы цифры корабля
                                list_index_cross.append([index_y,index_x])
                                #Условие разрешение разрушения корабля
                                for index in list_index_cross:
                                    if list_cross_point_enemy[index[0]][index[1]] != '1':
                                        flag_destroy = False
                                        break
                                    else:
                                        flag_destroy = True
                            #Если нажали на часть корабля(не на цифру)
                            if enemy_list_map_player1[index_y][index_x] == 'b':
                                
                                #Создаем список с индексами
                                list_index = list()
                                #Создаем список индексов попаданий(крестиков)
                                list_index_cross = list()
                                #Переменная направления
                                direction = 'right'
                                #Цикл вправо
                                while True:
                                    #Условие выхода за пределы карты(если не вышли)
                                    if index_x+1 < WIDTH_MAP:
                                        #Двигаемся вправо
                                        index_x += 1
                                        #Условие при котором зададуться координаты цифры корабля
                                        if enemy_list_map_player1[index_y][index_x] in ['2','3','4']:
                                            #Записываем координта в список 
                                            list_index = [index_y,index_x]
                                            #Возвращаем индекс Х к изначальному значению
                                            index_x = obj.X//cell-14
                                            #Выходим из цикла
                                            break
                                        #Если неправильное направление или вышли за длину корабля
                                        elif enemy_list_map_player1[index_y][index_x] == '0':
                                            #Возвращаем индекс Х к изначальному значению
                                            index_x = obj.X//cell-14
                                            #Выходим из цикла
                                            break
                                    #Иначе
                                    else:
                                        #Возвращаем индекс Х к изначальному значению
                                        index_x = obj.X//cell-14
                                        #Выходим из цикла
                                        break
                                #Тоже самое, но влево
                                if not list_index:
                                    while True:
                                        if index_x-1 >= 0:
                                            index_x -= 1
                                            if enemy_list_map_player1[index_y][index_x] in ['2','3','4']:
                                                list_index = [index_y,index_x]
                                                index_x = obj.X//cell-14
                                                break
                                            elif enemy_list_map_player1[index_y][index_x] == '0':
                                                index_x = obj.X//cell-14
                                                break
                                        else:
                                            index_x = obj.X//cell-14
                                            break
                                #Тоже самое, но вниз
                                if not list_index:
                                    while True:
                                        if index_y+1 <= HEIGHT_MAP-1:
                                            index_y += 1
                                            if enemy_list_map_player1[index_y][index_x] in ['2','3','4']:
                                                list_index = [index_y,index_x]
                                                index_y = obj.Y//cell-1
                                                break
                                            elif enemy_list_map_player1[index_y][index_x] == '0':
                                                index_y = obj.Y//cell-1
                                                break
                                        else:
                                            index_y = obj.Y//cell-1
                                            break
                                #Тоже самое, но вверх
                                if not list_index:
                                    while True:
                                        if index_y-1 >= 0:
                                            index_y -= 1
                                            if enemy_list_map_player1[index_y][index_x] in ['2','3','4']:
                                                list_index = [index_y,index_x]
                                                index_y = obj.Y//cell-1
                                                break
                                            elif enemy_list_map_player1[index_y][index_x] == '0':
                                                index_y = obj.Y//cell-1
                                                break
                                        else:
                                            index_y = obj.Y//cell-1
                                            break
                                #Определяем направление корабля 
                                if list_index[1]+1 <= WIDTH_MAP-1:
                                    if enemy_list_map_player1[list_index[0]][list_index[1]+1] == 'b':
                                        direction = 'right'
                                if list_index[1]-1 >= 0:
                                    if enemy_list_map_player1[list_index[0]][list_index[1]-1] == 'b':
                                        direction = 'left'
                                if list_index[0]-1 >= 0:
                                    if enemy_list_map_player1[list_index[0]-1][list_index[1]] == 'b':
                                        direction = 'up'
                                if list_index[0]+1 <= HEIGHT_MAP-1:
                                    if enemy_list_map_player1[list_index[0]+1][list_index[1]] == 'b':
                                        direction = 'down'
                                #Записываем координаты клеток корабля
                                for i in range(int(enemy_list_map_player1[list_index[0]][list_index[1]])-1):
                                    if direction == 'right':
                                        list_index_cross.append([list_index[0],list_index[1]+1+i])
                                    if direction == 'left':
                                        list_index_cross.append([list_index[0],list_index[1]-1-i])
                                    if direction == 'up':
                                        list_index_cross.append([list_index[0]-1-i,list_index[1]])
                                    if direction == 'down':
                                        list_index_cross.append([list_index[0]+1+i,list_index[1]])
                                #Записываем координату цифры корабля
                                list_index_cross.append([list_index[0],list_index[1]])
                                #Условие уничтожение корабля
                                for index in list_index_cross:
                                    #Проверяем что на всех клетках корабля крестики(попадания)
                                    if list_cross_point_enemy[index[0]][index[1]] != '1':
                                        flag_destroy = False
                                        
                                        break
                                    else:
                                        flag_destroy = True
                                        index_y = list_index[0]
                                        index_x = list_index[1]
                            #Условие разрушение корабля
                            if flag_destroy:
                                #Меняем количество оставшихся кораблей
                                list_ships_menu[int(enemy_list_map_player1[index_y][index_x])-1].NUMBER_SHIP -= 1
                                #Меняем текст количества оставшихся кораблей
                                list_ships_menu[int(enemy_list_map_player1[index_y][index_x])-1].TEXT_NUMBER_SHIP.CONTENT = str(list_ships_menu[int(enemy_list_map_player1[index_y][index_x])-1].NUMBER_SHIP)
                                #Перебираем список с частями корабля(индексы)
                                for element in list_index_cross:
                                    #Меняем текущую клетку на клетку корабля
                                    index_y_miss = element[0]
                                    index_x_miss = element[1]
                                    #Перебираем ряды(У)
                                    for a in range(3):
                                        #Перебираем клетки в ряду
                                        for b in range(3):
                                            #Условие не выхода за карту
                                            if index_y_miss-1 >= 0 and index_x_miss+b-1 >= 0 and index_y_miss-1 < HEIGHT_MAP and index_x_miss+b-1 < WIDTH_MAP:
                                                #Меняем клетки перебора на промахи
                                                list_cross_point_enemy[index_y_miss-1][index_x_miss+b-1 ] = '2'
                                                #Меняем картинку клетки на промах
                                                list_enemy_objects[(index_y_miss-1)*10+index_x_miss+b-1].PATH_IMG = 'images/point.png'
                                                list_enemy_objects[(index_y_miss-1)*10+index_x_miss+b-1].load_image()
                                        #Переходим на след. ряд
                                        index_y_miss+=1
                                #Перебираем список с индесами букв b(частей корабля)
                                for i in list_index_cross:
                                    #Задаем в перменную все клетки корабля
                                    sprite = list_enemy_objects[i[0]*10+i[1]]
                                    #Удаляем изображениеr
                                    sprite.PATH_IMG = None
                                    sprite.IMG = None
                                #Меняем сам объект на уничтоженный корабль
                                list_enemy_objects[index_y*10+index_x] = Ship(
                                                                            len_ship=int(enemy_list_map_player1[index_y][index_x]),
                                                                            direction_ship=direction,
                                                                            x = (index_x+14)*cell, y = (index_y+1)*cell,
                                                                            width = cell*int(enemy_list_map_player1[index_y][index_x]),
                                                                            height = cell,
                                                                            path_img = 'images/ship'+enemy_list_map_player1[index_y][index_x]+'_d.png'
                                                                            )
                                #Проверяем что корабль смотрит вниз
                                if direction == 'down':
                                    #Загружаем изображение
                                    list_enemy_objects[index_y*10+index_x].load_image()
                                    #Меняем направление
                                    list_enemy_objects[index_y*10+index_x].change_direction()
                                #Проверяем что корабль смотрит вверх
                                if direction == 'up':
                                    list_enemy_objects[index_y*10+index_x].Y = list_enemy_objects[index_y*10+index_x].Y-(list_enemy_objects[index_y*10+index_x].LEN_SHIP-1)*cell
                                    #Загружаем изображение
                                    list_enemy_objects[index_y*10+index_x].load_image()
                                    #Меняем направление
                                    list_enemy_objects[index_y*10+index_x].change_direction(-270)
                                #Проверяем что корабль смотрит вправо
                                if direction == 'right':
                                    #Загружаем изображение
                                    list_enemy_objects[index_y*10+index_x].load_image()
                                #Проверяем что корабль смотрит влево
                                if direction == 'left':
                                    list_enemy_objects[index_y*10+index_x].X = list_enemy_objects[index_y*10+index_x].X-cell*(list_enemy_objects[index_y*10+index_x].LEN_SHIP-1)
                                    #Загружаем изображение
                                    list_enemy_objects[index_y*10+index_x].load_image()
                                    #Меняем направление
                                    list_enemy_objects[index_y*10+index_x].change_direction(-180)  
                        #Если нажатая клетка пустая
                        if list_cross_point_enemy[index_y][index_x] == '0':
    
                            
                            #На нажатую клетку, ставим изображение промаха
                            obj.PATH_IMG = 'images/point.png'
                            #Разрешаем сделать выбор клетки 
                            flag_select = False
                            #Загружаем изображение объекта
                            obj.load_image()
                            #Нажатую пустую клетку меняем на промах
                            list_cross_point_enemy[index_y][index_x] = '2'
                            flag_move = False
                            send_data(index_y,index_x,flag_move)
                            break
        #Отрисовка своих кораблей
        for obj in list_map:
            obj.show_image()
        for obj in self_list_objects:
            obj.show_image()
        #Отрисовка кораблей противника
        for obj in list_enemy_objects:
            if obj.PATH_IMG != None:
                obj.show_image()
        
        #Перебираем список с кораблями меню
        for ship in list_ships_menu:
            #Если число кораблей больше 0 
            if ship.NUMBER_SHIP > 0:
                #Показываем корабль
                ship.show_image()
                #Показываем количество кораблей
                ship.TEXT_NUMBER_SHIP.show_text()
        flag_win = False
        for ship in list_ships_menu:
            if ship.NUMBER_SHIP <= 0:
                flag_win = True
            else:
                flag_win = False
                break
            
        if flag_win:
            scene = 'win'
            client1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            client1.connect((IP,PORT))
            client1.send('WIN'.encode('utf-8'))
            client1.close()
        flag_defeat = 0
        for list_y in list_cross_point_self:
            flag_defeat += list_y.count('s')
        if flag_defeat == 0:
            client1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            client1.connect((IP,PORT))
            client1.send('DEFEAT'.encode('utf-8'))
            client1.close()
            scene = 'defeat'
    #Задаем FPS
    time.tick(fps)
    #Обновляем экран
    pygame.display.flip()
