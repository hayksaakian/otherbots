import rg
import operator

allyDistance = 15
enemyDistance = 7
class Robot:
    def act(self, game):
        # if there are enemies around get em
        bestDistance = 999
        bestLoc = (0,0)
        for loc, bot in game['robots'].iteritems():
            if bot.player_id != self.player_id:
                if rg.dist(loc, self.location) < bestDistance:
                    bestDistance = rg.dist(loc, self.location)
                    bestLoc = loc
        if game['robots'][self.location].hp <= 10:
            away = tuple(map(lambda x, y: x - y, rg.toward(self.location, bestLoc), self.location))
            move = tuple(map(lambda x, y: x - y, self.location, away))
            goodPlaces = rg.locs_around(self.location, filter_out=('invalid', 'obstacle', 'spawn'))
            if move in goodPlaces:
                return ['move', move]
            for loc in rg.locs_around(self.location, filter_out=('invalid', 'obstacle')):
                if loc in game['robots']:
                    if game['robots'][loc].player_id != self.player_id:
                        return ['suicide']

            else:
                return ['guard']
        for loc, bot in game['robots'].iteritems():
            if bot.player_id != self.player_id:
                if rg.dist(loc, self.location) <= 1:
                    return ['attack', loc]
        if rg.dist(bestLoc, self.location) <= enemyDistance:
            return ['move', rg.toward(self.location, bestLoc)]

                
        # otherwise clump up
        for loc, bot in game['robots'].iteritems():
            if bot.player_id == self.player_id:
                if rg.dist(loc, self.location) <= allyDistance:
                    return ['move', rg.toward(self.location, loc)]
        if self.location == rg.CENTER_POINT:
            return ['guard']
        return ['move', rg.toward(self.location, rg.CENTER_POINT)]
