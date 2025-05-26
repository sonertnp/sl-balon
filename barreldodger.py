import pygame
import streamlit as st
import random
import barrel as ba
import collision
import constants as c
import player as pl
import sound
import shelve


def get_hiscore():
	d = shelve.open('hiscore')
	score = d['score']
	d.close()
	return score


hi_score = get_hiscore()
is_inside_hover_area = False


def set_hiscore(score):
	global hi_score
	if score > hi_score:
		hi_score = score
		d = shelve.open('hiscore')
		d['score'] = score
		d.close()


def main():
	running = True
	fps = c.FPS
	barrels = []
	barrel_velocity = c.BARRELSPEED
	player_velocity = c.PLAYERSPEED
	level = 0
	wave = 0
	clock = pygame.time.Clock()
	main_font = pygame.font.SysFont(c.FONT, 16)
	lost_font = pygame.font.SysFont(c.FONT, 80)

	player = pl.Player(c.HANDGUNPOSX, c.HANDGUNPOSY)

	lost = False
	gameover_counter = 0

	def draws():
		if player.attack_type == pl.AttackType.TANK:
			player.walk_tank()
		elif player.attack_type == pl.AttackType.RIFLE:
			player.walk_rifle()
		else:
			player.walk_handgun()
		WIN.blit(c.BG, (0, 0))
		player.draw(WIN)

		if c.DEBUGMODEON:
			pygame.draw.rect(WIN, (255, 0, 0), pygame.Rect(player.x, player.y, player.image.get_width(),
														   player.image.get_height()), 1)
			for bullet in player.bullets:
				pygame.draw.rect(WIN, (0, 0, 255), pygame.Rect(bullet.x, bullet.y, bullet.image.get_width(),
															   bullet.image.get_height()), 1)

		for barrel in barrels:
			barrel.draw(WIN)
			if c.DEBUGMODEON:
				pygame.draw.rect(WIN, (0, 255, 0), pygame.Rect(barrel.x, barrel.y, barrel.image.get_width(),
															   barrel.image.get_height()), 1)

		wave_label = main_font.render("WAVE: %s" % wave, True, (5, 5, 5))
		WIN.blit(wave_label, (15, 45))

		score_label = main_font.render("SCORE: %s" % player.score, True, (5, 5, 5))
		WIN.blit(score_label, (15, 25))

		global hi_score
		current_hiscore = hi_score
		if player.score >= hi_score:
			current_hiscore = player.score

		hiscore_label = main_font.render("HI SCORE: %s" % current_hiscore, True, (5, 5, 5))
		WIN.blit(hiscore_label, (15, 5))

		if lost:
			set_hiscore(player.score)

			gameover = lost_font.render("GAME OVER!", True, (200, 0, 0))
			WIN.blit(gameover,
					 (int(c.WIDTH / 2 - (gameover.get_width() / 2)),
					  int(c.HEIGHT / 2 - (gameover.get_height() / 2)) - 50))

		pygame.display.update()

	def create_barrel(x):
		new_barrel = ba.Barrel(x, 0)
		new_barrel.health = random.randrange(new_barrel.health_min, new_barrel.health_max)
		new_barrel.previous_health = new_barrel.health
		new_barrel.explosion_image = c.random_explosion()
		new_barrel.has_rifle = ba.is_barrel_lucky(50)
		new_barrel.has_tank = ba.is_barrel_lucky(50)
		new_barrel.has_heart = ba.is_barrel_lucky(50)
		barrels.append(new_barrel)

	while running:
		clock.tick(fps)
		draws()

		if player.health <= 0:
			if gameover_counter == 0:
				sound.play_gameover_sound()
			lost = True
			if lost:
				gameover_counter += 1
				if gameover_counter >= fps * 4:
					sound.play_menu_song()
					running = False
				else:
					continue

		if len(barrels) == 0:
			wave += 1

			if wave % 5 == 0:
				barrel_velocity += c.BARRELSPEEDINCREASE
				level += 1
				if player.attack_type != pl.AttackType.TANK:
					player.cool_down_points -= c.PLAYERCOOLDOWNDECREASE

			create_barrel(13)
			create_barrel(27 + c.BARRELWIDTH)
			create_barrel(54 + 2 * c.BARRELWIDTH)
			create_barrel(73 + 3 * c.BARRELWIDTH)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sound.play_menu_song()
				running = False

		keys = pygame.key.get_pressed()

		if keys[pygame.K_LEFT] and player.x > -15:
			player.x -= player_velocity
		if keys[pygame.K_RIGHT] and player.x < 505:
			player.x += player_velocity

		for gone_barrel in barrels:
			gone_barrel.move(barrel_velocity)  # comment this line to prevent barrels moving

			if collision.collide(gone_barrel, player):
				player.health -= c.BARRELDAMAGE
				if player.health > 0:
					sound.play_human_hit_sound()
					player.bleeding = True
					player.blood_image = c.random_blood()
					player.bleeding_counter = 0
				else:
					sound.play_human_death_sound()

				barrels.remove(gone_barrel)

			if gone_barrel.y > c.HEIGHT:
				barrels.remove(gone_barrel)

		player.move_bullets(barrels)


def start_button():
	sg_button = c.SG
	pos = pygame.mouse.get_pos()
	sg_x = int(c.WIDTH / 2 - c.SG.get_width() / 2)
	sg_y = int(c.HEIGHT / 2 - c.SG.get_height() / 2) + 250
	sg_rect = pygame.Rect(sg_x, sg_y, c.SG.get_width(), c.SG.get_height())
	colliding = False
	global is_inside_hover_area
	if sg_rect.collidepoint(pos):
		pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
		if not is_inside_hover_area:
			sound.play_hover_sound()
			is_inside_hover_area = True
		sg_button = c.SGHVR
		colliding = True
	else:
		is_inside_hover_area = False
		pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

	WIN.blit(sg_button, (sg_x, sg_y))
	return colliding


def menu():
	sound.play_menu_song()
	running = True

	while running:
		WIN.blit(c.BGMENU, (0, 0))
		WIN.blit(c.LOGO, (int(c.WIDTH / 2 - c.LOGO.get_width() / 2), int(c.HEIGHT / 2 - c.LOGO.get_height() / 2) - 130))

		is_startable = start_button()

		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN and is_startable:
				sound.play_main_song()
				main()

	pygame.quit()


st.title("Barrel Dodger")

if st.button("Oyunu Başlat", icon="🎈", use_container_width=True):
	WIN = pygame.display.set_mode((c.WIDTH, c.HEIGHT))

	pygame.font.init()
	pygame.display.set_caption(c.CAPTION)
	pygame.display.set_icon(c.BARREL)

	menu()
