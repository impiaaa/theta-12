import pygame
from pgu import gui

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
		
		t = gui.Table()
		t.tr()
		nt = gui.Table()
		nt.tr()
		nt.td(gui.Image(pygame.image.load("/Users/impiaaa/Downloads/theta-12/global/sprites/Velociraptor2.png")), rowspan=3)
		nt.td(gui.Input("Foo Monster", width=192), align=1)
		nt.tr()
		nt.td(gui.Label("0"), align=-1)
		nt.tr()
		nt.td(LabeledCheckbox("Invisible"), align=-1)
		nt.tr()
		t.td(nt, align=-1)
		
		t.tr()
		t.td(gui.Label("Attributes"), align=-1)
		t.tr()
		l = gui.List(272, 80)
		l.add("health = 4")
		l.add("stage = 9")
		t.td(l, align=-1) # These dimensions could be dynamic

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

class LevelEditor(gui.App):
	def __init__(self):
		gui.App.__init__(self)
		
		self.connect(gui.QUIT, self.quit, None)
		self.library = Library()
		self.baseEntityEditor = BaseEntityEditor()
		self.t = gui.Table()
		self.t.tr()
		self.t.td(self.library)
		self.t.td(self.baseEntityEditor)

app = LevelEditor()
app.run(app.t)