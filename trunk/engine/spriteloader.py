import xml.dom.mindom
import graphwrap

def load(fname):
	doc = xml.dom.minidom.parse(fname)
	spritelist = self.doc.getElementsByNodeName("spritelist")
	relative = bool(int(spritelist.attributes["relative"].value))
	for sprite in spritelist.getElementsByNodeName("sprite"):
		name = sprite.attributes["name"].value
		default = sprite.attributes["default"].value
		for sequence in sprite.getElementsByNodeName("sequence"):
			duration = float(sequence.attributes["duration"].value)
			name = sequence.attributes["name"].value
			attrs

# note to spencer:
# 	if the spritelist.relative="1", the path should be converted to an absolute path.
#	If a spritelist is relative, the paths are relative to the directory the .xml file is in.

def create_seq(framepaths, duration, looping, flipx, flipy):
	return graphwrap.AnimSequence(framepaths, duration, False, flipx, flipy, looping)
