import os, sys

player = None
current_level = None
imageLoader = None
ent_currentid = 0
game_entities = {}
seq_currentid = 0
anim_sequences = {}
sprites = {}
gravity = 386 # 9.8 m/s, according to the art team's scale
camy = 0 # vertical camera offset to be reset each time a room is loaded.
seconds_passed = 0 # time passed in the last frame
game_time = 0 # seconds passed during the whole game

dir_up = 1
dir_down = 10
dir_left = 2
dir_right = 20
dir_upleft = dir_up + dir_left
dir_downleft = dir_down + dir_left
dir_upright = dir_up + dir_right
dir_downright = dir_down + dir_right

flags = {"input left": False, "input right": False}

def fullPath(path):
	return os.path.join(os.path.normpath(sys.path[0]+'/..'), path)