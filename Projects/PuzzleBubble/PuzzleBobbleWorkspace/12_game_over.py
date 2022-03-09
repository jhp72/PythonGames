# 게임 종료 처리
# 성공 : 화면 내에 모든 버블이 사라지면 성공
# 실패 : 바닥에 어떤 정해진 높이보다 버블이 낮게 내려오면 실패
import os, random, math
import pygame

# 버블 클래스 생성
class Bubble(pygame.sprite.Sprite):
    def __init__(self, image, color, position=(0,0), row_idx=-1, col_idx=-1):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)
        self.radius = 18
        self.row_idx = row_idx
        self.col_idx = col_idx

    def set_rect(self, position):
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen, to_x=None):
        if to_x:
            screen.blit(self.image, (self.rect.x + to_x, self.rect.y))
        else:
            screen.blit(self.image, self.rect)

    def set_angle(self, angle):
        self.angle = angle
        self.rad_angle = math.radians(self.angle)

    def move(self):
        to_x = self.radius * math.cos(self.rad_angle)
        to_y = self.radius * math.sin(self.rad_angle) * -1

        self.rect.x += to_x
        self.rect.y += to_y

        if self.rect.left < 0 or self.rect.right > screen_width:
            self.set_angle(180 - self.angle)

    def set_map_index(self, row_idx, col_idx):
        self.row_idx = row_idx
        self.col_idx = col_idx

    def drop_downward(self, height):
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery + height))

# 발사대 클래스 생성
class Pointer(pygame.sprite.Sprite):
    def __init__(self, image, position, angle):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.angle = angle
        self.original_image = image
        self.position = position

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # 회전
    def rotate(self, angle):
        self.angle += angle

        if self.angle > 170:
            self.angle = 170
        elif self.angle < 10:
            self.angle = 10

        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.position)

# 맵 만들기
def setup():
    global map
    # lv1
    map = [
        # ["R", "R", "Y", "Y", "B", "B", "G", "G"],
        list("RRYYBBGG"),
        list("RRYYBBG/"), # / : 버블이 위치할 수 없는 곳
        list("BBGGRRYY"),
        list("BGGRRYY/"),
        list("........"), # . : 비어 있는 곳
        list("......./"),
        list("........"),
        list("......./"),
        list("........"),
        list("......./"),
        list("........")        
    ]

    # lv2
    # map = [
    #     list("...YY..."),
    #     list("...G.../"),
    #     list("...R...."),
    #     list("...B.../"),
    #     list("...R...."),
    #     list("...G.../"),
    #     list("...P...."),
    #     list("...P.../"),
    #     list("........"),
    #     list("......./"),
    #     list("........")
    # ]    

    # lv3
    # map = [
    #     list("G......G"),
    #     list("RGBYRGB/"),
    #     list("Y......Y"),
    #     list("BYRGBYR/"),
    #     list("...R...."),
    #     list("...G.../"),
    #     list("...R...."),
    #     list("......./"),
    #     list("........"),
    #     list("......./"),
    #     list("........")
    # ]

    for row_idx, row in enumerate(map):
        for col_idx, col in enumerate(row):
            if col in [".", "/"]:
                continue
            position = get_bubble_position(row_idx, col_idx)
            image = get_bubble_image(col)
            bubble_group.add(Bubble(image, col, position, row_idx, col_idx))
       
def get_bubble_position(row_idx, col_idx):
    pos_x = col_idx * CELL_SIZE + (BUBBLE_WIDTH // 2)
    pos_y = row_idx * CELL_SIZE + (BUBBLE_HEIGHT // 2) + wall_height
    if row_idx % 2 == 1:
        pos_x += CELL_SIZE // 2
    return pos_x, pos_y

def get_bubble_image(color):
    if color == "R":
        return bubble_images[0]
    elif color == "Y":
        return bubble_images[1]
    elif color == "B":
        return bubble_images[2]
    elif color == "G":
        return bubble_images[3]
    elif color == "P":
        return bubble_images[4]
    else: # BLACK
        return bubble_images[-1]

def prepare_bubbles():
    global curr_bubble, next_bubble
    if next_bubble:
        curr_bubble = next_bubble
    else:
        curr_bubble = create_bubble() # 새 버블 만들기

    curr_bubble.set_rect((screen_width // 2, 624))
    next_bubble = create_bubble()
    next_bubble.set_rect((screen_width // 4, 688))

def create_bubble():
    color = get_random_bubble_color()
    image = get_bubble_image(color)
    return Bubble(image, color)

def get_random_bubble_color():
    colors = []
    for row in map:
        for col in row:
            if col not in colors and col not in [".", "/"]:
                colors.append(col)
    return random.choice(colors)

def process_collision():
    global curr_bubble, fire, curr_fire_count
    hit_bubble = pygame.sprite.spritecollideany(curr_bubble, bubble_group, pygame.sprite.collide_mask)
    if hit_bubble or curr_bubble.rect.top <= wall_height:
        row_idx, col_idx = get_map_index(*curr_bubble.rect.center) # (x, y)
        place_bubble(curr_bubble, row_idx, col_idx)
        remove_adjacent_bubbles(row_idx, col_idx, curr_bubble.color)
        curr_bubble = None
        fire = False
        curr_fire_count -= 1

def get_map_index(x, y):
    row_idx = (y - wall_height) // CELL_SIZE
    col_idx = x // CELL_SIZE
    if row_idx % 2 == 1:
        col_idx = (x - (CELL_SIZE // 2)) // CELL_SIZE
        if col_idx < 0:
            col_idx = 0
        elif col_idx > MAP_COLUMN_COUNT - 2:
            col_idx = MAP_COLUMN_COUNT - 2
    return row_idx, col_idx

def place_bubble(bubble, row_idx, col_idx):
    map[row_idx][col_idx] = bubble.color
    position = get_bubble_position(row_idx, col_idx)
    bubble.set_rect(position)
    bubble.set_map_index(row_idx, col_idx)
    bubble_group.add(bubble)

def remove_adjacent_bubbles(row_idx, col_idx, color):
    visited.clear()
    visit(row_idx, col_idx, color)
    if len(visited) >= 3:
        remove_visited_bubbles()
        remove_hanging_bubbles()

def visit(row_idx, col_idx, color=None):
    # 맵의 범위를 벗어나는지 확인
    if row_idx < 0 or row_idx >= MAP_ROW_COUNT or col_idx < 0 or col_idx >= MAP_COLUMN_COUNT:
        return
    # 현재 Cell 의 색상이 color 와 같은지 확인
    if color and map[row_idx][col_idx] != color:
        return
    # 빈 공간이거나, 버블이 존재할 수 없는 위치인지 확인
    if map[row_idx][col_idx] in [".", "/"]:
        return
    # 이미 방문했는지 여부 확인
    if (row_idx, col_idx) in visited:
        return
    # 방문 처리
    visited.append((row_idx, col_idx))

    rows = [0, -1, -1, 0, 1, 1]
    cols = [-1, -1, 0, 1, 0, -1]
    if row_idx % 2 == 1:
        rows = [0, -1, -1, 0, 1, 1]
        cols = [-1, 0, 1, 1, 1, 0]

    for i in range(len(rows)):
        visit(row_idx + rows[i], col_idx + cols[i], color)

def remove_visited_bubbles():
    bubbles_to_remove = [b for b in bubble_group if (b.row_idx, b.col_idx) in visited]
    for bubble in bubbles_to_remove:
        map[bubble.row_idx][bubble.col_idx] = "."
        bubble_group.remove(bubble)

def remove_not_visited_bubbles():
    bubbles_to_remove = [b for b in bubble_group if (b.row_idx, b.col_idx) not in visited]
    for bubble in bubbles_to_remove:
        map[bubble.row_idx][bubble.col_idx] = "."
        bubble_group.remove(bubble)

def remove_hanging_bubbles():
    visited.clear()
    for col_idx in range(MAP_COLUMN_COUNT):
        if map[0][col_idx] != ".":
            visit(0, col_idx)
    remove_not_visited_bubbles()

def draw_bubbles():
    to_x = None
    if curr_fire_count == 2:
        to_x = random.randint(0, 2) - 1 # -1 ~ 1
    elif curr_fire_count == 1:
        to_x = random.randint(0, 8) - 4 # -4 ~ 4
    
    for bubble in bubble_group:
        bubble.draw(screen, to_x)

def drop_wall():
    global wall_height, curr_fire_count
    wall_height += CELL_SIZE
    for bubble in bubble_group:
        bubble.drop_downward(CELL_SIZE)
    curr_fire_count = FIRE_COUNT

def get_lowest_bubble_bottom():
    bubble_bottoms = [bubble.rect.bottom for bubble in bubble_group]
    return max(bubble_bottoms)

def change_bubble_image(image):
    for bubble in bubble_group:
        bubble.image = image

def display_game_over():
    txt_game_over = game_font.render(game_result, True, WHITE)
    rect_game_over = txt_game_over.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(txt_game_over, rect_game_over)
    
pygame.init()
screen_width = 448
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Puzzle Bobble")
clock = pygame.time.Clock()

# 배경 이미지 불러오기
current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "background.png"))
# 벽 이미지 불러오기
wall = pygame.image.load(os.path.join(current_path, "wall.png"))

# 버블 이미지 불러오기
bubble_images = [
    pygame.image.load(os.path.join(current_path, "red.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "yellow.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "blue.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "green.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "purple.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "black.png")).convert_alpha()
]

# 발사대 이미지 불러오기
pointer_image = pygame.image.load(os.path.join(current_path, "pointer.png"))
pointer = Pointer(pointer_image, (screen_width // 2, 624), 90)

# 게임 관련 변수
CELL_SIZE = 56
BUBBLE_WIDTH = 56
BUBBLE_HEIGHT = 62
RED = (255,0,0)
WHITE = (255,255,255)
MAP_ROW_COUNT = 11
MAP_COLUMN_COUNT = 8
FIRE_COUNT = 7

# 화살표 관련 변수
# to_angle = 0 # 좌우로 움직일 각도 정보
to_angle_left = 0 # 왼쪽으로 움직일 각도 정보
to_angle_right = 0 # 오른쪽으로 움직일 각도 정보
angle_speed = 1.5 # 1.5 도씩 움직이게 됨

curr_bubble = None # 이번에 쏠 버블
next_bubble = None # 다음에 쏠 버블
fire = False # 발사 여부
curr_fire_count = FIRE_COUNT
wall_height = 0 # 화면에 보여지는 벽의 높이

is_game_over = False
game_font = pygame.font.SysFont("arialrounded", 40)
game_result = None

map = [] # 맵
visited = [] # 방문 위치 기록
bubble_group = pygame.sprite.Group()
setup()

running = True
while running:
    clock.tick(60) # FPS 60 으로 설정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_angle_left += angle_speed
            elif event.key == pygame.K_RIGHT:
                to_angle_right -= angle_speed
            elif event.key == pygame.K_SPACE:
                if curr_bubble and not fire:
                    fire = True
                    curr_bubble.set_angle(pointer.angle)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_angle_left = 0
            elif event.key == pygame.K_RIGHT:
                to_angle_right = 0

    if not curr_bubble:
        prepare_bubbles()

    if fire:
        process_collision() # 충돌 처리

    if curr_fire_count == 0:
        drop_wall()

    if not bubble_group:
        game_result = "Mission Complete"
        is_game_over = True
    elif get_lowest_bubble_bottom() > len(map) * CELL_SIZE:
        game_result = "Game Over"
        is_game_over = True
        change_bubble_image(bubble_images[-1])

    screen.blit(background, (0, 0))
    screen.blit(wall, (0, wall_height - screen_height))
    
    draw_bubbles()
    pointer.rotate(to_angle_left + to_angle_right)
    pointer.draw(screen)
    if curr_bubble:
        if fire:
            curr_bubble.move()
        curr_bubble.draw(screen)

    if next_bubble:
        next_bubble.draw(screen)

    if is_game_over:
        display_game_over()
        running = False

    pygame.display.update()

pygame.time.delay(2000)
pygame.quit()