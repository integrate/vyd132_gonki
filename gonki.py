import wrap
import time
wrap.add_sprite_dir("img")

width = 600
height = 800

wrap.world.create_world(width,height)

start = time.time()
speed = -1

@wrap.on_key_always(wrap.K_UP,wrap.K_DOWN)
def player_move(keys):
    global start,speed
    if wrap.K_UP in keys:
        wrap.sprite.move(player, 0, speed)
        def_start = time.time()
        if def_start >= start+2:
            speed-=1
            start = time.time()

    if wrap.K_DOWN in keys:
        wrap.sprite.move(player,0,1)




road = wrap.sprite.add("back",width/2,height/2,"road")
wrap.sprite.set_size_percent(road,50,50)
player = wrap.sprite.add("cars",width/2,height/2,"player")
wrap.sprite.set_angle(player,0)
wrap.sprite.set_size_percent(player,75,75)