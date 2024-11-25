import sys
import time
import os
import pygame
from pygame.locals import *
from mineblock import *
from config import DEFAULT_BOARD_SIZE, DEFAULT_DIFFICULTY, BoardSize, Difficulty, BOARD_SIZES, SIZE, MENU_WIDTH, MENU_HEIGHT, GAME_TEXT

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (200, 40, 40)

class GameState(Enum):
    MENU = 1
    GAME = 2

class GameStatus(Enum):
    READY = 1
    STARTED = 2
    OVER = 3
    WON = 4

def draw_button(screen, text, rect, font, color=BLACK, bg_color=WHITE, hover=False):
    if hover:
        bg_color = GRAY
    pygame.draw.rect(screen, bg_color, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def draw_menu(screen, font, selected_difficulty, selected_size):
    screen.fill(WHITE)
    
    # Title
    title = font.render(GAME_TEXT["title"], True, BLACK)
    title_rect = title.get_rect(center=(MENU_WIDTH // 2, 50))
    screen.blit(title, title_rect)
    
    # Difficulty buttons
    diff_y = 150
    diff_buttons = {}
    for i, diff in enumerate(Difficulty):
        rect = pygame.Rect(MENU_WIDTH // 2 - 100, diff_y + i * 60, 200, 40)
        text = GAME_TEXT["difficulty_prefix"] + GAME_TEXT["difficulty"][diff]
        is_selected = diff == selected_difficulty
        draw_button(screen, text, rect, font, bg_color=GRAY if is_selected else WHITE)
        diff_buttons[diff] = rect
    
    # Size buttons
    size_y = 350
    size_buttons = {}
    for i, size in enumerate(BoardSize):
        rect = pygame.Rect(MENU_WIDTH // 2 - 100, size_y + i * 60, 200, 40)
        text = GAME_TEXT["size_prefix"] + GAME_TEXT["size"][size]
        is_selected = size == selected_size
        draw_button(screen, text, rect, font, bg_color=GRAY if is_selected else WHITE)
        size_buttons[size] = rect
    
    # Start button
    start_rect = pygame.Rect(MENU_WIDTH // 2 - 100, 550, 200, 40)
    draw_button(screen, GAME_TEXT["start_button"], start_rect, font)
    
    return diff_buttons, size_buttons, start_rect

def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))

def main():
    pygame.init()
    
    # Initialize with default settings from config
    board_size = DEFAULT_BOARD_SIZE
    difficulty = DEFAULT_DIFFICULTY
    game_state = GameState.MENU
    game_status = GameStatus.READY
    
    menu_screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
    pygame.display.set_caption(GAME_TEXT["title"])
    
    # Load resources
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Load images
    img_dict = {}
    for i in range(9):
        img_dict[i] = pygame.image.load(os.path.join(SCRIPT_DIR, f"resources/{i}.bmp")).convert()
    
    img_blank = pygame.image.load(os.path.join(SCRIPT_DIR, "resources/blank.bmp")).convert()
    img_flag = pygame.image.load(os.path.join(SCRIPT_DIR, "resources/flag.bmp")).convert()
    img_ask = pygame.image.load(os.path.join(SCRIPT_DIR, "resources/ask.bmp")).convert()
    img_mine = pygame.image.load(os.path.join(SCRIPT_DIR, "resources/mine.bmp")).convert()
    img_blood = pygame.image.load(os.path.join(SCRIPT_DIR, "resources/blood.bmp")).convert()
    img_error = pygame.image.load(os.path.join(SCRIPT_DIR, "resources/error.bmp")).convert()
    img_face_normal = pygame.image.load(os.path.join(SCRIPT_DIR, "resources/face_normal.bmp")).convert()
    img_face_fail = pygame.image.load(os.path.join(SCRIPT_DIR, "resources/face_fail.bmp")).convert()
    img_face_success = pygame.image.load(os.path.join(SCRIPT_DIR, "resources/face_success.bmp")).convert()
    
    try:
        # Try to use system Chinese fonts first
        system_fonts = ['Microsoft YaHei', 'SimHei', 'Microsoft JhengHei']
        font_found = False
        for font_name in system_fonts:
            try:
                font1 = pygame.font.SysFont(font_name, SIZE)
                menu_font = pygame.font.SysFont(font_name, SIZE - 10)
                # Test if font can render Chinese
                test = font1.render('測試', True, (0, 0, 0))
                font_found = True
                break
            except:
                continue
                
        if not font_found:
            # Fallback to default TTF file
            font1 = pygame.font.Font(os.path.join(SCRIPT_DIR, 'resources', 'a.TTF'), SIZE)
            menu_font = pygame.font.Font(os.path.join(SCRIPT_DIR, 'resources', 'a.TTF'), SIZE - 10)
    except Exception as e:
        print(f"Font loading error: {e}")
        # Last resort fallback
        font1 = pygame.font.SysFont(None, SIZE)
        menu_font = pygame.font.SysFont(None, SIZE - 10)
    
    # Initialize game variables
    block = None
    start_time = None
    elapsed_time = 0
    game_screen = None
    x = 0
    y = 0
    b1 = False
    b2 = False
    b3 = False
    
    while True:
        if game_state == GameState.MENU:
            menu_screen.fill(WHITE)
            
            # Draw title
            title = menu_font.render(GAME_TEXT["title"], True, BLACK)
            title_rect = title.get_rect(center=(MENU_WIDTH // 2, 50))
            menu_screen.blit(title, title_rect)
            
            # Draw difficulty buttons
            diff_y = 150
            diff_buttons = {}
            for i, diff in enumerate(Difficulty):
                rect = pygame.Rect(MENU_WIDTH // 2 - 100, diff_y + i * 60, 200, 40)
                text = GAME_TEXT["difficulty_prefix"] + GAME_TEXT["difficulty"][diff]
                is_selected = diff == difficulty
                draw_button(menu_screen, text, rect, menu_font, bg_color=GRAY if is_selected else WHITE)
                diff_buttons[diff] = rect
            
            # Draw size buttons
            size_y = 350
            size_buttons = {}
            for i, size in enumerate(BoardSize):
                rect = pygame.Rect(MENU_WIDTH // 2 - 100, size_y + i * 60, 200, 40)
                text = GAME_TEXT["size_prefix"] + GAME_TEXT["size"][size]
                is_selected = size == board_size
                draw_button(menu_screen, text, rect, menu_font, bg_color=GRAY if is_selected else WHITE)
                size_buttons[size] = rect
            
            # Draw start button
            start_button = pygame.Rect(MENU_WIDTH // 2 - 100, 550, 200, 40)
            draw_button(menu_screen, GAME_TEXT["start_button"], start_button, menu_font)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check difficulty buttons
                    for diff, rect in diff_buttons.items():
                        if rect.collidepoint(mouse_pos):
                            difficulty = diff
                            break
                    
                    # Check size buttons
                    for size, rect in size_buttons.items():
                        if rect.collidepoint(mouse_pos):
                            board_size = size
                            break
                    
                    # Check start button
                    if start_button.collidepoint(mouse_pos):
                        # Calculate game window size
                        board_dims = BOARD_SIZES[board_size]
                        game_width = board_dims["width"] * SIZE
                        game_height = board_dims["height"] * SIZE + SIZE * 2
                        
                        # Create game window
                        game_screen = pygame.display.set_mode((game_width, game_height))
                        pygame.display.set_caption(GAME_TEXT["title"])
                        
                        game_state = GameState.GAME
                        block = MineBlock(board_size, difficulty)
                        game_status = GameStatus.READY
                        start_time = None
                        elapsed_time = 0
        
        else:  # GameState.GAME
            # Fill background
            game_screen.fill((225, 225, 225))
            
            # Get current mouse button states
            b1, b2, b3 = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            x = mouse_pos[0] // SIZE
            y = mouse_pos[1] // SIZE - 2
            
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if y < 0:
                        face_pos_x = (block.width * SIZE - int(SIZE * 1.25)) // 2
                        face_pos_y = (SIZE * 2 - int(SIZE * 1.25)) // 2
                        if face_pos_x <= mouse_pos[0] <= face_pos_x + int(SIZE * 1.25) and face_pos_y <= mouse_pos[1] <= face_pos_y + int(SIZE * 1.25):
                            # Switch back to menu
                            menu_screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                            pygame.display.set_caption(GAME_TEXT["title"])
                            game_state = GameState.MENU
                            continue

                    if game_status == GameStatus.READY:
                        game_status = GameStatus.STARTED
                        start_time = time.time()
                        elapsed_time = 0
                    
                    if game_status == GameStatus.STARTED:
                        mine = block.getmine(x, y)
                        if mine:
                            if event.button == 1 and not b3:  # 左键
                                if mine.status == BlockStatus.normal:
                                    if not block.open_mine(x, y):
                                        game_status = GameStatus.OVER
                            elif event.button == 3 and not b1:  # 右键
                                if mine.status == BlockStatus.normal:
                                    mine.status = BlockStatus.flag
                                elif mine.status == BlockStatus.flag:
                                    mine.status = BlockStatus.ask
                                elif mine.status == BlockStatus.ask:
                                    mine.status = BlockStatus.normal
                            elif event.button == 1 and b3 or event.button == 3 and b1:  # 左右键同时按下
                                if mine.status == BlockStatus.opened:
                                    if not block.double_mouse_button_down(x, y):
                                        game_status = GameStatus.OVER

                elif event.type == MOUSEBUTTONUP:
                    if game_status == GameStatus.STARTED:
                        mine = block.getmine(x, y)
                        if mine and mine.status == BlockStatus.double:
                            block.double_mouse_button_up(x, y)
            
            # Draw game board
            flag_count = 0
            opened_count = 0
            
            for row in block.block:
                for mine in row:
                    pos = (mine.x * SIZE, (mine.y + 2) * SIZE)
                    if mine.status == BlockStatus.opened:
                        game_screen.blit(img_dict[mine.around_mine_count], pos)
                        opened_count += 1
                    elif mine.status == BlockStatus.double:
                        game_screen.blit(img_dict[mine.around_mine_count], pos)
                    elif mine.status == BlockStatus.bomb:
                        game_screen.blit(img_blood, pos)
                    elif mine.status == BlockStatus.flag:
                        game_screen.blit(img_flag, pos)
                        flag_count += 1
                    elif mine.status == BlockStatus.ask:
                        game_screen.blit(img_ask, pos)
                    elif mine.status == BlockStatus.hint:
                        game_screen.blit(img_dict[0], pos)
                    elif game_status == GameStatus.OVER and mine.value:
                        game_screen.blit(img_mine, pos)
                    elif mine.value == 0 and mine.status == BlockStatus.flag:
                        game_screen.blit(img_error, pos)
                    elif mine.status == BlockStatus.normal:
                        game_screen.blit(img_blank, pos)
            
            # Draw mine count and timer
            print_text(game_screen, font1, 30, (SIZE * 2 - font1.get_height()) // 2 - 2, 
                      '%02d' % (block.mine_count - flag_count), RED)
            
            if game_status == GameStatus.STARTED:
                elapsed_time = int(time.time() - start_time)
            print_text(game_screen, font1, game_screen.get_width() - 100, (SIZE * 2 - font1.get_height()) // 2 - 2, 
                      '%03d' % elapsed_time, RED)
            
            # Check win condition
            if flag_count + opened_count == block.width * block.height:
                game_status = GameStatus.WON
            
            # Draw face
            face_pos_x = (block.width * SIZE - int(SIZE * 1.25)) // 2
            face_pos_y = (SIZE * 2 - int(SIZE * 1.25)) // 2
            
            if game_status == GameStatus.OVER:
                game_screen.blit(img_face_fail, (face_pos_x, face_pos_y))
            elif game_status == GameStatus.WON:
                game_screen.blit(img_face_success, (face_pos_x, face_pos_y))
            else:
                game_screen.blit(img_face_normal, (face_pos_x, face_pos_y))
        
        pygame.display.update()

if __name__ == '__main__':
    main()
