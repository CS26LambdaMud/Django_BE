from adventure.models import Player, Room
import random


class MapWorld:
    def __init__(self):
        self.grid = []
        self.width = 0
        self.height = 0

    def __str__(self):
        s = '__' * self.width
        s += '\n'
        for y in range(self.height - 1, -1, -1):
            for x in range(0, self.width):
                if x < 1:
                    s += '|'
                if not self.grid[x][y].s_to:
                    s += '_'
                else:
                    s += ' '
                if not self.grid[x][y].e_to:
                    s += '|'
                else:
                    s += ' '
            s += '\n'
        return s

    def connected(self, room):
        connected = False
        if room.n_to:
            connected = True
        if room.s_to:
            connected = True
        if room.w_to:
            connected = True
        if room.e_to:
            connected = True
        return connected

    def find_neighbors(self, room):
        delta = [('w', (-1, 0)),
                 ('e', (1, 0)),
                 ('s', (0, -1)),
                 ('n', (0, 1))
                 ]
        neighbors = []
        for direction, (dx, dy) in delta:
            x2, y2 = room.x + dx, room.y + dy
            if (0 <= x2 < self.width) and (0 <= y2 < self.height):
                neighbor = self.grid[x2][y2]
                if not self.connected(neighbor):
                    neighbors.append((direction, neighbor))
        return neighbors

    def get_directions_str(self, room):
        dirs = []
        output = ''
        if room.n_to:
            dirs.append('north')
        if room.s_to:
            dirs.append('south')
        if room.w_to:
            dirs.append('west')
        if room.e_to:
            dirs.append('east')
        for x in range(0, len(dirs)):
            if x == len(dirs) - 1:
                output += f'and {dirs[x]}.'
            else:
                output += f'{dirs[x]}, '
        return output

    def generate_description(self, room, unique=False, descriptions=[]):
        import random
        from util.descriptions import variants, dead_end
        if unique and len(descriptions):
            t, d = descriptions.pop(random.randrange(0, len(descriptions)))
            room.title = t
            room.description = d
            room.save()
        elif unique:
            room.title = 'Dead End'
            room.description = dead_end
            room.save()
        else:
            selections = random.sample(variants, 3)
            room.title = 'Sewer Passageway'
            room.description = f'{selections[0]} {selections[1]} {selections[2]}'
            room.description += f' Tunnels continue {self.get_directions_str(room)} '
            room.save()

    def find_neighbors(self, room):
        delta = [('w', (-1, 0)),
                 ('e', (1, 0)),
                 ('s', (0, -1)),
                 ('n', (0, 1))
                 ]
        neighbors = []
        for direction, (dx, dy) in delta:
            x2, y2 = room.x + dx, room.y + dy
            if (0 <= x2 < self.width) and (0 <= y2 < self.height):
                neighbor = self.grid[x2][y2]
                if not self.connected(neighbor):
                    neighbors.append((direction, neighbor))
        return neighbors

    def generate_map(self, width, height):
        if width < 1 or height < 1:
            return False
        from adventure.models import Room
        import random
        from util.descriptions import descriptions
        Room.objects.all().delete()
        self.width = width
        self.height = height
        self.grid = [[Room(x=x, y=y) for y in range(self.height)]
                     for x in range(self.width)]
        room = None
        for x in range(0, self.width):
            for y in range(0, self.height):
                room = self.grid[x][y]
                if room:
                    room.save()
        n = self.width * self.height
        # random starting place
        ix, iy = random.randrange(
            0, self.width - 1), random.randrange(0, self.height - 1)
        room_stack = []
        current = self.grid[ix][iy]
        nv = 1
        reverse_direction = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}
        backtracked = False
        while nv < n:
            neighbors = self.find_neighbors(current)
            if not neighbors:
                if len(descriptions) and not backtracked:
                    self.generate_description(current, True, descriptions)
                else:
                    self.generate_description(current)
                current = room_stack.pop()
                backtracked = True
                continue
            backtracked = False
            direction, next_room = random.choice(neighbors)
            current.connectRooms(next_room, direction)
            next_room.connectRooms(current, reverse_direction[direction])
            # setup title and description
            self.generate_description(current)  # other params are defaulted
            room_stack.append(current)
            current = next_room
            nv += 1
