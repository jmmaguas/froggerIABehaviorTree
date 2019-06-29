#! /usr/bin/env python
import pygame
import random as Random
from pygame.locals import *
from sys import exit
from BehaviourTree import *
from __builtin__ import True
from time import sleep

pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, 32, 2, 4096)

font_name = pygame.font.get_default_font()
game_font = pygame.font.SysFont(font_name, 72)
info_font = pygame.font.SysFont(font_name, 24)
menu_font = pygame.font.SysFont(font_name, 36)

screen = pygame.display.set_mode((448, 546), 0, 32)

# --- Carregando imagens ---
background_filename = './images/bg.png'
frog_filename = './images/sprite_sheets_up.png'
arrived_filename = './images/frog_arrived.png'
car1_filename = './images/car1.png'
car2_filename = './images/car2.png'
car3_filename = './images/car3.png'
car4_filename = './images/car4.png'
car5_filename = './images/car5.png'
plataform_filename = './images/tronco.png'

background = pygame.image.load(background_filename).convert()
sprite_sapo = pygame.image.load(frog_filename).convert_alpha()
sprite_arrived = pygame.image.load(arrived_filename).convert_alpha()
sprite_car1 = pygame.image.load(car1_filename).convert_alpha()
sprite_car2 = pygame.image.load(car2_filename).convert_alpha()
sprite_car3 = pygame.image.load(car3_filename).convert_alpha()
sprite_car4 = pygame.image.load(car4_filename).convert_alpha()
sprite_car5 = pygame.image.load(car5_filename).convert_alpha()
sprite_plataform = pygame.image.load(plataform_filename).convert_alpha()

# --- Carregando Efeitos Sonoros ---
hit_sound = pygame.mixer.Sound('./sounds/boom.wav')
agua_sound = pygame.mixer.Sound('./sounds/agua.wav')
chegou_sound = pygame.mixer.Sound('./sounds/success.wav')
trilha_sound = pygame.mixer.Sound('./sounds/guimo.wav')

pygame.display.set_caption('Frogger')
clock = pygame.time.Clock()

lista = []


class Object():

    def __init__(self, position, sprite):
        self.sprite = sprite
        self.position = position

    def draw(self):
        screen.blit(self.sprite, (self.position))

    def rect(self):
        return Rect(self.position[0], self.position[1], self.sprite.get_width(), self.sprite.get_height())


class Frog(Object):

    def __init__(self, position, sprite_sapo):
        self.sprite = sprite_sapo
        self.position = position
        self.lives = 3 
        self.animation_counter = 0
        self.animation_tick = 1
        self.way = "UP"
        self.can_move = 1
        self.mybehaviour = self.defineBehaviour()
        
    # Define o comportamento do frog sobre a forma de uma behaviourTree
    
    def defineBehaviour(self):
        return Selector(
            Sequence(
                Atomic(self.estaEstrada),
                Selector(
                    Sequence(
                        Atomic(self.podeFrenteCarro),
                        Atomic(self.andarFrente)
                        ),
                    Sequence(
                        Atomic(self.direcaoPar),
                        Selector(
                            Sequence(
                                Atomic(self.temCarroVirEsquerda),
                                Atomic(self.podeBaixoCarro),
                                Atomic(self.andarBaixo)
                                ),
                            Sequence(Atomic(self.podeDireitaCarro), Atomic(self.andarDireita)),
                            Atomic(self.success)
                            )
                        ),
                    Sequence(
                        Inverter(Atomic(self.direcaoPar)),
                        Selector(
                            Sequence(
                                Atomic(self.temCarroVirDireita),
                                Atomic(self.podeBaixoCarro),
                                Atomic(self.andarBaixo)
                                ),
                            Sequence(Atomic(self.podeEsquerdaCarro), Atomic(self.andarEsquerda)),
                            Atomic(self.success)
                            )
                        ),
                    Atomic(self.success)
                    )
                ),
            Sequence(
                Atomic(self.estouLimiarNotRdy),
                Atomic(self.andarEsquerda)
                ),
            Sequence(
                Atomic(self.estaLago),
                Selector(
                    Atomic(self.estamosPenultimaNotRdy),
                    Sequence(
                        Atomic(self.podeFrenteLago),
                        Atomic(self.andarFrente),
                        Atomic(self.andarTroco)
                        ),
                    Sequence(
                        Atomic(self.estamosPontas),
                        Selector(
                            Sequence(
                                Atomic(self.moveLadoLago),
                                Atomic(self.andarTroco)
                                ),
                            Sequence(
                                Atomic(self.podeTrasLago),
                                Atomic(self.andarBaixo),
                                Atomic(self.andarTroco)
                                ),
                            
                            Atomic(self.success)
                            )
                        ),
                    Atomic(self.success)
                    )
                ),
            Sequence(
                Atomic(self.quaseNenufar),
                Atomic(self.nenufarFrente),
                Atomic(self.andarFrente)                                 
                ),
            Atomic(self.success)
            )

    def success(self):
        # print "success"
        return True
    
    def estouLimiarNotRdy(self):
        return self.position[1] == 241 and self.position[0] > 207
    
    def direcaoPar(self):
        # carros a mexer para a direita
        return self.position[1] % 2 == 0
    
    #===========================================================================
    # def canMove(self):
    #     if self.can_move == 1:
    #         return True
    #     else:
    #         return False
    #===========================================================================
    
    def teste(self):
        print "ola"
        return True
    
    def estamosPontas(self):
        if self.position[1] % 2 == 0:
            return self.position[0] > 390
        else:
            return self.position[0] < 25
    
    def querAndarParaTras(self):
        if self.position[1] % 2 == 0:
            return self.position[0] < 25
        else:
            return self.position[0] > 390
    
    def estamosPenultimaNotRdy(self):
        if self.position[1] == 85:
            if self.position[0] > faltam[0] - (3 * game.speed):
                return True
        return False
        
    
    def nenufarFrente(self):
        if self.position[0] > 33 and self.position[0] < 53:
            if 43 in faltam:
                return True
            return False
    
        elif self.position[0] > 115 and self.position[0] < 135:
            if 125 in faltam:                    
                return True
            return False
    
        elif self.position[0] > 197 and self.position[0] < 217:
            if 207 in faltam:
                return True
            return False
    
        elif self.position[0] > 279 and self.position[0] < 299:
            if 289 in faltam:
                return True
            return False
    
        elif self.position[0] > 361 and self.position[0] < 381:
            if 371 in faltam:
                return True
            return False
        return False
    
    def quaseNenufar(self):
        return self.position[1] < 85
    
    def estaLago(self):
        return self.position[1] <= 241 and self.position[1] > 84
    
    def estaEstrada(self):
        return self.position[1] > 245

    def paraTroco(self):
        frog.position[0] = frog.position[0] + 0
        return True

    def andarTroco(self):
        if self.position[1] % 2 != 0:
            frog.position[0] = frog.position[0] - game.speed
        else:
            frog.position[0] = frog.position[0] + game.speed
        return True
    
    def rectanguloGrandeLago(self, posicaoNova):
        return Rect(self.position[0] + posicaoNova[0] + 14 , self.position[1] + posicaoNova[1], 2, 30)
    
    def podeFrenteLago(self):
        # pode andar Lago
        for plat in plataforms:
            if plat.position[1] == self.position[1] - 39:
                plataformRect = plat.rect()
                
                if self.direcaoPar():
                    frogRect = self.rectanguloGrandeLago((game.speed * 3, -39)) 
                    if frogRect.colliderect(plataformRect):
                        frogRect2 = self.rectanguloGrandeLago((game.speed * 6, -39))
                        if frogRect2.colliderect(plataformRect):
                            return True
                else:
                    frogRect = self.rectanguloGrandeLago((-game.speed * 3, -39)) 
                    if frogRect.colliderect(plataformRect):
                        frogRect2 = self.rectanguloGrandeLago((-game.speed * 6, -39))
                        if frogRect2.colliderect(plataformRect):
                            return True

        return False
        
    def podeTrasLago(self):
        for plat in plataforms:
            if plat.position[1] == self.position[1] + 39:
                plataformRect = plat.rect()
                
                frogRect = self.rectanguloGrandeLago((0, +39)) 
                if frogRect.colliderect(plataformRect):
                    pygame.draw.rect(screen, [255, 0, 0], frogRect, 0)
                    pygame.display.flip()
                    
                    if self.direcaoPar():
                        frogRect2 = self.rectanguloGrandeLago((game.speed * 6, +39))
                    else:
                        frogRect2 = self.rectanguloGrandeLago((-game.speed * 6, +39))
                    
                    if frogRect2.colliderect(plataformRect):
                        #=======================================================
                        # pygame.draw.rect(screen, [0, 255, 0], frogRect2, 0)
                        # pygame.display.flip()
                        # sleep(0.2)
                        #=======================================================
                        return True
    
    def moveLadoLago(self):
        for plat in plataforms:
            if plat.position[1] == self.position[1]:
                plataformRect = plat.rect()
                if self.position[1] % 2 == 0:
                    frogRect = frog.rectanguloGrandeLago((-41, 0))
                    
                    if frogRect.colliderect(plataformRect):
                        lista.append("left")
                        return True
                else:
                    frogRect = frog.rectanguloGrandeLago((41, 0))
                    
                    if frogRect.colliderect(plataformRect):
                        lista.append("right")
                        return True
                
        return False

    def rectanguloGrande(self, posicaoNova):
        if posicaoNova[0] > 0:
            return Rect(self.position[0], self.position[1] + posicaoNova[1], 30 + posicaoNova[0], 30)
        else:
            return Rect(self.position[0] + posicaoNova[0], self.position[1] + posicaoNova[1], 30 - posicaoNova[0], 30)

    def podeFrenteCarro(self):
        margem = 20 + (game.speed * game.level)
        for inimigo in enemys:
            if inimigo.position[1] == self.position[1] - 39:
                fator = inimigo.factor
                enemyRect = inimigo.rect()
                
                if self.direcaoPar():
                    frogRect = self.rectanguloGrande((margem * fator, -39))
                else:
                    frogRect = self.rectanguloGrande((-margem * fator, -39))
                
                if frogRect.colliderect(enemyRect):
                    return False

        return True
    
    def podeBaixoCarro(self):
        margem = 20 + (game.speed * game.level)
        
        for inimigo in enemys:
            if inimigo.position[1] == self.position[1] + 39:
                fator = inimigo.factor
                enemyRect = inimigo.rect()
                
                if self.direcaoPar():
                    frogRect = self.rectanguloGrande((margem * fator, 39))
                else:
                    frogRect = self.rectanguloGrande((-margem * fator, 39))
                
                if frogRect.colliderect(enemyRect):
                    return False
        return True
       
    def podeEsquerdaCarro(self):
        if self.position[0] == 2:
            return False
        
        for inimigo in enemys:
            if inimigo.position[1] == self.position[1]:
                enemyRect = inimigo.rect()
                frogRect = self.rectanguloGrande((-41, 0))
                if frogRect.colliderect(enemyRect):
                    return False
        
        return True
               
    def podeDireitaCarro(self):
        if self.position[0] == 412:
            return False
        
        for inimigo in enemys:
            if inimigo.position[1] == self.position[1]:
                enemyRect = inimigo.rect()
                frogRect = self.rectanguloGrande((41, 0))
                if frogRect.colliderect(enemyRect):
                    return False
            
        return True
    
    def temCarroVirEsquerda(self):
        
        for inimigo in enemys:
            if inimigo.position[1] == self.position[1]:
                enemyRect = inimigo.rect()
                margem = -(41 + game.speed * inimigo.factor)
                frogRect = self.rectanguloGrande((margem, 0))
                if frogRect.colliderect(enemyRect):
                    return True
        
        return False
    
    def temCarroVirDireita(self):
                
        for inimigo in enemys:
            if inimigo.position[1] == self.position[1]:
                enemyRect = inimigo.rect()
                margem = (41 + game.speed * inimigo.factor)
                frogRect = self.rectanguloGrande((margem, 0))
                if frogRect.colliderect(enemyRect):
                    return True
            
        return False
    
    def andarFrente(self):
        lista.append("up")
        return True
    
    def andarBaixo(self):
        lista.append("down")
        return True
    
    def andarDireita(self):
        lista.append("right")
        return True
    
    def andarEsquerda(self):
        lista.append("left")
        return True
    
    def updateSprite(self, key_pressed):
       
        if self.way != key_pressed:
            self.way = key_pressed
            if self.way == "up":
                frog_filename = './images/sprite_sheets_up.png'
                self.sprite = pygame.image.load(frog_filename).convert_alpha()
            elif self.way == "down":
                frog_filename = './images/sprite_sheets_down.png'
                self.sprite = pygame.image.load(frog_filename).convert_alpha()
            elif self.way == "left":
                frog_filename = './images/sprite_sheets_left.png'
                self.sprite = pygame.image.load(frog_filename).convert_alpha()
            elif self.way == "right":
                frog_filename = './images/sprite_sheets_right.png'
                self.sprite = pygame.image.load(frog_filename).convert_alpha()

    def moveFrog(self, key_pressed, key_up):
        # sleep(0.05)
        # Tem que fazer o if das bordas da tela ainda
        # O movimento na horizontal ainda no ta certin
        if self.animation_counter == 0 :
            self.updateSprite(key_pressed)
        self.incAnimationCounter()
        if key_up == 1:
            if key_pressed == "up":
                if self.position[1] > 39:
                    self.position[1] = self.position[1] - 13
            elif key_pressed == "down":
                if self.position[1] < 473:
                    self.position[1] = self.position[1] + 13
            if key_pressed == "left":
                if self.position[0] > 2:
                    if self.animation_counter == 2 :
                        self.position[0] = self.position[0] - 13
                    else:
                        self.position[0] = self.position[0] - 14
            elif key_pressed == "right":
                if self.position[0] < 401:
                    if self.animation_counter == 2 :
                        self.position[0] = self.position[0] + 13
                    else:
                        self.position[0] = self.position[0] + 14

    def animateFrog(self, key_pressed, key_up):
        
        if self.animation_counter != 0 :
            if self.animation_tick <= 0 :
                self.moveFrog(key_pressed, key_up)
                self.animation_tick = 1
            else :
                self.animation_tick = self.animation_tick - 1

    def setPos(self, position):
        self.position = position

    def decLives(self):
        self.lives = self.lives - 1

    def cannotMove(self):
        self.can_move = 0

    def incAnimationCounter(self):
        self.animation_counter = self.animation_counter + 1
        if self.animation_counter == 3 :
            self.animation_counter = 0
            self.can_move = 1
            lista.__delitem__(0)

    def frogDead(self, game):
        self.setPositionToInitialPosition()
        self.decLives()
        game.resetTime()
        self.animation_counter = 0
        self.animation_tick = 1
        self.way = "UP"
        self.can_move = 1
        if len(lista) > 0:
            lista.__delitem__(0)

    def setPositionToInitialPosition(self):
        self.position = [207, 475]

    def draw(self):
        current_sprite = self.animation_counter * 30
        screen.blit(self.sprite, (self.position), (0 + current_sprite, 0, 30, 30 + current_sprite))

    def rect(self):
        return Rect(self.position[0], self.position[1], 30, 30)


class Enemy(Object):

    def __init__(self, position, sprite_enemy, way, factor):
        self.sprite = sprite_enemy
        self.position = position
        self.way = way
        self.factor = factor

    def move(self, speed):
        if self.way == "right":
            self.position[0] = self.position[0] + speed * self.factor
        elif self.way == "left":
            self.position[0] = self.position[0] - speed * self.factor


class Plataform(Object):

    def __init__(self, position, sprite_plataform, way):
        self.sprite = sprite_plataform
        self.position = position
        self.way = way

    def move(self, speed):
        if self.way == "right":
            self.position[0] = self.position[0] + speed
        elif self.way == "left":
            self.position[0] = self.position[0] - speed


class Game():

    def __init__(self, speed, level):
        self.speed = speed
        self.level = level
        self.points = 0
        self.time = 30
        self.gameInit = 0

    def incLevel(self):
        self.level = self.level + 1

    def incSpeed(self):
        self.speed = self.speed + 1

    def incPoints(self, points):
        self.points = self.points + points

    def decTime(self):
        self.time = self.time - 1

    def resetTime(self):
        self.time = 30


# Funcoess gerais
def drawList(list):
    for i in list:
        i.draw()


def moveList(list, speed):
    for i in list:
        i.move(speed)


def destroyEnemys(list):
    for i in list:
        if i.position[0] < -80:
            list.remove(i)
        elif i.position[0] > 516:
            list.remove(i)


def destroyPlataforms(list):
    for i in list:
        if i.position[0] < -100:
            list.remove(i)
        elif i.position[0] > 448:
            list.remove(i)


def createEnemys(list, enemys, game):
    for i, tick in enumerate(list):
        list[i] = list[i] - 1
        if tick <= 0:
            if i == 0:
                list[0] = (40 * game.speed) / game.level
                position_init = [-55, 436]
                enemy = Enemy(position_init, sprite_car1, "right", 1)
                enemys.append(enemy)
            elif i == 1:
                list[1] = (30 * game.speed) / game.level
                position_init = [506, 397]
                enemy = Enemy(position_init, sprite_car2, "left", 2)
                enemys.append(enemy)
            elif i == 2:
                list[2] = (40 * game.speed) / game.level
                position_init = [-80, 358]
                enemy = Enemy(position_init, sprite_car3, "right", 2)
                enemys.append(enemy)
            elif i == 3:
                list[3] = (30 * game.speed) / game.level
                position_init = [516, 319]
                enemy = Enemy(position_init, sprite_car4, "left", 1)
                enemys.append(enemy)
            elif i == 4:
                list[4] = (50 * game.speed) / game.level
                position_init = [-56, 280]
                enemy = Enemy(position_init, sprite_car5, "right", 1)
                enemys.append(enemy)


def createPlataform(list, plataforms, game):
    for i, tick in enumerate(list):
        list[i] = list[i] - 1
        if tick <= 0:
            if i == 0:
                list[0] = (30 * game.speed) / game.level
                position_init = [-100, 202]
                plataform = Plataform(position_init, sprite_plataform, "right")
                plataforms.append(plataform)
            elif i == 1:
                list[1] = (30 * game.speed) / game.level
                position_init = [448, 163]
                plataform = Plataform(position_init, sprite_plataform, "left")
                plataforms.append(plataform)
            elif i == 2:
                list[2] = (40 * game.speed) / game.level
                position_init = [-100, 124]
                plataform = Plataform(position_init, sprite_plataform, "right")
                plataforms.append(plataform)
            elif i == 3:
                list[3] = (40 * game.speed) / game.level
                position_init = [448, 85]
                plataform = Plataform(position_init, sprite_plataform, "left")
                plataforms.append(plataform)
            elif i == 4:
                list[4] = (20 * game.speed) / game.level
                position_init = [-100, 46]
                plataform = Plataform(position_init, sprite_plataform, "right")
                plataforms.append(plataform)


def carChangeRoad(enemys):
    enemy = Random.choice(enemys)
    initialPosition = enemy.position[1]

    choice = Random.randint(1, 2)
    if (choice % 2 == 0):
        enemy.position[1] = enemy.position[1] + 39
    else :
        enemy.position[1] = enemy.position[1] - 39

    if enemy.position[1] > 436:
        enemy.position[1] = initialPosition
    elif enemy.position[1] < 280:
        enemy.position[1] = initialPosition


def frogOnTheStreet(frog, enemys, game):
    for i in enemys:
        enemyRect = i.rect()
        frogRect = frog.rect()
        if frogRect.colliderect(enemyRect):
            hit_sound.play()
            mortes[0] += 1
            frog.frogDead(game)


def frogInTheLake(frog, plataforms, game):
    # se o sapo esta sob alguma plataforma Seguro = 1
    seguro = 0
    wayPlataform = ""
    for i in plataforms:
        plataformRect = i.rect()
        frogRect = frog.rect()
        if frogRect.colliderect(plataformRect):
            seguro = 1
            wayPlataform = i.way

    if seguro == 0:
        agua_sound.play()
        mortes[1] += 1
        frog.frogDead(game)

    elif seguro == 1:
        if wayPlataform == "right":
            frog.position[0] = frog.position[0] + game.speed

        elif wayPlataform == "left":
            frog.position[0] = frog.position[0] - game.speed


def frogArrived(frog, chegaram, game):
    if frog.position[0] > 33 and frog.position[0] < 53:
        position_init = [43, 7]
        createArrived(frog, chegaram, game, position_init)

    elif frog.position[0] > 115 and frog.position[0] < 135:
        position_init = [125, 7]
        createArrived(frog, chegaram, game, position_init)

    elif frog.position[0] > 197 and frog.position[0] < 217:
        position_init = [207, 7]
        createArrived(frog, chegaram, game, position_init)

    elif frog.position[0] > 279 and frog.position[0] < 299:
        position_init = [289, 7]
        createArrived(frog, chegaram, game, position_init)

    elif frog.position[0] > 361 and frog.position[0] < 381:
        position_init = [371, 7]
        createArrived(frog, chegaram, game, position_init)

    else:
        frog.position[1] = 46
        frog.animation_counter = 0
        frog.animation_tick = 1
        frog.can_move = 1
        lista.__delitem__(0)


def whereIsTheFrog(frog):
    # Se o sapo ainda nao passou da estrada
    if frog.position[1] > 240 :
        frogOnTheStreet(frog, enemys, game)

    # Se o sapo chegou no rio
    elif frog.position[1] < 240 and frog.position[1] > 40:
        frogInTheLake(frog, plataforms, game)

    # sapo chegou no objetivo
    elif frog.position[1] < 40 :
        frogArrived(frog, chegaram, game)


def createArrived(frog, chegaram, game, position_init):
    sapo_chegou = Object(position_init, sprite_arrived)
    chegaram.append(sapo_chegou)
    for i in range (len(faltam)):
        if faltam[i] == position_init[0]:
            faltam.__delitem__(i)
            break

    chegou_sound.play()
    frog.setPositionToInitialPosition()
    game.incPoints(10 + game.time)
    game.resetTime()
    frog.animation_counter = 0
    frog.animation_tick = 1
    frog.can_move = 1
    lista.__delitem__(0)


def nextLevel(chegaram, enemys, plataforms, frog, game):
    if len(chegaram) == 5:
        chegaram[:] = []
        faltam[:] = [43, 125, 207, 289, 371]
        frog.setPositionToInitialPosition()
        game.incLevel()
        game.incSpeed()
        game.incPoints(100)
        game.resetTime()


# trilha_sound.play(-1)
text_info = menu_font.render(('Press any button to start!'), 1, (0, 0, 0))
gameInit = 0

while gameInit == 0:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        
        if event.type == KEYDOWN:
            #---------------------------- if pygame.key.name(event.key) == "up":
            gameInit = 1


    screen.blit(background, (0, 0))
    screen.blit(text_info, (80, 150))
    pygame.display.update()

mortes = [0, 0]

while True:
    gameInit = 1
    game = Game(3, 1)
    key_up = 1
    frog_initial_position = [207, 475]
    frog = Frog(frog_initial_position, sprite_sapo)

    enemys = []
    plataforms = []
    chegaram = []
    faltam = [43, 125, 207, 289, 371]
    # 30 ticks == 1 segundo
    # ticks_enemys = [120, 90, 120, 90, 150]
    # ticks_plataforms = [90, 90, 120, 120, 60]
    ticks_enemys = [30, 0, 30, 0, 60]
    ticks_plataforms = [0, 0, 30, 30, 30]
    ticks_time = 30
    pressed_keys = 0
    key_pressed = 0

    while frog.lives > 0:
        if len(lista) > 1:
            print "deu merda, lista maior: ", len(lista)
            break
        if len(lista) == 0:
            frog.mybehaviour.run()
        else:
            key_pressed = lista[0]
            frog.moveFrog(key_pressed, key_up)
            frog.cannotMove()
            
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            if event.type == KEYUP:
                key_up = 1
                
            #===================================================================
            # if event.type == KEYDOWN:
            #    if key_up == 1 and frog.can_move == 1 :
            #         key_pressed = pygame.key.name(event.key)
            #         frog.moveFrog(key_pressed, key_up)
            #         frog.cannotMove()
            #===================================================================
            
        if not ticks_time:
            ticks_time = 30
            game.decTime()
        else:
            ticks_time -= 1

        if game.time == 0:
            frog.frogDead(game)

        createEnemys(ticks_enemys, enemys, game)
        createPlataform(ticks_plataforms, plataforms, game)

        moveList(enemys, game.speed)
        moveList(plataforms, game.speed)

        whereIsTheFrog(frog)

        nextLevel(chegaram, enemys, plataforms, frog, game)

        text_info1 = info_font.render(('Level: {0}               Points: {1}'.format(game.level, game.points)), 1, (255, 255, 255))
        text_info2 = info_font.render(('Time: {0}           Lifes: {1}'.format(game.time, frog.lives)), 1, (255, 255, 255))
        screen.blit(background, (0, 0))
        screen.blit(text_info1, (10, 520))
        screen.blit(text_info2, (250, 520))

        #=======================================================================
        # random = Random.randint(0,100)
        # if(random % 100 == 0):
        #     carChangeRoad(enemys)
        #=======================================================================

        drawList(enemys)
        drawList(plataforms)
        drawList(chegaram)
        
        frog.animateFrog(key_pressed, key_up)
        frog.draw()

        destroyEnemys(enemys)
        destroyPlataforms(plataforms)

        pygame.display.update()
        time_passed = clock.tick(30)

    print mortes
    mortes[:] = [0, 0]
    while gameInit == 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                gameInit = 0

        screen.blit(background, (0, 0))
        text = game_font.render('GAME OVER', 1, (255, 0, 0))
        text_points = game_font.render(('Pontuacao: {0}'.format(game.points)), 1, (255, 0, 0))
        text_reiniciar = info_font.render('Pressione qualquer tecla para reiniciar!', 1, (255, 0, 0))
        screen.blit(text, (75, 120))
        screen.blit(text_points, (10, 170))
        screen.blit(text_reiniciar, (70, 250))

        pygame.display.update()
