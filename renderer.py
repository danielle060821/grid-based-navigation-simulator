import pygame

class Renderer:
    
    def __init__(self):
        self.CELL = 40
        self.ROWS, self.COLS = 15, 15
        self.WIDTH, self.HEIGHT = self.ROWS * self.CELL, self.COLS * self.CELL
        #background
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        #fonts  
        self.large_font = pygame.font.SysFont(None, 60)
        self.small_font = pygame.font.SysFont(None, 40) 
        #a renderer should be able to load these images once it exist
        self.load_imgs()
        
        pygame.display.set_caption("Space Game")
    
    def set_caption(self, title : str):
        pygame.display.set_caption(title)
        
    #be careful -- x, y and row, col are opposite   
    def center_of_cell(self, row, col):
        x = col * self.CELL + self.CELL // 2
        y = row * self.CELL + self.CELL // 2
        return (x, y)
    
    #countdown text before game starts
    def set_countdown(self, time):
        wait_text = self.large_font.render(
            f"Get Ready... {time}",
            True,
            (226, 83, 0)
        )
        rect = wait_text.get_rect(center = (self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(wait_text, rect)
    
    def game_start_text(self):
        game_start_text = self.large_font.render("GO!", True, (226, 83, 0))
        rect = game_start_text.get_rect(center = (self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(game_start_text, rect) 
           
    def over_text(self, text, color):
        over_text = self.large_font.render(text, True, color)
        rect = over_text.get_rect(center = (self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(over_text, rect)
    
    #display steps  
    def display_steps(self, name, steps):
        step_text = self.small_font.render(f"{name} Steps: {steps}", True, (47, 1, 108))
        self.screen.blit(step_text, (10, 10))  
        
    #draw background, or clear page(cover)
    def draw_background(self):
        self.screen.fill((20,20,20))
        
    def load_imgs(self):
        #player(spaceship)
        self.ship_img = pygame.image.load("assets/images/Space_Ship(Player).png").convert_alpha()
        self.ship_img = pygame.transform.scale(self.ship_img, (self.CELL, self.CELL))
        
        #goal(flag)
        self.flag_img = pygame.image.load("assets/images/Flag(Goal).png").convert_alpha()
        self.flag_img = pygame.transform.scale(self.flag_img, (self.CELL, self.CELL))
        
        #astar agent(alien)
        self.alien_img = pygame.image.load("assets/images/Alien(AStar_Agent).png").convert_alpha()
        self.alien_img = pygame.transform.scale(self.alien_img, (self.CELL, self.CELL))
        
        #bc agent(duck)
        self.duck_img = pygame.image.load("assets/images/Duck(BC_Agent).png")
        self.duck_img = pygame.transform.scale(self.duck_img, (self.CELL, self.CELL))
        
    #draw goal and grid(draw goal after girid, or will be covered)
    def draw_static_world(self, grid, goal_row, goal_col) -> None:
        #draw grid
        for r in range(self.ROWS):
            for c in range(self.COLS):
                color = (23, 16, 43) if grid[r][c] == 1 else (217, 211, 253)
                pygame.draw.rect(
                    self.screen,
                    color,
                    (self.CELL * c, self.CELL * r, self.CELL, self.CELL),
                    0
                )                   
        gx, gy = self.center_of_cell(goal_row, goal_col)
        rect = self.flag_img.get_rect(center = (gx, gy))
        self.screen.blit(self.flag_img, rect)
                
    #draw player(put player in the middle of a grid)
    def draw_player(self, player_row, player_col) -> None:
        px,py = self.center_of_cell(player_row, player_col)
        #center
        rect = self.ship_img.get_rect(center = (px, py))
        self.screen.blit(self.ship_img, rect)
        
    #draw A* agent
    def draw_astar_agent(self, astar_row, astar_col) -> None:
        astar_x, astar_y = self.center_of_cell(astar_row, astar_col)
        rect = self.alien_img.get_rect(center = (astar_x, astar_y))
        self.screen.blit(self.alien_img, rect)
        
    def draw_bc_agent(self, bc_row, bc_col) -> None:
        bc_x, bc_y = self.center_of_cell(bc_row, bc_col)
        rect = self.duck_img.get_rect(center = (bc_x, bc_y))
        self.screen.blit(self.duck_img, rect)
        