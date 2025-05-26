import os
import random
import pygame

MENU = os.path.join("sounds", "menu.ogg")
SONG = os.path.join("sounds", "Jungle.mp3")
MINIGUN = os.path.join("sounds", "minigun.ogg")
PISTOL = os.path.join("sounds", "pistol.ogg")
RIFLE = os.path.join("sounds", "rlauncher.ogg")
HOVER = os.path.join("sounds", "Menu Selection Click.wav")
GAMEOVER = os.path.join("sounds", "game_over_bad_chest.wav")
BARRELBREAK = os.path.join("sounds", "barrelbreak.ogg")

pygame.mixer.init()


def play_song(song, volume=1.0):
	music = pygame.mixer.music
	music.load(song)
	music.play()
	music.set_volume(volume)


def play_sound(sound, volume=1.0):
	effect = pygame.mixer.Sound(sound)
	effect.play()
	effect.set_volume(volume)


def play_menu_song():
	play_song(MENU, 0.2)


def play_main_song():
	play_song(SONG)


def play_handgun_sound():
	play_sound(PISTOL, 0.1)


def play_rifle_sound():
	play_sound(RIFLE, 0.1)


def play_minigun_sound():
	play_sound(MINIGUN, 0.1)


def play_hover_sound():
	play_sound(HOVER)


def play_barrel_hit_sound():
	sound_path = os.path.join("sounds", "click.%s.ogg" % str(random.randint(1, 10)))
	play_sound(sound_path, 0.5)


def play_human_hit_sound():
	sound_path = os.path.join("sounds", "humanYell%s.wav" % str(random.randint(1, 5)))
	play_sound(sound_path, 2)


def play_human_death_sound():
	sound_path = os.path.join("sounds", "humanDeath%s.wav" % str(random.randint(1, 2)))
	play_sound(sound_path, 1.7)


def play_barrel_break_sound():
	play_sound(BARRELBREAK, 1.5)


def play_gameover_sound():
	pygame.mixer.music.stop()
	play_sound(GAMEOVER, 0.8)
