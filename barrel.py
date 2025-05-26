import random
import pygame
import constants as c
import gameobject as go


def is_barrel_lucky(probability):
	if random.randint(1, 100) < probability:
		return True
	return False


class Barrel(go.GameObject):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.image = c.BARREL
		self.mask = pygame.mask.from_surface(self.image)
		self.previous_health = 0
		self.health_min = c.BARRELHEALTHMIN
		self.health_max = c.BARRELHEALTHMAX
		self.hit_label_counter = 0
		self.hit_label_points = 7
		self.explosion_image = None
		self.has_rifle = False
		self.has_tank = False
		self.has_heart = False

	def move(self, velocity):
		self.y += velocity + random.randint(0, 1)

	def display_hit_label(self, window, size):
		barrel_font = pygame.font.SysFont(c.FONT, size)
		barrel_label = barrel_font.render(str(self.health), True, (7, 7, 7))
		label_pos_x = self.x + (self.get_width() - barrel_label.get_width()) / 2
		label_pos_y = self.y + (self.get_height() - barrel_label.get_height()) / 2
		window.blit(barrel_label, (label_pos_x, label_pos_y))

	def hit_label(self, window):
		if self.hit_label_counter == 0:
			self.display_hit_label(window, 40)
		elif self.hit_label_counter < self.hit_label_points:  # This needs to decrease as the game speeds up
			window.blit(self.explosion_image, (self.x - 20, self.y + 10))
			self.display_hit_label(window, 50)
			self.hit_label_counter += 1
		else:
			self.hit_label_counter = 0
			self.explosion_image = c.random_explosion()

		if self.health != self.previous_health:
			self.display_hit_label(window, 55)
			self.previous_health = self.health
			self.hit_label_counter += 1

	def draw(self, window):
		super().draw(window)

		if self.has_heart:
			self.has_tank = False
			self.has_rifle = False
		if self.has_rifle:
			self.has_heart = False
			self.has_tank = False
		if self.has_tank:
			self.has_heart = False
			self.has_rifle = False

		if self.has_rifle:
			window.blit(c.RIFLE, (self.x + 11, self.y + 13))
		if self.has_heart:
			window.blit(c.HEART, (self.x + 29, self.y + 23))
		if self.has_tank:
			window.blit(c.BARRELTANK, (self.x + 35, self.y + 15))

		if self.health > 0:
			self.hit_label(window)
