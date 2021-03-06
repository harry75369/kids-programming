import sys
import pygame as pg
import random
import math

DEBUG = False

class Resource:

	@staticmethod
	def scale(size):
		SCALE = 1
		w, h = size
		return (int(w * SCALE), int(h * SCALE))

	def __init__(self):
		self.images = pg.image.load("images/resource.bmp")
		self.images.set_colorkey(pg.Color("black"))
		self.fire_sound = pg.mixer.Sound('sounds/fire.wav')
		self.hit_tank_sound = pg.mixer.Sound('sounds/hit_tank.wav')
		self.hit_wall_sound = pg.mixer.Sound('sounds/hit_wall.wav')
		self.hit_bullet_sound = pg.mixer.Sound('sounds/hit_bullet.wav')
		self.game_start_sound = pg.mixer.Sound('sounds/game_start.wav')
		self.game_pause_sound = pg.mixer.Sound('sounds/game_pause.wav')

    #######################################################################################
    # tank size and costumes
    #######################################################################################
	def get_tank_size(self):
		return (64, 64)

	def get_tank_size_scaled(self):
		return Resource.scale(self.get_tank_size())

	def get_tank_costumes(self, color):
		palettes = {
			'yellow': [pg.Color(0,0,0,255), pg.Color(104,104,0,255), pg.Color(231,156,33,255), pg.Color(231,231,148,255)],
			'white': [pg.Color(0,0,0,255),pg.Color(0,75,84,255),pg.Color(182,182,182,255),pg.Color(255,255,255,255)]
		}
		img = self.images.copy()
		img.set_palette(palettes[color])
		w, h = self.get_tank_size()
		costumes_dict = {
			'yellow': {
				'up':    [img.subsurface(pg.Rect(0, 0, w, h)), img.subsurface(pg.Rect(64, 0, w, h))],
				'left':  [img.subsurface(pg.Rect(128, 0, w, h)), img.subsurface(pg.Rect(192, 0, w, h))],
				'down':  [img.subsurface(pg.Rect(256, 0, w, h)), img.subsurface(pg.Rect(320, 0, w, h))],
				'right': [img.subsurface(pg.Rect(384, 0, w, h)), img.subsurface(pg.Rect(448, 0, w, h))]
			},
			'white': {
				'up':    [img.subsurface(pg.Rect(0, 256, w, h)), img.subsurface(pg.Rect(64, 256, w, h))],
				'left':  [img.subsurface(pg.Rect(128, 256, w, h)), img.subsurface(pg.Rect(192, 256, w, h))],
				'down':  [img.subsurface(pg.Rect(256, 256, w, h)), img.subsurface(pg.Rect(320, 256, w, h))],
				'right': [img.subsurface(pg.Rect(384, 256, w, h)), img.subsurface(pg.Rect(448, 256, w, h))]
			}
		}
		return costumes_dict[color]

	#######################################################################################
	# bullet size and costumes
	#######################################################################################
	def get_bullet_sizes(self):
		return {
			'up': (12, 16),
			'left': (16, 12),
			'down': (12, 16),
			'right': (16, 12)
		}

	def get_bullet_sizes_scaled(self):
		sizes = self.get_bullet_sizes()
		for key in sizes.keys():
			sizes[key] = Resource.scale(sizes[key])
		return sizes

	def get_bullet_costumes(self):
		img = self.images.copy()
		img.set_palette_at(2, pg.Color(182,182,182,255))
		sizes = self.get_bullet_sizes()
		costumes = {
			'up': img.subsurface(pg.Rect(268, 856, sizes['up'][0], sizes['up'][1])),
			'left': img.subsurface(pg.Rect(296, 856, sizes['left'][0], sizes['left'][1])),
			'down': img.subsurface(pg.Rect(332, 856, sizes['down'][0], sizes['down'][1])),
			'right': img.subsurface(pg.Rect(360, 856, sizes['right'][0], sizes['right'][1])),
		}
		return costumes

	#######################################################################################
	# boom size and costumes
	#######################################################################################
	def get_boom_size(self, boom_counter):
		sizes = [(64, 64), (64, 64), (64, 64), (128, 128), (128, 128)]
		return sizes[boom_counter]

	def get_boom_size_scaled(self, boom_counter):
		return Resource.scale(self.get_boom_size(boom_counter))

	def get_boom_costumes(self):
		img = self.images.copy()
		img.set_palette([pg.Color(0,0,0,255),pg.Color(101,0,134,255),pg.Color(189,56,36,255),pg.Color(255,255,255,255)])
		sizes = [self.get_boom_size(i) for i in range(5)]
		ws = [w for (w, h) in sizes]
		hs = [h for (w, h) in sizes]
		boom3 = img.subsurface(pg.Rect(256, 896, ws[3], hs[3])).copy()
		boom3_part2 = img.subsurface(pg.Rect(384, 896, ws[3], hs[3]/2))
		boom3.blit((boom3_part2), (0, hs[3]/2))
		boom4 = img.subsurface(pg.Rect(128, 896, ws[4], hs[4])).copy()
		boom4_part2 = img.subsurface(pg.Rect(0, 960, ws[4], hs[4]/2))
		boom4.blit((boom4_part2), (0, 0))
		costumes = [
			img.subsurface(pg.Rect(256, 960, ws[0], hs[0])),
			img.subsurface(pg.Rect(320, 960, ws[1], hs[1])),
			img.subsurface(pg.Rect(384, 960, ws[2], hs[2])),
			boom3,
			boom4
		]
		return costumes

	#######################################################################################
	# text size and costumes
	#######################################################################################
	def get_text_size(self, text):
		if (text == "pause"):
			return (160, 32)
		elif (text == "gameover"):
			return (160, 64)
		else:
			raise Exception("text not supported: %s" % text)

	def get_text_costume(self, text):
		img = self.images.copy()
		if (text == "pause" or text == "gameover"):
			img.set_palette([pg.Color(0,0,0,255),pg.Color(101,0,134,255),pg.Color(189,56,36,255),pg.Color(255,255,255,255)])
		w, h = self.get_text_size(text)
		if (text == "pause"):
			return img.subsurface(pg.Rect(352, 512, w, h))
		elif (text == "gameover"):
			return img.subsurface(pg.Rect(384, 768, w, h))
		else:
			raise Exception("text not supported: %s" % text)

	#######################################################################################
	# sounds
	#######################################################################################
	def play_fire_sound(self):
		self.fire_sound.play()

	def play_hit_tank_sound(self):
		self.hit_tank_sound.play()

	def play_hit_wall_sound(self):
		self.hit_wall_sound.play()

	def play_hit_bullet_sound(self):
		self.hit_bullet_sound.play()

	def play_game_start(self):
		self.game_start_sound.play()

	def play_game_pause(self):
		self.game_pause_sound.play()

class Text:

	def __init__(self, screen, resource, text, has_animation = False, hidden = True, x = 0, y = 0):
		self.screen = screen
		self.resource = resource
		self.size = resource.get_text_size(text)
		self.width, self.height = self.size
		if (text == "pause"):
			self.pos_x = (screen.get_width() - self.width) / 2
			self.pos_y = (screen.get_height() - self.height) / 2
		else:
			self.pos_x, self.pos_y = x, y
		self.costume = resource.get_text_costume(text)
		self.has_animation = has_animation
		self.animation_counter = 0
		self.is_hidden = hidden

	def type(self):
		return "TEXT"

	def finished(self):
		return False

	def position(self):
		return (self.pos_x, self.pos_y, self.width, self.height)

	def center(self):
		x, y, w, h = self.position()
		return (x + w / 2, y + h / 2)

	def draw(self):
		if self.has_animation:
			self.animation_counter += 1
		if (not self.is_hidden):
			if (self.has_animation):
				if (self.animation_counter % 80 < 40):
					self.screen.blit(self.costume, (self.pos_x, self.pos_y))
			else:
				self.screen.blit(self.costume, (self.pos_x, self.pos_y))

	def toggle_hidden(self):
		self.is_hidden = not self.is_hidden

	def toggle_stop(self):
		pass


def my_colliderect(bbox_a, bbox_b):
	ax, ay, aw, ah = bbox_a.x, bbox_a.y, bbox_a.width, bbox_a.height
	bx, by, bw, bh = bbox_b.x, bbox_b.y, bbox_b.width, bbox_b.height

	if ax + aw > bx and ay + ah > by and ax < bx + bw and  ay < by + bh:
		return True

	return False

def normalize(x):
	ax = math.fabs(x)
	if ax == 0: return 0
	return x / ax

class Tank:

	SPEED = 5

	def __init__(self, screen, resource, sprites, color = 'yellow'):
		self.screen = screen
		self.resource = resource
		self.sprites = sprites
		self.size = resource.get_tank_size_scaled()
		self.width, self.height = self.size
		self.pos_x = (screen.get_width() - self.width) / 2
		self.pos_y = (screen.get_height() - self.height) / 2
		self.costumes = resource.get_tank_costumes(color)
		self.dir = 'up'
		self.wheel = 0
		self.fire_time = None
		self.is_stop = False
		self.boom_costumes = resource.get_boom_costumes()
		self.state = "original"
		self.enemy = None
		self.bullets = []

		for costume in self.costumes.values():
			costume[0] = pg.transform.scale(costume[0], self.size)
			costume[1] = pg.transform.scale(costume[1], self.size)
		for idx in range(len(self.boom_costumes)):
			self.boom_costumes[idx] = pg.transform.scale(self.boom_costumes[idx], resource.get_boom_size_scaled(idx))

		if DEBUG:
			for costume in self.costumes.values():
				costume[0] = costume[0].convert(24)
				costume[1] = costume[1].convert(24)
				pg.draw.rect(costume[0], pg.Color('red'), pg.Rect(0, 0, self.width, self.height), 1)
				pg.draw.rect(costume[1], pg.Color('red'), pg.Rect(0, 0, self.width, self.height), 1)

	def set_enemy(self, enemy):
		self.enemy = enemy
		sIdx = 0
		while sIdx < len(self.bullets):
			if self.bullets[sIdx].finished():
				del self.bullets[sIdx]
			else:
				self.bullets[sIdx].set_target(enemy)
				sIdx += 1

	def type(self):
		return "TANK"

	def finished(self):
		return self.state == "finished"

	def booming(self):
		return self.state == "booming"

	def position(self):
		return (self.pos_x, self.pos_y, self.width, self.height)

	def center(self):
		x, y, w, h = self.position()
		return (x + w / 2, y + h / 2)

	def collide(self, new_x, new_y):
		reverted = False
		old_bbox = pg.Rect(self.pos_x, self.pos_y, self.width, self.height)
		new_bbox = pg.Rect(new_x, new_y, self.width, self.height)
		for sprite in self.sprites:
			if (self != sprite and sprite.type() == "TANK" and not sprite.finished() and not sprite.booming()):
				sx, sy, sw, sh = sprite.position()
				s_bbox = pg.Rect(sx, sy, sw, sh)
				#if (not old_bbox.colliderect(s_bbox) and new_bbox.colliderect(s_bbox)):
				if (not my_colliderect(old_bbox, s_bbox) and my_colliderect(new_bbox, s_bbox)):
					new_x, new_y = self.pos_x, self.pos_y
					reverted = True
					break
		return reverted, new_x, new_y

	def move_up(self):
		if self.is_stop: return
		if self.booming() or self.finished(): return
		self.dir = 'up'
		distance = Tank.SPEED
		reverted, self.pos_x, self.pos_y = self.collide(self.pos_x, self.pos_y - distance)
		while reverted:
			distance /= 2
			reverted, self.pos_x, self.pos_y = self.collide(self.pos_x, self.pos_y - distance)
		self.wheel = (self.wheel + 1) % 2
		self.make_within_screen()

	def move_left(self):
		if self.is_stop: return
		if self.booming() or self.finished(): return
		self.dir = 'left'
		distance = Tank.SPEED
		reverted, self.pos_x, self.pos_y = self.collide(self.pos_x - distance, self.pos_y)
		while reverted:
			distance /= 2
			reverted, self.pos_x, self.pos_y = self.collide(self.pos_x - distance, self.pos_y)
		self.wheel = (self.wheel + 1) % 2
		self.make_within_screen()

	def move_down(self):
		if self.is_stop: return
		if self.booming() or self.finished(): return
		self.dir = 'down'
		distance = Tank.SPEED
		reverted, self.pos_x, self.pos_y = self.collide(self.pos_x, self.pos_y + distance)
		while reverted:
			distance /= 2
			reverted, self.pos_x, self.pos_y = self.collide(self.pos_x, self.pos_y + distance)
		self.wheel = (self.wheel + 1) % 2
		self.make_within_screen()

	def move_right(self):
		if self.is_stop: return
		if self.booming() or self.finished(): return
		self.dir = 'right'
		distance = Tank.SPEED
		reverted, self.pos_x, self.pos_y = self.collide(self.pos_x + distance, self.pos_y)
		while reverted:
			distance /= 2
			reverted, self.pos_x, self.pos_y = self.collide(self.pos_x + distance, self.pos_y)
		self.wheel = (self.wheel + 1) % 2
		self.make_within_screen()

	def make_within_screen(self):
		self.pos_x = max(0, min(self.screen.get_width() - self.width, self.pos_x))
		self.pos_y = max(0, min(self.screen.get_height() - self.height, self.pos_y))

	def draw(self):
		if self.state == "original":
			self.screen.blit(self.costumes[self.dir][self.wheel], (self.pos_x, self.pos_y))
		elif self.state == "booming":
			bw, bh = self.resource.get_boom_size_scaled(int(self.boom_counter))
			pos_x = self.pos_x + (self.width - bw) / 2
			pos_y = self.pos_y + (self.height - bh) / 2
			self.screen.blit(self.boom_costumes[int(self.boom_counter)], (pos_x, pos_y))
			if not self.is_stop:
				self.boom_counter += 0.1
			if self.boom_counter >= self.boom_stop:
				self.state = "finished"

	def fire(self):
		if self.is_stop: return
		now = pg.time.get_ticks()
		if (self.fire_time == None or now - self.fire_time > 300):
			self.fire_time = now
			bullet = Bullet(self.screen, self.resource, self, self.sprites, self.pos_x, self.pos_y, self.dir)
			bullet.set_target(self.enemy)
			self.bullets.append(bullet)
			return bullet
		return None

	def toggle_stop(self):
		self.is_stop = not self.is_stop

	def got_hit(self):
		if not self.finished() and not self.booming():
			self.resource.play_hit_tank_sound()
			self.state = "booming"
			self.boom_counter = 2
			self.boom_stop = 5

class Bullet:

	SPEED = 10
	SPEED_DICT = {
		'up': (0, -SPEED),
		'left': (-SPEED, 0),
		'down': (0, SPEED),
		'right': (SPEED, 0)
	}
	
	def __init__(self, screen, resource, father, sprites, x, y, dir):
		self.screen = screen
		self.resource = resource
		self.father = father
		self.sprites = sprites
		self.tank_size = resource.get_tank_size_scaled()
		self.tank_width, self.tank_height = self.tank_size
		self.sizes = resource.get_bullet_sizes_scaled()
		w, h = self.sizes[dir]
		if dir == "up":
			self.pos_x = x + (self.tank_width - w) / 2
			self.pos_y = y
		elif dir == "left":
			self.pos_x = x
			self.pos_y = y + (self.tank_height - h) / 2
		elif dir == "down":
			self.pos_x = x + (self.tank_width - w) / 2
			self.pos_y = y + self.tank_height - h
		elif dir == "right":
			self.pos_x = x + self.tank_width - w
			self.pos_y = y + (self.tank_height - h) / 2
		self.costumes = resource.get_bullet_costumes()
		self.boom_costumes = resource.get_boom_costumes()
		self.speed = Bullet.SPEED_DICT[dir]
		self.dir = dir
		self.target = None
		self.is_stop = False

		self.resource.play_fire_sound()
		for key in self.costumes.keys():
			self.costumes[key] = pg.transform.scale(self.costumes[key], self.sizes[key])
		for idx in range(len(self.boom_costumes)):
			self.boom_costumes[idx] = pg.transform.scale(self.boom_costumes[idx], resource.get_boom_size_scaled(idx))

		self.state = "original"

	def type(self):
		return "BULLET"

	def finished(self):
		return self.state == "finished"

	def booming(self):
		return self.state == "booming"

	def position(self):
		w, h = self.sizes[self.dir]
		return (self.pos_x, self.pos_y, w, h)

	def center(self):
		x, y, w, h = self.position()
		return (x + w / 2, y + h / 2)
			
	def hit_bullet(self):
		if not self.finished() and not self.booming():
			self.resource.play_hit_bullet_sound()
			self.boom(2)
			
	def boom(self, boom_stop):
		self.state = "booming"
		self.boom_counter = 0
		self.boom_stop = boom_stop
		w, h = self.sizes[self.dir]
		self.pos_x -= (self.tank_width - w) / 2
		self.pos_y -= (self.tank_height - h) / 2

	def set_target(self, target):
		self.target = target

	def collide(self, new_x, new_y):
		target = None
		x, y, w, h = self.position()

		new_bbox = pg.Rect(new_x, new_y, w, h)
		for sprite in self.sprites:
			if (self != sprite and self.father != sprite and sprite.type() != "TEXT" and not sprite.finished() and not sprite.booming()):
				sx, sy, sw, sh = sprite.position()
				s_bbox = pg.Rect(sx, sy, sw, sh)
				#if (not old_bbox.colliderect(s_bbox) and new_bbox.colliderect(s_bbox)):
				if my_colliderect(new_bbox, s_bbox):
					new_x, new_y = x, y
					target = sprite
					break
		return target, new_x, new_y

	def get_speed(self):
		if self.target == None:
			speed_x, speed_y = Bullet.SPEED_DICT[self.dir]
		else:
			x, y = self.center()
			tx, ty = self.target.center()
			dx, dy = tx - x, ty - y
			speed_x = normalize(dx) * Bullet.SPEED
			speed_y = normalize(dy) * Bullet.SPEED

			if dy >= dx and dy > -dx:
				self.dir = 'down'
			elif dy <= -dx and dy > dx:
				self.dir = 'left'
			elif dy <= dx and dy < -dx:
				self.dir = 'up'
			elif dy >= -dx and dy < dx:
				self.dir = 'right'
		return (self.dir, speed_x, speed_y)

	def draw(self):
		if self.state == "original":
			if not self.is_stop:
				self.dir, dx, dy = self.get_speed()
				target, self.pos_x, self.pos_y = self.collide(self.pos_x + dx, self.pos_y + dy)
				if target and target != self.father:
					self.hit_bullet()
					self.father.set_enemy(None)
					target.got_hit()
			self.screen.blit(self.costumes[self.dir], (self.pos_x, self.pos_y))
		elif self.state == "booming":
			bw, bh = self.resource.get_boom_size_scaled(int(self.boom_counter))
			pos_x = self.pos_x + (self.tank_width - bw) / 2
			pos_y = self.pos_y + (self.tank_height - bh) / 2
			self.screen.blit(self.boom_costumes[int(self.boom_counter)], (pos_x, pos_y))
			if not self.is_stop:
				self.boom_counter += 0.1
			if self.boom_counter >= self.boom_stop:
				self.state = "finished"

	def toggle_stop(self):
		self.is_stop = not self.is_stop

	def got_hit(self):
		if not self.finished() and not self.booming():
			self.resource.play_hit_bullet_sound()
			self.boom(2)

class Game:

	def __init__(self):
		pg.mixer.pre_init(44100, -16, 1, 2048)
		pg.mixer.init()
		pg.init()
		#pg.key.set_repeat(30)
		self.clock = pg.time.Clock()
		self.screen = pg.display.set_mode((800, 600))
		self.resource = Resource()
		self.sprite_queue = []
		self.tank_queue = []

		self.my_tank = Tank(self.screen, self.resource, self.sprite_queue)
		self.your_tank = Tank(self.screen, self.resource, self.sprite_queue, 'white')
		self.my_tank.set_enemy(self.your_tank)
		self.your_tank.set_enemy(self.my_tank)

		self.sprite_queue.append(self.my_tank)
		self.sprite_queue.append(self.your_tank)
		self.tank_queue.append(self.my_tank)
		self.tank_queue.append(self.your_tank)

		self.pause_message = Text(self.screen, self.resource, "pause", has_animation = True)
		self.sprite_queue.append(self.pause_message)

	def run(self):
		#self.resource.play_game_start()
		screen_w, screen_h = self.screen.get_size()
		while True:
			self.clock.tick(80)

			key = pg.key.get_pressed()

			if self.my_tank in self.sprite_queue:
				if key[pg.K_UP]: self.my_tank.move_up()
				elif key[pg.K_LEFT]: self.my_tank.move_left()
				elif key[pg.K_DOWN]: self.my_tank.move_down()
				elif key[pg.K_RIGHT]: self.my_tank.move_right()

			if self.your_tank in self.sprite_queue:
				if key[pg.K_w]: self.your_tank.move_up()
				elif key[pg.K_a]: self.your_tank.move_left()
				elif key[pg.K_s]: self.your_tank.move_down()
				elif key[pg.K_d]: self.your_tank.move_right()

			for event in pg.event.get():
				if event.type == pg.QUIT:
					sys.exit()
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						sys.exit()
					elif event.key == pg.K_SPACE and self.my_tank in self.sprite_queue:
						bullet = self.my_tank.fire()
						if bullet: self.sprite_queue.append(bullet)
					elif event.key == pg.K_e and self.your_tank in self.sprite_queue:
						bullet = self.your_tank.fire()
						if bullet: self.sprite_queue.append(bullet)
					elif event.key == pg.K_p:
						self.resource.play_game_pause()
						self.pause_message.toggle_hidden()
						for sprite in self.sprite_queue:
							sprite.toggle_stop()

			for sprite in self.sprite_queue:
				if sprite.type() == "BULLET":
					x, y, w, h = sprite.position()
					if (x < 0) or (x + w > screen_w) or (y < 0) or (y + h > screen_h):
						sprite.hit_bullet()

			sIdx = 0
			while sIdx < len(self.sprite_queue):
				if self.sprite_queue[sIdx].finished():
					del self.sprite_queue[sIdx]
				else: sIdx += 1

			self.screen.fill(pg.Color("black"))
			for sprite in self.sprite_queue:
				sprite.draw()
			pg.display.flip()

if __name__ == "__main__":                
	game = Game()
	game.run()
