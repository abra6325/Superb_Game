import sys
import pygame
import math
import random
import time
import tkinter as tk
import pickle
import tkinter.messagebox as tm

win = "undecide"
condition = "normal"
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)
WHITE = (0, 0, 0)
lvlcount = 0
BLACK = (255, 255, 255)
done_1 = True
mode = 'normal'
face = 'u'
screenwidth = 1000
fire_time = 0
screenhigh = 700
random_list = [200, 600, 800]
try:
  with open("hiscore.txt","r") as f_obj:
    hiscore = f_obj.read()
except FileNotFoundError:
  pass

class Button(pygame.sprite.Sprite):
  def __init__(self,x,y,image):
    super().__init__()
    self.image = pygame.image.load(image)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y

  
class Player(pygame.sprite.Sprite):
  def __init__(self,ammo,health,x,y,w,h,enemy,wall):
    super().__init__()
    self.image=pygame.image.load("Player.png")

    self.rect = self.image.get_rect()
    self.rect.y = y
    self.score = 0
    self.rect.x = x
    self.ammo = ammo
    self.damage=5
    self.maxhealth = 30
    self.health = health
    self.ammo_from = 8
    self.moveright = False
    self.wall=wall
    self.moveleft = False
    self.moveup = False
    self.movedown = False
    self.enemy = enemy
    self.collide_time = 0
    
  def update(self):
    
    if self.health <=0:
      self.kill()
    if self.moveright:
      if self.rect.x<970:
        self.rect.x +=2
      pc1=pygame.sprite.spritecollide(self,self.wall,False)
      for ps1 in pc1:
        self.rect.x-=2
    if self.moveleft:
      if self.rect.x>15:
        self.rect.x-=2
      pc2=pygame.sprite.spritecollide(self,self.wall,False)
      for ps2 in pc2:
        self.rect.x+=2
    if self.moveup:
      if self.rect.y>10:
        self.rect.y-=2
      pc3=pygame.sprite.spritecollide(self,self.wall,False)
      for ps3 in pc3:
        self.rect.y+=2
    if self.movedown:
      if self.rect.y<670:
        self.rect.y+=2
      pc4=pygame.sprite.spritecollide(self,self.wall,False)
      for ps4 in pc4:
        self.rect.y-=2
    if (time.time() - self.collide_time)>1.5:
      self.image=pygame.image.load("player.png")
      enemy_hit = pygame.sprite.spritecollide(self,self.enemy,False)
      for enemy in enemy_hit:
        self.collide_time = time.time()
        self.health-=enemy.damage
    else:
      for i in range(1,50):

        self.image.fill((0,0,0))

    
    

class Ammonum(pygame.sprite.Sprite):
  def __init__(self,color=(255,255,255),size=48,font = "Arial",text='hello',x=0,y=0):
    super().__init__()
    self.value = str(text)
    self.color = color
    self.font = pygame.font.SysFont("Arial",40)
    self.x = x
    self.y = y
    self.prep(self.value)
  def prep(self,text):
    text = str(text)
    self.image = self.font.render(text,True,self.color)
    self.rect = self.image.get_rect()
    self.rect.x = self.x
    self.rect.y = self.y
  
class Enemy(pygame.sprite.Sprite):
  def __init__(self,x,y,player,bullet,bullet_list,player_list,enemy_bullet_list,wall):
    super().__init__()
    self.image = pygame.image.load("Enemy.png")

    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.damage = 5
    self.player = player
    self.player_list = player_list
    self.bullet_list = bullet_list
    self.my_bullet_list = enemy_bullet_list
    self.health = 10
    self.clock = pygame.time.Clock()
    self.face = 'u'
    self.wall=wall
  def update(self):
    dire = random.randint(1,4)
    
    self.clock.tick(80)
    
    
    
    if dire == 1:
      self.face = 'u'
      for i in range(10):
        
        if self.rect.y>10:

          self.rect.y-=1
        ec1 = pygame.sprite.spritecollide(self,self.wall,False)
        for wall_single in ec1:
          self.rect.y+=i

    elif dire == 2:
      self.face = 'd'
      for i in range(10):
        if self.rect.y<670:
        
          self.rect.y+=1
        ec1 = pygame.sprite.spritecollide(self,self.wall,False)
        for wall_single in ec1:
          self.rect.y-=i
    elif dire == 3:
      self.face = 'r'
      for i in range(10):
        if self.rect.x<970:
        
          self.rect.x+=1
        ec1 = pygame.sprite.spritecollide(self,self.wall,False)
        for wall_single in ec1:
          self.rect.x-=i
    elif dire == 4:
      self.face = 'l'
      for i in range(10):
        if self.rect.x>15:
        
          self.rect.x-=1
        ec1 = pygame.sprite.spritecollide(self,self.wall,False)
        for wall_single in ec1:
          self.rect.x+=i
    if self.health <= 0:


      player.ammo+=player.ammo_from

      player.score += 1
      self.kill()

    bullet_hit = pygame.sprite.spritecollide(self, self.bullet_list, False)
    for bullet_single in bullet_hit:
      if bullet_single.face == 'u':
        self.bullet = Bullet('d', self.rect.x, self.rect.y, self.player_list, 5,self.wall)
        self.my_bullet_list.add(self.bullet)

      elif bullet_single.face == 'd':
        self.bullet = Bullet('u', self.rect.x, self.rect.y, self.player_list, 10,self.wall)
        self.my_bullet_list.add(self.bullet)
      elif bullet_single.face == 'r':
        self.bullet = Bullet('l', self.rect.x, self.rect.y, self.player_list, 10,self.wall)
        self.my_bullet_list.add(self.bullet)
      elif bullet_single.face == 'l':
        self.bullet = Bullet('r', self.rect.x, self.rect.y, self.player_list, 10,self.wall)
        self.my_bullet_list.add(self.bullet)

class Bullet2(pygame.sprite.Sprite):
  def __init__(self, x, y, base_speed, speed_x, speed_y,enemy,wall):
    # call the parent class (Sprite) constructor
    pygame.sprite.Sprite.__init__(self)
    # load image or generate image
    self.image = pygame.Surface([5, 5])
    self.image.fill(BLACK)
    self.damage=10
    # initialize rect/hitbox
    self.rect = self.image.get_rect()
    # handle misc variables
    self.rect.centerx = x
    self.rect.centery = y
    self.base_speed = base_speed
    self.speed_x = base_speed * speed_x
    self.speed_y = base_speed * speed_y
    self.enemy=enemy
    self.wall=wall
  # update - mandatory
  def update(self):
    self.rect.x += self.speed_x
    self.rect.y += self.speed_y
    enemy_hit = pygame.sprite.spritecollide(self, self.enemy, False)
    for enemy in enemy_hit:
      enemy.health -= self.damage
      self.kill()
    if self.rect.x >= 1000 or self.rect.x <= 0 or self.rect.y >= 700 or self.rect.y <= 0:
      self.kill()
    wall_hit=pygame.sprite.spritecollide(self,self.wall,False)
    for wall_single in wall_hit:
      self.kill()



class Boss(pygame.sprite.Sprite):

  def __init__(self,enemy,bossbullet,wall):

    pygame.sprite.Sprite.__init__(self)
    self.enemy=enemy
    self.bullet_list=bossbullet
    self.image = pygame.image.load("Boss.png")

    self.rect = self.image.get_rect()
    self.win=False
    self.clock=pygame.time.Clock()
    self.rect.x = random.randint(0, screenwidth)
    self.rect.y = random.randint(0, screenhigh)
    self.damage=15
    self.x_spd, self.x_curr_spd = 5, 0
    self.y_spd, self.y_curr_spd = 5, 0
    self.health=100
    self.shootlast = pygame.time.get_ticks()
    self.movelast = pygame.time.get_ticks()
    self.shootcooldown = 200
    self.mvcooldown = 20
    self.speed = 5
    self.wall=wall

  def update(self):

    now = pygame.time.get_ticks()
    if now - self.shootlast >= self.shootcooldown:
      self.shootlast = now

      self.shoot()

    if now - self.movelast >= self.mvcooldown:
      self.movelast = now

      self.handle_movement()
    if self.health<=0:
      self.win=True
      self.kill()



  def shoot(self):
    p_x, p_y = self.get_pos()

    for i in range(0, 360, 30):
      rad = math.radians(i)
      c = 10

      temp = c / math.sin(math.radians(90))
      a = temp * math.sin(rad)
      b = temp * math.sin(math.radians(90 - i))

      bull = Bullet2(p_x, p_y, 1, a, b,self.enemy,self.wall)
      self.bullet_list.add(bull)



  def handle_movement(self):
    dire = random.randint(1, 4)

    self.clock.tick(80)

    if dire == 1:
      self.face = 'u'
      for i in range(7):

        if self.rect.y > 10:
          self.rect.y -= 1
    elif dire == 2:
      self.face = 'd'
      for i in range(7):
        if self.rect.y < 670:
          self.rect.y += 1
    elif dire == 3:
      self.face = 'r'
      for i in range(7):
        if self.rect.x < 970:
          self.rect.x += 1
    elif dire == 4:
      self.face = 'l'
      for i in range(7):
        if self.rect.x > 15:
          self.rect.x -= 1

  def get_pos(self):
    return self.rect.centerx, self.rect.centery


class Bullet(pygame.sprite.Sprite):
  def __init__(self,face,x,y,enemy,damage,wall):
    super().__init__()
    self.enemy = enemy
    self.face = face
    self.reloadspeed = 0.8
    self.movespeed = 9
    self.damage = damage
    self.image = pygame.image.load("Bullet.png")

    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.wall=wall
    self.fire_time = 0
  def update(self):
    
      
    if self.face == 'u':
      self.rect.y -= self.movespeed
    elif self.face == 'd':
      self.rect.y += self.movespeed
    elif self.face =='r':
      self.rect.x += self.movespeed
    elif self.face == 'l':
      self.rect.x -= self.movespeed
    enemy_hit = pygame.sprite.spritecollide(self,self.enemy,False)
    for enemy in enemy_hit:
            
      enemy.health -= self.damage
      self.kill()
    if self.rect.x >= 1000 or self.rect.x <=0 or self.rect.y >=700 or self.rect.y <=0:
      self.kill()
    wall_hit=pygame.sprite.spritecollide(self,self.wall,False)
    for wall_single in wall_hit:
      self.kill()
class Upgrade1(pygame.sprite.Sprite):
  def __init__(self,color=(255,0,255),size=48,font = None,text='hello',random_list=0,player=0):
    super().__init__()
    self.value = str(text)
    self.color = color
    self.font = pygame.font.SysFont("Arial",30)
    self.x = 200
    self.complete = False
    self.y = 350
    self.player=player
    self.prep(self.value)
  def prep(self,text):
    text = str(text)
    self.image = self.font.render(text,True,self.color)
    self.rect = self.image.get_rect()
    self.rect.x = self.x
    self.rect.y = self.y
    player_hit = pygame.sprite.spritecollide(self,self.player,False)
    for player in player_hit:
      player.damage+=5
      self.complete = True

class Upgrade2(pygame.sprite.Sprite):
  def __init__(self, color=(255, 0, 255), size=48, font=None, text='hello', random_list=0,player=0):
    super().__init__()
    self.value = str(text)
    self.color = color
    self.font = pygame.font.SysFont("Arial", 30)
    self.x = 600
    self.complete = False
    self.y = 350
    self.player = player
    self.prep(self.value)

  def prep(self, text):
    text = str(text)
    self.image = self.font.render(text, True, self.color)
    self.rect = self.image.get_rect()
    self.rect.x = self.x
    self.rect.y = self.y
    player_hit = pygame.sprite.spritecollide(self,self.player,False)
    for player in player_hit:
      player.ammo_from+=5
      self.complete = True

class Upgrade3(pygame.sprite.Sprite):
  def __init__(self, color=(255, 0, 255), size=48, font=None, text='hello', random_list=0,player=0):
    super().__init__()
    self.value = str(text)
    self.color = color
    self.font = pygame.font.SysFont("Arial", 30)
    self.x = 800
    self.complete=False
    self.y = 350
    self.player = player
    self.prep(self.value)

  def prep(self, text):
    text = str(text)
    self.image = self.font.render(text, True, self.color)
    self.rect = self.image.get_rect()
    self.rect.x = self.x
    self.rect.y = self.y
    player_hit = pygame.sprite.spritecollide(self,self.player,False)
    for player in player_hit:
      player.maxhealth+=5
      self.complete = True
class Wall(pygame.sprite.Sprite):# A wall
  def __init__(self,w,h,x,y):
    super().__init__()
    self.image=pygame.Surface([w,h])
    self.image.fill(GRAY)
    self.rect=self.image.get_rect()
    self.rect.x=x
    self.rect.y=y







def main_script():
  win = "undecide"
  condition = "normal"
  RED = (255, 0, 0)
  GREEN = (0, 255, 0)
  BLUE = (0, 0, 255)
  GRAY = (169, 169, 169)
  WHITE = (0, 0, 0)
  lvlcount = 0
  BLACK = (255, 255, 255)
  done_1 = True
  mode = 'normal'
  face = 'u'
  screenwidth = 1000
  fire_time = 0
  screenhigh = 700
  random_list = [200, 600, 800]
  pygame.init()
  screen = pygame.display.set_mode((screenwidth, screenhigh))
  pygame.display.set_caption('Superb Game')
  pygame.display.set_icon(pygame.image.load("ico/icon.ico"))
  clock = pygame.time.Clock()
  run = True
  run3 = False
  try:
    button = Button(450,350,"start_button.png")
    button_normal = Button(450,500,"normal_start.png")
  except:
    pass
  text_start = Ammonum(text="Superb Game",x=425,y=100)
  try:
    text_hiscore = Ammonum(text="high score: "+str(hiscore),x=400,y=150)
  except:
    pass
  button_list = pygame.sprite.Group()
  text_list1 = pygame.sprite.Group()
  button_list.add(button)
  button_list.add(button_normal)
  text_list1.add(text_start)
  try:
    text_list1.add(text_hiscore)
  except:
    pass

  run2 = True
  try:
    while run2:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False
          run2 = False
        if event.type == pygame.MOUSEBUTTONDOWN:
          if pygame.mouse.get_pressed()[0]:
            mousex,mousey = pygame.mouse.get_pos()
            if button.rect.collidepoint(mousex,mousey):
              button.kill()
              button_normal.kill()
              text_start.kill()
              mode = "endless"
              run2 = False
            elif button_normal.rect.collidepoint(mousex,mousey):
              button.kill()
              button_normal.kill()
              text_start.kill()
              mode = "normal"
              run2 = False
      screen.fill(BLUE)
      button_list.draw(screen)
      text_list1.draw(screen)
      pygame.display.flip()
      clock.tick(60)
  except:
    pass
  all_sprite = pygame.sprite.Group()
  text_list = pygame.sprite.Group()
  enemy_group = pygame.sprite.Group()
  player_list = pygame.sprite.Group()
  upgrade_group = pygame.sprite.Group()
  bullet_list = pygame.sprite.Group()
  enemy_bullet_list = pygame.sprite.Group()
  wall_list=pygame.sprite.Group()
  player = Player(12,30,500,350,20,20,enemy_group,wall_list)
  player_list.add(player)
  ammonum = Ammonum(color = (255,255,255),size = 48,text = "ammo: "+str(player.ammo),x = 50,y = 20)
  mode_text = Ammonum(color = (0,255,255),size = 48, text = "mode: " +mode, x = 410, y = 20)
  health_text = Ammonum(color =(255,255,255),size = 48,text = "health:"+str(player.health)+"/"+str(player.maxhealth),x=50,y=50)
  text_list.add(ammonum)
  text_list.add(health_text)
  text_list.add(mode_text)
  boss_list = pygame.sprite.Group()
  bullet_list1=pygame.sprite.Group()

  if mode == "endless":
    score_text = Ammonum(color = (255,0,255),size = 48, text = "score: " +str(player.score), x = 760, y = 20)
    text_list.add(score_text)
  for i in range(10):
    wallx = random.randint(15, 960)
    wally = random.randint(10, 660)
    enemyx=random.randint(15,960)
    enemyy=random.randint(10,660)

    wall=Wall(random.randint(10,50),random.randint(10,50),wallx,wally)
    wall_list.add(wall)
    while True:
      if enemyx!=wallx and enemyy!=wally and not wall.rect.collidepoint(enemyx,enemyy):
        enemy = Enemy(random.randint(15,960),random.randint(10,660),player,Bullet,bullet_list,player_list,enemy_bullet_list,wall_list)
        enemy_group.add(enemy)
        break
      else:
        enemyx = random.randint(15, 960)
        enemyy = random.randint(10, 660)
        continue




  while run:

    if player.health <= 0:

      win = False
      break
    if player.ammo <= 0 and len(bullet_list)== 0:
      condition = "ammo"
      win = False
      break

    elif len(enemy_group)<=0:
      if mode == 'normal':
        boss1= Boss(player_list,bullet_list1,wall_list)
        boss_list.add(boss1)
        enemy_group.add(boss1)
        player.ammo+=100
      elif mode == "endless":
        if done_1:
          upgrade1 = Upgrade1(text = "Damage",random_list= random_list,player=player_list)

          upgrade2 = Upgrade2(text = "Ammo",random_list= random_list,player=player_list)

          upgrade3 = Upgrade3(text = "MaxHP",random_list= random_list,player=player_list)


          upgrade_group.add(upgrade1)
          upgrade_group.add(upgrade2)
          upgrade_group.add(upgrade3)
          upgrade1.prep("Damage")
          upgrade2.prep("Ammo")
          upgrade3.prep("MaxHP")

          done_1=False
          player.rect.x=500
          player.rect.y=500


        upgrade1.prep("Damage")
        upgrade2.prep("Ammo")
        upgrade3.prep("MaxHP")


        if upgrade1.complete or upgrade2.complete or upgrade3.complete:
          upgrade1.kill()
          upgrade2.kill()
          upgrade3.kill()
          lvlcount+=1
          if lvlcount >=5:
            boss1=Boss(player_list,bullet_list1,wall_list)
            boss_list.add(boss1)
            enemy_group.add(boss1)
            lvlcount=0
          else:
            for i in range(10):
              wallx = random.randint(15, 960)
              wally = random.randint(10, 660)
              enemyx = random.randint(15, 960)
              enemyy = random.randint(10, 660)

              wall = Wall(random.randint(10, 50), random.randint(10, 50), wallx, wally)
              wall_list.add(wall)
              while True:
                if enemyx != wallx and enemyy != wally and not wall.rect.collidepoint(enemyx, enemyy):
                  enemy = Enemy(random.randint(15, 960), random.randint(10, 660), player, Bullet, bullet_list,
                                player_list, enemy_bullet_list, wall_list)
                  enemy_group.add(enemy)
                  break
                else:
                  enemyx = random.randint(15, 960)
                  enemyy = random.randint(10, 660)
                  continue
          if player.health <= player.maxhealth-5:
            player.health+=5
          elif player.health <=player.maxhealth and player.health > player.maxhealth-5:
            player.health=player.maxhealth


          continue

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
          player.moveup = True
          face = 'u'
        elif event.key == pygame.K_s:
          player.movedown = True
          face = 'd'
        elif event.key == pygame.K_a:
          player.moveleft = True
          face = 'l'
        elif event.key == pygame.K_d:
          player.moveright = True
          face = 'r'
        if event.key == pygame.K_SPACE:

          if (time.time()-fire_time) > 0.1 and player.ammo > 0:
            player.ammo-=1

            bullet = Bullet(face,player.rect.x,player.rect.y,enemy_group,player.damage,wall_list)

            bullet_list.add(bullet)
            fire_time = time.time()


      elif event.type == pygame.KEYUP:
        if event.key == pygame.K_w:
          player.moveup = False
        elif event.key == pygame.K_s:
          player.movedown = False
        elif event.key == pygame.K_a:
          player.moveleft = False
        elif event.key == pygame.K_d:
          player.moveright = False

    screen.fill(BLUE)
    all_sprite.update()
    player.update()
    ammonum.prep("ammo: "+str(player.ammo))
    health_text.prep("health:"+str(player.health)+"/"+str(player.maxhealth))
    if mode == "endless":
      score_text.prep("score: "+str(player.score))
    if len(boss_list)>=1:
      if boss1.win:
        win=True
        run=False
    wall_list.draw(screen)
    wall_list.update()
    bullet_list.draw(screen)
    bullet_list.update()
    bullet_list1.draw(screen)
    bullet_list1.update()
    boss_list.draw(screen)
    boss_list.update()
    text_list.draw(screen)
    text_list.update()
    enemy_group.draw(screen)
    upgrade_group.draw(screen)
    upgrade_group.update()

    player_list.draw(screen)
    player_list.update()

    all_sprite.draw(screen)
    enemy_group.update()
    enemy_bullet_list.draw(screen)
    enemy_bullet_list.update()
    pygame.display.flip()
    
    clock.tick(80)


  pygame.quit()
  if win == "undecide":
    msg=False
  elif win:
    root = tk.Tk()
    root.withdraw()
    if mode == "normal":
      msg = tm.askretrycancel("Win","You win, Retry?")
    elif mode == "endless":
      msg = tm.askretrycancel("Win", "You Won(score: "+str(player.score)+")")
    root.wm_deiconify()
    root.destroy()
    root.mainloop()
  elif not win:
    root = tk.Tk()
    root.withdraw()
    if mode == "normal":
      if condition == "normal":
        msg = tm.askretrycancel("Loose","You Lost")
      elif condition == "ammo":
        msg = tm.askretrycancel("Ran out of Ammo", "You Lost")
    elif mode == "endless":
      if condition == "normal":
        msg = tm.askretrycancel("Loose", "You Lost(score: "+str(player.score)+")")
      elif condition == "ammo":
        msg = tm.askretrycancel("Ran out of Ammo", "You Lost(score: " + str(player.score) + ")")



    root.wm_deiconify()
    root.destroy()
    root.mainloop()
  try:
    if player.score > int(hiscore):
      open_hi = open("hiscore.txt","w+")
      open_hi.write(str(player.score))
      open_hi.close()
  except:
    pass
  if msg==True:
    main_script()
if __name__ == '__main__':
    main_script()