import xml.dom.minidom
import graphwrap
import os.path
import t12

def load(fname):
    if not hasattr(t12, "sprites"): t12.sprites = {}
    doc = xml.dom.minidom.parse(fname)
    spritelist = self.doc.getElementsByTagName("spritelist")
    relative = bool(int(spritelist.getAttribute("relative").value))
    for spriteNode in spritelist.getElementsByTagName("sprite"):
        sprite = graphwrap.AnimSprite()
        sprName = spriteNode.getAttribute("name")
        defaultSeq = spriteNode.getAttribute("default")
        for sequenceNode in spriteNode.getElementsByTagName("sequence"):
            duration = float(sequenceNode.getAttribute("duration"))
            seqName = sequenceNode.getAttribute("name")
            flipx, flipy = bool(int(sequenceNode.getAttribute("flipx"))),\
                           bool(int(sequenceNode.getAttribute("flipy")))
            loop = bool(int(sequenceNode.getAttribute("loop")))
            frames = [node.firstChild.data for node in sequenceNode.getElementsByTagName("frame")]
            # I like list comprehensions :-)
            if relative:
                base = os.path.split(fname)[0]
                frames = [os.path.normpath(os.path.join(f, base)) for f in frames]
            sprite.putSequence(seqName, graphwrap.AnimSequence(frames, duration, False, flipx, flipy, loop))
        sprite.runSequence(defaultSeq)
        t12.sprites[sprName] = sprite
