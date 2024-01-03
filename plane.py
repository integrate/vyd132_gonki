import random

import wrap
import time
wrap.add_sprite_dir("img")

width = 800
height = 600
start = time.time()

bullet_speed = 5
bullet_speed_level = 0
lives = 100
points = 0
expl_time = 0
reload_speed = 3
s_level = 0
wawe = 0
gruz_enemies = 0
istrebitel_enemies = 0
big_plane_enemies = 0
time_wawe =0
gruz_enemie_hit=0
istrebitel_enemie_hit=0
big_plane_enemie_hit=0
time_wawe= 0


wrap.world.create_world(width,height)
bullet = None
expl = None

sky = wrap.sprite.add("back",width/2,height/2-220,"sky")
ground = wrap.sprite.add("back",width/2,height/2+220,"images")
turrel = wrap.sprite.add("turrel",width/2,height/2+190,"turrel")
coin = wrap.sprite.add("mario-items",width-60,24,"coin")
heart = wrap.sprite.add("back",width-130,80,"heart")
speed_button = wrap.sprite.add("back",width-40,height-70,"speed")
mouse = wrap.sprite.add("pacman",1,1,"dot",False)
wrench = wrap.sprite.add("back",60,height-70,"wrench")
plane_wawe = wrap.sprite.add("cars", 50, 40, "plane")
istribitel_wawe = wrap.sprite.add("cars", 50, 60, "istribitel")
bullet_level = wrap.sprite.add("turrel", width -195, height -80, "patron")
big_plane_wawe = wrap.sprite.add("cars", 50, 80, "big_plane")

point = wrap.sprite.add_text(str(points),width-30,24,font_size=60,text_color=[255,160,68])
heal = wrap.sprite.add_text(str(lives),width-50,80,font_size=60,text_color=[121,240,47])
level_speed = wrap.sprite.add_text(str(s_level),width-120,height-80,font_size=60,)
gruz_text = wrap.sprite.add_text(str(gruz_enemies),90,40,font_size=20,)
istribitel_text = wrap.sprite.add_text(str(istrebitel_enemies),90,60,font_size=20,)
big_plane_text = wrap.sprite.add_text(str(big_plane_enemies),90,80,font_size=20,)
bullet_text = wrap.sprite.add_text(str(bullet_speed_level),width-260,height-80,font_size=60,)
wawe_text = wrap.sprite.add_text("Волна номер: "+str(wawe),80,20,font_size=20,)

wrap.sprite.add_text("Перезарядка",width-70,height-140,font_size=20,)
wrap.sprite.add_text("Починка",60,height-140,font_size=20,)
wrap.sprite.add_text("Скрорость пули",width-220,height-140,font_size=20,)

wrap.sprite.set_angle(speed_button,45)
wrap.sprite.set_angle(turrel,0)
wrap.sprite.set_angle(bullet_level,30)

wrap.sprite.set_size(mouse,1,1)

wrap.sprite.set_size_percent(speed_button,10,10)
wrap.sprite.set_size_percent(plane_wawe,10,10)
wrap.sprite.set_size_percent(istribitel_wawe,2,2)
wrap.sprite.set_size_percent(big_plane_wawe,5,5)
wrap.sprite.set_size_percent(wrench,10,10)
wrap.sprite.set_size_percent(bullet_level,200,200)
wrap.sprite.set_size_percent(turrel,50,50)
wrap.sprite.set_size_percent(coin,150,150)
wrap.sprite.set_size_percent(heart,15,15)
wrap.sprite.set_size_percent(ground,300,100)


wrap.sprite.set_reverse_x(istribitel_wawe,True)
wrap.sprite.set_reverse_x(big_plane_wawe,True)

plane = None
istribitel=None
big_plane=None

@wrap.on_mouse_move()
def turrel_move(pos_x,pos_y):
    wrap.sprite.set_angle_to_point(turrel,pos_x,pos_y)


def boom(x,y):
    global expl_time,expl
    expl = wrap.sprite.add("battle_city_items", x, y, "effect_explosion1")
    expl_time = time.time()
    wrap.sprite.set_size_percent(expl,150,150)


@wrap.always()
def explosin():
    global expl,expl_time
    if expl == None:
        return
    def_time = time.time()
    anim_time = def_time-expl_time
    if anim_time >= 0.2:
        wrap.sprite.set_costume_next(expl)
        expl_time  = time.time()
        expl_costume= wrap.sprite.get_costume(expl)
        if expl_costume=="effect_explosion_big2":
            wrap.sprite.remove(expl)
            expl=None

@wrap.on_key_down(wrap.K_SPACE)
def fire():
    global start,bullet
    tur_angle = wrap.sprite.get_angle(turrel)
    def_time = time.time()
    move_time = def_time-start
    if move_time >=reload_speed:
        bullet = wrap.sprite.add("turrel", width / 2, height / 2 + 190, "patron")
        wrap.sprite.set_angle(bullet, tur_angle)
        wrap.sprite.move_at_angle_dir(bullet,92)
        start=time.time()

@wrap.always()
def mouse_move(pos_x,pos_y):
    wrap.sprite.move_to(mouse,pos_x,pos_y)

@wrap.on_mouse_down(wrap.BUTTON_LEFT)
def speed_upgrade(pos_x,pos_y):
    global s_level,reload_speed,points
    click = wrap.sprite.is_collide_sprite(mouse,speed_button)
    if s_level == 5:
        wrap.sprite_text.set_text(level_speed, "MAX")
        return
    if click == True and points >= 6:
        s_level+=1
        wrap.sprite_text.set_text(level_speed, str(s_level))
        reload_speed-=0.5
        points_check(-6)


@wrap.on_mouse_down(wrap.BUTTON_LEFT)
def repair(pos_x,pos_y):
    global points,lives
    click = wrap.sprite.is_collide_sprite(mouse,wrench)
    if click == True and points >= 10:
        lives_check(10)
        wrap.sprite_text.set_text(level_speed, str(s_level))
        points_check(-10)

@wrap.on_mouse_down(wrap.BUTTON_LEFT)
def bullet_speed_button():
    global bullet_speed,bullet_speed_level
    click = wrap.sprite.is_collide_sprite(mouse, bullet_speed)
    if bullet_speed_level == 5:
        wrap.sprite_text.set_text(level_speed, "MAX")
        return
    if click == True and points >= 6:
        bullet_speed_level += 1
        wrap.sprite_text.set_text(bullet_text, str(bullet_speed_level))
        bullet_speed += 0.5
        points_check(-6)


@wrap.always()
def wawes():
    global gruz_enemies,istrebitel_enemies,time_wawe,start,istribitel,big_plane,plane,big_plane_enemies
    if gruz_enemies == 0:
        wrap.sprite.remove(plane)
        plane=None
    if istrebitel_enemies == 0:
        wrap.sprite.remove(istribitel)
        istribitel=None
    if big_plane_enemies == 0:
        wrap.sprite.remove(big_plane)
        big_plane=None
    wawe_perexod(0, 0, 10, 0)
    wawe_perexod(1,5,10,0)
    wawe_perexod(2, 10, 10, 0)
    wawe_perexod(3,10,10,5)
    wawe_perexod(4,10,10,10)
    if big_plane_enemies == 0 and gruz_enemies == 0 and istrebitel_enemies == 0 and wawe == 5:
        wrap.sprite.add_text("YOU WIN",width,height,font_size=60)

def points_check(col):
    global points
    points+=col
    wrap.sprite_text.set_text(point, str(points))

def wawe_check(col):
    global wawe
    wawe+=col
    wrap.sprite_text.set_text(wawe_text,"Волна номер: " + str(wawe))

def wawe_perexod(old_wawe_number,gruz_enemies_col,istrebitel_enemies_col,big_plane_enemies_col):
    global start,plane,istribitel,big_plane,time_wawe
    if wawe != old_wawe_number:
        return
    if gruz_enemies>0 or istrebitel_enemies>0 or big_plane_enemies>0:
        return

    def_time = time.time()
    timer = def_time - start
    print(time_wawe)
    if timer < 1:
        return
    time_wawe += 1
    start = time.time()
    if time_wawe != 5:
        return
    if gruz_enemies_col >0:
        plane = wrap.sprite.add("cars", -500, random.randint(50, 300), "plane")
        wrap.sprite.set_size_percent(plane,50,50)
    if istrebitel_enemies_col>0:
        istribitel = wrap.sprite.add("cars", -500, random.randint(50, 300), "istribitel")
        wrap.sprite.set_size_percent(istribitel, 5, 5)
        wrap.sprite.set_reverse_x(istribitel,True)
    if big_plane_enemies_col>0:
        big_plane = wrap.sprite.add("cars", -500, random.randint(50, 300), "big_plane")
        wrap.sprite.set_size_percent(big_plane, 10, 10)
        wrap.sprite.set_reverse_x(big_plane, True)
    wawe_check(1)
    time_wawe=0
    gruz_check(gruz_enemies_col)
    istribitel_check(istrebitel_enemies_col)
    big_plane_check(big_plane_enemies_col)


def lives_check(col):
    global lives
    lives += col
    hp_check()
    wrap.sprite_text.set_text(heal, str(lives))

def gruz_check(col):
    global gruz_enemies
    gruz_enemies+=col
    wrap.sprite_text.set_text(gruz_text, str(gruz_enemies))

def istribitel_check(col):
    global istrebitel_enemies
    istrebitel_enemies+=col
    wrap.sprite_text.set_text(istribitel_text, str(istrebitel_enemies))

def big_plane_check(col):
    global big_plane_enemies
    big_plane_enemies+=col
    wrap.sprite_text.set_text(big_plane_text, str(big_plane_enemies))


def hp_check():
    if lives == 0:
        wrap.sprite.add_text("Game Over",width/2,height/2,font_size=100,)
    elif lives <= 25:
        wrap.sprite_text.set_text_color(heal, 255, 0, 0)
    elif lives <= 50:
        wrap.sprite_text.set_text_color(heal, 255, 144, 19)
    elif lives <= 75:
        wrap.sprite_text.set_text_color(heal,255,255,0)
    else:
        wrap.sprite_text.set_text_color(heal, 121,240,47)

def plane_home(sprite_id):
    wrap.sprite.move_to(sprite_id,-300,random.randint(50, 300))

def plane_hit(id,hp,enemie,points_give,enemie_hit):
    global points,point,bullet,plane,gruz_enemies,istrebitel_enemies,big_plane_enemies
    if bullet == None:
        return enemie_hit
    if id==None:
        return enemie_hit
    shot = wrap.sprite.is_collide_sprite(bullet, id)
    if shot != True:
        return enemie_hit
    enemie_hit+=1
    wrap.sprite.remove(bullet)
    bullet = None
    if enemie_hit == hp:
        plane_x = wrap.sprite.get_x(id)
        plane_y = wrap.sprite.get_y(id)
        boom(plane_x,plane_y)
        plane_home(id)
        enemie(-1)
        points_check(points_give)
        enemie_hit=0
    return enemie_hit


"""
если пули нет то
    прекращяем работу
двигаем пулю под углом на заданой скорости
если есть грузовой самолета
    проверяем попала ли пуля
    если пуля попала
        -1 одна жизнь у самолета
        если у него 0 жизней
            узнаем координаты
            удаляем пулю
            проигрываем анимацию взрыва
            возвращаем самолет за экран
            вычесляем количество грузовых самолетов в волне
            начисляем очки
тоже самое для истребителя и большого самолета 
"""

@wrap.always(10)
def bullet_move():
    global points,point,bullet,plane,gruz_enemies,enemy_hit,gruz_enemie_hit,istrebitel_enemie_hit,big_plane_enemie_hit
    if bullet == None:
        return
    wrap.sprite.move_at_angle_dir(bullet,bullet_speed)
    gruz_enemie_hit= plane_hit(plane,2,gruz_check,2,gruz_enemie_hit)
    istrebitel_enemie_hit= plane_hit(istribitel, 1,istribitel_check, 1,istrebitel_enemie_hit)
    big_plane_enemie_hit= plane_hit(big_plane, 3,big_plane_check, 3,big_plane_enemie_hit)




@wrap.always(10)
def plane_move():
    global lives,plane,gruz_enemies
    if plane==None:
        return
    wrap.sprite.move(plane, 2, 0)
    plane_x = wrap.sprite.get_x(plane)
    if plane_x >=width+100:
        plane_home(plane)
        lives_check(-2)
        gruz_check(-1)


@wrap.always(10)
def istribitel_move():
    global lives,plane,gruz_enemies,istribitel
    if istribitel==None:
        return
    wrap.sprite.move(istribitel, 2, 0)
    istribitel_x = wrap.sprite.get_x(istribitel)
    if istribitel_x >=width+100:
        plane_home(istribitel)
        lives_check(-1)
        istribitel_check(-1)

@wrap.always(10)
def big_plane_move():
    global lives,plane,gruz_enemies,big_plane
    if big_plane==None:
        return
    wrap.sprite.move(big_plane, 1, 0)
    big_plane_x = wrap.sprite.get_x(big_plane)
    if big_plane_x >=width+100:
        plane_home(big_plane)
        lives_check(-3)
        big_plane_check(-1)
