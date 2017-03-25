import sys
import pygame as pg

SCALE = 1

class Resource:

	def __init__(self):
		self.images = pg.image.load("images/resource.bmp")
		self.images.set_colorkey(pg.Color("black"))
		self.fire_sound = pg.mixer.Sound('sounds/fire.wav')
		self.hit_tank_sound = pg.mixer.Sound('sounds/hit_tank.wav')
		self.hit_wall_sound = pg.mixer.Sound('sounds/hit_wall.wav')
		self.hit_nothing_sound = pg.mixer.Sound('sounds/hit_nothing.wav')

	def get_tank_size(self):
		return 64;

	def get_tank_size_scaled(self):
		return int(self.get_tank_size() * SCALE);

	def get_tank_costumes(self):
		img = self.images.copy()
		img.set_palette([pg.Color(0,0,0,255), pg.Color(104,104,0,255), pg.Color(231,156,33,255), pg.Color(231,231,148,255)])
		size = self.get_tank_size()
		costumes = {
			'up':    [img.subsurface(pg.Rect(0, 0, size, size)), img.subsurface(pg.Rect(64, 0, size, size))],
			'left':  [img.subsurface(pg.Rect(128, 0, size, size)), img.subsurface(pg.Rect(192, 0, size, size))],
			'down':  [img.subsurface(pg.Rect(256, 0, size, size)), img.subsurface(pg.Rect(320, 0, size, size))],
			'right': [img.subsurface(pg.Rect(384, 0, size, size)), img.subsurface(pg.Rect(448, 0, size, size))]
		}
		return costumes

	def get_bullet_size(self, dir = 'up'):
		size_dict = {
			'up': (12, 16),
			'left': (16, 12),
			'down': (12, 16),
			'right': (16, 12)
		}
		return size_dict[dir]

	def get_bullet_size_scaled(self, dir = 'up'):
		w, h = self.get_bullet_size(dir)
		return (int(w * SCALE), int(h * SCALE))

	def get_bullet_costumes(self, dir):
		img = self.images.copy()
		img.set_palette_at(2, pg.Color(182,182,182,255))
		w, h = self.get_bullet_size()
		costume_dict = {
			'up': pg.Rect(268, 856, w, h),
			'left': pg.Rect(296, 856, h, w),
			'down': pg.Rect(332, 856, w, h),
			'right': pg.Rect(360, 856, h, w)
		}
		costumes = {
			'original': img.subsurface(costume_dict[dir]),
			'boom1': None,
			'boom2': None,
			'boom3': None
		}
		return costumes

	def play_fire_sound(self):
		self.fire_sound.play()

	def play_hit_tank_sound(self):
		self.hit_tank_sound.play()

	def play_hit_wall_sound(self):
		self.hit_wall_sound.play()

	def play_hit_nothing_sound(self):
		self.hit_nothing_sound.play()

class Tank:

	SPEED = 5

	def __init__(self, screen, resource):
		self.screen = screen
		self.resource = resource
		self.size = resource.get_tank_size_scaled()
		self.pos_x = (screen.get_width() - self.size) / 2
		self.pos_y = (screen.get_height() - self.size) / 2
		self.costumes = resource.get_tank_costumes()
		self.dir = 'up'
		self.wheel = 0
		self.fire_time = None

		for costume in self.costumes.values():
			costume[0] = pg.transform.scale(costume[0], (self.size, self.size))
			costume[1] = pg.transform.scale(costume[1], (self.size, self.size))

	def type(self):
		return "TANK"

	def finished(self):
		return False

	def position(self):
		return (self.pos_x, self.pos_y, self.size, self.size)

	def move_up(self):
		self.dir = 'up'
		self.pos_y -= Tank.SPEED
		self.wheel = (self.wheel + 1) % 2
		self.make_within_screen()

	def move_left(self):
		self.dir = 'left'
		self.pos_x -= Tank.SPEED
		self.wheel = (self.wheel + 1) % 2
		self.make_within_screen()

	def move_down(self):
		self.dir = 'down'
		self.pos_y += Tank.SPEED
		self.wheel = (self.wheel + 1) % 2
		self.make_within_screen()

	def move_right(self):
		self.dir = 'right'
		self.pos_x += Tank.SPEED
		self.wheel = (self.wheel + 1) % 2
		self.make_within_screen()

	def make_within_screen(self):
		w = self.screen.get_width()
		h = self.screen.get_height()
		self.pos_x = max(0, min(w - self.size, self.pos_x))
		self.pos_y = max(0, min(h - self.size, self.pos_y))

	def draw(self):
		self.screen.blit(self.costumes[self.dir][self.wheel], (self.pos_x, self.pos_y))

	def fire(self):
		now = pg.time.get_ticks()
		if (self.fire_time == None or now - self.fire_time > 400):
			self.fire_time = now
			return Bullet(self.screen, self.resource, self.pos_x, self.pos_y, self.dir)
		return None

class Bullet:

	SPEED = 6
	SPEED_DICT = {
		'up': (0, -SPEED),
		'left': (-SPEED, 0),
		'down': (0, SPEED),
		'right': (SPEED, 0)
	}
	
	def __init__(self, screen, resource, x, y, dir):
		self.screen = screen
		self.resource = resource
		self.tank_size = resource.get_tank_size_scaled()
		self.size = resource.get_bullet_size_scaled(dir)
		self.w, self.h = self.size
		self.pos_x = x + (self.tank_size - self.w) / 2
		self.pos_y = y + (self.tank_size - self.h) / 2
		self.costumes = resource.get_bullet_costumes(dir)
		self.speed = Bullet.SPEED_DICT[dir]

		self.resource.play_fire_sound()
		for key in self.costumes.keys():
			if self.costumes[key] and key == 'original':
				c = self.costumes[key]
				self.costumes[key] = pg.transform.scale(c, self.size)

		self.state = "original"

	def type(self):
		return "BULLET"

	def finished(self):
		return self.state == "finished"

	def position(self):
		return (self.pos_x, self.pos_y, self.w, self.h)

	def hit_tank(self):
		self.resource.play_hit_tank_sound()
		self.state = "finished"

	def hit_wall(self):
		self.resource.play_hit_wall_sound()
		self.state = "finished"

	def hit_nothing(self):
		self.resource.play_hit_nothing_sound()
		self.state = "finished"

	def draw(self):
		if not self.finished():
			dx, dy = self.speed
			self.pos_x += dx
			self.pos_y += dy
			self.screen.blit(self.costumes[self.state], (self.pos_x, self.pos_y))

class Game:

	def __init__(self):
		pg.mixer.pre_init()
		pg.init()
		pg.mixer.init()
		pg.key.set_repeat(30)
		self.clock = pg.time.Clock()
		self.screen = pg.display.set_mode((800, 600))
		self.resource = Resource()

		self.sprite_queue = []
		self.my_tank = Tank(self.screen, self.resource)
		self.sprite_queue.append(self.my_tank)

	def run(self):
		screen_w, screen_h = self.screen.get_size()
		while True:
			self.clock.tick(100)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					sys.exit()
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						sys.exit()
					if event.key == pg.K_UP:
						self.my_tank.move_up()
					elif event.key == pg.K_LEFT:
						self.my_tank.move_left()
					elif event.key == pg.K_DOWN:
						self.my_tank.move_down()
					elif event.key == pg.K_RIGHT:
						self.my_tank.move_right()
					elif event.key == pg.K_SPACE:
						bullet = self.my_tank.fire()
						if bullet:
							self.sprite_queue.append(bullet)

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
