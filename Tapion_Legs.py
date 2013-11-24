import rg

UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)

class Robot:

	def act(self, game):
		x,y = self.location
		bot = None
		active_team = {}
		active_enemy = {}
		enemy_distance  = {}
		for loc, bot in game.get('robots').items():
			if bot.get('player_id') != self.player_id:
				active_enemy[loc] = bot
				enemy_distance[loc] = 0
			else:
				active_team[loc] = bot
		for loc in active_enemy:
			for myloc in active_team:
				enemy_distance[loc] = enemy_distance[loc] + rg.dist(loc, myloc)

	def check_adjacent(self, active_enemy, loc, direction):
		x, y = loc
		list_of_locs = []
		for d in direction:
			dx, dy = direction[d]
			if (x+dx,y+dy) in active_enemy:
				list_of_locs.append((x+dx, y+dy))
		return list_of_locs