###############################################################################
## All of the important coding done here was done by Gabriel Ortega-Gingrich ##
###############################################################################

# ^-- Unfortunately, he didn't realize that sound_id is a string (despite the comments) and not an actual sound clip.

# dictionary of sound files
# key should be string, value should be a pygame sound clip
sound_library = {}
def loadSound(filepath):
	# generate sound id
	# load filepath
	# ...
	sound_library[sound_id] = loaded_sound
	return sound_id

def unloadSounds():
	sound_library.clear()

# keys are strings, values are filepaths.
track_library = {}
def loadTrack(track_id, filepath):
	track_library[track_id] = filepath
	return track_id


def playSound(sound_id,loop,maxtim):
	""" Plays the sound with the given string id """
    sound_library[sound_id].play(loops=loop,maxtime=maxtim)
	
def isSoundPlaying():
	""" Returns true if the sound with the id is playing """
    pygame.mixer.get_busy()

def stopSound(sound_id):
	""" Stops the sound if it is playing, or does nothing if it is not """
    sound_library[sound_id].stop()

def playTrack(track_id,loop):
	""" Plays the music track with the given string id """
    pygame.mixer.music.load(track_id)
    pygame.mixer.music.play(loops=loop)

def isTrackPlaying():
	""" Returns true if the track id is playing """
    pygame.mixer.music.get_busy() # can't more than one be going at once?

def stopTrack(track_id):
	""" Stops the given track """
    pygame.mixer.music.stop() # I only want to stop this one, not all of them!

def fadeOutTrack(track_id, time):
	""" If the given id is playing, it fades out the track
		over the given time interval (in ms) """
    track_id.fadeout(time)

def stopAllTracks():
	""" Stops all the playing tracks """
    pygame.mixer.music.stop()

def fadeOutAllTracks(time):
	""" Fades out all playing tracks over the given time interval (ms) """
    pygame.mixer.fadeout(time)

def stopAllSounds():
	""" Stops all playing sounds """
    pygame.mixer.stop()
