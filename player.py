import random
import pygame
import constants as c
import bullet as b
import gameobject as go
import sound
import enum


class AttackType(enum.Enum):
	HANDGUN = 1
	RIFLE = 2
	TANK = 3


class Player(go.GameObject):
	walk_number = 1

	def __init__(self, x, y):
		super().__init__(x, y)
		self.image = c.HANDGUN0
		self.attack_type = None
		self.bullet_img = c.BULLETHANDGUN
		self.max_health = 100
		self.mask = pygame.mask.from_surface(self.image)
		self.cool_down_counter = 0
		self.cool_down_points = c.COOLDOWN
		self.bullets = []
		self.score = 0
		self.blood_image = None
		self.bleeding = False
		self.bleeding_counter = 0
		self.bleeding_points = 5
		self.bullet_velocity = c.HANDGUNBULLETSPEED
		self.tank_duration = 0

	def change_attack_type(self, attack_type):
		self.attack_type = attack_type
		if attack_type == AttackType.RIFLE:
			self.y = c.RIFLEPOSY
			self.bullet_velocity = c.RIFLEBULLETSPEED
			self.bullet_img = c.BULLETRIFLE
			self.cool_down_points = c.RIFLECOOLDOWN
		elif attack_type == AttackType.TANK:
			self.y = c.TANKPOSY
			self.bullet_velocity = c.TANKBULLETSPEED
			self.bullet_img = c.BULLETTANK
			self.cool_down_points = c.TANKCOOLDOWN
		else:
			self.y = 705
			self.bullet_velocity = c.HANDGUNBULLETSPEED
			self.bullet_img = c.BULLETHANDGUN
			self.cool_down_points = c.COOLDOWN

	def draw(self, window):
		window.blit(self.image, (self.x, self.y))
		self.health_bar(window)
		for bullet in self.bullets:
			bullet.draw(window)
		if self.bleeding and self.bleeding_counter < self.bleeding_points:
			window.blit(self.blood_image, (self.x - 8, self.y - 10))
			self.bleeding_counter += 1
		else:
			self.bleeding_counter = 0
			self.bleeding = False

	def shoot(self):
		if self.cool_down_counter == 0:
			if self.attack_type == AttackType.TANK:
				sound.play_minigun_sound()
				bullet = b.Bullet(self.x + random.randint(52, 62), self.y - 30, self.bullet_img)
				self.bullets.append(bullet)
			elif self.attack_type == AttackType.RIFLE:
				sound.play_rifle_sound()
				bullet = b.Bullet(self.x + 57, self.y - 24, self.bullet_img)
				self.bullets.append(bullet)
			else:
				sound.play_handgun_sound()
				bullet = b.Bullet(self.x + 61, self.y - 24, self.bullet_img)
				self.bullets.append(bullet)

	def cool_down(self):
		if self.cool_down_counter >= self.cool_down_points:
			self.cool_down_counter = 0
		else:
			self.cool_down_counter += 1

	def move_bullets(self, with_objects):
		self.cool_down()
		for bullet in self.bullets:
			bullet.move(self.bullet_velocity)

			if bullet.off_screen(c.HEIGHT):
				self.bullets.remove(bullet)
			else:
				for with_object in with_objects:
					if bullet.detect_collision(with_object):
						sound.play_barrel_hit_sound()
						with_object.health -= 1
						self.score += 1
						if bullet in self.bullets:
							self.bullets.remove(bullet)
						if with_object.health == 0:
							if with_object.has_tank:
								self.change_attack_type(AttackType.TANK)
							elif with_object.has_heart and self.health < 100:
								self.health += c.HEALTHRESTORE
							if with_object.has_rifle:
								self.change_attack_type(AttackType.RIFLE)
							sound.play_barrel_break_sound()
							with_objects.remove(with_object)

	def health_bar(self, window):
		pygame.draw.rect(window, (255, 0, 0), (0, c.HEIGHT - c.HBHEIGHT, c.WIDTH, c.HBHEIGHT))
		pygame.draw.rect(window, (0, 255, 0),
						 (0, c.HEIGHT - c.HBHEIGHT, int(c.WIDTH * (self.health / self.max_health)), c.HBHEIGHT))

	def walk_handgun(self):
		self.walk(c.HANDGUN0, c.HANDGUN1, c.HANDGUN2)

	def walk_rifle(self):
		self.walk(c.RIFLE0, c.RIFLE1, c.RIFLE2)

	def walk(self, gun0, gun1, gun2):
		if self.health <= 0:
			self.image = c.SKULL
			return

		self.shoot()

		self.walk_number = (self.walk_number + 1) % 30
		if self.walk_number < 10:
			self.image = gun0
		elif self.walk_number < 20:
			self.image = gun1
		else:
			self.image = gun2

	def walk_tank(self):
		if self.health <= 0:
			self.image = c.SKULL
			return

		self.shoot()

		self.tank_duration += 1

		if self.tank_duration == c.TANKDURATION:
			self.tank_duration = 0
			self.change_attack_type(AttackType.HANDGUN)

		self.walk_number = (self.walk_number + 1) % 40
		if self.walk_number < 5:
			self.image = c.TANKFLAMELEFT
		elif self.walk_number < 10:
			self.image = c.TANK
		elif self.walk_number < 15:
			self.image = c.TANKFLAMEMIDDLE
		elif self.walk_number < 20:
			self.image = c.TANK
		elif self.walk_number < 25:
			self.image = c.TANKFLAMERIGHT
		elif self.walk_number < 30:
			self.image = c.TANK
		elif self.walk_number < 35:
			self.image = c.TANKFLAMEMIDDLE
		else:
			self.image = c.TANK
