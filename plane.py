import random

import wrap
import time
wrap.add_sprite_dir("img")

width = 800
height = 600
start = time.time()

lives = 100
points = 0
expl_time = 0
reload_speed = 3
s_level = 0
wawe = 1
gruz_enemies = 10

wrap.world.create_world(width,height)
bullet = None
expl = None

sky = wrap.sprite.add("back",width/2,height/2-220,"sky")
ground = wrap.sprite.add("back",width/2,height/2+220,"images")
turrel = wrap.sprite.add("turrel",width/2,height/2+190,"turrel")
plane = wrap.sprite.add("cars", -500, random.randint(50, 300), "plane")
coin = wrap.sprite.add("mario-items",width-60,24,"coin")
point = wrap.sprite.add_text(str(points),width-30,24,font_size=60,text_color=[255,160,68])
heal = wrap.sprite.add_text(str(lives),width-50,80,font_size=60,text_color=[121,240,47])
heart = wrap.sprite.add("back",width-130,80,"heart")
speed_button = wrap.sprite.add("back",width-40,height-70,"speed")
wrap.sprite.add_text("Перезарядка",width-70,height-140,font_size=20,)
level_speed = wrap.sprite.add_text(str(s_level),width-120,height-80,font_size=60,)
mouse = wrap.sprite.add("pacman",1,1,"dot",False)
wrench = wrap.sprite.add("back",60,height-70,"wrench")
wrap.sprite.add_text("Волна номер: "+str(1),80,20,font_size=20,)
plane_wawe = wrap.sprite.add("cars", 50, 40, "plane")
gruz_text = wrap.sprite.add_text(str(gruz_enemies),90,40,font_size=20,)
wrap.sprite.add_text("Починка",60,height-140,font_size=20,)
wrap.sprite.set_size(mouse,1,1)
wrap.sprite.set_size_percent(speed_button,10,10)
wrap.sprite.set_angle(speed_button,45)
wrap.sprite.set_size_percent(plane,50,50)
wrap.sprite.set_size_percent(plane_wawe,10,10)
wrap.sprite.set_size_percent(wrench,10,10)
wrap.sprite.set_size_percent(turrel,50,50)
wrap.sprite.set_size_percent(coin,150,150)
wrap.sprite.set_size_percent(heart,15,15)
wrap.sprite.set_size_percent(ground,300,100)
wrap.sprite.set_angle(turrel,0)
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


def points_check(col):
    global points
    points+=col
    wrap.sprite_text.set_text(point, str(points))


def lives_check(col):
    global lives
    lives += col
    hp_check()
    wrap.sprite_text.set_text(heal, str(lives))

def gruz_check(col):
    global gruz_enemies
    gruz_enemies+=col
    wrap.sprite_text.set_text(gruz_text, str(gruz_enemies))


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





@wrap.always(10)
def points_get():
    global points,point,bullet,plane,gruz_enemies
    if bullet == None:
        return
    wrap.sprite.move_at_angle_dir(bullet,5)
    shot = wrap.sprite.is_collide_sprite(bullet,plane)
    if shot == True:
        plane_x = wrap.sprite.get_x(plane)
        plane_y = wrap.sprite.get_y(plane)
        wrap.sprite.remove(bullet)
        bullet = None
        boom(plane_x,plane_y)
        wrap.sprite.remove(plane)
        plane=None
        gruz_check(-1)
        points_check(1)



@wrap.always(5)
def plane_move():
    global lives,plane,gruz_enemies
    if plane==None:
        plane = wrap.sprite.add("cars", -200, random.randint(50, 300), "plane")
        wrap.sprite.set_size_percent(plane, 50, 50)
        return
    wrap.sprite.move(plane, 2, 0)
    plane_x = wrap.sprite.get_x(plane)
    if plane_x >=width+100:
        wrap.sprite.move_to(plane,-100,random.randint(50, 300))
        lives_check(-2)
        gruz_check(-1)



