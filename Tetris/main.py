import sys
import time
import pygame
from pygame.locals import *
import blocks

# 遊戲區域設定
SIZE = 30  # 每個小方格大小
BLOCK_HEIGHT = 25  # 遊戲區高度
BLOCK_WIDTH = 10   # 遊戲區寬度
BORDER_WIDTH = 4   # 遊戲區邊框寬度

# 顏色定義
BORDER_COLOR = (40, 40, 200)  # 遊戲區邊框顏色
BG_COLOR = (40, 40, 60)      # 背景色
BLOCK_COLOR = (20, 128, 200)  # 方塊顏色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 30, 30)         # GAME OVER 顏色
BUTTON_COLOR = (60, 60, 100)
BUTTON_HOVER_COLOR = (80, 80, 120)

# 螢幕設定
INFO_WIDTH = 200  # 資訊區域寬度
SCREEN_WIDTH = SIZE * BLOCK_WIDTH + BORDER_WIDTH + INFO_WIDTH  # 遊戲螢幕的寬
SCREEN_HEIGHT = SIZE * BLOCK_HEIGHT      # 遊戲螢幕的高

# 支援的字體列表
FONT_LIST = ['微軟正黑體', 'Microsoft JhengHei', 'PMingLiU', 'MingLiU']

def get_system_font():
    """獲取系統支援的中文字體"""
    available_font = None
    for font_name in FONT_LIST:
        if font_name.lower() in [f.lower() for f in pygame.font.get_fonts()]:
            available_font = font_name
            break
    return available_font or pygame.font.get_default_font()

def print_text(screen, font, x, y, text, fcolor=WHITE):
    """繪製文字"""
    try:
        imgText = font.render(text, True, fcolor)
        screen.blit(imgText, (x, y))
    except pygame.error:
        pass  # 忽略字體渲染錯誤

class Button:
    """按鈕類"""
    def __init__(self, screen, text, x, y, width, height, color, hover_color, font):
        self.screen = screen
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        
    def draw(self):
        """繪製按鈕"""
        pygame.draw.rect(self.screen, self.current_color, self.rect)
        pygame.draw.rect(self.screen, WHITE, self.rect, 2)  # 白色邊框
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        """處理按鈕事件"""
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.hover_color
            else:
                self.current_color = self.color
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('俄羅斯方塊')

    # 初始化字體
    system_font = get_system_font()
    font1 = pygame.font.SysFont(system_font, 24)  # 一般文字
    font2 = pygame.font.Font(None, 72)  # GAME OVER 字體
    button_font = pygame.font.SysFont(system_font, 20)  # 按鈕文字

    # 計算位置
    info_area_x = BLOCK_WIDTH * SIZE + BORDER_WIDTH + 20
    button_width = 160
    button_height = 40
    button_margin = 20  # Increased margin between buttons
    
    # 計算按鈕起始位置，將按鈕位置往下移動
    button_start_y = SCREEN_HEIGHT // 2  # Start buttons from middle of screen

    # 初始化按鈕
    buttons = {
        'start': Button(screen, '開始遊戲', info_area_x, button_start_y, 
                       button_width, button_height, BUTTON_COLOR, BUTTON_HOVER_COLOR, button_font),
        'pause': Button(screen, '暫停', info_area_x, button_start_y + button_height + button_margin,
                       button_width, button_height, BUTTON_COLOR, BUTTON_HOVER_COLOR, button_font),
        'rotate': Button(screen, '旋轉', info_area_x, button_start_y + (button_height + button_margin) * 2,
                        button_width, button_height, BUTTON_COLOR, BUTTON_HOVER_COLOR, button_font),
        'left': Button(screen, '左移', info_area_x, button_start_y + (button_height + button_margin) * 3,
                      button_width, button_height, BUTTON_COLOR, BUTTON_HOVER_COLOR, button_font),
        'right': Button(screen, '右移', info_area_x, button_start_y + (button_height + button_margin) * 4,
                       button_width, button_height, BUTTON_COLOR, BUTTON_HOVER_COLOR, button_font),
        'down': Button(screen, '快速下落', info_area_x, button_start_y + (button_height + button_margin) * 5,
                      button_width, button_height, BUTTON_COLOR, BUTTON_HOVER_COLOR, button_font)
    }

    # 初始化遊戲變數
    global cur_block, next_block, game_area, cur_pos_x, cur_pos_y, game_over, score, speed, orispeed, last_drop_time, last_press_time, pause, start
    
    # Initialize the game variables
    cur_block = blocks.get_block()
    next_block = blocks.get_block()
    game_area = [['.'] * BLOCK_WIDTH for _ in range(BLOCK_HEIGHT)]
    cur_pos_x = (BLOCK_WIDTH - cur_block.end_pos.X - 1) // 2
    cur_pos_y = -1 - cur_block.end_pos.Y
    game_over = True  # Start with game over state
    score = 0
    orispeed = 0.5
    speed = orispeed
    last_drop_time = time.time()
    last_press_time = time.time()
    pause = False
    start = False

    def _dock():
        """處理方塊著陸"""
        global cur_block, next_block, game_area, cur_pos_x, cur_pos_y, game_over, score, speed
        for _i in range(cur_block.start_pos.Y, cur_block.end_pos.Y + 1):
            for _j in range(cur_block.start_pos.X, cur_block.end_pos.X + 1):
                if cur_block.template[_i][_j] != '.':
                    game_area[cur_pos_y + _i][cur_pos_x + _j] = '0'
        if cur_pos_y + cur_block.start_pos.Y <= 0:
            game_over = True
        else:
            # 計算消除
            remove_idxs = []
            for _i in range(cur_block.start_pos.Y, cur_block.end_pos.Y + 1):
                if all(_x == '0' for _x in game_area[cur_pos_y + _i]):
                    remove_idxs.append(cur_pos_y + _i)
            if remove_idxs:
                # 計算得分
                remove_count = len(remove_idxs)
                if remove_count == 1:
                    score += 100
                elif remove_count == 2:
                    score += 300
                elif remove_count == 3:
                    score += 700
                elif remove_count == 4:
                    score += 1500
                speed = orispeed - 0.03 * (score // 10000)
                # 消除
                _i = _j = remove_idxs[-1]
                while _i >= 0:
                    while _j in remove_idxs:
                        _j -= 1
                    if _j < 0:
                        game_area[_i] = ['.'] * BLOCK_WIDTH
                    else:
                        game_area[_i] = game_area[_j]
                    _i -= 1
                    _j -= 1
            cur_block = next_block
            next_block = blocks.get_block()
            cur_pos_x, cur_pos_y = (BLOCK_WIDTH - cur_block.end_pos.X - 1) // 2, -1 - cur_block.end_pos.Y

    def _judge(pos_x, pos_y, block):
        """判斷方塊是否可以移動到指定位置"""
        global game_area
        for _i in range(block.start_pos.Y, block.end_pos.Y + 1):
            if pos_y + block.end_pos.Y >= BLOCK_HEIGHT:
                return False
            for _j in range(block.start_pos.X, block.end_pos.X + 1):
                if pos_y + _i >= 0 and block.template[_i][_j] != '.' and game_area[pos_y + _i][pos_x + _j] != '.':
                    return False
        return True

    def _draw_background(screen):
        """繪製背景"""
        # 填充背景色
        screen.fill(BG_COLOR)
        # 画游戏区域分隔线
        pygame.draw.line(screen, BORDER_COLOR,
                         (SIZE * BLOCK_WIDTH + BORDER_WIDTH // 2, 0),
                         (SIZE * BLOCK_WIDTH + BORDER_WIDTH // 2, SCREEN_HEIGHT), BORDER_WIDTH)

    def _draw_gridlines(screen):
        """繪製網格線"""
        # 画网格线 竖线
        for x in range(BLOCK_WIDTH):
            pygame.draw.line(screen, BLACK, (x * SIZE, 0), (x * SIZE, SCREEN_HEIGHT), 1)
        # 画网格线 横线
        for y in range(BLOCK_HEIGHT):
            pygame.draw.line(screen, BLACK, (0, y * SIZE), (BLOCK_WIDTH * SIZE, y * SIZE), 1)

    def _draw_game_area(screen, game_area):
        """繪製遊戲區域"""
        if game_area:
            for i, row in enumerate(game_area):
                for j, cell in enumerate(row):
                    if cell != '.':
                        pygame.draw.rect(screen, BLOCK_COLOR, (j * SIZE, i * SIZE, SIZE, SIZE), 0)

    def _draw_block(screen, block, offset_x, offset_y, pos_x, pos_y):
        """繪製方塊"""
        if block:
            for i in range(block.start_pos.Y, block.end_pos.Y + 1):
                for j in range(block.start_pos.X, block.end_pos.X + 1):
                    if block.template[i][j] != '.':
                        pygame.draw.rect(screen, BLOCK_COLOR,
                                         (offset_x + (pos_x + j) * SIZE, offset_y + (pos_y + i) * SIZE, SIZE, SIZE), 0)

    def _draw_info(screen, font, pos_x, font_height, score):
        """繪製遊戲資訊"""
        info_y = 10
        line_spacing = font_height + 10
        
        # 遊戲狀態資訊
        print_text(screen, font, pos_x, info_y, f'得分：{score}')
        info_y += line_spacing
        print_text(screen, font, pos_x, info_y, f'速度：{score//10000}')
        info_y += line_spacing * 2
        
        # 下一個方塊提示
        print_text(screen, font, pos_x, info_y, '下一個方塊：')
        info_y += line_spacing * 2
        
        # 鍵盤操作說明
        print_text(screen, font, pos_x, info_y, '鍵盤操作：')
        info_y += line_spacing
        print_text(screen, font, pos_x, info_y, '↑ : 旋轉')
        info_y += line_spacing
        print_text(screen, font, pos_x, info_y, '← → : 左右移動')
        info_y += line_spacing
        print_text(screen, font, pos_x, info_y, '↓ : 加速下落')
        info_y += line_spacing
        print_text(screen, font, pos_x, info_y, 'Space : 暫停')
        info_y += line_spacing
        print_text(screen, font, pos_x, info_y, 'Enter : 開始')

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            
            # 處理按鈕事件
            if buttons['start'].handle_event(event):
                if game_over:
                    start = True
                    game_over = False
                    score = 0
                    speed = orispeed
                    last_drop_time = time.time()
                    last_press_time = time.time()
                    game_area = [['.'] * BLOCK_WIDTH for _ in range(BLOCK_HEIGHT)]
                    cur_block = blocks.get_block()
                    next_block = blocks.get_block()
                    cur_pos_x, cur_pos_y = (BLOCK_WIDTH - cur_block.end_pos.X - 1) // 2, -1 - cur_block.end_pos.Y
            
            if not game_over:
                if buttons['pause'].handle_event(event):
                    pause = not pause

            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_SPACE:
                        pause = not pause
                    
                    if not pause:
                        if event.key in (pygame.K_UP, pygame.K_w):
                            if time.time() - last_press_time > 0.1:
                                last_press_time = time.time()
                                if 0 <= cur_pos_x <= BLOCK_WIDTH - len(cur_block.template[0]):
                                    _next_block = blocks.get_next_block(cur_block)
                                    if _judge(cur_pos_x, cur_pos_y, _next_block):
                                        cur_block = _next_block
                        
                        elif event.key == pygame.K_LEFT:
                            if time.time() - last_press_time > 0.1:
                                last_press_time = time.time()
                                if cur_pos_x > - cur_block.start_pos.X:
                                    if _judge(cur_pos_x - 1, cur_pos_y, cur_block):
                                        cur_pos_x -= 1
                        
                        elif event.key == pygame.K_RIGHT:
                            if time.time() - last_press_time > 0.1:
                                last_press_time = time.time()
                                if cur_pos_x + cur_block.end_pos.X + 1 < BLOCK_WIDTH:
                                    if _judge(cur_pos_x + 1, cur_pos_y, cur_block):
                                        cur_pos_x += 1
                        
                        elif event.key == pygame.K_DOWN:
                            if time.time() - last_press_time > 0.1:
                                last_press_time = time.time()
                                if not _judge(cur_pos_x, cur_pos_y + 1, cur_block):
                                    _dock()
                                else:
                                    last_drop_time = time.time()
                                    cur_pos_y += 1

        _draw_background(screen)

        _draw_game_area(screen, game_area)

        _draw_gridlines(screen)

        if not game_over:
            if pause:
                # Draw pause text in the center of the game area
                pause_text = font2.render("PAUSE", True, WHITE)
                text_rect = pause_text.get_rect(center=(BLOCK_WIDTH * SIZE // 2, SCREEN_HEIGHT // 2))
                screen.blit(pause_text, text_rect)
            else:
                # Draw current block and handle dropping
                _draw_block(screen, cur_block, 0, 0, cur_pos_x, cur_pos_y)
                cur_drop_time = time.time()
                if cur_drop_time - last_drop_time > speed:
                    if not _judge(cur_pos_x, cur_pos_y + 1, cur_block):
                        _dock()
                    else:
                        last_drop_time = cur_drop_time
                        cur_pos_y += 1
        else:
            if start:
                print_text(screen, font2,
                          (SCREEN_WIDTH - font2.size('GAME OVER')[0]) // 2,
                          (SCREEN_HEIGHT - font2.size('GAME OVER')[1]) // 2,
                          'GAME OVER', RED)

        # Always draw score and next block
        _draw_info(screen, font1, info_area_x, font1.size('得分')[1], score)
        _draw_block(screen, next_block, info_area_x, 30 + (font1.size('得分')[1] + 6) * 5, 0, 0)

        # Draw buttons
        for button in buttons.values():
            button.draw()

        pygame.display.flip()

if __name__ == '__main__':
    main()
