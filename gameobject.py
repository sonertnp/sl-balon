class GameObject:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.health = 100
		self.image = None

	def draw(self, window):
		window.blit(self.image, (self.x, self.y))

	def get_width(self):
		return self.image.get_width()

	def get_height(self):
		return self.image.get_height()
