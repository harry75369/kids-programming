import sys
import pygame


pygame.init()
surface = pygame.display.set_mode((400,300))
pygame.display.set_caption('Hello World!')
surface.fill((0, 0, 255))


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.flip()