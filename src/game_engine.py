import pygame
import sys
from player import Player
from enemy import EnemyManager

class GameEngine:
    def __init__(self, screen_width=800, screen_height=600):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = None
        self.clock = None
        self.player = None
        self.enemy_manager = None
        self.running = False
        self.game_state = "menu"  # menu, playing, game_over
        self.font = None
        
    def initialize(self):
        """初始化游戏引擎"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Dodge Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        # 初始化游戏对象
        self.player = Player(self.screen_width // 2, self.screen_height - 100)
        self.enemy_manager = EnemyManager()
        
    def handle_events(self):
        """处理游戏事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE and self.game_state == "menu":
                    self.start_game()
                elif event.key == pygame.K_r and self.game_state == "game_over":
                    self.restart_game()
    
    def start_game(self):
        """开始新游戏"""
        self.game_state = "playing"
        self.player.health = 100
        self.player.score = 0
        self.enemy_manager.enemies.clear()
    
    def restart_game(self):
        """重新开始游戏"""
        self.player = Player(self.screen_width // 2, self.screen_height - 100)
        self.enemy_manager = EnemyManager()
        self.start_game()
    
    def update(self):
        """更新游戏状态"""
        if self.game_state != "playing":
            return
            
        # 获取按键状态
        keys = pygame.key.get_pressed()
        
        # 更新玩家
        self.player.move(keys)
        
        # 更新敌人
        self.enemy_manager.update(self.screen_width, self.screen_height)
        
        # 检查碰撞
        collisions = self.enemy_manager.check_collisions(self.player.get_rect())
        for enemy in collisions:
            if self.player.take_damage(10):
                self.game_state = "game_over"
            self.enemy_manager.enemies.remove(enemy)
    
    def draw(self):
        """绘制游戏画面"""
        self.screen.fill((0, 0, 0))  # 黑色背景
        
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "playing":
            self.draw_game()
        elif self.game_state == "game_over":
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_menu(self):
        """绘制开始菜单"""
        title = self.font.render("Dodge Game", True, (255, 255, 255))
        instruction = self.font.render("Press SPACE to start", True, (255, 255, 255))
        
        self.screen.blit(title, (self.screen_width//2 - title.get_width()//2, 200))
        self.screen.blit(instruction, (self.screen_width//2 - instruction.get_width()//2, 300))
    
    def draw_game(self):
        """绘制游戏画面"""
        # 绘制玩家
        self.player.draw(self.screen)
        
        # 绘制敌人
        self.enemy_manager.draw(self.screen)
        
        # 绘制UI
        health_text = self.font.render(f"Health: {self.player.health}", True, (255, 255, 255))
        score_text = self.font.render(f"Score: {self.player.score}", True, (255, 255, 255))
        
        self.screen.blit(health_text, (10, 10))
        self.screen.blit(score_text, (10, 50))
    
    def draw_game_over(self):
        """绘制游戏结束画面"""
        game_over = self.font.render("GAME OVER", True, (255, 0, 0))
        score = self.font.render(f"Final Score: {self.player.score}", True, (255, 255, 255))
        restart = self.font.render("Press R to restart", True, (255, 255, 255))
        
        self.screen.blit(game_over, (self.screen_width//2 - game_over.get_width()//2, 200))
        self.screen.blit(score, (self.screen_width//2 - score.get_width()//2, 250))
        self.screen.blit(restart, (self.screen_width//2 - restart.get_width()//2, 300))
    
    def run(self):
        """运行游戏主循环"""
        self.initialize()
        self.running = True
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()
