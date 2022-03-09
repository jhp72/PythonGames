# 집게 발사
# 현재 위치로부터 집게를 쭉 뻗는 동작
# 화면 밖으로 뻗어나가면 다시 돌아오도록 처리
# 뻗을 때 속도, 돌아올 때 속도 적용
import os
import pygame

# 집게 클래스
class Claw(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.original_image = image
        self.rect = image.get_rect(center=position)

        self.offset = pygame.math.Vector2(default_offset_x_claw, 0)
        self.position = position

        self.direction = LEFT # 집게의 이동 방향
        self.angle_speed = 2.5 # 집게의 각도 변경 폭 (좌우 이동 속도)
        self.angle = 10 # 최초 각도 정의 (오른쪽 끝)

    def update(self, to_x):
        if self.direction == LEFT: # 왼쪽 방향으로 이동하고 있다면
            self.angle += self.angle_speed # 이동 속도만큼 각도 증가
        elif self.direction == RIGHT: # 오른쪽 방향으로 이동하고 있다면
            self.angle -= self.angle_speed

        # 만약에 허용 각도 범위를 벗어나면?
        if self.angle > 170:
            self.angle = 170
            self.set_direction(RIGHT)
        elif self.angle < 10:
            self.angle = 10
            self.set_direction(LEFT)

        self.offset.x += to_x
        self.rotate() # 회전 처리

    def rotate(self):        
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1) # 회전 대상 이미지, 회전 각도, 이미지 크기(scale)
        offset_rotated = self.offset.rotate(self.angle)
        self.rect = self.image.get_rect(center=self.position+offset_rotated)

    def set_direction(self, direction):
        self.direction = direction

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.line(screen, BLACK, self.position, self.rect.center, 5) # 직선 그리기

    def set_init_state(self):
        self.offset.x = default_offset_x_claw
        self.angle = 10
        self.direction = LEFT

# 보석 클래스
class Gemstone(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)

def setup_gemstone():
    # 작은 금
    small_gold = Gemstone(gemstone_images[0], (200, 380)) # 0번째 이미지를 (200, 380) 위치에
    gemstone_group.add(small_gold) # 그룹에 추가
    # 큰 금
    gemstone_group.add(Gemstone(gemstone_images[1], (300, 500)))
    # 돌
    gemstone_group.add(Gemstone(gemstone_images[2], (300, 380)))
    # 다이아몬드
    gemstone_group.add(Gemstone(gemstone_images[3], (900, 420)))



pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gold Miner")
clock = pygame.time.Clock()

# 게임 관련 변수
default_offset_x_claw = 40 # 중심점으로부터 집게까지의 기본 x 간격
to_x = 0 # x 좌표 기준으로 집게 이미지를 이동시킬 값 저장 변수

# 속도 변수
move_speed = 12 # 발사할 때 이동 스피드 (x 좌표 기준으로 증가되는 값)
return_speed = 20 # 아무것도 없이 돌아올 때 이동 스피드

# 방향 변수
LEFT = -1 # 왼쪽 방향
STOP = 0 # 이동 방향이 좌우가 아닌 고정인 상태 (집게를 뻗음)
RIGHT = 1 # 오른쪽 방향

# 색깔 변수
RED = (255,0,0) # RGB, 빨간색
BLACK = (0,0,0) # 검은색

# 배경 이미지 불러오기
current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
background = pygame.image.load(os.path.join(current_path, "background.png"))

# 4개 보석 이미지 불러오기 (작은 금, 큰 금, 돌, 다이아몬드)
gemstone_images = [
    pygame.image.load(os.path.join(current_path, "small_gold.png")), # 작은 금
    pygame.image.load(os.path.join(current_path, "big_gold.png")), # 큰 금
    pygame.image.load(os.path.join(current_path, "stone.png")), # 돌
    pygame.image.load(os.path.join(current_path, "diamond.png"))] # 다이아몬드

# 보석 그룹
gemstone_group = pygame.sprite.Group()
setup_gemstone() # 게임에 원하는 만큼의 보석을 정의

# 집게
claw_image = pygame.image.load(os.path.join(current_path, "claw.png"))
claw = Claw(claw_image, (screen_width // 2, 110)) # 가로위치는 화면 가로 크기 기준으로 절반, 세로위치는 위에서 110 px

running = True
while running:
    clock.tick(30) # FPS 값이 30 으로 고정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN: # 마우스 버튼 누를 때 집게를 뻗음
            claw.set_direction(STOP) # 좌우 멈춤
            to_x = move_speed # move_speed 만큼 빠르게 쭉 뻗음

    if claw.rect.left < 0 or claw.rect.right > screen_width or claw.rect.bottom > screen_height:
        to_x = -return_speed

    if claw.offset.x < default_offset_x_claw: # 원위치에 오면
        to_x = 0
        claw.set_init_state() # 처음 상태로 되돌림

    screen.blit(background, (0, 0))

    gemstone_group.draw(screen) # 그룹 내 모든 스프라이트를 screen 에 그림
    claw.update(to_x)
    claw.draw(screen)
    
    pygame.display.update()

pygame.quit()