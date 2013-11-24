import rg
import math
from itertools import product
from operator import attrgetter, itemgetter, add, or_
import random

# via https://gist.github.com/arcr/56a43d45802bc30d4528

NORMAL = 0
OBSTACLE = 1
FLOOR = 2
SPAWN = 4
ENEMY = 8
ALLY = 16
ALL = ENEMY|ALLY

types = {
    "obstacle":OBSTACLE,
    "spawn":SPAWN,
    "normal":NORMAL,
    "invalid":OBSTACLE,
    "enemy":ENEMY,
    "floor":FLOOR,
    "ally":ALLY
}

_map = None

dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]

done = 0

friends = []

class Map(object):

    def __init__(self, ally_id):
        self._b = {}
        self._ = {}
        self.generate_map()
        self.game = None
        self._mods = []

        #The id which consider your allies ;)
        self.ally_id = ally_id

    def generate_map(self):
        '''Populates the dictionary _b (the base map)
           with the types from the map (without players)

           types can be:
                > OBSTACLE (black squares)
                > SPAWN (spawn places)
                > FLOOR (white squares)
                > ENEMY
                > ALLY
           '''
        self._b.update(dict.fromkeys(rg.settings.spawn_coords, SPAWN|FLOOR))
        self._b.update(dict.fromkeys(rg.settings.obstacles, OBSTACLE))

        for i, j in product(range(19), repeat=2):
            self._b.setdefault((i,j), FLOOR)

        #self._ is the dummy map
        self._ = self._b.copy()


    def update_map(self, obstacles=0):
        '''
            cleans the changes made to the dummy map
        '''
        for i in self._mods:
            self._[i] = self._b[i]

        ally = ALLY
        enemy = ENEMY

        ''' Adds 'obstacle' so ALLY or ENEMY will be
        considered also an obtacle '''

        if obstacles:
            ally |= OBSTACLE if (obstacles & ALLY) else 0
            enemy |= OBSTACLE if (obstacles & ENEMY) else 0

        robots = self.game.get('robots')
        #the modifications made will be the locations in
        #game.robots
        self._mods[:] = robots.keys()[:]

        for loc, bot in robots.items():
            if self.ally_id == bot.player_id:
                self._[loc] |= ally
            else:
                self._[loc] |= enemy

    def get_type(self, *locs):
        '''
        Returns a tuple of the form ((loc1,TYPES))
        TYPES can be any of the constants defined at top
        combined. Example: (((10,3),FLOOR|ALLY|SPAWN),...)
        '''
        return ((loc,self._.get(loc,OBSTACLE)) for loc in locs)        

    def cross_types(self, loc, exclude=None, include = None):
        '''
        Returns a tuple of the types around a location

        if exclude is defined, these types will not be considered.
        Include does the opposite.

        So for example you only wants the enemies that surround you
        then you call self.cross_types(self.location, include="ENEMY")

        returns (((10,8),ENEMY),((12,8),ENEMY)))
        '''
        cross = cross_pos(loc)
        types = self.get_type(*cross)
        if exclude:
            return filter(lambda x: not(exclude & x[1]), types)
        elif include:
            return filter(lambda x: include & x[1], types)

        return types

def cross_pos(loc):
    '''
    returns a tuple of the locs around a location
    '''
    return [tuple(map(add,loc,d)) for d in dirs]

class Robot:

    def init(self, game):
        
        self.game = game

        self.enemy_id = 1 - self.player_id
        self.attacked = 0
        self.previous_hp = 50
        self.previous_loc = self.location
        
    def act(self, game):
        global _map
        global done

        turn = game.turn

        if turn == 1:
            _map = Map(self.player_id)
            self.init(game)

        _map.game = game
        _map.update_map()

        check_run = self.check_run()
        check_attack = self.check_cross_attack()
        check_suicide = self.check_suicide()
        
        if self.previous_loc == self.location:
            if self.previous_hp == self.hp:
                if self.attacked:
                    check_attack = self.check_cross_attack()

        if check_run:
            self.previous_hp = self.hp
            self.previous_loc = self.location
            self.attacked = 0
            return check_run

        if check_attack:
            self.previous_hp = self.hp
            self.previous_loc = self.location
            self.attacked = 1            
            return check_attack

        cross = _map.cross_types(self.location, exclude=OBSTACLE|ALLY|ENEMY|SPAWN)

        if cross:
            next_post = cross[random.randint(0, len(cross)-1)][0]
        
            return ['move', next_post]
        else:
            cross = _map.cross_types(self.location, exclude=OBSTACLE|ALLY|ENEMY)
            if cross:
                next_post = cross[random.randint(0, len(cross)-1)][0]
            
                return ['move', next_post]
            else:
                return ['guard']
        
        
    def check_run(self):
        global _map
        cross = _map.cross_types(self.location, include=ENEMY)
        if cross:
            enemy_hp = map(lambda x: _map.game.get('robots')[x[0]].hp, cross)
            # print enemy_hp, len(cross)
            if self.hp < sum(enemy_hp) and len(cross)>=2:
                return self.check_suicide()
            elif self.hp < sum(enemy_hp):
                return self.move_random(exclude=ENEMY|ALLY|OBSTACLE)
        return None                

    def move_random(self, exclude=0):
        cross = _map.cross_types(self.location, exclude=exclude)
        if cross:
            next_post = cross[random.randint(0, len(cross)-1)][0]
            return ['move', next_post]
        
    def check_suicide(self):
        global _map
        cross = _map.cross_types(self.location, include=ENEMY)
        if cross and self.hp<=8*len(cross):
            return ["suicide"]
        return None
        
    def check_cross_attack(self):
        global _map
        cross = _map.cross_types(self.location, include=ENEMY)
        if cross:
            weaker = min(map(lambda x: _map.game.get('robots')[x[0]], cross),key=itemgetter("hp"))
            # print weaker
            return ["attack", weaker.location]
        return None