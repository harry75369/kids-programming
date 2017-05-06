import sys
import pygame as pg
import random

DEBUG = True

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
		self.hit_nothing_sound = pg.mixer.Sound('sounds/hit_nothing.wav')
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
	def get_bullet_size(self, dir):
		size_dict = {
			'up': (12, 16),
			'left': (16, 12),
			'down': (12, 16),
			'right': (16, 12)
		}
		return size_dict[dir]

	def get_bullet_size_scaled(self, dir):
		return Resource.scale(self.get_bullet_size(dir))

	def get_bullet_costumes(self):
		img = self.images.copy()
		img.set_palette_at(2, pg.Color(182,182,182,255))
		w, h = self.get_bullet_size('up')
		costumes = {
			'up': img.subsurface(pg.Rect(268, 856, w, h)),
			'left': img.subsurface(pg.Rect(296, 856, h, w)),
			'down': img.subsurface(pg.Rect(332, 856, w, h)),
			'right': img.subsurface(pg.Rect(360, 856, h, w))
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

	def play_hit_nothing_sound(self):
		self.hit_nothing_sound.play()

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


def my_colliderect(bbox_a, bbox_b):
	ax, ay, aw, ah = bbox_a.x, bbox_a.y, bbox_a.width, bbox_a.height
	bx, by, bw, bh = bbox_b.x, bbox_b.y, bbox_b.width, bbox_b.height

	if ax + aw > bx and ay + ah > by and ax < bx + bw and  ay < by + bh:
		return True

	return False

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

		for costume in self.costumes.values():
			costume[0] = pg.transform.scale(costume[0], self.size)
			costume[1] = pg.transform.scale(costume[1], self.size)

		if DEBUG:
			for costume in self.costumes.values():
				costume[0] = costume[0].convert(24)
				costume[1] = costume[1].convert(24)
				pg.draw.rect(costume[0], pg.Color('red'), pg.Rect(0, 0, self.width, self.height), 1)
				pg.draw.rect(costume[1], pg.Color('red'), pg.Rect(0, 0, self.width, self.height), 1)

	def type(self):
		return "TANK"

	def finished(self):
		return False

	def position(self):
		return (self.pos_x, self.pos_y, self.width, self.height)

	def collide(self, new_x, new_y):
		old_bbox = pg.Rect(self.pos_x, self.pos_y, self.width, self.height)
		new_bbox = pg.Rect(new_x, new_y, self.width, self.height)
		for sprite in self.sprites:
			if (self != sprite and sprite.type() == "TANK"):
				sx, sy, sw, sh = sprite.position()
				s_bbox = pg.Rect(sx, sy, sw, sh)
				#if (not old_bbox.colliderect(s_bbox) and new_bbox.colliderect(s_bbox)):
				if (not my_colliderect(old_bbox, s_bbox) and my_colliderect(new_bbox, s_bbox)):
					new_x, new_y = self.pos_x, self.pos_y
					break
		return new_x, new_y

	def move_up(self):
		if self.is_stop: return
		self.dir = 'up'
		self.pos_x, self.pos_y = self.collide(self.pos_x, self.pos_y - Tank.SPEED)
		self.wheel = (self.wheel + 1) % 2
		self.make_within_screen()

	def move_left(self):
		if self.is_stop: return
		self.dir = 'left'
		self.pos_x, self.pos_y = self.collide(self.pos_x - Tank.SPEED, self.pos_y)
		self.wheel = (self.wheel + 1) % 2
		self.make_within_screen()

	def move_down(self):
		if self.is_stop: return
		self.dir = 'down'
		self.pos_x, self.pos_y = self.collide(self.pos_x, self.pos_y + Tank.SPEED)
		self.wheel = (self.wheel + 1) % 2
		self.make_within_screen()

	def move_right(self):
		if self.is_stop: return
		self.dir = 'right'
		self.pos_x, self.pos_y = self.collide(self.pos_x + Tank.SPEED, self.pos_y)
		self.wheel = (self.wheel + 1) % 2
		self.make_within_screen()

	def make_within_screen(self):
		self.pos_x = max(0, min(self.screen.get_width() - self.width, self.pos_x))
		self.pos_y = max(0, min(self.screen.get_height() - self.height, self.pos_y))

	def draw(self):
		self.screen.blit(self.costumes[self.dir][self.wheel], (self.pos_x, self.pos_y))

	def fire(self):
		if self.is_stop: return
		now = pg.time.get_ticks()
		if (self.fire_time == None or now - self.fire_time > 300):
			self.fire_time = now
			return Bullet(self.screen, self.resource, self.sprites, self.pos_x, self.pos_y, self.dir)
		return None

	def toggle_stop(self):
		self.is_stop = not self.is_stop

class Bullet:

	SPEED = 20
	SPEED_DICT = {
		'up': (0, -SPEED),
		'left': (-SPEED, 0),
		'down': (0, SPEED),
		'right': (SPEED, 0)
	}
	
	def __init__(self, screen, resource, sprites, x, y, dir):
		self.screen = screen
		self.resource = resource
		self.sprites = sprites
		self.tank_size = resource.get_tank_size_scaled()
		self.tank_width, self.tank_height = self.tank_size
		self.size = resource.get_bullet_size_scaled(dir)
		self.width, self.height = self.size
		self.pos_x = x + (self.tank_width - self.width) / 2
		self.pos_y = y + (self.tank_height - self.height) / 2
		self.costumes = resource.get_bullet_costumes()
		self.boom_costumes = resource.get_boom_costumes()
		self.speed = Bullet.SPEED_DICT[dir]
		self.dir = dir

		self.resource.play_fire_sound()
		for key in self.costumes.keys():
			self.costumes[key] = pg.transform.scale(self.costumes[key], self.size)
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
		return (self.pos_x, self.pos_y, self.width, self.height)

	def hit_tank(self):
		if not self.finished() and not self.booming():
			self.resource.play_hit_tank_sound()
			self.boom(5)

	def hit_wall(self):
		if not self.finished() and not self.booming():
			self.resource.play_hit_wall_sound()
			self.boom(3)

	def hit_nothing(self):
		if not self.finished() and not self.booming():
			self.resource.play_hit_nothing_sound()
			self.boom(2)

	def boom(self, boom_stop):
		self.state = "booming"
		self.boom_counter = 0
		self.boom_stop = boom_stop
		self.pos_x -= (self.tank_width - self.width) / 2
		self.pos_y -= (self.tank_height - self.height) / 2

	def draw(self):
		if self.state == "original":
			dx, dy = self.speed
			self.pos_x += dx
			self.pos_y += dy
			self.screen.blit(self.costumes[self.dir], (self.pos_x, self.pos_y))
			if random.randint(0, 10) < 1:
				self.dir = ['up', 'left', 'down', 'right'][random.randint(0, 3)]
				self.speed = Bullet.SPEED_DICT[self.dir]
		elif self.state == "booming":
			bw, bh = self.resource.get_boom_size_scaled(int(self.boom_counter))
			pos_x = self.pos_x + (self.tank_width - bw) / 2
			pos_y = self.pos_y + (self.tank_height - bh) / 2
			self.screen.blit(self.boom_costumes[int(self.boom_counter)], (pos_x, pos_y))
			self.boom_counter += 0.1
			if self.boom_counter >= self.boom_stop:
				self.state = "finished"

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
		self.sprite_queue.append(self.my_tank)
		self.sprite_queue.append(self.your_tank)
		self.tank_queue.append(self.my_tank)
		self.tank_queue.append(self.your_tank)

		self.pause_message = Text(self.screen, self.resource, "pause", has_animation = True)
		self.sprite_queue.append(self.pause_message)

	def run(self):
		self.resource.play_game_start()
		screen_w, screen_h = self.screen.get_size()
		while True:
			self.clock.tick(80)

			key = pg.key.get_pressed()

			if key[pg.K_UP]: self.my_tank.move_up()
			elif key[pg.K_LEFT]: self.my_tank.move_left()
			elif key[pg.K_DOWN]: self.my_tank.move_down()
			elif key[pg.K_RIGHT]: self.my_tank.move_right()

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
					elif event.key == pg.K_SPACE:
						bullet = self.my_tank.fire()
						if bullet: self.sprite_queue.append(bullet)
					elif event.key == pg.K_e:
						bullet = self.your_tank.fire()
						if bullet: self.sprite_queue.append(bullet)
					elif event.key == pg.K_p:
						self.resource.play_game_pause()
						self.pause_message.toggle_hidden()
						for tank in self.tank_queue:
							tank.toggle_stop()

			for sprite in self.sprite_queue:
				if sprite.type() == "BULLET":
					x, y, w, h = sprite.position()
					if (x < 0) or (x + w > screen_w) or (y < 0) or (y + h > screen_h):
						sprite.hit_nothing()

			self.sprite_queue = [s for s in self.sprite_queue if not s.finished()]

			self.screen.fill(pg.Color("black"))
			for sprite in self.sprite_queue:
				sprite.draw()
			pg.display.flip()

if __name__ == "__main__":                
	game = Game()
	game.run()
