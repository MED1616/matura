import pygame
"""
def createMoves(a, b, n):
    moves = []
    for x in range(a, b):
        for y in range(a, b):
            if x != 0 or y != 0:
                moves.append((x, y))
    
    moves2 = moves

    for m in moves2:
        for i in range(2, n):
            print((m[0] * i, m[1] * i))
    return moves
"""

class Piece:
    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.sprite = pygame.image.load("Sprites/" + color + "_" + name + ".png")
    def findMoves():
        
        return True

class King(Piece):
    
    def __init__(self, color):
        moves = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x != 0 or y != 0:
                    moves.append((x, y))
        print("king: ", moves)
        self.moves = moves
        super().__init__(color, "king")

    def inCheck():
        return False
    def castle():
        return True

class Queen(Piece):
    
    def __init__(self, color):
        moves = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x != 0 or y != 0:
                    moves.append((x, y))
        print("queen: ", moves)
        """
        for x in range(-8, 8):
            for y in range(-8, 8):
                if abs(x) == abs(y) and (x != 0):
                    moves.append((x, y))
        moves2 = []
        for x in range(-8, 8):
            for y in range(-8, 8):
                if (x == 0 or y == 0) and (x != 0 or y != 0):
                    moves2.append((x, y))
        print("queen: ", moves + moves2)
        """
        self.moves = moves 
        """+ moves2"""
        super().__init__(color, "queen")

    

class Rook(Piece):
    def __init__(self, color):
        moves = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x == 0 or y == 0) and (x != 0 or y != 0):
                    moves.append((x, y))
        print("rook: ", moves)
        self.moves = moves
        super().__init__(color, "rook")

   

class Bishop(Piece):
    
    def __init__(self, color):
        moves = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if abs(x) == abs(y) and (x != 0):
                    moves.append((x, y))
        print("bishop: ", moves)
        self.moves = moves
        super().__init__(color, "bishop")



class Knight(Piece):
   
    def __init__(self, color):
        moves = []
        for x in range(-2, 3):
            for y in range(-2, 3):
                if (abs(x) + abs(y) == 3):
                    moves.append((x, y))
        print("knight: ", moves)
        self.moves = moves
        super().__init__(color, "knight")



class Pawn(Piece):
    
    def __init__(self, color):
        moves = []
        if color == "white":
            moves.append((0, -1))
        else:
            moves.append((0, 1))
        self.moves = moves
        super().__init__(color, "pawn")

    def enPassant():
        return True
    def firstMove():
        
        return True