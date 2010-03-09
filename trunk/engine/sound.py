# ... means you need to code something


def playSound(sound_id,loop,maxtim):
	""" Plays the sound with the given string id """
    sound_id.play(loops=loop,maxtime=maxtim)
	
def isSoundPlaying():
	""" Returns true if the sound with the id is playing """
    pygame.mixer.get_busy()

def stopSound(sound_id):
	""" Stops the sound if it is playing, or does nothing if it is not """
    sound_id.stop()

def playTrack(track_id,loop):
	""" Plays the music track with the given string id """
	# ... The implementation of this should be
	#     different than playSound() because it is bad to load
	#	  a whole track into memory, so it must be streamed.
    pygame.mixer.music.load(track_id)
    pygame.mixer.music.play(loops=loop)

def isTrackPlaying():
	""" Returns true if the track id is playing """
    pygame.mixer.music.get_busy()

def stopTrack(track_id):
	""" Stops the given track """
    pygame.mixer.music.stop()

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
