import tkinter as tk
import random

# 游戏界面的行数和列数
ROWS = 4
COLS = 4
# 卡片的宽度和高度（像素）
CARD_WIDTH = 80
CARD_HEIGHT = 100
# 卡片的总数量（需为偶数）
TOTAL_CARDS = ROWS * COLS
# 用于存储卡片对应图案的列表（每个图案有两张卡片对应）
card_symbols = []
# 用于存储卡片按钮对象的二维列表
buttons = [[None for _ in range(COLS)] for _ in range(ROWS)]
# 用于记录已经翻开的卡片（最多同时翻开两张）
flipped_cards = []
# 用于记录匹配成功的卡片对数
matched_pairs = 0

# 创建主窗口
root = tk.Tk()
root.title("记忆翻牌游戏")

# 生成卡片对应的图案列表（确保每种图案有两张）
def generate_symbols():
    symbols = list(range(TOTAL_CARDS // 2)) * 2
    random.shuffle(symbols)
    return symbols

# 创建卡片按钮并绑定点击事件
def create_buttons():
    global card_symbols
    card_symbols = generate_symbols()
    for row in range(ROWS):
        for col in range(COLS):
            index = row * COLS + col
            button = tk.Button(root, width=CARD_WIDTH, height=CARD_HEIGHT,
                               command=lambda r=row, c=col: flip_card(r, c))
            button.grid(row=row, column=col)
            buttons[row][col] = button

# 卡片翻面的处理函数
def flip_card(row, col):
    global flipped_cards, matched_pairs
    button = buttons[row][col]
    index = row * COLS + col
    if button['text'] == "" and len(flipped_cards) < 2:
        button['text'] = card_symbols[index]
        flipped_cards.append(button)
        if len(flipped_cards) == 2:
            check_match()

# 检查翻开的两张卡片是否匹配
def check_match():
    global flipped_cards, matched_pairs
    card1, card2 = flipped_cards
    if card1['text'] == card2['text']:
        card1['state'] = tk.DISABLED
        card2['state'] = tk.DISABLED
        matched_pairs += 1
        if matched_pairs == TOTAL_CARDS // 2:
            game_won()
    else:
        root.after(1000, lambda: hide_cards())
    flipped_cards = []

# 将翻开的不匹配卡片重新翻面隐藏
def hide_cards():
    for card in flipped_cards:
        card['text'] = ""

# 游戏胜利的处理函数，弹出提示框告知玩家获胜
def game_won():
    tk.messagebox.showinfo("游戏胜利", "恭喜你，成功匹配所有卡片！")

# 主函数，启动游戏流程
def main():
    create_buttons()
    root.mainloop()

if __name__ == "__main__":
    main()
