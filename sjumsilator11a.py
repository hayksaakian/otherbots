import rg
 
__author__ = 'sjums'
 
#Objective: Find the enimy within 5 fields with the highest HP. Attack him.
#if own HP is less or equal to 8 and standing next to an enemy, do suicide.
#the last move part is actually buggy i see... hmm!
class Robot:
    def act(self, game):
        targets = []
 
        center = {'hp': 100, 'location': rg.CENTER_POINT}
 
        targets.append(center)
 
        max_hp = 0
        for loc, robot in game['robots'].items():
            if robot.player_id != self.player_id:
                if robot.hp > max_hp and rg.dist(self.location, loc) < 5:
                    max_hp = robot.hp
 
                    rob = {'hp': 0, 'location': rg.CENTER_POINT}
                    rob['hp '] = robot.hp
                    rob['location'] = loc
 
                    targets.append(rob)
 
                if self.hp <= 8 and rg.wdist(self.location, loc) <= 1:
                    return ['suicide']
 
                if rg.wdist(self.location, loc) <= 1:
                    return ['attack', loc]
 
 
        best_target = sorted(targets, key=lambda target: target['hp'])[-1]['location']
 
        #loc_types = rg.loc_types(rg.toward(self.location, best_target))
 
        if self.location == rg.CENTER_POINT:
            if best_target != rg.CENTER_POINT:
                return ['move', rg.toward(self.location, best_target)]
            else:
                return ['guard']
        else:
            return ['move', rg.toward(self.location, rg.CENTER_POINT)]