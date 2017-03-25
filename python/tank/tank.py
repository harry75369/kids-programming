import sys
import pygame as pg

SPRITE_SZ = 64

class Tank:

	def __init__(self, screen):
		resource = pg.image.load("images/resource.bmp")
		resource.set_palette([
			pg.Color(0,0,0,255), pg.Color(104,104,0,255), pg.Color(231,156,33,255), pg.Color(231,231,148,255)
		])
		self.screen = screen
		self.pos_x = (screen.get_width() - SPRITE_SZ) / 2
		self.pos_y = (screen.get_height() - SPRITE_SZ) / 2
		self.costumes = {
			'up':    [resource.subsurface(pg.Rect(0, 0, SPRITE_SZ, SPRITE_SZ)), resource.subsurface(pg.Rect(64, 0, SPRITE_SZ, SPRITE_SZ))],
			'left':  [resource.subsurface(pg.Rect(128, 0, SPRITE_SZ, SPRITE_SZ)), resource.subsurface(pg.Rect(192, 0, SPRITE_SZ, SPRITE_SZ))],
			'down':  [resource.subsurface(pg.Rect(256, 0, SPRITE_SZ, SPRITE_SZ)), resource.subsurface(pg.Rect(320, 0, SPRITE_SZ, SPRITE_SZ))],
			'right': [resource.subsurface(pg.Rect(384, 0, SPRITE_SZ, SPRITE_SZ)), resource.subsurface(pg.Rect(448, 0, SPRITE_SZ, SPRITE_SZ))]
		}
		self.dir = 'up'
		self.wheel = 0
		self.speed = 5
		self.time = None
		for costumes in self.costumes.values():
			costumes[0].set_colorkey(pg.Color("black"))
			costumes[1].set_colorkey(pg.Color("black"))

	def move_up(self):
		self.dir = 'up'
		self.pos_y -= self.speed
		self.wheel = (self.wheel + 1) % 2
		self.make_within_screen()

	def move_left(self):
		self.dir = 'left'
		self.pos_x -= self.speed
		self.wheel = (self.wheel + 1) % 2
		self.make_within_screen()

	def move_down(self):
		self.dir = 'down'
		self.pos_y += self.speed
		self.wheel = (self.wheel + 1) % 2
		self.make_within_screen()

	def move_right(self):
		self.dir = 'right'
		self.pos_x += self.speed
		self.wheel = (self.wheel + 1) % 2
		self.make_within_screen()

	def make_within_screen(self):
		w = self.screen.get_width()
		h = self.screen.get_height()
		self.pos_x = max(0, min(w - SPRITE_SZ, self.pos_x))
		self.pos_y = max(0, min(h - SPRITE_SZ, self.pos_y))

	def draw(self):
		self.screen.blit(self.costumes[self.dir][self.wheel], (self.pos_x, self.pos_y))

	def fire(self):
		time = pg.time.get_ticks()
		if (self.time == None or time - self.time > 400):
			self.time = time
			return Bullet(self.screen, self.pos_x, self.pos_y, self.dir)
		return None

class Bullet:

	def __init__(self, screen, x, y, dir):
		resource = pg.image.load("images/resource.bmp")
		resource.set_palette_at(2, pg.Color(182,182,182,255))
		costume_dict = {
			'up': pg.Rect(268, 856, 12, 16),
			'left': pg.Rect(296, 856, 16, 12),
			'down': pg.Rect(332, 856, 12, 16),
			'right': pg.Rect(360, 856, 16, 12)
		}
		speed = 6
		speed_dict = {
			'up': (0, -speed),
			'left': (-speed, 0),
			'down': (0, speed),
			'right': (speed, 0)
		}
		isHorizontal = dir == 'left' or dir == 'right';
		self.screen = screen
		self.pos_x = x + (SPRITE_SZ - (16 if isHorizontal else 12)) / 2
		self.pos_y = y + (SPRITE_SZ - (12 if isHorizontal else 16)) / 2
		self.costume = resource.subsurface(costume_dict[dir])
		self.speed = speed_dict[dir]
		self.costume.set_colorkey(pg.Color("black"))
		self.fire_sound = pg.mixer.Sound('sounds/fire.wav')
		self.hit_tank_sound = pg.mixer.Sound('sounds/hit_tank.wav')
		self.hit_wall_sound = pg.mixer.Sound('sounds/hit_wall.wav')
		self.hit_nothing_sound = pg.mixer.Sound('sounds/hit_nothing.wav')
		self.fire_sound.play()

	def hit_tank(self):
		pass

	def hit_wall(self):
		pass

	def hit_nothing(self):
		pass

	def draw(self):
		dx, dy = self.speed
		self.pos_x += dx
		self.pos_y += dy
		self.screen.blit(self.costume, (self.pos_x, self.pos_y))


class Game:

	def __init__(self):
		pg.mixer.pre_init()
		pg.init()
		pg.mixer.init()
		pg.key.set_repeat(30)
		self.clock = pg.time.Clock()
		self.screen = pg.display.set_mode((800, 600))
		self.sprites = []

		self.my_tank = Tank(self.screen)
		self.sprites.append(self.my_tank)

	def run(self):
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
							self.sprites.append(bullet)

			self.screen.fill(pg.Color("black"))
			for sprite in self.sprites:
				sprite.draw()
			pg.display.flip()

if __name__ == "__main__":                
	game = Game()
	game.run()
