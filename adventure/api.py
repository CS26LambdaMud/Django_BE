from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))

@csrf_exempt
@api_view(["GET"])
def initialize(request):
    
    user = request.user
    
    player = user.player
    
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_id)
    pos_x, pos_y = room.pos_x, room.pos_y
    items_in_room = {}
    for i in Item.objects.filter(room_id=room.id):
        items_in_room[i.name] = i.id
    if items_in_room == {}:
        items_in_room = None
    player_items = {}
    for i in Item.objects.filter(player_id=player_id):
        player_items[i.name] = i.id
    if player_items == {}:
        player_items = None   

    return JsonResponse({'uuid': uuid, 'name':player.user.username, 'pos_x':pos_x, 'pos_y': pos_y, 'items_in_room':items_in_room,'player_items':player_items, 'players':players}, safe=True)

@api_view(["POST"])
def drop(request):

    player = request.user.player
    playerid = player.id
    room = player.room()
    roomid = room.id
    data = json.loads(request.body)
    itemid = data['itemid']
    item = Item.objects.get(id=itemid)
    item.room_id = roomid
    item.player_id = 0
    item.save()
    players = room.playerNames(playerid)

    items_in_room = {}
    player_items = {}
    for i in Item.objects.filter(room_id=room.id):
        items_in_room[i.name] = i.id
    if items_in_room == {}:
        items_in_room = None

    player_items = {}
    for i in Item.objects.filter(player_id=playerid):
        player_items[i.name] = i.id
    if player_items == {}:
        player_items = None     
    return JsonResponse({'name':player.user.username, 'pos_x':room.pos_x, 'pos_y':room.pos_y, 'players':players, 'items_in_room':items_in_room,'player_items':player_items, 'error_msg':""}, safe=True)

@api_view(["POST"])
def pickup(request):

    player = request.user.player
    playerid = player.id
    room = player.room()
    roomid = room.id
    data = json.loads(request.body)
    itemid = data['itemid']
    item = Item.objects.get(id=itemid)
    item.room_id = 0
    item.player_id = playerid
    item.save()
    players = room.playerNames(playerid)

    items_in_room = {}
    player_items = {}
    for i in Item.objects.filter(room_id=room.id):
        items_in_room[i.name] = i.id
    if items_in_room == {}:
        items_in_room = None

    player_items = {}
    for i in Item.objects.filter(player_id=playerid):
        player_items[i.name] = i.id
    if player_items == {}:
        player_items = None     
    return JsonResponse({'name':player.user.username, 'pos_x':room.pos_x, 'pos_y':room.pos_y, 'players':players, 'items_in_room':items_in_room,'player_items':player_items, 'error_msg':""}, safe=True)
# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs={"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player

    room = player.room()
  
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']

    nextRoomID = None
    if direction == "n":
        nextRoomID = room.s_to
        
    elif direction == "s":
        nextRoomID = room.n_to
        
    elif direction == "e":
        nextRoomID = room.e_to
        
    elif direction == "w":
        nextRoomID = room.w_to
     
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        player.currentRoom=nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        items_in_room = {}
        for i in Item.objects.filter(room_id=nextRoomID):
            items_in_room[i.name] = i.id
        if items_in_room == {}:
            items_in_room = None

        player_items = {}
        for i in Item.objects.filter(player_id=player_id):
            player_items[i.name] = i.id
        if player_items == {}:
            player_items = None   
            
        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'name':player.user.username, 'pos_x':nextRoom.pos_x, 'pos_y':nextRoom.pos_y, 'players':players, 'items_in_room':items_in_room,'player_items':player_items, 'error_msg':""}, safe=True)
    else:
        players = room.playerNames(player_id)
        items_in_room = {}
        for i in Item.objects.filter(room_id=room.id):
            items_in_room[i.name] = i.id
        if items_in_room == {}:
            items_in_room = None 

        player_items = {}
        for i in Item.objects.filter(player_id=player_id):
            player_items[i.name] = i.id
        if player_items == {}:
            player_items = None     
        return JsonResponse({'name':player.user.username, 'pos_x':room.pos_x, 'pos_y':room.pos_y, 'players':players, 'items_in_room':items_in_room,'player_items':player_items, 'error_msg':""}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error':"Not yet implemented"}, safe=True, status=500)


@api_view(["GET"])
def allmaps(request):
    all_rooms = Room.objects.all()
    res = {}
    for i in all_rooms:
        res[i.id] = {'x_pos': i.pos_x, 'y_pos':i.pos_y, 'room_type':i.roomtype}
    return JsonResponse(res)