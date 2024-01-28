#Imports:
import numpy as np
import random
import pygame
import sys
import math
from tkinter import *

#Color RGB Values:
Grey = (140,140,140) #Board Color
White = (255,255,255) #Background Color
Blue = (0,191,255) #Player One Color
Red = (255,51,51) #Player Two Color

#Constants:
No_of_rows,No_of_columns = 6,7
Size,Radius = 80,35
Height,Width = (No_of_rows+1)*Size,No_of_columns*Size
Screensize = (Width,Height)
Screen = pygame.display.set_mode(Screensize)
Player,Robot =0, 1 #Computer Auto Player
Robot_Piece,Player_Piece =2,1
Empty = 0
Length_of_window = 4

#Functions:
def Create_Board():
    Board = np.zeros((No_of_rows,No_of_columns))
    return Board
def Drop_Piece(Board,Row,Column,Piece):
    Board[Row][Column] = Piece
def Valid_Location(Board,Column):    
    return Board[No_of_rows-1][Column] == 0
def Find_next_valid_row(Board,Column):
    for i in range(No_of_rows):
        if Board[i][Column]== 0:
            return i
def Print_Board(Board): 
    print(np.flip(Board,0))
def Find_Winner(Board,Piece):
    #Vertical Winning:
    for Column in range(No_of_columns):
        for Row in range(No_of_rows-3):
            if Board[Row][Column] == Piece and Board[Row+1][Column] == Piece and Board[Row+2][Column] == Piece and Board[Row+3][Column] == Piece:
                return True
    #Horizontal Winning:  
    for Column in range(No_of_columns-3):
        for Row in range(No_of_rows):
            if Board[Row][Column] == Piece and Board[Row][Column+1] == Piece and Board[Row][Column+2] == Piece and Board[Row][Column+3] == Piece:
                return True
    #Right-slopped Winning:  
    for Column in range(No_of_columns-3):
        for Row in range(No_of_rows-3):
            if Board[Row][Column] == Piece and Board[Row+1][Column+1] == Piece and Board[Row+2][Column+2] == Piece and Board[Row+3][Column+3] == Piece:
                return True            
    #Left-slopped Winning:  
    for Column in range(No_of_columns-3):
        for Row in range(3,No_of_rows):
            if Board[Row][Column] == Piece and Board[Row-1][Column+1] == Piece and Board[Row-2][Column+2] == Piece and Board[Row-3][Column+3] == Piece:
                return True            
def Check_Window(Window,Piece):
    Score=0
    Opponent_Piece= Player_Piece
    if Piece == Player_Piece:
        Opponent_Piece = Robot_Piece
    if Window.count(Piece) == 4:
        Score=Score+100
    elif Window.count(Piece)==3 and Window.count(Empty) == 1:
        Score= Score+5
    elif Window.count(Piece)==2 and Window.count(Empty) == 2:
        Score= Score+2        
    if Window.count(Opponent_Piece)==3 and Window.count(Empty) == 1:
        Score= Score-4
    return Score
def Score_Position(Board,Piece):
    Score=0
    # Score center column
    Center_array = [int(i) for i in list(Board[:, No_of_columns//2])]
    Center_count = Center_array.count(Piece)
    Score = Score+Center_count * 3
    # Score Horizontal
    for r in range(No_of_rows):
        Row_array = [int(i) for i in list(Board[r,:])]
        for col in range(No_of_columns-3):
            Window = Row_array[col:col+Length_of_window]
            Score=Score+ Check_Window(Window,Piece)
    # Score Vertical
    for col in range(No_of_columns):
        col_array = [int(i) for i in list(Board[:,col])]
        for row in range(No_of_rows-3):
            Window = col_array[row:row+Length_of_window]
            Score = Score+Check_Window(Window,Piece)
    # Score posiive sloped diagonal
    for row in range(No_of_rows-3):
        for col in range(No_of_columns-3):
            Window = [Board[row+i][col+i] for i in range(Length_of_window)]
            Score =Score+ Check_Window(Window,Piece)
    # Score negative sloped diagonal
    for row in range(No_of_rows-3):
        for col in range(No_of_columns-3):
            Window = [Board[row+3-i][col+i] for i in range(Length_of_window)]
            Score =Score+ Check_Window(Window,Piece)    
    return Score


def Final_Point(Board):
    return Find_Winner(Board,Player_Piece) or Find_Winner(Board,Robot_Piece) or len(Collect_valid_locations(Board))== 0
def Minimax(Board,Depth,Alpha,Beta,MaximizingPlayer):
    Valid_Locations = Collect_valid_locations(Board)
    Terminal = Final_Point(Board)
    if Depth == 0 or Terminal:
        if Terminal:
            if Find_Winner(Board, Robot_Piece):
                return (None, 100000000000000)
            elif Find_Winner(Board, Player_Piece):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, Score_Position(Board, Robot_Piece))        
    if MaximizingPlayer:
        Value = -math.inf
        Column = random.choice(Valid_Locations)
        for col in Valid_Locations:
            row = Find_next_valid_row(Board, col)
            board_copy = Board.copy()
            Drop_Piece(board_copy, row, col, Robot_Piece)
            New_Score = Minimax(board_copy, Depth-1, Alpha, Beta, False)[1]
            if New_Score > Value:
                Value = New_Score
                Column = col
            Alpha = max(Alpha,Value)
            if Alpha >= Beta:
                break
        return Column,Value            
    else: # Minimizing player
        Value = math.inf
        Column = random.choice(Valid_Locations)
        for col in Valid_Locations:
            row =Find_next_valid_row(Board, col)
            board_copy = Board.copy()
            Drop_Piece(board_copy, row, col,Player_Piece)
            New_Score = Minimax(board_copy,Depth-1,Alpha,Beta, True)[1]
            if New_Score < Value:
                Value = New_Score
                Column = col
            Beta = min(Beta,Value)
            if Alpha >= Beta:
                break
        return Column, Value

def Collect_valid_locations(Board):
    Valid_Locations=[]
    for col in range(No_of_columns):
        if Valid_Location(Board,col):
            Valid_Locations.append(col)
    return Valid_Locations   
def Pick_Best_Spot(Board,Piece):
    Valid_Locations = Collect_valid_locations(Board)
    Best_Score = -10000
    Best_col = random.choice(Valid_Locations)
    for col in Valid_Locations:
        row = Find_next_valid_row(Board, col)
        Temporary_board = board.copy()
        Drop_Piece(Temporary_board, row, col,Piece)
        Score = Score_Position(Temporary_board,Piece)
        if Score > Best_Score:
            Best_Score = Score
            Best_col = col

    return Best_col
def Draw_Board(Board):
    for column in range(No_of_columns):
        for row in range(No_of_rows):
            pygame.draw.rect(Screen,Grey,(column*Size,row*Size+Size,Size,Size))
            pygame.draw.circle(Screen,White,(int(column*Size+Size/2),int(row*Size+Size+Size/2)),Radius)
    for column in range(No_of_columns):
        for row in range(No_of_rows):		
            if Board[row][column] == 1:
                pygame.draw.circle(Screen,Blue, (int(column*Size+Size/2),Height-int(row*Size+Size/2)),Radius)
            elif Board[row][column] == 2: 
                pygame.draw.circle(Screen,Red,(int(column*Size+Size/2),Height-int(row*Size+Size/2)),Radius)
    pygame.display.update()
def Mode1():   
    #1 Player Game:
    #Game Initilaization
    Board=Create_Board()
    Print_Board(Board)
    Game_Over=False
    pygame.init()
    Draw_Board(Board)
    pygame.display.update()
    Font= pygame.font.SysFont("comicsansms",65)
    Turn=random.randint(Player,Robot)
    #Running the Game...
    while not Game_Over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(Screen,White,(0,0,Width,Size))
                posx = event.pos[0]
                if Turn == Player: 
                    pygame.draw.circle(Screen,Blue,(posx,int(Size/2)),Radius)
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(Screen,White,(0,0,Width,Size))
                #1st Player
                if Turn == Player:
                    posx = event.pos[0]
                    Column = int(math.floor(posx/Size))
                    if Valid_Location(Board,Column):
                        Row = Find_next_valid_row(Board,Column)
                        Drop_Piece(Board,Row,Column,Player_Piece)
                        if Find_Winner(Board,Player_Piece):
                            Statement= Font.render("1st Player Wins!",1,Blue)
                            Screen.blit(Statement,(50,10))
                            Game_Over=True    
                        Turn=Turn+1
                        Turn=Turn%2
                        Print_Board(Board)
                        Draw_Board(Board)
                        
    #Robot Player(Auto Player)
        if Turn== Robot and not Game_Over:
            Column,Minimax_Score= Minimax(Board,5,-math.inf,math.inf,True)  
            if Valid_Location(Board,Column):
                Row = Find_next_valid_row(Board,Column)
                Drop_Piece(Board,Row,Column,Robot_Piece)
                if Find_Winner(Board,Robot_Piece):
                    Statement= Font.render("2nd Player Wins!",1,Red)
                    Screen.blit(Statement,(50,10))
                    Game_Over=True
                Print_Board(Board)
                Draw_Board(Board)
                Turn=Turn+1
                Turn=Turn%2
        if Game_Over:
            pygame.time.wait(500)
    
def Mode2():
    #2 Player Game:
    #Game Initilaization
    Board=Create_Board()
    Print_Board(Board)
    Game_Over=False
    Turn=0
    pygame.init()
    Draw_Board(Board)
    pygame.display.update()
    Font= pygame.font.SysFont("comicsansms",65)
    #Running Game
    while not Game_Over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(Screen,White,(0,0,Width,Size))
                posx = event.pos[0]
                if Turn == 0: 
                    pygame.draw.circle(Screen,Blue,(posx,int(Size/2)),Radius)
                else: 
                    pygame.draw.circle(Screen,Red,(posx,int(Size/2)),Radius)
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(Screen,White,(0,0,Width,Size))
                #1st Player
                if Turn == 0:
                    posx = event.pos[0]
                    Column = int(math.floor(posx/Size))
                    if Valid_Location(Board,Column):
                        Row = Find_next_valid_row(Board,Column)
                        Drop_Piece(Board,Row,Column,1)
                        if Find_Winner(Board,1):
                            Statement= Font.render("1st Player Wins!",1,Blue)
                            Screen.blit(Statement,(50,10))
                            Game_Over=True                
                #2nd Player
                else:
                    posx=event.pos[0]
                    Column=int(math.floor(posx/Size))
                    if Valid_Location(Board,Column):
                        Row = Find_next_valid_row(Board,Column)
                        Drop_Piece(Board,Row,Column,2)
                        if Find_Winner(Board,2):
                            Statement= Font.render("2nd Player Wins!",1,Red)
                            Screen.blit(Statement,(50,10))
                            Game_Over=True
                Print_Board(Board)
                Draw_Board(Board)
                Turn=Turn+1
                Turn=Turn%2
                if Game_Over:
                    pygame.time.wait(500)


#Main Window:
MainWindow = Tk()
MainWindow.title("Connect Four Game")
MainWindow.geometry("350x225")
MainWindow.configure(bg='azure')
#Headers:
Label1 = Label(MainWindow,text="Connect 4",bg='azure',fg="Black",font="none 30 bold",width=200,anchor=CENTER) 
Label1.pack()
Label2 = Label(MainWindow,text="Please choose a mode:",bg="Black",fg='azure',font="none 15 bold",width=210,anchor=W) 
Label2.pack()
#Mode Buttons:
Playeris1Button= Button(MainWindow,text=" 1 Player ",bg= 'firebrick2',fg="White",font="none 26 bold",command=Mode1)
Playeris1Button.pack()                                    
Playeris2Button= Button(MainWindow,text="2 Players",bg='DeepSkyBlue2',fg="White",font="none 26 bold",command=Mode2)                                     
Playeris2Button.pack()
MainWindow.mainloop()