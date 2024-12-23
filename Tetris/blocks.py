import random
from collections import namedtuple

Point = namedtuple('Point', 'X Y')
Shape = namedtuple('Shape', 'X Y Width Height')
Block = namedtuple('Block', 'template start_pos end_pos name next')

# 方塊形狀設計說明：
# 1. 使用 4×4 的矩陣來設計方塊，因為所有方塊的長寬最大都是4格
# 2. 這樣的設計可以簡化旋轉邏輯，只需要替換成預定義的下一個方向即可
# 3. 通過固定左上角座標來確保方塊位置的一致性

# S形方塊
S_BLOCK = [Block(['.OO',
                  'OO.',
                  '...'], Point(0, 0), Point(2, 1), 'S', 1),
           Block(['O..',
                  'OO.',
                  '.O.'], Point(0, 0), Point(1, 2), 'S', 0)]

# Z形方塊
Z_BLOCK = [Block(['OO.',
                  '.OO',
                  '...'], Point(0, 0), Point(2, 1), 'Z', 1),
           Block(['.O.',
                  'OO.',
                  'O..'], Point(0, 0), Point(1, 2), 'Z', 0)]

# I型方塊
I_BLOCK = [Block(['.O..',
                  '.O..',
                  '.O..',
                  '.O..'], Point(1, 0), Point(1, 3), 'I', 1),
           Block(['....',
                  '....',
                  'OOOO',
                  '....'], Point(0, 2), Point(3, 2), 'I', 0)]

# O型方塊
O_BLOCK = [Block(['OO',
                  'OO'], Point(0, 0), Point(1, 1), 'O', 0)]

# J型方塊
J_BLOCK = [Block(['O..',
                  'OOO',
                  '...'], Point(0, 0), Point(2, 1), 'J', 1),
           Block(['.OO',
                  '.O.',
                  '.O.'], Point(1, 0), Point(2, 2), 'J', 2),
           Block(['...',
                  'OOO',
                  '..O'], Point(0, 1), Point(2, 2), 'J', 3),
           Block(['.O.',
                  '.O.',
                  'OO.'], Point(0, 0), Point(1, 2), 'J', 0)]

# L型方塊
L_BLOCK = [Block(['..O',
                  'OOO',
                  '...'], Point(0, 0), Point(2, 1), 'L', 1),
           Block(['.O.',
                  '.O.',
                  '.OO'], Point(1, 0), Point(2, 2), 'L', 2),
           Block(['...',
                  'OOO',
                  'O..'], Point(0, 1), Point(2, 2), 'L', 3),
           Block(['OO.',
                  '.O.',
                  '.O.'], Point(0, 0), Point(1, 2), 'L', 0)]

# T型方塊
T_BLOCK = [Block(['.O.',
                  'OOO',
                  '...'], Point(0, 0), Point(2, 1), 'T', 1),
           Block(['.O.',
                  '.OO',
                  '.O.'], Point(1, 0), Point(2, 2), 'T', 2),
           Block(['...',
                  'OOO',
                  '.O.'], Point(0, 1), Point(2, 2), 'T', 3),
           Block(['.O.',
                  'OO.',
                  '.O.'], Point(0, 0), Point(1, 2), 'T', 0)]

BLOCKS = {'O': O_BLOCK,
          'I': I_BLOCK,
          'Z': Z_BLOCK,
          'T': T_BLOCK,
          'L': L_BLOCK,
          'S': S_BLOCK,
          'J': J_BLOCK}


def get_block():
    """隨機取得一個方塊"""
    block_name = random.choice('OIZTLSJ')
    b = BLOCKS[block_name]
    idx = random.randint(0, len(b) - 1)
    return b[idx]


def get_next_block(block):
    """取得方塊的下一個旋轉狀態"""
    b = BLOCKS[block.name]
    return b[block.next]
