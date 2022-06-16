# encoding=utf-8
import numpy as np
import copy
import pygame, random, datetime, time, threading

pygame.init()
flashtime = 300
fpsClock = pygame.time.Clock()

WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("game")

candy = pygame.image.load('15b9875454c170af.jpeg').convert_alpha()
candy = pygame.transform.scale(candy,(15,12))

drawing = pygame.Surface(screen.get_size())
drawing = drawing.convert()
drawing.fill((255, 255, 255))  # alive是黑色

food_max_account = 20  # 食物最大個數
food_account=0 #食物個數
ant1_account = 0  # 螞蟻1個數
ant2_account=0 #螞蟻2個數
ant3_account=0 #螞蟻3個數
food1=0
food2=0

ant_disappear = 0
foot_dead = 0
t1 = 50  # 陣列長
t2 = 50  # 陣列寬
unit = 10
matrix = [[0 for x in range(t1)] for y in range(t2)]  # 場地
# flavor = [[0 for x in range(t1)] for y in range(t2)]  # 食物的味道
foot = np.zeros((t1, t2))  # 腳
foot_timer = True
foot_row = 0  # 上一個腳出現的row
foot_col = 0  # 上一個腳出現的col


# matrix[][] == 1  => 螞蟻，黑色
# matrix[][] == 2  => 食物，黃色
# matrix[][] == 3  => 蟻穴，咖啡色

class Food:
    def __init__(self, i, j, Stime):
        self.i = i
        self.j = j
        self.Stime = Stime

    def set_i(self, i):
        self.i = i

    def set_j(self, j):
        self.j = j


class Ant:
    def __init__(self, i, j, Stime):
        super().__init__()
        self.i = i
        self.j = j
        self.Stime = Stime
        self.eat = 0
        self.step = None
        self.weight = random.randint(1, 100)
        self.targetFood=-1
    def up(self):
        self.i = self.i - 1

    def down(self):
        self.i = self.i + 1

    def left(self):
        self.j = self.j - 1

    def right(self):
        self.j = self.j + 1
    # def destination(self, s_i, s_j):
    #     self.s_i = s_i
    #     self.s_j = s_j
    #     self.step = 1
    #
    # def forword(self):
    #     self.step = self.step + 1


# 初始化
food = []  # 食物
ant1 = []  # 螞蟻1
ant2 = []
ant3 = []


def foodappear():
    global food_account
    while True:
        i = random.randint(2,t1-3)
        j = random.randint(2,t2-3)
        if(matrix[i][j]==0):
            matrix[i][j]= 2
            food.append(Food(i,j,time.time()))
            food_account=food_account+1
            break

def fooddisappear(i,j):
    global food_account
    k=0
    while k <= food_account-1:
        if (food[k].i==i and food[k].j==j):
            del food[k]
            food_account=food_account-1
            break
        k=k+1

def antappear(ant_account,ant,classant):
    i, j = 0, 0
    if(classant==1):#redAnt
        i=46
        j=2
    elif(classant==2):#blueAnt
        i=3
        j=47
    elif(classant==3):
        i=3
        j=3
    matrix[i][j] = 1  # "1" means ant
    ant.append(Ant(i,j,time.time()))
    ant_account=ant_account+1
    return ant_account

def antdisappear(k,ant):
    f=0
    if(ant==ant1):
        f=10
    elif(ant==ant2):
        f=20
    else:
        f=30
    matrix[ant[k].i][ant[k].j]=f
    del ant[k]


def find_ant_to_antdisappear(ant_account,ant,classant):
    if(ant_account==0):
        return 0
    # print(ant_account)
    k = 0
    while k <= ant_account-1:
        if(classant==1):
            if (timeinterval(ant[k].Stime)>=10):
                antdisappear(k,ant)
                ant_account=ant_account-1
        elif (classant == 2):
            if (timeinterval(ant[k].Stime) >= 10):
                antdisappear(k, ant)
                ant_account = ant_account - 1
        elif (classant == 3):
            if (timeinterval(ant[k].Stime) >= 10):
                antdisappear(k, ant)
                ant_account = ant_account - 1
        k=k+1
    return ant_account
# 時間計算
def timeinterval(Stime):
    Etime = time.time()
    return Etime-Stime

def ant1_find_food(k, ant):
    if(food_account==0 or ant[k].eat==1):
        return 0
    t=0
    target_food=0
    mix_dis=100000
    f=0
    if(ant==ant1):
        f=10
    else:
        f=30
    global food1
    while t<=food_account-1:
        distance=(ant[k].i-food[t].i)**2+(ant[k].j-food[t].j)**2
        if(distance<mix_dis):
            mix_dis=distance
            target_food=t
        t=t+1
    matrix[ant[k].i][ant[k].j]=f####224,163,177
    for i in range(-1,2):
        for j in range(-1,2):
            if(matrix[ant[k].i+i][ant[k].j+j]==2):
                eat_food(k, target_food, ant, ant[k].i+i, ant[k].j+j)
                if(ant==ant1):
                    food1=food1+1
                return 0
    i=0
    j=0
    if(food[target_food].i<ant[k].i):
        i=i-1#ant1[k].up()
        if(food[target_food].j<ant[k].j):
            j=j-1#ant1[k].left()
        elif(food[target_food].j>ant[k].j):
            j=j+1#ant1[k].right()
    elif (food[target_food].i>ant[k].i):
        i=i+1#ant1[k].down()
        if (food[target_food].j < ant[k].j):
            j=j-1#ant1[k].left()
        elif (food[target_food].j > ant[k].j):
            j=j+1#ant1[k].right()
    elif (food[target_food].i == ant[k].i):
        if (food[target_food].j < ant[k].j):
            j=j-1#ant1[k].left()
        elif (food[target_food].j > ant[k].j):
            j=j+1#ant1[k].right()
    if(matrix[ant[k].i+i][ant[k].j+j]==0 or matrix[ant[k].i+i][ant[k].j+j]==f):
        if(i==-1):
            ant[k].up()
        elif(i==1):
            ant[k].down()
        if(j==-1):
            ant[k].left()
        elif(j==1):
            ant[k].right()
    else:
        if(matrix[ant[k].i+i][ant[k].j]==0 or matrix[ant[k].i+i][ant[k].j]==f):
            if (i == -1):
                ant[k].up()
            elif (i == 1):
                ant[k].down()
        elif(matrix[ant[k].i][ant[k].j+j]==0 or matrix[ant[k].i][ant[k].j+j]==f):
            if (j == -1):
                ant[k].left()
            elif (j == 1):
                ant[k].right()
    if (i == 0 and j == 0):
        while((i==0 and j==0) or (matrix[ant[k].i+i][ant[k].j+j]!=0 and matrix[ant[k].i+i][ant[k].j+j]!=f)):
            i=random.randint(-1,1)
            j=random.randint(-1,1)
        if (i == -1):
            ant[k].up()
        elif (i == 1):
            ant[k].down()
        if (j == -1):
            ant[k].left()
        elif (j == 1):
            ant[k].right()
    matrix[ant[k].i][ant[k].j]=1


def find_food_target(i,j):
    target=-1
    for n in range(food_account):
        if(food[n].i==i and food[n].j==j):
            target=n
    return target
def ant2_find_food(k,ant,ant_account):
    if (ant[k].eat == 1):
        return 0
    global food2
    f=0
    if(ant==ant2):
        f=20
    else:
        f=30
    index2=ant_targetFood(ant,ant_account)
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (matrix[ant[k].i + i][ant[k].j + j] == 2 and food[ant[k].targetFood].i==ant[k].i + i and food[ant[k].targetFood].j==ant[k].j + j):
                eat_food(k, ant[k].targetFood, ant, ant[k].i + i, ant[k].j + j)
                if (ant==ant2):
                    food2=food2+1
                return 0
    i = 0
    j = 0
    step=0

    if (food[ant[k].targetFood].i < ant[k].i):
        i = i - 1  # ant1[k].up()
        if (food[ant[k].targetFood].j < ant[k].j):
            j = j - 1  # ant1[k].left()
        elif (food[ant[k].targetFood].j > ant[k].j):
            j = j + 1  # ant1[k].right()
    elif (food[ant[k].targetFood].i > ant[k].i):
        i = i + 1  # ant1[k].down()
        if (food[ant[k].targetFood].j < ant[k].j):
            j = j - 1  # ant1[k].left()
        elif (food[ant[k].targetFood].j > ant[k].j):
            j = j + 1  # ant1[k].right()
    elif (food[ant[k].targetFood].i == ant[k].i):
        if (food[ant[k].targetFood].j < ant[k].j):
            j = j - 1  # ant1[k].left()
        elif (food[ant[k].targetFood].j > ant[k].j):
            j = j + 1  # ant1[k].right()

    if (matrix[ant[k].i + i][ant[k].j + j] == 0 or matrix[ant[k].i + i][ant[k].j + j] == f):
        matrix[ant[k].i][ant[k].j] = f####173,200,255
        if (i == -1):
            ant[k].up()
        elif (i == 1):
            ant[k].down()
        if (j == -1):
            ant[k].left()
        elif (j == 1):
            ant[k].right()
        step=1
    else:
        if (matrix[ant[k].i + i][ant[k].j] == 0 or matrix[ant[k].i + i][ant[k].j] == f):
            matrix[ant[k].i][ant[k].j] = f####173,200,255
            if (i == -1):
                ant[k].up()
                step = 1
            elif (i == 1):
                ant[k].down()
                step=1
        elif (matrix[ant[k].i][ant[k].j + j] == 0 or matrix[ant[k].i][ant[k].j + j] == f):
            matrix[ant[k].i][ant[k].j] = f###
            if (j == -1):
                ant[k].left()
                step = 1
            elif (j == 1):
                ant[k].right()
                step=1
    if (step==0):
        i=0
        j=0
        while ((i == 0 and j == 0) or (matrix[ant[k].i+i][ant[k].j+j]!=0 and matrix[ant[k].i+i][ant[k].j+j]!=f)):
            i = random.randint(-1, 1)
            j = random.randint(-1, 1)
        matrix[ant[k].i][ant[k].j] = f
        if (i == -1):
            ant[k].up()
        elif (i == 1):
            ant[k].down()
        if (j == -1):
            ant[k].left()
        elif (j == 1):
            ant[k].right()
    matrix[ant[k].i][ant[k].j] = 1
def ant_targetFood(ant, ant_account):
    index=[]
    T=time.time()
    for i in range(ant_account):
        k=-1
        Ltime=0
        for j in range(ant_account):
            if(j not in index):
                if(T-ant[j].Stime>Ltime):
                    Ltime=T-ant[j].Stime
                    k=j
        index.append(k)
    index2=[]
    for i in range(ant_account):
        distance=99999999
        k=-1
        for j in range(food_account):
            if(j not in index2):
                if((ant[index[i]].i-food[j].i)**2+(ant[index[i]].j-food[j].j)**2<distance):
                    distance=(ant[index[i]].i-food[j].i)**2+(ant[index[i]].j-food[j].j)**2
                    k=j
        index2.append(k)
        ant[index[i]].targetFood=k

def search(index,y):
    for j in range(len(index)):
        if (y == index[j]):
            return 1
    return 0

def eat_food(k,target_food,ant,food_i,food_j):
    global food_account
    ant[k].Stime=time.time()
    if(ant==ant2):
        matrix[ant[k].i][ant[k].j]=20###
    elif(ant==ant1):
        matrix[ant[k].i][ant[k].j]=10###
    else:
        matrix[ant[k].i][ant[k].j]=30###
    ant[k].i=food_i
    ant[k].j=food_j
    ant[k].eat=1
    matrix[food_i][food_j]=1
    del food[target_food]
    food_account=food_account-1

def findtogohome(k,ant,classant):
    if (ant[k].eat == 0):
        return 0
    i=0
    j=0
    f=0
    if(classant==1):
        i=46
        j=3
        f=10
    elif(classant==2):
        i=3
        j=46
        f=20
    elif(classant==3):
        i=3
        j=3
        f=30
    matrix[ant[k].i][ant[k].j]=f
    if(ant[k].i<i):
        i=1
    elif(ant[k].i>i):
        i=-1
    elif(ant[k].i==i):
        i=0
    if(ant[k].j>j):
        j=-1
    elif(ant[k].j<j):
        j=1
    elif(ant[k].j==j):
        j=0
    if(matrix[ant[k].i+i][ant[k].j+j]==0 or matrix[ant[k].i+i][ant[k].j+j]==f):
        if(i==1):
            ant[k].down()
        elif(i==-1):
            ant[k].up()
        if(j==-1):
            ant[k].left()
        elif(j==1):
            ant[k].right()
    else:
        if (matrix[ant[k].i+i][ant[k].j]==0 or matrix[ant[k].i+i][ant[k].j]==f):
            if (i == 1):
                ant[k].down()
            elif (i == -1):
                ant[k].up()
        if (matrix[ant[k].i][ant[k].j+j]==0 or matrix[ant[k].i][ant[k].j+j]==f):
            if (j == -1):
                ant[k].left()
            elif (j == 1):
                ant[k].right()
        i=0
        j=0
    if (i == 0 and j == 0):
        while ((i == 0 and j == 0) or (matrix[ant[k].i+i][ant[k].j+j]!=0 and matrix[ant[k].i+i][ant[k].j+j]!=f)):
            i = random.randint(-1, 1)
            j = random.randint(-1, 1)
        if (i == -1):
            ant[k].up()
        elif (i == 1):
            ant[k].down()
        if (j == -1):
            ant[k].left()
        elif (j == 1):
            ant[k].right()
    matrix[ant[k].i][ant[k].j]=1

def iftohome(k,ant,classant):
    if(ant[k].eat==1):
        for i in range(-1, 2):
            for j in range(-1, 2):
                # if(ant[k].i+i>=t1):
                #     return 0
                # if (ant[k].j + j <0):
                #     continue
                if(classant==1):
                    if (matrix[ant[k].i + i][ant[k].j + j] == 3):
                        ant[k].eat=0
                        ant[k].Stime = time.time()
                        return 1
                if (classant == 2):
                    if (matrix[ant[k].i + i][ant[k].j + j] ==4):
                        ant[k].eat = 0
                        ant[k].Stime = time.time()
                        return 1
                if (classant == 3):
                    if (matrix[ant[k].i + i][ant[k].j + j] == 5):
                        ant[k].eat = 0
                        ant[k].Stime = time.time()
                        return 1

    return 0
def show():  # 畫圖
    for i in range(0, t1):
        for j in range(0, t2):
            # 螞蟻
            # if (matrix[i][j] == 1):
            #     pygame.draw.rect(drawing, (0,0,0), [j * unit, i * unit, unit, unit], 0)
            #     screen.blit(drawing, (0, 0))
            if(matrix[i][j] == 4):#藍螞蟻的家
                pygame.draw.rect(drawing, (95, 20, 128), [j * unit, i * unit, unit, unit], 0)
                screen.blit(drawing, (0, 0))
            elif(matrix[i][j]==2):# 食物
                #pygame.draw.rect(drawing, (235, 194, 67), [j * unit, i * unit, unit, unit], 0)
                # screen.blit(drawing, (0, 0))
                pass
            elif(matrix[i][j] == 3):#紅螞蟻的家
                pygame.draw.rect(drawing, (77, 31, 0), [j * unit, i * unit, unit, unit], 0)
                screen.blit(drawing, (0, 0))
            elif (matrix[i][j] == 5):  #綠螞蟻的家
                pygame.draw.rect(drawing, (20, 77, 11), [j * unit, i * unit, unit, unit], 0)
                screen.blit(drawing, (0, 0))
            elif (matrix[i][j] == 10):
                pygame.draw.rect(drawing, (224,163,177), [j * unit, i * unit, unit, unit], 0)
                screen.blit(drawing, (0, 0))
            elif (matrix[i][j] == 20):  #182,237,179
                pygame.draw.rect(drawing, (173, 200, 255), [j * unit, i * unit, unit, unit], 0)
                screen.blit(drawing, (0, 0))
            elif (matrix[i][j] == 30):
                pygame.draw.rect(drawing, (182,237,179), [j * unit, i * unit, unit, unit], 0)
                screen.blit(drawing, (0, 0))
            else:
                pygame.draw.rect(drawing, (255, 255, 255), [j * unit, i * unit, unit, unit], 0)
                screen.blit(drawing, (0, 0))
    #紅螞蟻
    for n in range(ant1_account):
        colorR = 255
        colorG = 0
        colorB = 55*int(timeinterval(ant1[n].Stime))
        if(colorB>=255):
            colorB=255
            colorG= 23*int(timeinterval(ant1[n].Stime))
            if(colorG>=255):
                colorG=255
        pygame.draw.rect(drawing, (colorR, colorG, colorB), [ant1[n].j * unit, ant1[n].i * unit, unit, unit], 0)
        screen.blit(drawing, (0, 0))
    #藍螞蟻
    for n in range(ant2_account):
        colorR = 0
        colorG = 55 * int(timeinterval(ant2[n].Stime))#20
        colorB = 255
        if(colorG>=255):
            colorG=255
            colorR= 23*int(timeinterval(ant2[n].Stime))#12
            if(colorR>=255):
                colorR=255
        pygame.draw.rect(drawing, (colorR, colorG, colorB), [ant2[n].j * unit, ant2[n].i * unit, unit, unit], 0)
        screen.blit(drawing, (0, 0))
    #綠螞蟻
    for n in range(ant3_account):
        colorR = 55 * int(timeinterval(ant3[n].Stime))
        colorG = 255
        colorB = 0
        if(colorR>=255):
            colorR=255
            colorB= 10*int(timeinterval(ant3[n].Stime))
            if(colorB>=255):
                colorB=255
        pygame.draw.rect(drawing, (colorR, colorG, colorB), [ant3[n].j * unit, ant3[n].i * unit, unit, unit], 0)
        screen.blit(drawing, (0, 0))

def candy_show():
    for i in range(0, t1):
        for j in range(0, t2):
            if(matrix[i][j] == 2):
                candy_rect = pygame.Rect((j * unit), (i * unit), unit, unit)
                screen.blit(candy,candy_rect)

# 蟻穴位置
def home():#兇兇的紅螞蟻
    for i in range(1,4):
        for j in range(0, 3):
            matrix[t1 - i][j] = 3

def home2():#被紅螞蟻欺負的藍螞蟻
    for i in range(0, 3):
        for j in range(1, 4):
            matrix[i][t2 - j] = 4
def home3():
    for i in range(0, 3):
        for j in range(0, 3):
            matrix[i][j] = 5

home()
home2()
home3()
running=True
for x in range(15):
    foodappear()
Ftime=time.time()
Ntime=time.time()
ant1_account=antappear(ant1_account, ant1,1)
ant2_account=antappear(ant2_account,ant2,2)
ant3_account=antappear(ant3_account,ant3,3)
while running:
    if(timeinterval(Ftime)>1):
        foodappear()
        Ftime=time.time()
    for n in range(ant1_account):
        ant1_find_food(n,ant1)
    for n in range(ant2_account):
        ant2_find_food(n,ant2,ant2_account)
    if(food1<food2):
        for n in range(ant3_account):
            print(2)
            ant2_find_food(n, ant3, ant3_account)
    else:
        for n in range(ant3_account):
            ant1_find_food(n, ant3)

    ant1_account=find_ant_to_antdisappear(ant1_account,ant1,1)
    ant2_account=find_ant_to_antdisappear(ant2_account,ant2,2)
    ant3_account=find_ant_to_antdisappear(ant3_account,ant3,3)

    for n in range(ant1_account):
        if(iftohome(n,ant1,1)):
            ant1_account=antappear(ant1_account,ant1,1)
        else:
            findtogohome(n,ant1,1)
    for n in range(ant2_account):
        if(iftohome(n,ant2,2)):
            ant2_account=antappear(ant2_account,ant2,2)
        else:
            findtogohome(n,ant2,2)
    for n in range(ant3_account):
        if(iftohome(n,ant3,3)):
            ant3_account=antappear(ant3_account,ant3,3)
        else:
            findtogohome(n,ant3,3)
    print('ant1:', food1)
    print('ant2:', food2)
    show()
    candy_show()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 使用者按關閉鈕
             running = False
    pygame.display.update()
pygame.quit()
