#Programmed by: Jonathon Gooch
#Project: Brick Breaker
#Last Updated: 21/11/2013

#Importing modules
import pygame, sys, time, random
from pygame.locals import *
from timeit import default_timer

#initiating pygame
pygame.init()

#Declaring the clock to limit the amount of times the screen is refreshed per second
Clock = pygame.time.Clock()

#Declares Colour Variables
BLACK = [0 , 0, 0]
WHITE = [255, 255, 255]
GREY = [127, 127, 127]
RED = [255, 0, 0]

#States the game has not started
Game_Started = False

#Declaring direction for the ball movement variables
UP = 'UP'
UPLEFT = 'UPLEFT'
UPRIGHT = 'UPRIGHT'
DOWN = 'DOWN'
DOWNLEFT = 'DOWNLEFT'
DOWNRIGHT = 'DOWNRIGHT'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

class Screen:
    #Declaring Screen Size variables
    Width = 800
    Height = 600
    
    def Setup(self):
        #Draws the window, Sets the caption and the game icon on the top of the window
        self.Window = pygame.display.set_mode((self.Width,self.Height),0,32)
        pygame.display.set_caption("Brick Breaker")
        self.Icon = pygame.image.load("Assets/Computing game images/BB_Icon.bmp")
        pygame.display.set_icon(self.Icon)

        #Makes mouse invisible when hovering over game.
        pygame.mouse.set_visible(False)
        

class Background:
    #Declares the movement per iteration in the x axis for the background.
    MoveX = 1
    Moving = True
    
    def Animate(self):
        Background_Text = ('Press Space to Pause the background')
        Background_Font = pygame.font.SysFont('Calibri', 25)
        #Animates the background by having 2 images which move across the screen side by side
        #When one leaves the right side of the screen its X position changes to the left side
        
        #Increases the x value of the X of both of the images which are moving across the screen
        #by however many pixels it moves per iteration
        if self.Moving == True:
            self.BG_1.X += self.MoveX
            self.BG_2.X += self.MoveX

        #Draws the images to the screen with the new positions and writes the toggle text to the screen.
        Screen.Window.blit(self.BG_1.Image, (self.BG_1.X ,self.BG_1().Y))
        Screen.Window.blit(self.BG_2.Image, (self.BG_2.X ,self.BG_2().Y))
        Write_line(Background_Text, Background_Font, WHITE, 400, 10, "Center")
        
        #Changes the X position of the image to the left side of the screen
        #if the image leaves the right side of the screen.
        if self.BG_1.X >= Screen.Width or self.BG_1.X < -1600:
            self.BG_1.X = -1600
        if self.BG_2.X >= Screen.Width or self.BG_2.X < -1600:
            self.BG_2.X = -1600

    def Toggle(self):
        if self.Moving == True:
            self.Moving = False
            
        elif self.Moving == False:
            self.Moving = True
        
    class BG_1:
        #Holds all of the image properties for the first background image
        #Position
        X = 0
        Y = 0
    
        #Image file
        File_name = "Assets/Computing game images/Stars.jpg"
        Image = pygame.image.load(File_name)
        

    class BG_2:
        #Holda all of the image properties for the second background image
        #Position
        X = -1600
        Y = 0

        #Image file
        File_name = "Assets/Computing game images/Stars.jpg"
        Image = pygame.image.load(File_name)

class Leaderboards:
    #Holds all of the leaderboard data and subroutines
    #Holds the 3 highest scores until the game is shut down.
    Scorelist = []
    
    #Holds the 3 highest scorers names until the game is shut down.
    Namelist = []
    
    def Update(self):
    #Checks if the Score is more than any of the scores in the leaderboards if it is then the score is replaced with the new score
    #and the existing scores are moved down the leaderboards. Then the scores are saved.
        #For every score in The score list.
        for Scores in range(len(self.Scorelist)):

            #Scores between the first and last ( in this case score 2)
            if Scores > 0 and Scores < len(self.Scorelist) - 1:
                if Score > self.Scorelist[Scores] and Score > self.Scorelist[Scores - 1] and Score < self.Scorelist[Scores + 1]:
                    for items in range(Scores):
                        self.Scorelist[Scores - 1] = self.Scorelist[Scores]
                        self.Namelist[Scores - 1] = self.Namelist[Scores]
                    self.Scorelist[Scores] = Score
                    self.Save()
                    
            #Lowest Score (in this case score 0)    
            if Score > self.Scorelist[0] and Score < self.Scorelist[1]:
                self.Scorelist[Scores] = Score
                self.Save()
                
            #Highest Score (in this case score 1) 
            elif Scores == len(self.Scorelist) - 1:
                if Score > self.Scorelist[Scores] and Score > self.Scorelist[len(self.Scorelist) - 1]:
                    for items in range(len(self.Scorelist)):
                        if items != 0:
                            self.Scorelist[items - 1] = self.Scorelist[items]
                            self.Namelist[Scores - 1] = self.Namelist[Scores]
                    self.Scorelist[Scores] = Score
                    self.Save()

    def Load(self):
        #Opens the HighScore File
        HighScore_File = open('Assets/HighScore.txt', 'r')

        #For every line in the file the data is taken and put into the appropriate list
        for line in HighScore_File:
            self.Scorelist.append(int(line[:-4]))
            self.Namelist.append(str(line[-4:-1]))
            
        #Closes the file
        HighScore_File.close

    def Save(self):
        #Opens the HighScore File
        HighScore_File = open('Assets/HighScore.txt', 'w')
        
        #For every peice of data in each list write the data to the file which is linked together
        for Scores in range(len(self.Scorelist)):
            HighScore_File.write(str(self.Scorelist[Scores]) + " " + self.Namelist[Scores] + '\n')

        #Closes the file
        HighScore_File.close
        
class BlockSet:
    def Respawn(self):
        #Setting Identifiers for Block Settings
        #List to hold the how many hits the block has taken.
        self.Destroyed = []

        #Positional
        self.X = 20       
        self.Y = 1

        #Area
        self.Width = 60     
        self.Height = 20
                
    def Setup(self):
        global Blocks_Rows
        #List holding all of the row types.
        Rowlist = [
        "----------",
        "-=-=-=-=-=",
        "=-=-=-=-=-",
        "=--------=",
        "==------==",
        "===----===",
        "====--====",
        "==========",
        "----==----",
        "---====---",
        "--======--",
        "-========-"
        ]
        
        #How many rows of blocks need  to be made
        Rows = 4
        
        #Makes a list for new rows Y positions
        RowY = []

        #Holds the data of a single row ready for adding to the list of rows
        Blocks_Row = []
        
        #Declares where all rows are kept.
        Blocks_Rows = []
    
        #For however many rows are wanted add a row to the list of rows.    
        for i in range(Rows):
            #Randomises the type of row added to the row list and adds it to the list
            Randomiser = random.randint(0, len(Rowlist)-1)
            Blocks_Row = list(Rowlist[Randomiser])
            
            #For all blocks in the row...
            for b in range(len(Blocks_Row)):
                #Sets the position of the next object
                self.Y = (80+(i*30))
                self.X = (70*(b + 1))
                
                #If the block type was block type 1 then...
                if Blocks_Row[b] == "-":
                    #Set the rectangular area and replaces the character
                    Blocks_Row[b] = pygame.Rect(self.X, self.Y, self.Width, self.Height)

                    #sets the amount of hits it takes to 1
                    self.Destroyed.append(1)
                    
                #If the block type was block type 2 then...
                if Blocks_Row[b] == "=":
                    #Set the rectangular area and replaces the character
                    Blocks_Row[b] = pygame.Rect(self.X, self.Y, self.Width, self.Height)
                    
                    #sets the amount of hits it takes to 2
                    self.Destroyed.append(2)
                    
                else:
                    #If any other character then the loop continue and leaves the space blank
                    continue
    
                
            #The row is then added to the list of rows
            Blocks_Rows.append(Blocks_Row)
            
      
class Player:
    def Area(self):
        #Declares the player area variables to help the readability
        self.left = self.Sprite.left
        self.right = self.Sprite.right 
        self.top = self.Sprite.top
        self.bottom = self.Sprite.bottom
    
    def Move(self):
        # Moves the player by the movement per iteration value
        self.X += self.MoveX
        
        #Draws the image to the screen
        self.Sprite = pygame.Rect(self.X, self.Y, self.Width, self.Height)
        pygame.draw.rect(Screen.Window,self.Colour, self.Sprite, 0)
        
    def Respawn(self):
        #Declares and Resets Player Variables
        #Positional
        self.X = 370
        self.Y = 550

        #Movement
        self.MoveX = 0
        self.MoveY = 0
        self.MoveSpeed = Level + 3

        #Colour
        self.Colour = GREY

        #Area
        self.Width = 60
        self.Height = 20
        self.Sprite = pygame.Rect(self.X, self.Y, self.Width, self.Height)
  
class Ball:
    def Area(self):
        #Declares the ball area variables to help the readability
        self.left = self.Sprite.left
        self.right = self.Sprite.right 
        self.top = self.Sprite.top
        self.bottom = self.Sprite.bottom
        
    def Move(self):
        #Changes the Movement variables depending on what the direction of the ball is and then moves it
        #If the direction is down then the movement in the Y direction moves down by the movespeed
        if self.Direction == DOWN:
            self.MoveY = self.MoveSpeed
            
        #If the direction is up then the movement in the Y direction moves up by the movespeed
        elif self.Direction == UP:
            self.MoveY = -self.MoveSpeed

        #If the direction is upleft then the movement in the Y direction moves upleft by the movespeed
        elif self.Direction == UPLEFT:
            self.MoveY = -self.MoveSpeed
            self.MoveX = -self.MoveSpeed

        #If the direction is upright then the movement in the Y direction moves upright by the movespeed
        elif self.Direction == UPRIGHT:
            self.MoveY = -self.MoveSpeed
            self.MoveX = self.MoveSpeed

        #If the direction is downleft then the movement in the Y direction moves downleft by the movespeed
        elif self.Direction == DOWNLEFT:
            self.MoveY = self.MoveSpeed
            self.MoveX = -self.MoveSpeed

        #If the direction is downright then the movement in the Y direction moves downright by the movespeed
        elif self.Direction == DOWNRIGHT:
            self.MoveY = self.MoveSpeed
            self.MoveX = self.MoveSpeed

        #Moves the ball by the movement per iteration in both dimensions.    
        self.Y += self.MoveY
        self.X += self.MoveX

        #Refreshes the ball drawing variable with the required values.
        self.Sprite = pygame.draw.circle(Screen.Window, self.Colour, (self.X, self.Y) , self.Radius)
        
    def Respawn(self):
        #Declares and Resets Ball Variables
        #Positional
        self.Direction = DOWN
        self.X = 400
        self.Y = 500

        #Movement
        self.MoveX = 0
        self.MoveY = 1
        self.MoveSpeed = 0
        
        #Colour
        self.Colour = GREY

        #Area
        self.Radius = 10
        self.Sprite = pygame.draw.circle(Screen.Window, self.Colour, (self.X, self.Y) , self.Radius)

def Refresh_Screen():
    #Updates the whole screen at 60 frames per second.
    pygame.display.update()
    Clock.tick(60)

def Write_Text(Text, Font, Colour, x , y, distance_apart, Area):
    #Writes out multiple line text onto the screen when given the appropriate parameters
    #Puts the entered Area data into lower case to make it more reliable.
    Area = Area.lower()

    #For every line entered.
    for line in Text:
        #Defines the text to be rendered
        Render = Font.render(line, True, Colour)
        
        #Defines the position the text will go
        Position = Render.get_rect()
        Position.centery = (Text.index(line) * distance_apart) + y
        if Area == "center":
            Position.centerx = x
        else:
            Position.x = x
        
        #Draws text to the screen
        Screen.Window.blit(Render, Position)
        
        
def Write_line(Text, Font, Colour, x , y, Area):
    #Writes out single line text onto the screen when given the appropriate parameters
    #Puts the entered Area data into lower case to make it more reliable.
    Area = Area.lower()
    
    #Defines the text to be rendered
    Render = Font.render(Text, True, Colour)
        
    #Defines the position the text will go
    Position = Render.get_rect()
    Position.centery = y
    if Area == "center":
        Position.centerx = x
    elif Area == "left":
        Position.x = x
        
    #Draws text to the screen
    Screen.Window.blit(Render, Position)
    
def Write_Level(Level):
    Time_Delay = 1
    Timer_start = default_timer()
    duration = default_timer() - Timer_start
    while duration < Time_Delay:
        duration = default_timer() - Timer_start
        
        #This subroutine tells the player which level the player is on before the level starts.
        #Background is animated
        Background.Animate()
    
        #Declares the font to use.
        Level_Font = pygame.font.SysFont('Calibri', 30)
    
        #Declares the text which comes up when the screen comes up.
        Level_Text = ("Level: " + str(Level))
    
        #Draws the title text to the screen.
        Write_line(Level_Text, Level_Font, WHITE, 400, 300, "Center")
        
        #Refreshes the image
        Refresh_Screen()
    
        
 
def Start_Screen():
    #This is the Start Screen which runs when the game is started.
    #Declares the menu background image file
    File_name = "Assets/Computing game images/Menu image.png"
    Image = pygame.image.load(File_name).convert_alpha()

    #Positions the menu background image file
    ImagePos = Image.get_rect()
    ImagePos.centerx = Screen.Window.get_rect().centerx
    ImagePos.centery = Screen.Window.get_rect().centery

    #Declares the font and text used for the title of the screen.
    Title_Text = ("Brick",
                  "Breaker")
    Title_Font = pygame.font.SysFont('Calibri', 90)
    
    #Declares the text and font used for the highscore displayed under the title
    HighScore_Text = ("HighScore: " + str(Leaderboards.Scorelist[len(Leaderboards.Scorelist) - 1]))
    HighScore_Font = pygame.font.SysFont('Calibri', 40)
    
    #Declares the text and font used for the menu text
    Menu_Text = ('Play',
                'Instructions',
                'Leaderboards',
                'Exit')
    Menu_Font = pygame.font.SysFont('Calibri', 30)

    #Sets the Option which is highlighted when the game starts to the first option
    Option_Highlighted = 0
    
    while True:
        #Animates the background
        Background.Animate()
        
        #Draws Content box to screen
        Screen.Window.blit(Image, ImagePos)
        
        #Writes and positions text for Start menu
        Write_Text(Title_Text, Title_Font, WHITE, 400, 150 , 65, "Center")
        Write_line(HighScore_Text, HighScore_Font, WHITE, 400, 270 , "Center")
        Write_Text(Menu_Text, Menu_Font, WHITE, 260, 320 , 50, "Left")

        #For all of the options in the menu if the option highlighted number is the
        #same as the option number then the option is highlighted.
        for Options in range(len(Menu_Text)):
            if Option_Highlighted == Options:
                Selector_Y = (Options * 50) + 320
                Write_line(">", Menu_Font, WHITE, 250, Selector_Y , "Center")
                
        #If the option highlighted is more than the options on the screen then the first option is highlighted
        if Option_Highlighted > len(Menu_Text) - 1:
            Option_Highlighted = 0
            
        #If the option highlighted is less than the first option then the last option is highlighted    
        elif Option_Highlighted < 0:
            Option_Highlighted = len(Menu_Text) - 1 

        Refresh_Screen()
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    # If the option 1 is highlighted and enter is pressed then the game starts
                    if Option_Highlighted == 0:
                        return
                    
                    # If the option 2 is highlighted and enter is pressed then the instructions screen loads
                    if Option_Highlighted == 1:
                        Instructions()

                    # If the option 3 is highlighted and enter is pressed then the Leaderboards screen loads    
                    if Option_Highlighted == 2:
                        Leaderboards_Screen()

                    # If the option 4 is highlighted and enter is pressed then the game shuts down
                    if Option_Highlighted == 3:
                        pygame.quit()
                        sys.exit()
                        
                # If the up key is pressed the previous option is selected
                if event.key == K_UP:
                    Option_Highlighted -= 1
                    
                # If the down key is pressed the next option is selected
                if event.key == K_DOWN:
                    Option_Highlighted += 1

                # If the space key is pressed the background stops moving
                if event.key == K_SPACE:
                    Background.Toggle()
                    
            #If the window X button is pressed then the game shuts down        
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

def Instructions():
    #Writes instructions to screen until player goes back to menu.
    #Declares the Image file ready for use
    File_name = "Assets/Computing game images/Menu image.png"
    Image = pygame.image.load(File_name).convert_alpha()

    #Declares the positions for the menu box image.
    ImagePos = Image.get_rect()
    ImagePos.centerx = Screen.Window.get_rect().centerx
    ImagePos.centery = Screen.Window.get_rect().centery

    #Declares the text and font used for the title on the instructions screen
    Instructions_Title = "Instructions"
    Instructions_Title_Font = pygame.font.SysFont('Calibri', 60)
    
    #Declares the text and font used for the instructions on the instructions screen
    Instructions_Text =('The objective of this game is to destroy as many',
                        'blocks as possible by bouncing the ball into them',
                        'with the paddle. If the ball destroys a block you',
                        'gain points equal to your Level * 100. If you clear',
                        'the blocks in the level you proceed to the next',
                        'level. Every level contains 40 blocks to destroy.',
                        'When you complete a level your paddle and',
                        'ball\'s speed increase.',
                        ' ',
                        'Controls:',
                        'Left arrow key = Move Left',
                        'Right arrow key = Move Right',
                        'esc = pause game')

    Backspace_Text = ('Press Backspace to go back to the main menu')
    
    Instructions_Font = pygame.font.SysFont('Calibri', 20)
 
    while True:
        #Animates background
        Background.Animate()
        
        #Draws the text and images to the window
        Screen.Window.blit(Image,ImagePos)
        Write_line(Instructions_Title, Instructions_Title_Font, WHITE, 400, 120, "CENTER")
        Write_Text(Instructions_Text, Instructions_Font, WHITE, 200, 160, 25, "Left")
        Write_line(Backspace_Text, Instructions_Font, WHITE, 400, 500, "Center")

        #Updates the infomation displayed on the window.
        Refresh_Screen()

        #Controls
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                #If the backspace key is pressed the previous screen is opened
                if event.key == K_BACKSPACE:
                    return
                
                # If the space key is pressed the background stops moving
                if event.key == K_SPACE:
                    Background.Toggle()
                
            #If the X on the top of the window is pressed the game shuts down.
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

def Leaderboards_Screen():
    Leaderboards.Update()
    #Subroutine which draws all of the leaderboards to the screen.
    #Defines and positions the background box image.
    File_name = "Assets/Computing game images/Leaderboards.png"
    Image = pygame.image.load(File_name).convert_alpha()
    ImagePos = Image.get_rect()
    ImagePos.centerx = Screen.Window.get_rect().centerx
    ImagePos.centery = Screen.Window.get_rect().centery
    
    #Defines the Leaderboards title text and font ready for writing.
    Leaderboards_Title = "Leaderboards"
    Leaderboards_Title_Font = pygame.font.SysFont('Calibri', 60)

    #Defines the Leaderboards Score text and font ready for writing.
    Leaderboards_Scores = (str(Leaderboards.Scorelist[2]),
                         str(Leaderboards.Scorelist[1]),
                         str(Leaderboards.Scorelist[0]))
    
    Leaderboards_Names = (Leaderboards.Namelist[2],
                          Leaderboards.Namelist[1],
                          Leaderboards.Namelist[0])
    
    Leaderboards_Font = pygame.font.SysFont('Calibri', 60)

    Backspace_Text = ('Press Backspace to go back to the main menu')
    Backspace_Font = pygame.font.SysFont('Calibri', 20)
    
    while True:
        #Animates the background
        Background.Animate()
        
        #Draws the Images and text to the screen.
        Screen.Window.blit(Image, ImagePos)
        Write_line(Leaderboards_Title, Leaderboards_Title_Font, WHITE, 400, 150 , "Center")
        Write_Text(Leaderboards_Scores, Leaderboards_Font, WHITE, 300, 240, 75, "LEFT")
        Write_Text(Leaderboards_Names, Leaderboards_Font, WHITE, 450, 240, 75, "LEFT")
        Write_line(Backspace_Text, Backspace_Font, WHITE, 400, 500, "Center")
        
        #Refreshes the screen
        Refresh_Screen()
        
        #Controls
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                #If the backspace key is pressed the previous screen is opened
                if event.key == K_BACKSPACE:
                    return
                
                # If the space key is pressed the background stops moving
                if event.key == K_SPACE:
                    Background.Toggle()
                
            #If the X on the top of the window is pressed the game shuts down.
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
def C_D_Window_Edge():
    #IF BALL HITS SIDE OF WINDOW        
    # If The ball hits the right side of the window in the direction upright then the ball moves upleft    
    if Ball.right >= Screen.Width and Ball.Direction == UPRIGHT:
        Ball.right = Screen.Width - 1
        Ball.Direction = UPLEFT
      
    # If The ball hits the right side of the window in the direction downright then the ball moves downleft      
    elif Ball.right >= Screen.Width and Ball.Direction == DOWNRIGHT:
        Ball.right = Screen.Width - 1
        Ball.Direction = DOWNLEFT

    # If The ball hits the Left side of the window in the direction upleft then the ball moves upright     
    elif Ball.left <= 0 and Ball.Direction == UPLEFT:
        Ball.left = 1
        Ball.Direction = UPRIGHT
        
    # If The ball hits the Left side of the window in the direction downleft then the ball moves downright        
    elif Ball.left <= 0 and Ball.Direction == DOWNLEFT:
        Ball.left = 1
        Ball.Direction = DOWNRIGHT
   
    # If The ball hits the top of the window in the direction upleft then the ball moves downleft     
    elif Ball.top <= 0 and Ball.Direction == UPLEFT:
        Ball.top = 1
        Ball.Direction = DOWNLEFT 
        
    # If The ball hits the top of the window in the direction upright then the ball moves downright     
    elif Ball.top <= 0 and Ball.Direction == UPRIGHT:
        Ball.top = 1
        Ball.Direction = DOWNRIGHT

    # If the ball hits the bottom of the screen...    
    elif Ball.bottom >=Screen.Height :
        #Then Player is respawned.
        global Game_Started
        global Respawned
        global Lives
        Respawned = 0
        Lives -= 1
        Game_Started = False
        if Lives <= 0:
            End_Game_Screen()
            Reset_Game()
        
    # Makes sure the player doesn't leave the screen. 
    # X Coordinates
    #Right Side
    if Player.X > (Screen.Width - Player.Width):
        Player.MoveX = 0
        Player.X = Screen.Width - Player.Width
    #Left Side    
    elif Player.X < 0:
        Player.MoveX = 0
        Player.X = 0

def C_D_Two_Objects(Obj1, Obj2, Block_ListPos):
    #Collision detection between 2 objects Obj1 = Object 1, Obj2 = Object 2
    global Score
    #Checks which side of the 2nd object is hit
    Sidehit = Checkside(Obj1, Obj2)

    #If the side hit is the top then...
    if Sidehit == 'Top':
        #If the ball is moving downleft then...
        if Obj1.Direction == DOWNLEFT:
            Obj1.bottom = Obj2.top
            Obj1.Direction = UPLEFT

        #If the ball is moving downright then...    
        elif Obj1.Direction == DOWNRIGHT:
            Obj1.bottom = Obj2.top
            Obj1.Direction = UPRIGHT
            
        # If The ball hits the paddle while travelling down (This happens when first dropped)...
        elif Obj1.Direction == DOWN:
            # A direction randomiser chooses which direction the ball moves...
            Direction_Randomiser = random.randint(1,2)
            #If the randomiser chooses 1 then the direction becomes Up and right
            if Direction_Randomiser == 1:
                Obj1.Direction = UPRIGHT

            #If the randomiser chooses 2 then the direction becomes Up and right
            if Direction_Randomiser == 2:
                Obj1.Direction = UPLEFT
                
    #If the side hit is the bottom then...            
    elif Sidehit == 'Bottom':
        #If the ball is moving upleft then...
        if Obj1.Direction == UPLEFT:
            Obj1.top = Obj2.bottom
            Obj1.Direction = DOWNLEFT

        #If the ball is moving upright then...    
        elif Obj1.Direction == UPRIGHT:
            Obj1.top = Obj2.bottom
            Obj1.Direction = DOWNRIGHT

    #If the side hit is the left then...        
    elif Sidehit == 'Left':
        #If the ball is moving upright then...
        if Obj1.Direction == UPRIGHT:
            Obj1.right = Obj2.left
            Obj1.Direction = UPLEFT

        #If the ball is moving downright then...
        elif Obj1.Direction == DOWNRIGHT:
            Obj1.right = Obj2.left
            Obj1.Direction = DOWNLEFT

    #If the side hit is the right then...                      
    elif Sidehit == 'Right':
        #If the ball is moving upleft then... 
        if Obj1.Direction == UPLEFT:
            Obj1.left = Obj2.right
            Obj1.Direction = UPRIGHT
            
        #If the ball is moving downleft then...    
        elif Obj1.Direction == DOWNLEFT:
            Obj1.left = Obj2.right
            Obj1.Direction = DOWNRIGHT
        
    #If the side
    if Sidehit != "" and Obj2 == Block:
        BlockSet.Destroyed[Block_ListPos] -= 1
        Score += (100*Level)
        Power_ups.drop() 
    
def Checkside(Obj1, Obj2):
    Sidehit = ""
    if Obj1.top <= Obj2.bottom and Obj1.X > Obj2.left and Obj1.X < Obj2.right and Obj1.top > Obj2.top:
        Sidehit = 'Bottom'
    if Obj1.bottom >= Obj2.top and Obj1.X > Obj2.left and Obj1.X < Obj2.right and Obj1.bottom < Obj2.bottom:
        Sidehit = 'Top'
    if Obj1.Y <= Obj2.bottom and Obj1.Y >= Obj2.top and Obj1.left <= Obj2.right and Obj1.left > Obj2.left:
        Sidehit = 'Right'
    if Obj1.Y <= Obj2.bottom and Obj1.Y >= Obj2.top and Obj1.right >= Obj2.left and Obj1.right < Obj2.right:
        Sidehit = 'Left'
    return Sidehit
    
def Collision_Detection ():
    global Block
    Ball.Area()
    Player.Area()
    for i in range(len(Blocks_Rows)):
           Row = Blocks_Rows[i]
           for b in range(len(Row)):
               Block = Row[b]
               Block_ListPos = (b) + (i * len(Blocks_Rows[i]))
               if BlockSet.Destroyed[Block_ListPos] > 0:
                   C_D_Two_Objects(Ball, Block, Block_ListPos)
    C_D_Two_Objects(Ball, Player, Block_ListPos)
    C_D_Window_Edge()
        
def Draw_HUD():
    #Writes and draws HUD to the bottom of the screen.
    #Declares the text and font for the text drawn on the bottom of the screen
    HUD_Font = pygame.font.SysFont('Calibri', 20)
    HUD_Text =("Level: " + str(Level) + "       Score: " + str(Score) + "       Lives: " + str(Lives) + "      HighScore: "  + str(Leaderboards.Scorelist[len(Leaderboards.Scorelist) - 1]))

    #Draws the text to the screen
    Write_line(HUD_Text, HUD_Font, WHITE, 400, Screen.Height - 10, "Center" )
    
def Respawn():
    #Globalises the respawned variable
    global Respawned
    
    # If player hasn't been respawned...
    if Respawned == False:        
        #Resets player and ball variables to the original settings
        Player.Respawn()
        Ball.Respawn()
        Power_ups.Dropped = False
        Power_ups.Timer.started = False
        #Player respawned beocmes true
        Respawned = True
            
    #Declares the text and font for respawn message
    Respawn_Msg = ("Press ENTER to release ball")
    Respawn_Msg_Font = pygame.font.SysFont('Calibri', 25)

    #Draws the text to the screen.
    Write_line(Respawn_Msg, Respawn_Msg_Font, WHITE, Screen.Width/2, Screen.Height/2, "Center")
    
def Level_Layout():
    global Score
    global Level
    Destroyed_Counter = 0
    # for each row in row list
    for i in range(len(Blocks_Rows)):
        Row = Blocks_Rows[i]
        
        #for every block in the row
        for b in range(len(Row)):
            Block = Row[b]
            
            #Assigns the number to which block is being checked to an identifier
            Block_ListPos = (b) + (i * len(Row))
            
            #If block is not destroyed
            if BlockSet.Destroyed[Block_ListPos] > 0:
                
                #Draw the block depending on how many hits are left
                if BlockSet.Destroyed[Block_ListPos] ==  1:
                    pygame.draw.rect(Screen.Window,GREY, Block, 0)
                elif BlockSet.Destroyed[Block_ListPos] >= 2:
                    pygame.draw.rect(Screen.Window,WHITE, Block, 0)
                
                    
            # If the block is destroyed add 1 to Destroyed counter and
            # if the block has not been checked then score increases
            # and The block is marked as checked
            elif BlockSet.Destroyed[Block_ListPos] == 0:
                Destroyed_Counter += 1
                BlockSet.Destroyed[Block_ListPos] -= 1
                
            if BlockSet.Destroyed[Block_ListPos] == -1:
                Destroyed_Counter += 1
                
                if Destroyed_Counter >= (len(Blocks_Rows) * len(Row)) + 1:
                # Checks if all blocks on field are destroyed.
                # if yes then the score is added, the level is increased
                # and the field is reset.
                    global Respawned
                    global Game_Started
                    Level += 1
                    Write_Level(Level)
                    Respawned = False
                    Game_Started = False
                    BlockSet.Respawn()
                    BlockSet.Setup()

def Display_Score():
    #Displays the Score after playing by drawing the score to the screen.
    #Declares the font and text used for the Final Score display
    Score_Font = pygame.font.SysFont('Calibri', 40)
    Score_Text =("Your Score: " + str(Score))

    #Declares the text used for the Highest score scored locally
    HighScore_Text = ("HighScore: " + str(Leaderboards.Scorelist[len(Leaderboards.Scorelist)-1]))                     
        
    #Declares the text used for the level reached in the previous game
    Level_Text =("Level Reached: " + str(Level))

    #Draws the Text to the screen.
    Write_line(Score_Text, Score_Font, WHITE, 40, 40, "Left")
    Write_line(HighScore_Text, Score_Font, WHITE, 40, 560, "Left")
    Write_line(Level_Text, Score_Font, WHITE, 40, 80, "Left")
    
def Name_Input(Input_Length):
    #Subroutine for the name input to identify the scorer of the highscore in the leaderboards.
    #Name is cleared ready for a new entry
    Name = ""
    
    #Name's entry font is declared
    Name_Font = pygame.font.SysFont('Calibri', 40)
    
    while len(Name) < Input_Length:
            for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        #If a letter key is pressed then the letter is added to the name input
                        if event.key == K_a:
                            Name += "A"
                        if event.key == K_b:
                            Name += "B"
                        if event.key == K_c:
                            Name += "C"    
                        if event.key == K_d:
                            Name += "D"
                        if event.key == K_e:
                            Name += "E"
                        if event.key == K_f:
                            Name += "F"
                        if event.key == K_g:
                            Name += "G"
                        if event.key == K_h:
                            Name += "H"
                        if event.key == K_i:
                            Name += "I"
                        if event.key == K_j:
                            Name += "J"
                        if event.key == K_k:
                            Name += "K"
                        if event.key == K_l:
                            Name += "L"
                        if event.key == K_m:
                            Name += "M"
                        if event.key == K_n:
                            Name += "N"
                        if event.key == K_o:
                            Name += "O"
                        if event.key == K_p:
                            Name += "P"
                        if event.key == K_q:
                            Name += "Q"
                        if event.key == K_r:
                            Name += "R"
                        if event.key == K_s:
                            Name += "S"
                        if event.key == K_t:
                            Name += "T"
                        if event.key == K_u:
                            Name += "U"
                        if event.key == K_v:
                            Name += "V"
                        if event.key == K_w:
                            Name += "W"
                        if event.key == K_x:
                            Name += "X"
                        if event.key == K_y:
                            Name += "Y"
                        if event.key == K_z:
                            Name += "Z"
                            
                        #If the backspace key is pressed then a letter is removec from the name input
                        if event.key == K_BACKSPACE:
                            Name = Name[:-1]

                        # If the space key is pressed the background stops moving
                        if event.key == K_SPACE:
                            Background.Toggle()
                            
                    #If the x in the window is clicked the game is closed.        
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                            
            #Animates Background            
            Background.Animate()

            #Draws the end screen
            Display_Score()

            #Declares the text ready for drawing to the screen
            Name_Text =("Please Input a 3 character name:",
                         Name)

            #Draws the text to the screen
            Write_Text(Name_Text, Name_Font, WHITE, 400, 300, 40, "Center")

            #Updates the image displayed on the window
            Refresh_Screen()
            
    #Sets the font for the prompts which appear when the text is full
    Instructions_Font = pygame.font.SysFont('Calibri', 30)

    #When the player reaches the character limit 
    while len(Name) >= Input_Length:

        #Makes the length of the name the first 3 characters
        if len(Name) > Input_Length:
            Name = Name[:-(len(Name) - Input_Length)]
            
        #Animates the background
        Background.Animate()

        #Draws the end screen
        Display_Score()

        #Declares the text which displays the name to the player.
        Name_Text =("Please Input a 3 character name:",
                    Name)

        #Declares the text which displays the instructions prompts to the player
        Instructions_Text = ("Press 'Enter' to continue",
                            "Press 'Backspace' to clear")

        #Draws the text to the screen
        Write_Text(Name_Text, Name_Font, WHITE, 400, 300, 40, "Center")
        Write_Text(Instructions_Text, Instructions_Font, WHITE, 400, 380, 25, "Center")

        #Updates the screens displayed data.
        Refresh_Screen()

        #Controls
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                #If backspace is pressed recursion is used to reenter the name again.
                if event.key == K_BACKSPACE:
                            Name_Input(3)
                            return
                        
                #If the enter key is pressed then the name  is stored and the game is restarted
                if event.key == K_RETURN:
                    for i in range(len(Leaderboards.Scorelist)):
                        if Score == Leaderboards.Scorelist[i]:
                            Leaderboards.Namelist[i] = Name
                    return

            #If the x in the top of the window then the game shuts down.
            if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                        
def End_Game_Screen():
    #The screen which comes up when the player has lost all of their lives
    #Animates the background
    Background.Animate()

    #Draws the data to show to the screen
    Display_Score()

    #Updates the leaderboards according to the score which has just been gathered.
    Leaderboards.Update()

    #Asks for the input of a name to identify who scored the score.
    Name_Input(3)

    #Saves the Scores 
    Leaderboards.Save()
    
def Reset_Game():
    #Resets the game
    #Declares global variables which are reset
    global Lives
    global Level
    global Respawned
    global Score
    
    #Declaring Respawned variable to false ready for when the player starts the game.
    Respawned = False
    
    #Sets the level to 1 ready for when the player next plays
    Level = 1

    #Sets the score to 0 ready for when the player next plays
    Score = 0
    
    #Sets the Lives to 3 ready for when the player next plays
    Lives = 3

    #Runs the Start game routine
    #Runs the start screen
    Start_Screen()
    
    #Writes the level to the player
    Write_Level(Level)

    #Positions the blocks on the field ready for playing
    BlockSet.Respawn()
    BlockSet.Setup()

    #Respawns the player to the screen
    Respawn()
    
def Pause():
    #Pauses the game
    global Paused
    
    #If the game isnt paused pause it and stop movement
    #else the game isnt paused and the game continues.
    if Paused == False:
        Paused = True
        
        #Stops ball movement
        Ball.MoveSpeed = 0
        
        #Stops Player movement
        Player.MoveSpeed = 0
        Player.MoveX = 0
        
    else:
        Paused = False
        
        #Movement goes back to normal
        Ball.MoveSpeed = Level + 2
        Player.MoveSpeed = Level + 3
        
        
def Game_Controls():
    #Globalises the variable which indicates the game has started.
    global Game_Started
    
    # When the X button on the window is clicked closes program 
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        # Controls 
        if event.type == KEYDOWN:
                #if the left key is pressed then the players paddle is moved to the left
                if event.key == K_LEFT:
                    Player.MoveX = -Player.MoveSpeed

                #if the right key is pressed then the players paddle is moved to the right    
                elif event.key == K_RIGHT:
                    Player.MoveX = Player.MoveSpeed

                #if the enter key is pressed the game indicates the player is readt then the ball begins to move. 
                if event.key == K_RETURN:
                    if Game_Started == False:
                        Game_Started = True
                        Ball.MoveSpeed = Level + 2

                #if the escape key is pressed and the game has started then the pause subroutine is run which either
                #Pauses or unpauses the game.
                if event.key == K_ESCAPE:
                    if Game_Started == True:
                        Pause()
                        
                # If the space key is pressed the background stops moving
                if event.key == K_SPACE:
                    Background.Toggle()
                        
        if event.type == KEYUP:
            #If the directional keys are released then the player stops moving.
            if event.key == K_LEFT:
                Player.MoveX = 0
                
            elif event.key == K_RIGHT:
                Player.MoveX = 0
#======================================================================================  ==========================================                 
class Power_ups:
    #Declares the settings used for the power up sprite
    Colour = RED
    X = 400
    Y = 0
    Radius = 20

    #Declares the variable which states whether the power up is being dropped.
    Dropped = False
    
    def drop(self):
        #If the Power up has not been dropped then the variables are set to get ready
        #to drop the power up and then it is dropped.
        if self.Dropped == False:
            self.X = 400
            self.Y = 0
            Randomiser = random.randint(0, 50)
            
            if Randomiser >= 0 and Randomiser <= 7:
                self.Dropped = True

        #If the power up has been dropped then the sprite is drawn and continues to move the powerup sprite
        #Down until it hits the player or leaves the screen
        elif self.Dropped == True:
            self.Sprite = pygame.draw.circle(Screen.Window, self.Colour, (self.X, self.Y) , self.Radius)
            self.Y += 2
            if Power_ups.Timer.started == True:
                self.Timer.Check(Power_ups.Timer.Time)
            if Player.Sprite.colliderect(Power_ups.Sprite) == True:
                self.Timer.Start()
                self.Randomise()
                self.Dropped = False
            if Power_ups.Sprite.top > Screen.Height:
                self.Dropped = False
                
    def Dropping(self):
        #Drops the ball in every loop if the ball has been dropped and
        #checks the timer if the timer has started.
        if Power_ups.Timer.started == True:
            self.Timer.Check(Power_ups.Timer.Time)
        if Power_ups.Dropped == True:
            self.drop()
            
    def Randomise(self):
        #Randomises a number between 0 and the amount of power ups available.
        Randomiser = random.randint(0, 3)
        
        #Sets the position of the power up sprite.
        self.X = 400
        self.Y = 0

        #If the randomiser comes out with the first number then
        #Power up 1(Double ball movespeed) is activated
        if Randomiser == 0:
            Ball.MoveSpeed += 2
            Power_ups.Timer.Time = 10
            self.Timer.Start()

        #If the randomiser comes out with the second number then
        #Power up 2(Double Player Width) is activated    
        if Randomiser == 1:
            Player.Width *= 2
            Power_ups.Timer.Time = 10
            self.Timer.Start()

        #If the randomiser comes out with the third number then
        #Power up 3(Half Player Width) is activated    
        if Randomiser == 2:
            Player.Width /= 2
            Power_ups.Timer.Time = 10

        #If the randomiser comes out with the fourth number then
        #Power up 4(Half ball movespeed) is activated    
        if Randomiser == 3:
            Ball.MoveSpeed -= 2
            Power_ups.Timer.Time = 10
            self.Timer.Start()
                
    def Reset(self):
        #Resets all power up changeable settings to put the game back to normal
        if Ball.MoveSpeed != Level + 2:
            Ball.MoveSpeed = Level + 2
        if Player.Width != 60:
            Player.Width = 60
            
    class Timer:
        #Timer which times the period in which the power up has been running
        start = 0
        started = False
        Time = 0
        
        def Start():
            #Starts the timer when called by making the start time equal to
            #the present time and declaring that the timer has started
            Power_ups.Timer.start = default_timer()
            Power_ups.Timer.started = True

        def Check(Time):
            #Checks if the duration of time has passed the time in which the timer was timing
            #if it has then the timer stops
            duration = default_timer() - Power_ups.Timer.start
            if duration > Power_ups.Timer.Time:
                Power_ups.Timer.Stop()
                
        def Stop():
            #Resets the timer when alled and resets the game to non power up state.
            Power_ups.Timer.started = False
            Power_ups.Reset()
            
#======================================================================================  ==========================================    
#Main Code--------------------------------------------------------------------------------------------
#Makes the Classes easier to read by removing the brackets from the declarations
Screen = Screen()
Player = Player()
Ball = Ball()
BlockSet = BlockSet()
Background = Background()
Leaderboards = Leaderboards()
Power_ups = Power_ups()


#Sets up the screen
Screen.Setup()

#Loads the leaderboards from the file
Leaderboards.Load()

#Respawns the blocks and positions them ready for drawing when the game starts.
BlockSet.Respawn()
BlockSet.Setup()

#Resets the game and performs the start routine
Reset_Game()

#Makes the game Unpaused
Paused = False

# Game Loop-------------------------------------------------------------------------------------------- 
while True:
    #Animates the background
    Background.Animate()

    #If the game has not started then the player is respawned    
    if Game_Started == False:
        Respawn()
        Ball.X = Player.Sprite.centerx
        
    #Runs the controls    
    Game_Controls()
    
    if Game_Started == True and Paused == True:
        #If the game has started and the player has paused then the pause text and font is declared and drawn to the screen.
        Pause_Font = pygame.font.SysFont('Calibri', 40)
        Pause_Text =("Game Paused press 'esc' to continue.")
        Write_line(Pause_Text, Pause_Font, WHITE, Screen.Width/2, Screen.Height/2, "Center")
                                 
    # Draws the player and ball to the screen.   
    Player.Move()
    Ball.Move()
    
    #Draws the bricks to the screen
    Level_Layout()
    
    #Checks for collision between objects
    Collision_Detection()

    #Changes the power ups coordinates every iteration when dropping.
    Power_ups.Dropping()
    
    #Draws HUD which shows the playes stats
    Draw_HUD()

    #Updates what is shown on the screen
    Refresh_Screen()
