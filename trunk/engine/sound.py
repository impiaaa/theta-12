# ... means you need to code something


def playSound(sound_id):
	""" Plays the sound with the given string id """
	# ...

def isSoundPlaying(sound_id):
	""" Returns true if the sound with the id is playing """
	# ...

def stopSound(sound_id):
	""" Stops the sound if it is playing, or does nothing if it is not """
	# ...

def playTrack(track_id):
	""" Plays the music track with the given string id """
	# ... The implementation of this should be
	#     different than playSound() because it is bad to load
	#	  a whole track into memory, so it must be streamed.

def isTrackPlaying(track_id):
	""" Returns true if the track id is playing """
	# ...

def stopTrack(track_id):
	""" Stops the given track """
	# ...

def fadeOutTrack(track_id, time):
	""" If the given id is playing, it fades out the track
		over the given time interval (in ms) """
	# ...

def stopAllTracks():
	""" Stops all the playing tracks """
	# ...

def fadeOutAllTracks(time):
	""" Fades out all playing tracks over the given time interval (ms) """
	# ...

def stopAllSounds():
	""" Stops all playing sounds """
	# ...
