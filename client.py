import pygame
from network import Network

widthWin, heightWin = 500, 500
win = pygame.display.set_mode((widthWin, heightWin))
pygame.display.set_caption("Client")

clientNum = 0

class Player():
    def __init__(self, x, y, width, height, color):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
    
    def move(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        
        self.update()
        
    def update(self):
        self.x, self.y = self.rect.x, self.rect.y
        

def read_pos(str): # 'string ex: 45,67   '
    str = str.split(",")
    return int(str[0]), int(str[1]) #converting string version which is recieved from server to pos for use in client code

def make_pos(tup):
    return str(tup[0]) + ',' + str(tup[1]) # converting client pos from it code, into string to send to server

def redrawWindow(win, player, player2):
    win.fill((255,255,255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def main():
    run = True
    n = Network()
    startPos = read_pos(n.getPos())
    player = Player(startPos[0], startPos[1], 100, 100, (0, 255, 0))
    player2 = Player(0,0, 100, 100, (255,0, 0))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        
        p2Pos = read_pos(n.send(make_pos((player.x, player.y)))) # sending our own position, to in return get player 2 position and sotring the info gained from server in the variable
        player2.rect.x = p2Pos[0]
        player2.rect.y = p2Pos[1]
        player2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        player.move()
        redrawWindow(win, player, player2)

if '__main__':
    main()