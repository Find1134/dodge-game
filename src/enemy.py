import pygame
import random

class Enemy:
    def __init__(self, x, y, enemy_type="normal"):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.speed = self._get_speed()
        self.color = self._get_color()
        self.size = self._get_size()
        self.health = self._get_health()
        
    def _get_speed(self):
        """根据敌人类型返回速度"""
        speeds = {
            "normal": 3,
            "fast": 6,
            "slow": 1,
            "boss": 2
        }
        return speeds.get(self.type, 3)
    
    def _get_color(self):
        """根据敌人类型返回颜色"""
        colors = {
            "normal": (255, 0, 0),    # 红色
            "fast": (255, 165, 0),    # 橙色
            "slow": (139, 0, 0),      # 深红色
            "boss": (128, 0, 128)     # 紫色
        }
        return colors.get(self.type, (255, 0, 0))
    
    def _get_size(self):
        """根据敌人类型返回大小"""
        sizes = {
            "normal": 30,
            "fast": 20,
            "slow": 40,
            "boss": 80
        }
        return sizes.get(self.type, 30)
    
    def _get_health(self):
        """根据敌人类型返回生命值"""
        health_points = {
            "normal": 1,
            "fast": 1,
            "slow": 2,
            "boss": 5
        }
        return health_points.get(self.type, 1)
    
    def update(self):
        """更新敌人位置"""
        self.y += self.speed
        
    def draw(self, screen):
        """绘制敌人"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
    
    def get_rect(self):
        """获取碰撞矩形"""
        return pygame.Rect(self.x, self.y, self.size, self.size)
    
    def is_off_screen(self, screen_height):
        """检查敌人是否离开屏幕"""
        return self.y > screen_height
    
    def take_damage(self):
        """敌人受到伤害"""
        self.health -= 1
        return self.health <= 0  # 返回是否死亡

class EnemyManager:
    def __init__(self):
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_delay = 60  # 帧数
        
    def update(self, screen_width, screen_height):
        """更新所有敌人"""
        # 生成新敌人
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_enemy(screen_width)
            self.spawn_timer = 0
            
        # 更新敌人位置并移除离开屏幕的敌人
        self.enemies = [enemy for enemy in self.enemies if not enemy.is_off_screen(screen_height)]
        for enemy in self.enemies:
            enemy.update()
    
    def spawn_enemy(self, screen_width):
        """生成新敌人"""
        x = random.randint(0, screen_width - 30)
        enemy_type = random.choice(["normal", "fast", "slow"])
        self.enemies.append(Enemy(x, -30, enemy_type))
    
    def draw(self, screen):
        """绘制所有敌人"""
        for enemy in self.enemies:
            enemy.draw(screen)
    
    def check_collisions(self, player_rect):
        """检查与玩家的碰撞"""
        collisions = []
        for enemy in self.enemies[:]:
            if player_rect.colliderect(enemy.get_rect()):
                collisions.append(enemy)
        return collisions
