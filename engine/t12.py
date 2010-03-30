player = None
current_level = None
imageLoader = None
ent_currentid = 0
game_entities = {}
seq_currentid = 0
anim_sequences = {}
gravity = 386 # 9.8 m/s, according to the art team's scale
camy = 0 # vertical camera offset to be reset each time a room is loaded.
seconds_passed = 0

flags = {"input left": False, "input right": False}
