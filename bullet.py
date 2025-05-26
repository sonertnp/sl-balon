import random
import pygame
import collision


class Bullet:
	def __init__(self, x, y, img):
		self.x = x
		self.y = y
		self.image = img
		self.mask = pygame.mask.from_surface(self.image)

	def move(self, velocity):
		self.y += velocity
		if random.randint(1, 15) < 2:
			self.x += random.randint(-1, 1)

	def draw(self, window):
		window.blit(self.image, (self.x, self.y))

	def detect_collision(self, with_object):
		return collision.collide(with_object, self)

	def off_screen(self, height):
		return not (height >= self.y >= 0)
