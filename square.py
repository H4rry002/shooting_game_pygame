import pygame
import math
import random

pygame.init()
pygame.font.init()
window = (1280,720)
black = (0,0,0)
white = (255,255,255)
blue = (51, 133, 255)
red = (253, 41, 40)
grey = (77, 77, 77 )
green = (46, 218, 34)
yellow = (229, 226, 19)
orange = (252, 129, 0 )
red_health = (243, 39, 2)
en_yellow = (255, 195, 0)
en_white = (186, 224, 45)

surface = pygame.display.set_mode(window)
font = pygame.font.SysFont('Comic Sans MS', 30)
size_player = 25
size_enemy = 20
size_bullet = 8
image = pygame.image.load('background.jpg')
image = pygame.transform.scale(image,(1280,720))

class Square:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.health = 100
    
    def player(self):
        pygame.draw.rect(surface,blue,(self.x ,self.y,size_player,size_player))

class Bullet:
    def __init__(self,x,y,mouse_x,mouse_y,velocity,color):
        self.x = x
        self.y = y
        self.mx = mouse_x + random.randint(0,100)/5
        self.my = mouse_y + random.randint(0,100)/5
        x_diff = self.mx - self.x
        y_diff = self.my - self.y
        angle = math.atan2(y_diff, x_diff)
        self.velocity = velocity
        self.changeX = math.cos(angle) * velocity
        self.changeY = math.sin(angle) * velocity
        self.color = color

    def update(self):
        self.x += self.changeX
        self.y += self.changeY
        if not 0 < self.x < window[0] or not 0 < self.y < window[1]:
             return False
        return True
    
    def draw(self):
        pygame.draw.rect(surface,self.color,(self.x,self.y,size_bullet,size_bullet))


class Enemy:
    def __init__(self):
        ######### RANDOM FUNCTION SET FROM WHERE THE ENEMY WILL ENTER UP DOWN LEFT RIGHT ###########
        if bool(random.getrandbits(1)):
            if bool(random.getrandbits(1)):
                self.x = 0
            else:
                self.x = window[0] + size_enemy
            self.y = random.randint(0,window[1]+ size_enemy)    
        else:
            if bool(random.getrandbits(1)):
                self.y = window[1] + size_enemy
            else: 
                self.y = 0
            self.x = random.randint(0,window[0]+ size_enemy)
        ####### LIST OF BULLETS OF ENEMY ##########
        self.b = []
        self.color = red
        self.health = 100
        self.velocity = -1
    ############ UPDATE THE VALUE OF ENEMY POSITION HAS THE POSITION OF PLAYER CHANGES#######
    def update(self,x,y):
        col = Collision()
        x_diff = self.x  - x
        y_diff = self.y - y
        angle = math.atan2(y_diff, x_diff)
        moveX = math.cos(angle) * self.velocity
        moveY = math.sin(angle) * self.velocity
        mX = moveX + self.x
        mY = moveY + self.y
        ########### CHECK FOR THE COLLISION OF ENEMY AND WALLS ################
        if moveX < 0 and moveY < 0:                                                 
            for i,j in walls.items():
                if col.collide(mX-3,mY,walls[i][0],walls[i][1],size_enemy,walls[i][2],walls[i][3],'left'):
                    moveX = 0
                    moveY *= 10
                elif col.collide(mX,mY-3,walls[i][0],walls[i][1],size_enemy,walls[i][2],walls[i][3],'up'):
                    moveY = 0
                    moveX *= 10 
        elif moveX > 0 and moveY < 0:
            for i,j in walls.items():
                if col.collide(self.x+3,self.y,walls[i][0],walls[i][1],size_enemy,walls[i][2],walls[i][3],'right'):
                    moveX = 0
                    moveY *= 10.0
                elif col.collide(self.x,self.y-3,walls[i][0],walls[i][1],size_enemy,walls[i][2],walls[i][3],'up'):
                    moveY = 0
                    moveX *= 10
        elif moveX > 0 and moveY > 0:
            for i,j in walls.items():
                if col.collide(self.x+3,self.y,walls[i][0],walls[i][1],size_enemy,walls[i][2],walls[i][3],'right'):
                    moveX = 0
                    moveY *= 10
                elif col.collide(self.x,self.y+3,walls[i][0],walls[i][1],size_enemy,walls[i][2],walls[i][3],'down'):
                    moveY = 0
                    moveX *= 10
        elif moveX < 0 and moveY > 0:
            for i,j in walls.items():
                if col.collide(self.x-3,self.y,walls[i][0],walls[i][1],size_enemy,walls[i][2],walls[i][3],'left'):
                    moveX = 0
                    moveY *= 10
                elif col.collide(self.x,self.y+3,walls[i][0],walls[i][1],size_enemy,walls[i][2],walls[i][3],'down'):
                    moveY = 0
                    moveX *= 10
        self.x += moveX
        self.y += moveY
        ####### CHECK IF THE BULLET HIT THE WINDOW ######
        for i in self.b:
            if not i.update():
                self.b.remove(i)
            i.draw()


    def draw(self):
        pygame.draw.rect(surface,self.color,(self.x,self.y,size_enemy,size_enemy))


############# COORDINATES OF WALLS ##############
walls = {
    'wall1': (100,130,200,100),
    'wall2': (100,320,200,300),
    'wall3': (500,575,200,200),
    'wall5': (550,250,450,125),
    'wall6': (850,330,150,400),
    'wall7': (400,60,800,120)
    
}
########### DRAW WALL ###########
def draw_wall():
    for i,j in walls.items():
        pygame.draw.rect(surface,black,(walls[i][0],walls[i][1],walls[i][2],walls[i][3]))


class Collision:
    ########## IF ENEMY OR PLAYER COLIDED WITH BULLET ##############
    def bullet_square(self,x1,y1,x2,y2,size1,size2):
        if x2 < x1 < x2 + size2 and y2 < y1 < y2 + size2:
            return True
        return False

    ######## IF BULLET COLIDED WITH WALL ######
    def wall_bullet(self,x1,y1,x2,y2,size1,size2,size3):
        if x2 < x1 < x2 + size2 and y2 < y1 < y2 + size3:
            return True
        return False


    ############## PLAYER AND ENEMY COLIDED WITH WALL ############
    def collide(self,playerX, playerY, wallX, wallY,size_player,length_wall,height_wall,direction):
        if direction == 'left':
            if wallX < playerX < wallX + length_wall and wallY < playerY < wallY + height_wall:
                return True
            if wallX < playerX < wallX + length_wall and wallY < playerY + size_player < wallY + height_wall:
                return True


        elif direction == 'right':
            if wallX < playerX + size_player< wallX + length_wall and wallY < playerY < wallY + height_wall:
                return True
            if wallX < playerX + size_player < wallX + length_wall and wallY < playerY + size_player < wallY + height_wall:
                return True


        elif direction == "up":
            if wallX < playerX< wallX + length_wall and wallY < playerY < wallY + height_wall:
                return True
            if wallX < playerX + size_player< wallX + length_wall and wallY < playerY < wallY + height_wall:
                return True


        elif direction == "down":
            if wallX < playerX < wallX + length_wall and wallY < playerY + size_player < wallY + height_wall:
                return True
            if wallX < playerX + size_player < wallX + length_wall and wallY < playerY + size_player< wallY + height_wall:
                return True
                
        return False
    
    ######## COLISION BETWEEN THE PLAYER AND ENEMY #########
    def player_enemy(self,x1,y1,x2,y2):
        if x2 < x1 < x2+size_player and y2 < y1 < y2 + size_player:
            return True
        elif x2 < x1 + size_enemy < x2 + size_player and y2 < y1 < y2 + size_player:
            return True
        elif x2 < x1 < x2 + size_player and y2 < y1 + size_enemy < y2 + size_player:
            return True
        elif x2 < x1 + size_enemy < x2 + size_player and y2 < y1 + size_enemy < y2 + size_player:
            return True
        return False
            
########### PROGRESS BAR #########
def progress(health):
    color = green
    if health <= 0:
        health = 0
    x = (health * 140 ) / 100
    pygame.draw.rect(surface,black,(30,30,145,25))
    if  50 <= health < 80:
        color = yellow
    elif 30 <= health <50:
        color = orange
    elif health < 30:
        color = red_health
    pygame.draw.rect(surface,color,(32,32,x,20))


def main():
    score = 0                       #Your score
    noenemy = 3                     # No of enemy (increase according to the score)
    sec_move = 1                    # if the player doesn't move for too long (The health will keep on decreasing)
    square = Square(400,300)        # Player class
    player_bullets = []             # list of class bullet stored as object (player)   
    enemy_bullets = []              # list of class bullet stored as object (enemy)
    running = True                  # Game doesn't end till you die or game is closed
    enemy = []                      # list of class Enemy stored as object  
    enemy_bullet_velocity = 3       # speed of enemy bullet (increase with score)
    player_velocity = 5             # movement speed of the player
    no_bullet = 60                  # frame % No of enemy bullet and random function decided to release a bullet from the enemy (increase with score) lower the value more the bullets
    collision = Collision()         # class has all the collision function
    clock = pygame.time.Clock()     # to increase the fps to 60
    FPS = 60                        # Frame per second
    frame = 0                       # frame used in enemy bullets and to increase the player health by 1 per 60 frame
    while running:
        frame += 1
        clock.tick(FPS)
        surface.blit(image,(0,0))
        draw_wall()

        # Game close if You click close button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        press = False               # this will check if player doesn't move for too long it will decrease the health of the player

        #################### FIRE #####################
        if pygame.mouse.get_pressed()[0]: 
            mouse =pygame.mouse.get_pos()
            if frame % 3 == 0:
                bullet = Bullet(square.x+5,square.y+5,mouse[0],mouse[1],15,blue)
                player_bullets.append(bullet)

        ############### Movement of Player #####################
        move = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and square.x - player_velocity> 0:
            press = True
            for i,j in walls.items():
                if collision.collide(square.x-3,square.y,walls[i][0],walls[i][1],size_player,walls[i][2],walls[i][3],'left'):
                    move = False
            if move:          
                square.x -= player_velocity

        elif keys[pygame.K_d] and square.x + player_velocity< (window[0]-size_player):
            press = True
            for i,j in walls.items():
                if collision.collide(square.x+3,square.y,walls[i][0],walls[i][1],size_player,walls[i][2],walls[i][3],'right'):
                    move = False
            if move:        
                square.x += player_velocity
        elif keys[pygame.K_w] and square.y - player_velocity> 0:
            press = True
            for i,j in walls.items():
                if collision.collide(square.x,square.y-3,walls[i][0],walls[i][1],size_player,walls[i][2],walls[i][3],'up'):
                    move = False
            if move:
                square.y -= player_velocity
        elif keys[pygame.K_s] and square.y + player_velocity < window[1]- size_player:
            press = True
            for i,j in walls.items():
                if collision.collide(square.x,square.y+3,walls[i][0],walls[i][1],size_player,walls[i][2],walls[i][3],'down'):
                    move = False
            if move:
                square.y += player_velocity

        ########### Decrease the health if it doesn't move #######################
        if press:
            sec_move = 1
        else:
            sec_move += 1

        if sec_move % 400 == 0:
            square.health -= 20
        ################## DISPLAY PLAYER ON THE SCREEN #############################
        square.player()
        ####################### display the bullet on the screen ###############    
        for bullet in player_bullets:
            if not bullet.update():                 # if bullet collide with window remove that bullet from the list
                player_bullets.remove(bullet)
                continue
            for i,j in walls.items():               # This check if bullet collide with any walls then remove is
                if collision.wall_bullet(bullet.x,bullet.y,walls[i][0],walls[i][1],size_bullet,walls[i][2],walls[i][3]):
                    try:
                        player_bullets.remove(bullet)
                    except:
                        pass
                    break   
            for en in enemy:                        # check if bullet colided with any enemy
                if collision.bullet_square(bullet.x,bullet.y,en.x,en.y,size_bullet,size_enemy):
                    en.health -= 20
                    player_bullets.remove(bullet)
                    break
            bullet.draw()

        if len(enemy) < noenemy:         # create new enemy if one died
            enemy.append(Enemy())
        ######################## ENEMY #############################    
        for i in enemy:
            if collision.player_enemy(i.x,i.y,square.x,square.y):       # check if any enemy is colided with player
                enemy.remove(i)
                square.health -= 20                                     # decrease the health of player if colided
                continue
            if i.health <= 0:                                           # if the health of enemy is 0 then remove the enemy    
                score += 1                                              
                if score % 10 == 0 and noenemy <= 6:                    # increase the no of enemy if score increase by 30 every time
                    noenemy += 1
                if score % 20 == 0 and no_bullet > 20:                  # increase the no of bullets as score increase
                    no_bullet -= 10
                    i.velocity -= 1
                if enemy_bullet_velocity < 6 and score % 10 == 0:       # increase the velocity of bullets
                    enemy_bullet_velocity += 1
                if score % 40 == 0:                                     # increase the health of enemy as score increase
                    i.health += 20
                enemy.remove(i)
        
            if  60 < i.health <= 80:                                    # color of enemy changes as his health decrease
                i.color = orange 
            elif  40 < i.health <= 60:
                i.color = yellow
            elif 20 < i.health <= 40:
                i.color = en_yellow
            elif i.health <= 20:
                i.color = en_white

            if frame % no_bullet == 0 and bool(random.getrandbits(1)):  # No. of bullet enemy fire decided by random function ( per frame )
                enemy_bullets.append(Bullet(i.x,i.y,square.x,square.y,enemy_bullet_velocity,red))
            i.update(square.x,square.y)
            i.draw()


        #######################     ENEMY BULLET #####################
        for bullet in enemy_bullets:
            bullet_exist = True                     # IF BULLET GOT REMOVE DON'T RUN THE WHOLE LOOP
            for i,j  in walls.items():              # IF BULLET HIT ANY WALL REMOVE IT    
                if collision.wall_bullet(bullet.x,bullet.y,walls[i][0],walls[i][1],size_bullet,walls[i][2],walls[i][3]):
                    enemy_bullets.remove(bullet)
                    bullet_exist = False
                    break
            if not bullet_exist:
                continue
            ###### IF ENEMY BULLET HIT THE PLAYER REMOVE IT #########
            if collision.bullet_square(bullet.x,bullet.y,square.x,square.y,size_bullet,size_player):
                enemy_bullets.remove(bullet)
                square.health -= 10
            bullet.update()     # ELSE UPDATE AND DRAW THE BULLET ON THE SCREEN
            bullet.draw()

        ###### DRAW PROGRESS BAR #####
        progress(square.health)  

        ###### IF PLAYER HEALTH BECOME 0 STOP THE GAME ######
        if square.health <= 0:
            running = False
        ###### REMDER THE SCORE #######
        text = font.render('Score  '+str(score), False,grey)
        surface.blit(text,(1100,10))
        pygame.display.update()

        ####### RESET THE FAME AND  INCREASE THE HEALTH OF PLAYER ################
        if frame == 120:
            if square.health < 100:
                square.health += 1
            frame = 0
main()



