import random

import wrap
import time
wrap.add_sprite_dir("img")

width = 800
height = 600
start = time.time()

points = 0


wrap.world.create_world(width,height)
bullet = None
sky = wrap.sprite.add("back",width/2,height/2-220,"sky")
ground = wrap.sprite.add("back",width/2,height/2+220,"images")
turrel = wrap.sprite.add("turrel",width/2,height/2+190,"turrel")
plane = wrap.sprite.add("cars", 100, random.randint(50, 300), "plane")
point = wrap.sprite.add_text(str(points),width-30,24,font_size=60)
wrap.sprite.set_size_percent(plane,50,50)
wrap.sprite.set_size_percent(turrel,50,50)
wrap.sprite.set_size_percent(ground,300,100)
wrap.sprite.set_angle(turrel,0)
@wrap.on_mouse_move()
def turrel_move(pos_x,pos_y):
    wrap.sprite.set_angle_to_point(turrel,pos_x,pos_y)


def boom(x,y):
    def_time = time.time()
    move_time = def_time - start
    if move_time >= 0.5:
        expl = wrap.sprite.add("battle_city_items", x, y, "effect_explosion1")
    if move_time >= 1:
        wrap.sprite.set_costume(expl, "effect_explosion2")
    if move_time >= 1.5:
        wrap.sprite.set_costume(expl, "effect_explosion3")
    if move_time >= 2:
        wrap.sprite.set_costume(expl, "effect_explosion2")
    if move_time >= 2.5:
        wrap.sprite.set_costume(expl, "effect_explosion1")
    if move_time >= 3:
        wrap.sprite.remove(expl)


@wrap.on_key_down(wrap.K_BACKSPACE)
def expl():
    boom(width/2,height/2)

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
        wrap.sprite.remove(bullet)
        bullet = None
        points +=1
        wrap.sprite_text.set_text(point,str(points))



@wrap.always(5)
def plane_move():
    wrap.sprite.move(plane, 2, 0)
    plane_x = wrap.sprite.get_x(plane)
    if plane_x >=width+100:
        wrap.sprite.move_to(plane,-100,random.randint(50, 300))


