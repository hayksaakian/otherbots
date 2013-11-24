import rg

BIG_DIST = 100000000
ALLY_CRITICAL = 35
SELF_CRITICAL = 11

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
		prio_loc, attack_loc = self.findPriority(active_team, active_enemy,enemy_distance)
		distance_to_prio = rg.dist(self.location,prio_loc)
		distance_to_attack = BIG_DIST
		if attack_loc:
			distance_to_attack = rg.dist(self.location,attack_loc)
			if distance_to_attack<=1:
				return ['attack', attack_loc]
			else:
				return ['move', rg.toward(self.location, prio_loc)]
		else:
			if prio_loc == self.location:
				if self.hp < SELF_CRITICAL:
					return ['suicide']
				return ['guard']
			return ['move',rg.toward(self.location,prio_loc)]
		return ['guard']
		
	def findPriority(self,active_team, active_enemy,enemy_distance):
		direction = {"up":(0,-1), "down":(0,1),"left":(-1,0),"right":(1,0)}
		dist = BIG_DIST
		closest_target = self.get_closest_dict(enemy_distance)
		nearest_weak = self.get_weakest_ally(active_team)
		adjacent_enemies = self.check_adjacent(active_enemy, nearest_weak, direction)
		target_enemy = self.get_closest_list(self.location,adjacent_enemies)
		prio_spot = None

		if nearest_weak in active_enemy:
			if active_team[nearest_weak].hp <ALLY_CRITICAL and target_enemy:
				x, y = self.location
				tx, ty = target_enemy
				dx = tx - x
				dy = ty - y
				if dx < 0 and dx<dy:
					prio_dir = direction["right"]
					prio_spot = (target_enemy[0]+prio_dir[0], target_enemy[1]+prio_dir[1])
				elif dx > 0 and dx>dy:
					prio_dir = direction["left"]
					prio_spot = (target_enemy[0]+prio_dir[0], target_enemy[1]+prio_dir[1])
				elif dy < 0 and dy<dx:
					prio_dir = direction["down"]
					prio_spot = (target_enemy[0]+prio_dir[0], target_enemy[1]+prio_dir[1])
				elif dy > 0 and dy>dx:
					prio_dir = direction["up"]
					prio_spot = (target_enemy[0]+prio_dir[0], target_enemy[1]+prio_dir[1])
				return prio_spot, target_enemy
		else:
			adjacent_enemies = self.check_adjacent(active_enemy, self.location,direction)
			if len(adjacent_enemies) == 4:
				return self.location, None
			elif len(adjacent_enemies) <4 and len(adjacent_enemies)>0:
				if target_enemy:
					move = self.find_move_spot(target_enemy,adjacent_enemies, direction)
					return move, target_enemy
				else:
					move = self.find_move_spot(closest_target, adjacent_enemies,direction)
					return move, closest_target
			else:
				return closest_target, closest_target

	def get_weakest_ally(self, active_team):
		temp_loc = (0,0)
		weak_team_near = BIG_DIST
		lowest_hp = 50
		for loc in active_team:
			distance = rg.dist(self.location, loc)
			if distance < weak_team_near and active_team[loc].hp < lowest_hp:
				weak_team_near = distance
				temp_loc = loc
		return temp_loc

	def check_adjacent(self, active_enemy, loc, direction):
		x, y = loc
		list_of_locs = []
		for d in direction:
			dx, dy = direction[d]
			if (x+dx,y+dy) in active_enemy:
				list_of_locs.append((x+dx, y+dy))
		return list_of_locs

	def get_closest_dict(self, dictio):
		dist = BIG_DIST
		temp_loc = (0,0)
		for loc in dictio:
			distance = dictio[loc]
			if dist>=distance:
				dist = distance
				temp_loc = loc
		return temp_loc

	def get_closest_list(self,location,list):
		if len(list) == 1:
			return list[0]
		elif len(list)>1:
			dist = BIG_DIST
			temp_loc = (0,0)
			for loc in list:
				distance = rg.dist(location, loc)
				if distance < dist:
					dist = distance
					temp_loc = loc
			return loc
		return None

	def find_move_spot(self, target_loc, adjacent, direction):
		x, y = self.location
		temp_list = []
		for d in direction:
			temp_d = direction[d]
			dx, dy  = temp_d[0], temp_d[1]
			temp_loc = (x+dx, y+dy)
			if not temp_loc in adjacent:
				temp_list.append(temp_loc)
		dist = BIG_DIST
		temp_loc = (0,0)
		if len(temp_list)>0:
			for loc in temp_list:
				distance = rg.dist(loc, target_loc)
				if distance<dist:
					temp_loc = loc
			return temp_loc
		else:
			return None