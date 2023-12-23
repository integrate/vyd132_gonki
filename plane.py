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

wrap.world.create_world(width,height)
bullet = None
expl = None
sky = wrap.sprite.add("back",width/2,height/2-220,"sky")
ground = wrap.sprite.add("back",width/2,height/2+220,"images")
turrel = wrap.sprite.add("turrel",width/2,height/2+190,"turrel")
plane = wrap.sprite.add("cars", 100, random.randint(50, 300), "plane")
coin = wrap.sprite.add("mario-items",width-60,24,"coin")
point = wrap.sprite.add_text(str(points),width-30,24,font_size=60,text_color=[255,160,68])
heal = wrap.sprite.add_text(str(lives),width-50,80,font_size=60,text_color=[121,240,47])
hp = wrap.sprite.add("pacman",width-110,80,"item_strawberry")
wrap.sprite.set_size_percent(plane,50,50)
wrap.sprite.set_size_percent(turrel,50,50)
wrap.sprite.set_size_percent(coin,150,150)
wrap.sprite.set_size_percent(hp,150,150)
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
    if move_time >=3:
        bullet = wrap.sprite.add("turrel", width / 2, height / 2 + 190, "patron")
        wrap.sprite.set_angle(bullet, tur_angle)
        wrap.sprite.move_at_angle_dir(bullet,92)
        start=time.time()



@wrap.always(10)
def points_get():
    global points,point,bullet
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
        wrap.sprite.hide(plane)
        points +=1
        wrap.sprite_text.set_text(point,str(points))



@wrap.always(5)
def plane_move():
    wrap.sprite.move(plane, 2, 0)
    plane_x = wrap.sprite.get_x(plane)
    if plane_x >=width+100:
        wrap.sprite.move_to(plane,-100,random.randint(50, 300))
        wrap.sprite.show(plane)


