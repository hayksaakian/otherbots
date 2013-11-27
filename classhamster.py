import rg
import euclid as eu
class Robot:
    def act(self, game):
        active_team = {}
        active_enemy = {}
        enemy_distance = {}
        active_bots = {}
        for loc, bot in game.get('robots').items():
            if bot.player_id != self.player_id:
                active_enemy[loc] = bot                
                enemy_distance[loc] = 0
            else:
                active_team[loc] = bot
        for loc, bot in game.get('robots').items():
            active_bots[loc] = bot
        for loc in active_enemy:
            for myloc in active_team:
                enemy_distance[loc] = enemy_distance[loc] + rg.dist(loc, myloc)
        if self.hp <= 20:
            return flee(self, active_enemy, active_team, game)
        if 'spawn' in rg.loc_types(self.location):
            if game['turn'] %10 == 0: #spawn about to happen, gtfo
                return ['move', rg.toward(self.location, rg.CENTER_POINT)]
        for loc, bot in game['robots'].iteritems():
            if bot.player_id != self.player_id:
                if rg.dist(loc, self.location) <= 1:
                    print("ATTACK")
                    return ['attack', loc]
                else:                    
                    return['move', rg.toward(self.location, bot.location)]