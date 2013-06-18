import pygame
from pygame.locals import *
from pgu import gui
import sys
# pathackery
sys.path += [sys.path[0][:sys.path[0].rfind('/')]]
sys.path += [sys.path[-1]+'/engine']
# we should fix this at some point by making everything a package
import t12
import entities, spriteloader, main

class LabeledCheckbox(gui.Table):
	def __init__(self, label, value=False, parent=None):
		gui.Table.__init__(self)
		self.tr()
		self.parent = parent
		def getind(box, n):
			if box.parent == None:
				return n
			else:
				return getind(box.parent, n+1)
		self.td(gui.Spacer(17*getind(self, 0), 1))
		self.switch = gui.Switch(value)
		self.td(self.switch)
		self.td(gui.Spacer(4, 1))
		self.label = gui.Label(label)
		self.td(self.label)
		if parent:
			self.parent.children.append(self)
		self.children = []
		self.connect(gui.CLICK, self.toggleChildren)
	def toggleChildren(self):
		for c in self.children:
			c.toggleChildren()
			c.disabled = self.switch.value
			c.repaintall()

class Library(gui.Table):
	def __init__(self, **params):
		params.setdefault('cls', 'dialog')
		gui.Table.__init__(self, **params)
		
		t = gui.Table()
		t.tr()
		g = gui.Group(value=0)
		g.connect(gui.CHANGE, self.changeTab)
		tt = gui.Table()
		tt.tr()
		tt.td(gui.Tool(g, gui.Label("Base Entities"), 0))
		tt.td(gui.Tool(g, gui.Label("Graphics"), 1))
		tt.td(gui.Tool(g, gui.Label("Behaviors"), 2))
		tt.td(gui.Tool(g, gui.Label("Markers"), 3))
		t.td(tt)
		
		t.tr()
		l = gui.List(348, 240)
		l.add("A Person")
		l.add("A Purple Person")
		l.add("Platform")
		l.add("Potato")
		l.add("Foo Monster")
		l.add("Boatcake")
		t.td(l)
		
		t.tr()
		tt = gui.Table()
		tt.tr()
		tt.td(gui.Button("New"), align=-1)
		tt.td(gui.Button("Edit"), align=-1)
		tt.td(gui.Button("Delete"), align=-1)
		tt.td(gui.Input("Search", width=168), align=1)
		t.td(tt)
		
		self.tr()
		self.td(gui.Label("Library"), cls=self.cls+'.bar', align=-1)
		self.tr()
		self.td(t, cls=self.cls+'.main')
	def changeTab(self):
		pass

class BaseEntityEditor(gui.Table):
	def __init__(self, **params):
		params.setdefault('cls', 'dialog')
		gui.Table.__init__(self, **params)
		if "entity" in params: self.entity = params["entity"]
	
	def layout(self):
		self.clear()
		t = gui.Table()
		t.tr()
		nt = gui.Table()
		nt.tr()
		self.im = gui.Image(self.entity.anim.sequences[self.entity.anim.sequences.keys()[0]].images[0])
		nt.td(self.im, rowspan=3)
		self.name = gui.Input(self.entity.name, width=192)
		self.name.connect(gui.CHANGE, self.change, self.name)
		nt.td(self.name, align=1)
		nt.tr()
		self.id = gui.Label(str(self.entity.id))
		nt.td(self.id, align=-1)
		nt.tr()
		self.invisible = LabeledCheckbox("Invisible")
		nt.td(self.invisible, align=-1)
		nt.tr()
		t.td(nt, align=-1)
		
		t.tr()
		t.td(gui.Label("Attributes"), align=-1)
		t.tr()
		self.attrList = gui.List(272, 80)
		self.attrList.add("health = 4")
		self.attrList.add("stage = 9")
		t.td(self.attrList, align=-1) # These dimensions could be dynamic

		t.tr()
		t.td(gui.Label("Groups"), align=-1)
		t.tr()
		gt = gui.Table()
		gt.tr()
		gt.td(LabeledCheckbox("Actors"), align=-1)
		gt.td(LabeledCheckbox("Geometry"), align=-1)
		gt.tr()
		gt.td(LabeledCheckbox("Background"), align=-1)
		gt.td(LabeledCheckbox("Activator"), align=-1)
		gt.tr()
		gt.td(LabeledCheckbox("Touch enemies"), align=-1)
		gt.td(LabeledCheckbox("Touch player"), align=-1)
		gt.tr()
		gt.td(LabeledCheckbox("Touch geometry"), align=-1)
		gt.td(LabeledCheckbox("Disruptive"), align=-1)
		t.td(gt)
				
		t.tr()
		t.td(gui.Label("Behaviors"), align=-1)
		#t.tr()
		#l = gui.List(272, 80)
		#l.add("Attack on sight")
		#l.add("Pace")
		#t.td(l, align=-1)

		self.tr()
		self.td(gui.Label("Base Entity"), cls=self.cls+'.bar', align=-1)
		self.tr()
		self.td(t, cls=self.cls+'.main')
	
	def change(self, widget):
		if widget == self.name: self.entity.name = widget.value

class PlayfieldWidget(gui.Widget):
	pass

class LevelEditor(gui.Desktop):
	def __init__(self, **params):
		gui.Desktop.__init__(self, **params)
		
		self.connect(gui.QUIT, self.quit, None)
	def init(self, *args, **params):
		gui.App.init(self, *args, **params)
		spriteloader.load("global.xml")

app = LevelEditor()
app.run(app.t)
