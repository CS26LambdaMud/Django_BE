from django.contrib.auth.models import User
from adventure.models import Player, Room

import numpy as np
import random


Room.objects.all().delete()


def create_zeros(lenth):
    a = np.zeros((lenth,lenth))
    return a, lenth

map_zero, lenth = create_zeros(20)


max_depth = lenth - 1
start_x = lenth // 2
start_y = lenth //2
counter = (lenth * lenth) // 2
map_zero[start_x][start_y] = 5
rooms = 1
directions = {'r':(0,1), 'l': (0, -1), 'u':(-1, 0), 'd': (1, 0)}
#     directions = {'u':['d','r','l'],
#                  'd':['u','r','l'],
#                  'r':['d','u','l'],
#                  'l':['d','r','u']}
run_vert = 'r'
run_hor = 'u'
while rooms < counter:
    can_move = []
    #left corner
    if start_x == 0 and start_y == 0:
        if map_zero[0][1] == 0:
            can_move.append('r')
        if map_zero[1][0] == 0:
            can_move.append('d')
    #right corner       
    elif start_x == 0 and start_y == max_depth:
        if map_zero[0][max_depth - 1] == 0:
            can_move.append('l')
        if map_zero[1][max_depth] == 0:
            can_move.append('d')
    #bottom left corner
    elif start_x == max_depth and start_y == 0:
        if map_zero[max_depth - 1][0] == 0:
            can_move.append('u')
        if map_zero[max_depth][1] == 0:
            can_move.append('r')
    #right bottom corner
    elif start_x == max_depth and start_y == max_depth:
        if map_zero[max_depth][max_depth - 1] == 0:
            can_move.append('l')
        if map_zero[max_depth - 1][max_depth] == 0:
            can_move.append('u')
    #right side
    elif start_y == max_depth:
        if map_zero[start_x - 1][start_y] == 0:
            can_move.append('u')
        if map_zero[start_x + 1][start_y] == 0:
            can_move.append('d')
        if map_zero[start_x][start_y - 1] == 0:
            can_move.append('l')
    #left side
    elif start_y == 0:
        if map_zero[start_x][start_y + 1]:
            can_move.append('r')
        if map_zero[start_x + 1][start_y]:
            can_move.append('d')
        if map_zero[start_x - 1][start_y] == 0:
            can_move.append('u')
    #top
    elif start_x == 0:
        if map_zero[start_x][start_y + 1]:
            can_move.append('r')
        if map_zero[start_x + 1][start_y]:
            can_move.append('d')
        if map_zero[start_x][start_y - 1] == 0:
            can_move.append('l')
    #bottom
    elif start_x == max_depth:
        if map_zero[start_x][start_y + 1]:
            can_move.append('r')
        if map_zero[start_x - 1][start_y]:
            can_move.append('u')
        if map_zero[start_x][start_y - 1] == 0:
            can_move.append('l')       
    else:
        if map_zero[start_x][start_y + 1] == 0:
            can_move.append('r')
        if map_zero[start_x][start_y - 1] == 0:
            can_move.append('l')
        if map_zero[start_x - 1][start_y] == 0:
            can_move.append('u')
        if map_zero[start_x + 1][start_y] == 0:
            can_move.append('d')
    if can_move != []:
        choi = random.choice(can_move)
        move_x, move_y = directions[choi]
        start_x, start_y = start_x + move_x, start_y + move_y

        daroom = Room(roomid = rooms, pos_y=start_x, pos_x = start_y)
        daroom.save()
        map_zero[start_x][start_y] = rooms
        rooms += 1
    else:
        if run_vert == 'r' and start_y == max_depth:
            run_vert = 'l'
        if run_vert == 'l' and start_y == 0:
            run_vert = 'r'
        if run_hor == 'u' and start_x == 0:
            run_hor = 'd'
        if run_hor == 'd' and start_x == max_depth:
            run_hor = 'u'
        shift = random.choice([run_hor, run_vert])
        move_x, move_y = directions[shift]
        start_x, start_y = start_x + move_x, start_y + move_y           
new_size = lenth + 2

new_map = np.zeros((new_size, new_size))
print(Room.objects.all())

new_size = lenth + 2

new_map = np.zeros((new_size, new_size))

newx = 0
newy = 0

vert_curs = -1
for x in range(lenth):
    newx += 1
    for y in range(lenth):
        newy += 1
        if newy > lenth:
            newy = 1
        rep = map_zero[vert_curs][y]
        new_map[newx][newy] = rep
    vert_curs += 1


forward_one = 1
lastx = 0
lasty = 0
for i in range(lenth):
    lastx += forward_one
    for y in range(lenth):
        
        lasty += forward_one
        if lasty > lenth:
            lasty = 1
        selected_room_id = new_map[lastx][lasty]
        if int(selected_room_id) != 0:
            selected_room = Room.objects.get(roomid=int(selected_room_id))
            looks = []
            
            north = new_map[lastx + 1][lasty]
            looks.append((north, 'n'))
            
            south = new_map[lastx - 1][lasty]
            looks.append((south, 's'))
            
            east = new_map[lastx][lasty + 1]
            looks.append((east, 'e'))
            
            west = new_map[lastx][lasty - 1]
            looks.append((west, 'w')) 
            
    #         if selected_room_id != 0.0:
    #             new_map[lastx][lasty] = 2
            
            for vals in looks:
                intval = int(vals[0])
                if intval != 0:
                    room_to_connect = Room.objects.get(roomid=selected_room_id)
                    selected_room.connectRooms(room_to_connect, vals[1])    