import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = 5
        self.color = (0, 255, 0)  # 绿色
        self.health = 100
        self.score = 0
        
    def move(self, keys):
        """根据键盘输入移动玩家"""
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
            
        # 边界检查
        self._check_boundaries()
    
    def _check_boundaries(self):
        """确保玩家不会移出屏幕"""
        # 需要根据你的屏幕尺寸调整
        screen_width = 800
        screen_height = 600
        
        self.x = max(0, min(self.x, screen_width - self.width))
        self.y = max(0, min(self.y, screen_height - self.height))
    
    def draw(self, screen):
        """绘制玩家"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def get_rect(self):
        """获取碰撞矩形"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def take_damage(self, damage):
        """受到伤害"""
        self.health -= damage
        return self.health <= 0  # 返回是否死亡
    
    def add_score(self, points):
        """增加分数"""
        self.score += points
