import rg

class Robot:
    def act(self, game):
        x,y = self.location
        dist = 999
        shortloc = (0,0)
        bot = None
        for loc, bot in game.get('robots').items():
            if bot.get('player_id') != self.player_id:
                dist2 = rg.dist(loc, self.location)
                if dist2 < dist:
                    dist = dist2
                    shortloc = loc
                    bot = bot
        if 'spawn' in rg.loc_types(self.location) :
            return ['move', rg.toward(self.location, shortloc)]
        elif dist <= 1:
            if bot.hp < self.hp:
            	return ['attack', shortloc]
            elif self.hp<=20:
                return ['guard']
        return ['move', rg.toward(self.location, rg.CENTER_POINT)]