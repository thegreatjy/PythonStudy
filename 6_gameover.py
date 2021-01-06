import pygame
import os


###########초기화##########
pygame.init()

screen_width = 640  # 가로크기
screen_height = 480  # 세로크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("~ PANG ~")

# FPS
clock = pygame.time.Clock()
######################
# 1. 사용자 게임 초기화 (배경, 게임 이미지, 좌표, 폰트)
current_path = os.path.dirname(__file__)  # 현재 파일 위치 반환
image_path = os.path.join(current_path, "images")  # images 폴더 위치 반환
# 배경
background = pygame.image.load(os.path.join(image_path, "background.png"))
# 스테이지
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]  # 스테이지 높이 위에 캐릭터를 두기 위함
# 캐릭터
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width / 2 - character_width / 2
character_y_pos = screen_height - character_height - stage_height
# 캐릭터 이동 방향
character_to_x = 0
# 캐릭터 이동 속도
character_speed = 5

# 무기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
# 무기 여러 발 발사 가능
weapons = []

# 무기 이동 속도
weapon_speed = 10

#공
ball_images=[
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))
]
#공 최초 속도 : 크기에 따라 속도가 다름
ball_speed_y=[-18, -15, -12, -9]
#공
balls=[]
#최초 발생하는 큰 공 추가
balls.append({
    "pos_x":50,
    "pos_y":50,
    "img_idx":0,    #공 이미지 인덱스
    "to_x":3,   #공 x축 이동, 음수 왼쪽, 양수 오른쪽
    "to_y":-6,  #공 y축 이동
    "init_spd_y":ball_speed_y[0]   #y 최초 속도
})
#사라질 무기, 공 정보 저장 변수
weapon_to_remove=-1
ball_to_remove=-1

#폰트 정의
game_font=pygame.font.Font(None, 40)
total_time=100  #sec
start_ticks=pygame.time.get_ticks() #시작 시간
#게임 종료 메세지 : Time out, Mission Complete, Game Over(공에 맞음)
game_result="Game Over"

# 이벤트 루프
running = True  # 게임 진행중인지
while running:
    dt = clock.tick(60)  # 게임 화면의 초당 프레임 수를 설정, 높을수록 부드러움
    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():  # 이벤트 발생 체크 리스너
        if event.type == pygame.QUIT:  # 창 닫는 이벤트 -> 게임 종료
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # 캐릭터 왼쪽 이동
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:  # 캐릭터 오른쪽으로
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:  # 무기 발사
                weapon_x_pos = character_x_pos + character_width / 2 - weapon_width / 2 #캐릭터의 중앙
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0
    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
    # 무기 위치 조정
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]  # 무기 위치를 위로 올린다
    # 천장에 닿은 무기 없애기
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]
    #공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x=ball_val["pos_x"]
        ball_pos_y=ball_val["pos_y"]
        ball_img_idx=ball_val["img_idx"]
        ball_size=ball_images[ball_img_idx].get_rect().size
        ball_width=ball_size[0]
        ball_height=ball_size[1]
        #공이 가로벽에 닿았을 때, 공 이동 위치 변경(튕겨나옴)
        if ball_pos_x<0 or ball_pos_x>screen_width-ball_width:
            ball_val["to_x"]=ball_val["to_x"]*-1

        #세로벽 : 스테이지 바닥에 튕겨서 올라가는 처리
        if ball_pos_y>=screen_height-stage_height-ball_height:
            ball_val["to_y"]=ball_val["init_spd_y"]
        else:   #포물선 효과
            ball_val["to_y"]+=0.5
        ball_val["pos_x"]+=ball_val["to_x"]
        ball_val["pos_y"]+=ball_val["to_y"]

    # 4. 충돌 처리
    #4-1. 캐릭터와 공 충돌
    character_rect=character.get_rect()
    character_rect.left=character_x_pos
    character_rect.top=character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x=ball_val["pos_x"]
        ball_pos_y=ball_val["pos_y"]
        ball_img_idx=ball_val["img_idx"]
        ball_rect=ball_images[ball_img_idx].get_rect()
        ball_rect.left=ball_pos_x
        ball_rect.top=ball_pos_y

        if character_rect.colliderect(ball_rect):
            running=False
            break

        #4-2. 무기와 공 충돌
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_x_pos=weapon_val[0]
            weapon_y_pos=weapon_val[1]

            weapon_rect=weapon.get_rect()
            weapon_rect.left=weapon_x_pos
            weapon_rect.top=weapon_y_pos
            #충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove=weapon_idx
                ball_to_remove=ball_idx
                #가장 작은 크기의 공이 아니라면 다음 단계의 공으로 나누기
                if ball_img_idx<3:
                    #현재 공 크기 정보를 가지고 옴
                    ball_width=ball_rect.size[0]
                    ball_height=ball_rect.size[1]
                    #나눠진 공 정보
                    small_ball_rect=ball_images[ball_img_idx+1].get_rect()
                    small_ball_width=small_ball_rect.size[0]
                    small_ball_height=small_ball_rect.size[1]
                    #왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x": ball_pos_x+(ball_width/2)-(small_ball_width/2),
                        "pos_y": ball_pos_y+(ball_height/2)-(small_ball_height/2),
                        "img_idx": ball_img_idx+1,  # 공 이미지 인덱스
                        "to_x": -3,  # 공 x축 이동, 음수 왼쪽, 양수 오른쪽
                        "to_y": -6,  # 공 y축 이동
                        "init_spd_y": ball_speed_y[ball_img_idx+1]  # y 최초 속도
                    })
                    #오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x": ball_pos_x+(ball_width/2)-(small_ball_width/2),
                        "pos_y": ball_pos_y+(ball_height/2)-(small_ball_height/2),
                        "img_idx": ball_img_idx+1,  # 공 이미지 인덱스
                        "to_x": 3,  # 공 x축 이동, 음수 왼쪽, 양수 오른쪽
                        "to_y": -6,  # 공 y축 이동
                        "init_spd_y": ball_speed_y[ball_img_idx+1]  # y 최초 속도
                    })
                break
        else:   #for-else문 공부하기
            continue
        break
    #충돌 : 공과 무기를 없앰
    if ball_to_remove>-1:
        del balls[ball_to_remove]
        ball_to_remove=-1
    if weapon_to_remove>-1:
        del weapons[weapon_to_remove]
        weapon_to_remove=-1

    #모든 공이 없는 경우 게임 종료
    if len(balls)==0:
        game_result="Mission Complete"
        running=False

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y=val["pos_y"]
        ball_img_idx=val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    #시간 계산
    elapsed_time=(pygame.time.get_ticks()-start_ticks)/1000
    timer=game_font.render("Time : {}".format(int(total_time-elapsed_time)), True, (255,255,255))
    screen.blit(timer, (10,10))
    #시간 초과
    if total_time-elapsed_time<=0:
        game_result="Time Over"
        running=False
    pygame.display.update()  # 게임 화면 다시 그리기
#게임 오버 메세지
msg=game_font.render(game_result, True, (0,0,255))
msg_rect=msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
screen.blit(msg, msg_rect)
pygame.display.update()
pygame.time.delay(2000) #2초 대기 후 창 꺼짐
pygame.quit()

#for-else문 공부하기!