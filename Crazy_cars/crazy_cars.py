import pygame, random, time, math
from random import randint
from utils import scale_image, blit_rotate_center, blit_text_center
pygame.font.init()

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0,0,255)

GRASS = pygame.image.load("img/pasto1.png")
TRACK = pygame.image.load("img/fond.png")

TRACK_BORDER = pygame.image.load("img/fond_border.png")
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load("img/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (20,200)

RED_CAR = pygame.image.load("img/playerup.png")
GREEN_CAR = pygame.image.load("img/playerup.png")

WIDTH ,HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CRAZY CARS")

MAIN_FONT = pygame.font.SysFont("comicsans", 44)

PATH = [(22, 25), (1139, 536), (1138, 21), (29, 533), (568, 276), (568, 19), (566, 540), (249, 278), 
(878, 269), (235, 23), (887, 20), (891, 539), (232, 535), (11, 286), (1144, 271), (1034, 270), (725, 275), 
(400, 275), (119, 284), (114, 22), (395, 20), (728, 18), (1021, 19), (1028, 538), (726, 536), (391, 535), 
(116, 530), (65, 140), (181, 140), (330, 142), (473, 144), (640, 136), (820, 132), (956, 136), (1092, 131), 
(1089, 394), (972, 387), (805, 384), (657, 383), (484, 378), (326, 377), (179, 385), (56, 386), (66, 83), 
(179, 72), (305, 75), (480, 69), (637, 71), (796, 64), (736, 150), (571, 170), (811, 197), (951, 206), 
(957, 71), (1069, 69), (1081, 208), (948, 294), (877, 346), (787, 326), (726, 389), (650, 470), (557, 421), 
(486, 475), (395, 435), (316, 473), (234, 446), (128, 448), (62, 330), (123, 341), (203, 332), (164, 205), 
(277, 203), (411, 203), (480, 264), (655, 287), (577, 342), (647, 209), (505, 206), (34, 449), (181, 489), 
(396, 495), (482, 526), (318, 527), (570, 491), (648, 523), (733, 457), (802, 499), (890, 440), (954, 516), 
(967, 456), (1058, 461), (1028, 343), (1119, 338), (1126, 461), (1016, 176), (1013, 95), (1129, 90), 
(1123, 182), (730, 208), (802, 257), (412, 357), (321, 287), 
(252, 371), (65, 226), (14, 162), (405, 102), (563, 97), (727, 87), (883, 177), (889, 104)]

pygame.init()
pygame.mixer.init()


clock = pygame.time.Clock()



def draw_text1(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def draw_text2(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, BLACK)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def draw_shield_bar(surface, x, y, percentage):
	BAR_LENGHT = 100
	BAR_HEIGHT = 10
	fill = (percentage / 100) * BAR_LENGHT
	border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
	fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surface, GREEN, fill)
	pygame.draw.rect(surface, WHITE, border, 2)

def draw_gas_bar(surface, x, y, percentage):
	BAR_LENGHT = 100
	BAR_HEIGHT = 10
	fill = (percentage / 100) * BAR_LENGHT
	border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
	fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surface, BLUE, fill)
	pygame.draw.rect(surface, WHITE, border, 2)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("img/player.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH // 2
		self.rect.bottom = HEIGHT - 10
		self.speed_x = 0
		self.speed_y = 0
		self.shield = 100

	def update(self):
		self.speed_x = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_a]:
			self.speed_x *= 2
		if keystate[pygame.K_d]:
			self.speed_x *= 2
		if keystate[pygame.K_w]:
			self.speed_y *= 2
		if keystate[pygame.K_s]:
			self.speed_y *= 2
		self.rect.x += self.speed_x
		self.rect.y += self.speed_y
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

def show_go_screen():
	
	WIN.fill(BLACK, [0,0])
	draw_text1(WIN, "Crazy Cars", 65, WIDTH // 2, HEIGHT // 4)
	draw_text1(WIN, "colecta xxx", 20, WIDTH // 2, HEIGHT // 2)
	draw_text1(WIN, "Press q", 20, WIDTH // 2, HEIGHT * 3/4)
	
	
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					waiting = False

class Moneda(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = mon_images[0]
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.rect.centerx, self.rect.centery = random.choice(PATH)
	
	def update(self):
		pass

class Gas(pygame.sprite.Sprite):
	
	def __init__(self):
		super().__init__()
		self.image = gas_images[0]
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.rect.centerx, self.rect.centery = random.choice(PATH)

class GameInfo():
	LEVELS = 10

	def __init__(self, level=1):
		self.level = level
		self.started = False
		self.level_start_time = 0

	def next_level(self):
		self.level += 1
		self.started = False

	def reset(self):
		self.level = 1
		self.started = False
		self.level_start_time = 0

	def game_finished(self):
		return self.level > self.LEVELS

	def start_level(self):
		self.started = True
		self.level_start_time = time.time()

	def get_level_time(self):
		if not self.started:
			return 0
		return  round(time.time() - self.level_start_time)


class AbstractCar:
	
	def __init__(self, max_vel, rotation_vel):
		self.img = self.IMG
		self.max_vel = max_vel
		self.vel = 0
		self.rotation_vel = rotation_vel
		self.angle = 0
		self.x, self.y = self.START_POS
		self.acceleration = 0.1
		self.mask = pygame.mask.from_surface(self.img)
		self.shield = 100
		self.gas = 100

	def update(self):
		self.shield += 1/24
		self.gas -= 1/10
		if self.shield > 100:
			self.shield = 100
		if self.gas < 0:
			self.gas = 0
		if self.gas > 100:
			self.gas = 100

	def rotate(self, left=False, right=False):
		if left:
			self.angle += self.rotation_vel
		if right:
			self.angle -= self.rotation_vel

	def draw(self,win):
		blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

	def move_forward(self):
		self.vel = min(self.vel + self.acceleration, self.max_vel)
		self.move()

	def move_backward(self):
		self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
		self.move()

	def move(self):
		radians = math.radians(self.angle)
		vertical = math.cos(radians) * self.vel
		horizontal = math.sin(radians) * self.vel

		self.y -= vertical
		self.x -= horizontal

	def collide(self,mask, x=0 , y=0):
		car_mask = pygame.mask.from_surface(self.img)
		offset = (int(self.x - x), int(self.y - y))
		poi = mask.overlap(car_mask, offset)
		return poi

	def reset(self):
		self.x, self.y = self.START_POS
		self.angle = 0
		self.vel = 0

	

class PlayerCar(AbstractCar):
	IMG = RED_CAR
	START_POS = (50,250)
	

	def reduce_speed(self):
		self.vel = max(self.vel - self.acceleration / 2,0)
		self.move()

	def bounce(self):
		#pass
		self.vel = -self.vel
		self.move()

class ComputerCar(AbstractCar):
	IMG = GREEN_CAR
	START_POS = (50,160)

	def __init__(self, max_vel, rotation_vel, path=[]):
		super().__init__(max_vel, rotation_vel)
		self.path = path
		self.current_point = randint(0,109)
		self.vel = max_vel

	def draw_points(self, win):
		for point in self.path:
			pygame.draw.circle(win,(255,0,0), point, 5)

	def draw(self, win):
		super().draw(win)
		#self.draw_points(win)

	def calculate_angle(self):
		target_x , target_y = self.path[self.current_point]
		x_diff = target_x - self.x
		y_diff = target_y - self.y

		if y_diff == 0:
			desired_radian_angle = math.pi / 2
		else:
			desired_radian_angle = math.atan(x_diff/y_diff)

		if target_y > self.y:
			desired_radian_angle += math.pi

		difference_in_angle = self.angle - math.degrees(desired_radian_angle)
		if difference_in_angle >= 180:
			difference_in_angle -= 360

		if difference_in_angle > 0:
			self.angle -= min(self.rotation_vel, abs(difference_in_angle))
		else:
			self.angle += min(self.rotation_vel, abs(difference_in_angle))

	def update_path_point(self):
		target = self.path[self.current_point]
		rect = pygame.Rect(self.x , self.y, self.img.get_width(), self.img.get_height())
		if rect.collidepoint(*target):
			self.current_point = randint(0,109)


	def move(self):
		if self.current_point >= len(self.path):
			return

		self.calculate_angle()
		self.update_path_point()
		super().move()

	def next_level(self, level):
		self.reset()
		self.vel = self.max_vel + (level -1)*0.2
		self.current_point = 0


def draw(win,images, player_car, computer_car, game_info):
	for img, pos in images:
		win.blit(img, pos)

	level_text = MAIN_FONT.render(f"Level {game_info.level}", 1 , (255,255,255))
	win.blit(level_text,(10, HEIGHT - level_text.get_height()-70))

	time_text = MAIN_FONT.render(f"Time: {game_info.get_level_time()}s", 1 , (255,255,255))
	win.blit(time_text,(10, HEIGHT - time_text.get_height()-40))

	vel_text = MAIN_FONT.render(f"Vel: {round(player_car.vel)}px/s", 1 , (255,255,255))
	win.blit(vel_text,(10, HEIGHT - vel_text.get_height()-10))

	player_car.draw(win)
	computer_car.draw(win)
	pygame.display.update()

def move_player(player_car):
	keys = pygame.key.get_pressed()
	moved = False

	if keys[pygame.K_a]:
		player_car.rotate(left=True)
	if keys[pygame.K_d]:
		player_car.rotate(right=True)
	if keys[pygame.K_w]:
		moved = True
		player_car.move_forward()
	if keys[pygame.K_s]:
		moved = True
		player_car.move_backward()

	if not moved:
		player_car.reduce_speed()

def handle_collision(player_car, computer_car, game_info):
	if player_car.collide(TRACK_BORDER_MASK) != None:
		pass
		#player_car.bounce()

	computer_finish_poi_collide = computer_car.collide(FINISH_MASK,*FINISH_POSITION)
	if computer_finish_poi_collide != None:
		pass
		#blit_text_center(WIN,MAIN_FONT,"You Lost!")
		#pygame.display.update()
		#pygame.time.wait(5000)
		#game_info.reset()
		#player_car.reset()
		#computer_car.reset()
	player_finish_poi_collide = player_car.collide(FINISH_MASK,*FINISH_POSITION)
	if player_finish_poi_collide != None:
		if player_finish_poi_collide[1] == 0:
			pass
			#player_car.bounce()
		else:
			pass
			#game_info.next_level()
			#player_car.reset()
			#computer_car.next_level(game_info.level)

mon_images = []
mon_list = ["img/mon.png"]
for img in mon_list:
	mon_images.append(pygame.image.load(img).convert())

gas_images = []
gas_list = ["img/gas.png"]
for img in gas_list:
	gas_images.append(pygame.image.load(img).convert())

Run = True
clock = pygame.time.Clock()
images = [(TRACK,(0,0)), (FINISH,(FINISH_POSITION))]#, (TRACK_BORDER,(0,0))]
player_car = PlayerCar(8,8)
computer_car = ComputerCar(4,6,PATH)
game_info = GameInfo()
moneda = Moneda()
gas = Gas()

all_sprites = pygame.sprite.Group()
all_sprites.add(moneda, gas)
gas_list = pygame.sprite.Group()
mon_list = pygame.sprite.Group()
player_car.score = 0

while Run:
	clock.tick(60)

	
	draw(WIN, images, player_car, computer_car, game_info)
	all_sprites.draw(WIN)
	draw_text1(WIN, str(player_car.score), 25, WIDTH // 2, 10)
	draw_shield_bar(WIN, 5, 5, player_car.shield)
	draw_text2(WIN, str(int(player_car.shield)) + "/100", 10, 55, 6)
	draw_gas_bar(WIN, 5, 20, player_car.gas)
	draw_text1(WIN, str(int(player_car.gas)) + "/100", 10, 55, 21)
	player_car.update()

	# Checar colisiones - jugador - monedas
	if player_car.collide(moneda.mask, moneda.rect.centerx,moneda.rect.centery) != None:
		moneda.kill()
		player_car.score += 50
		player_car.shield += 2
		moneda = Moneda()
		all_sprites.add(moneda)
		mon_list.add(moneda)

	# Checar colisiones - jugador - gas
	if player_car.collide(gas.mask, gas.rect.centerx,gas.rect.centery) != None:
		gas.kill()
		player_car.gas += randint(20,40)
		player_car.score += 50
		player_car.shield += 2
		gas = Gas()
		all_sprites.add(gas)
		mon_list.add(gas)

	# Checar colisiones - jugador - enemy car
	if computer_car.collide(player_car.mask, player_car.x,player_car.y) != None:
		player_car.bounce()
		player_car.score -= 2
		player_car.shield -= 10
		

	while not game_info.started:
		blit_text_center(WIN, MAIN_FONT, f"Press any key to start level {game_info.level}!")
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				break
			if event.type == pygame.KEYDOWN:
				game_info.start_level()

	pygame.display.update()
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			Run = False
			break

		#if event.type == pygame.MOUSEBUTTONDOWN:
			#pos = pygame.mouse.get_pos()
			#computer_car.path.append(pos)

	move_player(player_car)
	computer_car.move()

	handle_collision(player_car, computer_car, game_info)

	if game_info.game_finished():
		blit_text_center(WIN,MAIN_FONT,"You Won!")
		pygame.display.update()
		pygame.time.wait(5000)
		game_info.reset()
		player_car.reset()
		computer_car.reset()
			

	
#print(computer_car.path)
pygame.quit()

