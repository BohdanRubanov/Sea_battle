#Импортируем pygame
import pygame
#Импортируем константы
from constants import*
#Импортируем модуль os
import os
#Инициализируем настройки pygame
pygame.init()
#Создаем экран
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
#Задаем название экрана

pygame.display.set_caption(CAPTION)
#Задаем счётчик обнавления экрана
time = pygame.time.Clock()
#Создаем класс родитель Sprite
class Sprite:
    def __init__(
                self,
                x=0,
                y=0,
                width=0,
                height=0,
                path_img=None):
        #Свойство координат Х и У
        self.X = x
        self.Y = y
        #Свойство картинки
        self.IMG = None
        #Свойство пути картинки
        self.PATH_IMG = path_img
        #Свойство размера картинки Ширина и Высота
        self.WIDTH = width
        self.HEIGHT = height
        #Свойство изначальных координат
        self.START_X = self.X
        self.START_Y = self.Y
        #Задаем свойство Rect объекта
        self.RECT = pygame.Rect(self.X,self.Y,self.WIDTH,self.HEIGHT)
        #Условие если путь картинки не равен None
        if self.PATH_IMG != None:
            #Загружаем картинку
            self.load_image()
    #Метод загрузки картинки
    def load_image(self):
        #Задаем абсолютный путь к картинке
        path = os.path.abspath(__file__+"/..")
        #Сшиваем абсолютный путь
        self.PATH_IMG = os.path.join(path,self.PATH_IMG)
        #Загружаем картинку в pygame
        self.IMG = pygame.image.load(self.PATH_IMG)
        #Задаем размеры картинки
        self.IMG = pygame.transform.scale(self.IMG,(self.WIDTH,self.HEIGHT))
    #Метод отрисовки картинки
    def show_image(self):
        #Если картинка не None
        if self.IMG != None:
            #Отрисовываем картинку
            screen.blit(self.IMG,(self.X,self.Y))
    #Метод нажатия по клетке
    def click_on_rect(self,mouse_cor):
        #Если нажали по клетке
        if pygame.Rect.collidepoint(self.RECT,mouse_cor[0],mouse_cor[1]):
            #Возвращаем True
            return True
        #Иначе
        else:
            #Возвращаем False
            return False
    
#Создаем класс Корабля  от класса родителя Sprite
class Ship(Sprite):
    #Создаем конструктор класса
    def __init__(self,len_ship=0,number_ship=None,direction_ship='right',**kwargs):
        #Наследуем параметры класса родителя
        super().__init__(**kwargs)
        #Свойство длины корабля
        self.LEN_SHIP = len_ship
        #Свойство направления корабля
        self.DIRECTION_SHIP = direction_ship
        #Количество кораблей
        self.NUMBER_SHIP = number_ship
        #Свойство текста количества корабля
        self.TEXT_NUMBER_SHIP = Text(
                                    bold = True,
                                    size = self.HEIGHT,
                                    color = 'black',
                                    content = str(self.NUMBER_SHIP),
                                    x = self.X + self.WIDTH + 10,
                                    y = self.Y
                                    )
        #Свойство угла поворота
        self.ANGLE = -90
        #Свойство индекса направления 
        self.INDEX_DIRECTION = 0
        #Свойство индекса корабля по списку
        self.INDEX_SHIP = 0
    #Метод поворота корабля
    def change_direction(self,angle=-90):
        self.IMG = pygame.transform.rotate(self.IMG,angle)
        self.INDEX_DIRECTION += 1
    #Метод в котором проверяем по индексу направление
    def check_index_direction(self):
        #Если индекс картинки прошел полный круг, тогда обнуляем индекс
        if self.INDEX_DIRECTION == 4:
            self.INDEX_DIRECTION = 0
        #Исходя из индекса направления изменяем направление
        if self.INDEX_DIRECTION == 0:
            self.DIRECTION_SHIP = 'right'
        elif self.INDEX_DIRECTION == 1:
            self.DIRECTION_SHIP = 'down'
        elif self.INDEX_DIRECTION == 2:
            self.DIRECTION_SHIP = 'left'
        elif self.INDEX_DIRECTION == 3:
            self.DIRECTION_SHIP = 'up'      
#Создаем класс Текста и наследуем от Sprite
class Text(Sprite):
    #Метод конструктор класса и наследуем все свойства от родителя
    def __init__(self,bold=False,size=None,color=None,content=None,**kwargs):
        #Наследуем аргументы от класса родителя
        super().__init__(**kwargs)
        #Свойство жирности шрифта
        self.BOLD = bold
        #Свойство размера шрифта
        self.SIZE = size
        #Свойство цвета шрифта
        self.COLOR = color
        #Свойство текста шрифта
        self.CONTENT = content
        #Свойство шрифт шрифта
        self.FONT = None
    #Метод загрузки и отображения шрифта
    def show_text(self):
        #Создаем шрифт и задаем размер шрифта
        self.FONT = pygame.font.SysFont('Arial',self.SIZE)
        #Добавляем жирность шрифта к тексту
        pygame.font.Font.set_bold(self.FONT,self.BOLD)
        #Рендерим шрифт
        self.FONT = self.FONT.render(self.CONTENT,True,self.COLOR)
        #Отображаем текст
        screen.blit(self.FONT,(self.X,self.Y))




#Создаем кораблики для меню
ship1 = Ship(
            len_ship=1,direction_ship='right',number_ship=4,
            width=cell//2,height=cell//2,
            x=500,y=140,
            path_img='images/ship1.png'
            )
ship2 = Ship(
            len_ship=2,direction_ship='right',number_ship=3,
            width=cell,height=cell//2,
            x=500,y=100,
            path_img='images/ship2.png'
            )
ship3 = Ship(
            len_ship=3,direction_ship='right',number_ship=2,
            width=cell*1.5,height=cell//2,
            x=500,y=60,
            path_img='images/ship3.png'
            )
ship4 = Ship(
            len_ship=4,direction_ship='right',number_ship=1,
            width=cell*2,height=cell//2,
            x=500,y=20,
            path_img='images/ship4.png'
            )
#Создаем карту вращения
map_rotate = Sprite(
                    x=500,
                    y=200,
                    width=cell*4,
                    height=cell*4,
                    path_img='images/map_rotate.png'
)
#Создаем кнопку вращения
button_rotate = Sprite(
                        x=500,
                        y=400,
                        width=cell*4,
                        height=cell*2,
                        path_img='images/rotate.png'
)
#Кнопка закончить расстановку кораблей
button_end_set = Sprite(
                        x=500,
                        y=400,
                        width=cell*4,
                        height=cell*2,
                        path_img='images/button_end_set.png'
)
#Кнопка атаковать
button_fight = Sprite(
                    x= 500,
                    y= 450,
                    width= 200,
                    height= 100,
                    path_img='images/attack.png'
)
#Крестик(попадание)
cross = Sprite(
                    x=0,
                    y=0,
                    width=cell,
                    height=cell,
                    path_img='images/cross.png'
)
#Нолик(промах)
point = Sprite(
                    x=0,
                    y=0,
                    width=cell,
                    height=cell,
                    path_img='images/point.png'
)
#Создаем обводку корабля
select = Sprite(
                path_img='images/select.png'
)
#Создаем кораблик на карте вращения
ship_rotate_map = Ship()
#Список с кораблями в меню
list_ships_menu = [ship1,ship2,ship3,ship4]
#Бэкграунд
background = Sprite(
                    x=0,y=0,
                    width=500,
                    height=500    ,
                    path_img='images/background.png'
                    )
#Текст для союзного поля
self_text_map = Text(
                        size=40,color='black',content='Ваше поле',
                        x=150,y=0
                    )
#Текст для вражеского поля
enemy_text_map = Text(
                        size=40,color='black',content='Вражеское поле',
                        x=850,y=0
                    )
wait = Sprite(width=1200,height=550,path_img='images/wait.png')

bg_menu = Sprite(0,0,400,700,path_img='images/bg_menu.png')
button_start_play = Sprite(75,55,275,160,path_img='images/start.png')
button_exit = Sprite(75,270,275,160,path_img='images/exit.png')
button_developer = Sprite(75,485,275,160,path_img='images/developers.png')

client1 = Sprite(75,55,275,160,path_img='images/player1.png')
client2 = Sprite(75,270,275,160,path_img='images/player2.png')
bg_win = Sprite(0,0,1200,550,'images/win.png')
bg_defeat = Sprite(0,0,1200,550,'images/defeat.png')
button_back = Sprite(1100,450,100,100,path_img='images/button_exit.png')
button_menu = Sprite(300,600,100,100,path_img='images/button_menu.png')

bg_developers = Sprite(0,0,400,700,path_img='images/developer.png')
names = Sprite(75,75,250,550,path_img='images/names.png')


