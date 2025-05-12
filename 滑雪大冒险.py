# 游戏帧率与屏幕尺寸
FPS = 40
SCREENSIZE = (640, 640)

# 字体与图片路径配置
FONT_PATH = os.path.join('assets/fonts/STHUPO.TTF')  # 主字体
SKIER_IMAGE_PATHS = [
    'resources/images/skier_forward.png',  # 正面
    'resources/images/skier_right1.png',  # 右转1
    'resources/images/skier_right2.png',  # 右转2
    # ...其他姿态图片
]
滑雪者类（核心逻辑）

class SkierClass(pygame.sprite.Sprite):
    def __init__(self):
        self.direction = 0  # 0=正面, -1=左转, 1=右转
        self.image = pygame.image.load(self.imagepaths[self.direction])
        self.rect = self.image.get_rect()
        self.rect.center = [320, 100]  # 初始位置
        self.speed = [self.direction, 6]  # [横向速度, 纵向速度]

    def turn(self, num):  # 转向控制
        self.direction += num
        self.direction = max(-2, min(2, self.direction))  # 限制转向幅度
        self.image = pygame.image.load(self.imagepaths[self.direction])
        self.speed = [self.direction, 6-abs(self.direction)*2]  # 转向时减速
障碍物生成系统

def createObstacles(start_row, end_row, num=10):
    obstacles = pygame.sprite.Group()
    for _ in range(num):
        row = random.randint(start_row, end_row)
        col = random.randint(0, 9)
        location = [col*64+20, row*64+20]  # 网格化生成位置
        attribute = random.choice(['tree', 'flag'])  # 随机障碍物类型
        obstacle = ObstacleClass(img_path, location, attribute)
        obstacles.add(obstacle)
游戏主循环逻辑

while True:
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: 
                speed = skier.turn(-1)  # 左转
            elif event.key == pygame.K_RIGHT:
                speed = skier.turn(1)   # 右转
    
    # 游戏状态更新
    skier.move()
    distance += speed[1]  # 累计滑行距离
    if distance >= 1280:  # 到达场景边界时
        generateNewObstacles()  # 生成新障碍物
    
    # 碰撞检测
    if pygame.sprite.spritecollide(skier, obstacles, False):
        handleCollision()  # 处理碰撞逻辑
    
    # 画面渲染
    screen.fill((255, 255, 255))  # 白色背景
    drawAllElements()  # 绘制所有游戏元素
    pygame.display.update()
    clock.tick(FPS)  # 控制帧率
