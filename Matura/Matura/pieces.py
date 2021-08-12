import pygame

class Piece:
    def __init__(self, color, name, notation):
        self.color = color
        self.name = name
        self.notation = notation
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
        self.castlingAllowed = True
        self.moves = moves
        super().__init__(color, "king", "k")

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
        
        
        self.moves = moves 
        
        super().__init__(color, "queen", "q")

    

class Rook(Piece):
    def __init__(self, color):
        moves = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x == 0 or y == 0) and (x != 0 or y != 0):
                    moves.append((x, y))
        self.moves = moves
        self.castlingAllowed = True
        super().__init__(color, "rook", "r")

   

class Bishop(Piece):
    
    def __init__(self, color):
        moves = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if abs(x) == abs(y) and (x != 0):
                    moves.append((x, y))
        
        self.moves = moves
        super().__init__(color, "bishop", "b")



class Knight(Piece):
   
    def __init__(self, color):
        moves = []
        for x in range(-2, 3):
            for y in range(-2, 3):
                if (abs(x) + abs(y) == 3):
                    moves.append((x, y))
        
        self.moves = moves
        super().__init__(color, "knight", "n")



class Pawn(Piece):
    
    def __init__(self, color):
        moves = []
        if color == "white":
            moves.append((0, -1))
        else:
            moves.append((0, 1))
        self.moves = moves
        super().__init__(color, "pawn", "p")

    def enPassant():
        return True
    def firstMove():
        
        return True