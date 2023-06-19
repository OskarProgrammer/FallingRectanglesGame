import pygame 
import random
import time
class Game(object):
    def __init__(self):
        self.run()

    def loop(self):
        self.score = 0
        self.position_play = pygame.Vector2(self.screen.get_width()/2, self.screen.get_height()/2)
        self.coor = []
        self.i = 0

        self.RUNNING = True
        self.GAINED = True

        while self.RUNNING:
            self.background()
            self.player()
            
            if self.GAINED:
                self.generate_point()
                self.GAINED = False

            self.point()

            if self.event_handling():
                self.warning()
                time.sleep(3)
                self.loop()

            try:
                self.isPoint()
            except:
                pass

            self.score_tab()

            try: 
                self.isLose()
            except:
                pass

            if self.i % 10 == 0:
                self.generate_enemy()

            self.key = pygame.key.get_pressed()
            self.movement()
            self.move_enemy()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.key[pygame.K_ESCAPE]:
                    self.RUNNING = False

            self.i += 1

            pygame.display.flip()
            self.fps()
        
        pygame.quit()

    def event_handling(self) -> bool:
        if self.position_play.x > self.screen.get_width() or self.position_play.y > self.screen.get_height() or self.position_play.x < -20 or self.position_play.y < -20:
            self.position_play.y = self.screen.get_height()
            self.position_play.x = self.screen.get_width()
            return True
        return False

    def isPoint(self):
        if self.player_rect.colliderect(self.point_coor):
            self.add()
            self.GAINED = True

    def point(self):

        pygame.draw.rect(self.screen, "green",self.point_coor)

    def generate_point(self):
        x = random.randint(0,self.screen.get_width())
        y = random.randint(0,self.screen.get_height())

        self.point_coor = pygame.Rect(x,y,40,40)


    def warning(self):
        width = self.screen.get_width()/4 # set this to self.screen.get_width()/3 if you want fullscreen
        height = self.screen.get_height()/2

        self.font = pygame.font.SysFont('comicsans', 50)

        self.label = self.font.render(f'YOU CANT TOUCH THE BORDER', 1, "red", "white")
        self.label2 = self.font.render(f'RESTARTING WITH SCORE 0 ', 1, "red", "white")

        self.screen.blit(self.label, (width-70, height/2+100))
        self.screen.blit(self.label2, (width-40, height/2+135))

        pygame.display.flip()


    def add(self):
        self.score+=1

    def score_tab(self):
        self.font = pygame.font.SysFont('comicsans', 40)
        self.label = self.font.render(f'Score: {self.score}         ', 1, "black", "white")
        self.screen.blit(self.label, (0,0))

    def isLose(self):
        for x in range(0,len(self.coor)):
            enemy_rect = pygame.Rect(self.coor[x][0], self.coor[x][1],40,40)
            if self.player_rect.colliderect(enemy_rect):
                self.ending_screen()
            else:
                continue
    
    def ending_screen(self):
        self.background()

        width = self.screen.get_width()/4     #set this to self.screen.get_width()/3 if you want fullscreen, I think that would look better ! ;-)
        height = self.screen.get_height()/2

        self.font = pygame.font.SysFont('comicsans', 50)

        self.label = self.font.render(f'You lost... Your score: {self.score}', 1, "black", "white")
        self.label2 = self.font.render(f'Click y to play again', 1, "black", "white")
        self.label3 = self.font.render(f'Click q to leave', 1, "black", "white")

        x = 40
        self.screen.blit(self.label, (width, height-x)) 
        self.screen.blit(self.label2, (width+32, height+35-x)) 
        self.screen.blit(self.label3, (width+64, height+72-x)) 

        pygame.display.flip()

        while self.RUNNING:
            self.choice = pygame.key.get_pressed()
            
            for event in pygame.event.get():
                if self.choice[pygame.K_y] or self.choice[pygame.K_KP_ENTER]:
                    self.loop()
                elif self.choice[pygame.K_n] or self.choice[pygame.K_ESCAPE] or self.choice[pygame.K_q] or event.type == pygame.QUIT:
                    pygame.quit()
                    

    def generate_enemy(self):
        for _ in range(0,2):
            self.enemy()
        
    def enemy(self):
        left = random.randint(0, self.screen.get_width())

        EXIST = True

        while EXIST:
            for x in range(0,len(self.coor)):
                if self.coor[x][0] == left:
                    left = random.randint(0, self.screen.get_width())
                else:
                    continue
            EXIST = False

        self.coor.append([left, 0])

        self.enemy_rect = pygame.Rect(left, 0, 40, 40)
        pygame.draw.rect(self.screen, "red", self.enemy_rect)

    def move_enemy(self):
        for x in range(len(self.coor)):
            self.coor[x][1] += 5
            enemy = pygame.Rect(self.coor[x][0],self.coor[x][1],40,40)
            pygame.draw.rect(self.screen, "red", enemy)

    def player(self):
        self.player_rect = pygame.Rect(self.position_play.x, self.position_play.y, 34, 34)
        pygame.draw.rect(self.screen, "white", self.player_rect)

    def movement(self):
        if self.key[pygame.K_LEFT] or self.key[pygame.K_a]:
            self.position_play.x -=10
        elif self.key[pygame.K_RIGHT] or self.key[pygame.K_d]:
            self.position_play.x +=10
        elif self.key[pygame.K_DOWN] or self.key[pygame.K_s]:
            self.position_play.y +=10
        elif self.key[pygame.K_UP] or self.key[pygame.K_w]:
            self.position_play.y -=10

    def background(self):
        self.screen.fill("black")

    def run(self):
        pygame.init() #initialize application
        self.screen = pygame.display.set_mode((800, 600)) #setting resolution
        self.clock = pygame.time.Clock() #starting clock
        
        # pygame.display.toggle_fullscreen()  turning on the fullscreen if you want
        pygame.display.set_caption("Falling rectangles") #setting the title of app
        pygame.display.set_icon(pygame.image.load("pobrane.png")) #changing the icon

    def fps(self):
        self.clock.tick(45)/10000 #configurating frame rate

    def exit(self):
        pygame.quit()
        
App = Game()
App.loop()
