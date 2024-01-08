import pygame
import random
pygame.init()
clock = pygame.time.Clock()
width = 800
height = 800
screen = pygame.display.set_mode((width,height))
gameOver = True
green = (0,255,0)
red = (255,0,0)
x = 30
y = 30
block = 30
down=up=left=right=False
body = [[x,y]] #начальное тело змейки
score = 0
speed = 5
def snake_body(body): #нарисовать змейку
    for i in body:
        pygame.draw.rect(screen, green, (i[0],i[1],block,block))
def eat(x,y): #нарисовать еду
    pygame.draw.rect(screen, red, (x, y, block, block))
#окординаты еды
eatx = random.randrange(block*2,width-block,block)
eaty = random.randrange(block*2,height-block,block)
while gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                down = True
                up=left=right=False
            elif event.key == pygame.K_UP:
                up = True
                down=right=left=False
            elif event.key == pygame.K_LEFT:
                left = True
                right=up=down=False
            elif event.key == pygame.K_RIGHT:
                right = True
                up=down=left=False

        if event.type != pygame.KEYDOWN: #если не нажата ни одна клавиша то движение  вправо
            right = True

    screen.fill((0, 0, 0))

    if down == True:
        y +=block
    elif up == True:
        y -=block
    elif left == True:
        x -= block
    elif right == True:
        x += block

    #условие по увеличению змейки
    if x == eatx and y == eaty:
        body.append(head)
        score+=1
        eatx = random.randrange(block, width - block, block)
        eaty = random.randrange(block, height - block, block)
        if score%5 == 0:
            speed+=1   #увеличить скорость каждые +5 очков

    head = [x,y]  #голова
    body.append(head)
    # print(body)
    #условие врезаться в край экрана
    if x <= 0 or x+block >= width or y <= 0 or y + block >= height:
        gameOver = False
        print('Очков набрано: ',score)
    #условие нельзя врезаться в себя/ехать обратно
    for i in body[:-1]:
        if len(body)>1 and head == i:
            gameOver = False
            print(score)
    eat(eatx,eaty) #нарисовать еду
    snake_body(body) #нарисовать змейку
    body.pop(0) #удалить последний элемент чтобы тело не увеличивалось
    pygame.display.flip()
    pygame.display.set_caption('Очков набрано: '+str(score)+'  Текущая скорость движения: '+str(speed))
    clock.tick(speed)
