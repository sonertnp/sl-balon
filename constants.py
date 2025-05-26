import os
import pygame
import random

DEBUGMODEON = False
WIDTH = 600
HEIGHT = 800
HBHEIGHT = 5
BARRELDAMAGE = 50
HEALTHRESTORE = 10
COOLDOWN = 30
RIFLECOOLDOWN = 15
TANKDURATION = 900
CAPTION = "Barrel Dodger"
FONT = "rockwell"
FPS = 60
HANDGUNPOSX = 240
HANDGUNPOSY = 705
RIFLEPOSY = 677
TANKPOSY = 640
PLAYERSPEED = 5
HANDGUNBULLETSPEED = -11
RIFLEBULLETSPEED = -21
TANKBULLETSPEED = -27
BARRELSPEED = 1
BARRELSPEEDINCREASE = 0.75
PLAYERCOOLDOWNDECREASE = 5
TANKCOOLDOWN = 6
BG = pygame.image.load(os.path.join("images", "background.jpg"))
BGMENU = pygame.image.load(os.path.join("images", "backgroundmenu.jpg"))
LOGO = pygame.image.load(os.path.join("images", "logo.png"))
SG = pygame.image.load(os.path.join("images", "startgame.png"))
SGHVR = pygame.image.load(os.path.join("images", "startgamehover.png"))
BARREL = pygame.image.load(os.path.join("images", "s_barrel_0.png"))
BARRELTANK = pygame.image.load(os.path.join("images", "tank.png"))
SKULL = pygame.image.load(os.path.join("images", "skull.png"))
HEART = pygame.image.load(os.path.join("images", "heart.png"))
RIFLE = pygame.image.load(os.path.join("images", "rifle.png"))
BULLETHANDGUN = pygame.image.load(os.path.join("images", "bullets", "bullet_handgun.png"))
BULLETRIFLE = pygame.image.load(os.path.join("images", "bullets", "bullet_rifle.png"))
BULLETTANK = pygame.image.load(os.path.join("images", "bullets", "bullet_tank.png"))
HANDGUN0 = pygame.image.load(os.path.join("images", "attackers", "survivor-shoot_handgun_0.png"))
HANDGUN1 = pygame.image.load(os.path.join("images", "attackers", "survivor-shoot_handgun_1.png"))
HANDGUN2 = pygame.image.load(os.path.join("images", "attackers", "survivor-shoot_handgun_2.png"))
RIFLE0 = pygame.image.load(os.path.join("images", "attackers", "survivor-shoot_rifle_0.png"))
RIFLE1 = pygame.image.load(os.path.join("images", "attackers", "survivor-shoot_rifle_1.png"))
RIFLE2 = pygame.image.load(os.path.join("images", "attackers", "survivor-shoot_rifle_2.png"))
TANKFLAMELEFT = pygame.image.load(os.path.join("images", "attackers", "tank_flame_left.png"))
TANKFLAMEMIDDLE = pygame.image.load(os.path.join("images", "attackers", "tank_flame_middle.png"))
TANKFLAMERIGHT = pygame.image.load(os.path.join("images", "attackers", "tank_flame_right.png"))
TANK = pygame.image.load(os.path.join("images", "attackers", "tank.png"))
BARRELWIDTH = BARREL.get_width()
BARRELHEALTHMIN = 5
BARRELHEALTHMAX = 15


def random_explosion():
	return pygame.image.load(os.path.join("images", "explosions", "explosion%s.png" % str(random.randint(1, 9))))


def random_blood():
	return pygame.image.load(os.path.join("images", "blood", "blood%s.png" % str(random.randint(1, 4))))
