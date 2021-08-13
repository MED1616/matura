from pygame.version import PygameVersion
import pieces
import sys, pygame

pygame.init()


size = [1600, 900]

top = size[1]/10
left = (size[0] - (size[1] - 2*top)) / 2
squareSize = int((size[1] - 2*top) / 8)

screen = pygame.display.set_mode(size, pygame.RESIZABLE)
color = (0, 0, 0)
screen.fill(color)

brown = (153, 102, 51)
lightBrown = (236, 217, 198)

def defineSize():
    size = screen.get_size()
    top = size[1]/10
    left = (size[0] - (size[1] - 2*top)) / 2
    squareSize = int((size[1] - 2*top) / 8)
    return int(top), int(left), int(squareSize)

def drawBoard(board):
    top, left, squareSize = defineSize()
    
    screen.fill(color)

    for a in range(8):
        for b in range(8):
            
            if (a + b) % 2 == 1:
                square = ((left + a * squareSize), (top + b * squareSize), squareSize, squareSize)
                pygame.draw.rect(screen, brown, square)
                
                
            else:
                square = ((left + a * squareSize), (top + b * squareSize), squareSize, squareSize)
                pygame.draw.rect(screen, lightBrown, square)
                
    drawPieces(board)
    
    pygame.display.update()


def newBoard():
    def placePieces(color):
        return [pieces.Rook(color), pieces.Knight(color), pieces.Bishop(color), pieces.Queen(color),
                pieces.King(color), pieces.Bishop(color), pieces.Knight(color), pieces.Rook(color)]
    def placePawns(color):
        return [pieces.Pawn(color) for i in range(8)]

    board = [[None for i in range(8)] for i in range(8)]

    board[0] = placePieces("black")
    board[7] = placePieces("white")
    board[1] = placePawns("black")
    board[6] = placePawns("white")
    
    return board
    
def findClickedSquare(pos):
    top, left, squareSize = defineSize()
    x, y = pos

    x = int((x-left)/squareSize)
    y = int((y-top)/squareSize)
    return x, y

def drawPieces(board):
    top, left, squareSize = defineSize()
    
    for a in range(8):
        for b in range(8):
            
            if board[b][a] != None:
                coord = ((left + squareSize * a), (top + squareSize * b))
                image = pygame.transform.smoothscale(board[b][a].sprite, (squareSize, squareSize))
                screen.blit(image, coord)
                
def findLegalMoves(board, chosenPiece, turn):
    x, y = chosenPiece
    moveset = list(board[y][x].moves)

    mov = list(moveset)

    legalMoves = []
    
    ########################
    if board[y][x].name == "pawn":
        if board[y][x].color == "white" and y == 6:
            b = 2
        elif board[y][x].color == "black" and y == 1:
            b = 2
        else:
            b = 1 

        for m in mov:
            for a in range(1, b + 1):
                if 8 > x + m[0] * a > -1 and 8 > y + m[1] * a > -1 and board[y + m[1] * a][x + m[0] * a] == None:
                    moveset.append((m[0] * a, m[1] * a))
                    
                elif 8 > x + m[0] * a > -1 and 8 > y + m[1] * a > -1 and board[y + m[1] * a][x + m[0] * a].color != turn:
                    if (m[0] * a, m[1] * a) in moveset:
                        moveset.remove((m[0] * a, m[1] * a))
                    break
                    
                else:
                    break

        if board[y][x].color == "black":
            yDir = -1
        else:
            yDir = 1

        if 8 > x + 1 > -1 and 8 > y - 1 * yDir > -1 and board[y - 1 * yDir][x + 1] != None and board[y - 1 * yDir][x + 1].color != turn:
            legalMoves.append((1, - yDir))
                        
        elif 8 > x - 1 > -1 and 8 > y - 1 * yDir > -1 and board[y - 1 * yDir][x - 1] != None and board[y - 1 * yDir][x - 1].color != turn:
            legalMoves.append((-1, -yDir)) 

    ###############################################

    if board[y][x].name == "queen" or board[y][x].name == "rook" or board[y][x].name == "bishop":
        for m in mov:
            for a in range(1, 8):
                
                if 8 > x + m[0] * a > -1 and 8 > y + m[1] * a > -1 and board[y + m[1] * a][x + m[0] * a] == None:
                    moveset.append((m[0] * a, m[1] * a))
                elif 8 > x + m[0] * a > -1 and 8 > y + m[1] * a > -1 and board[y + m[1] * a][x + m[0] * a].color != turn:
                    moveset.append((m[0] * a, m[1] * a))
                    break
                else:
                    break
    ###########################################
    if board[y][x].name == "king":
        for m in mov:
            a = 1
            if 8 > x + m[0] * a > -1 and 8 > y + m[1] * a > -1 and board[y + m[1] * a][x + m[0] * a] == None:
                moveset.append((m[0] * a, m[1] * a))
            elif 8 > x + m[0] * a > -1 and 8 > y + m[1] * a > -1 and board[y + m[1] * a][x + m[0] * a].color != turn:
                moveset.append((m[0] * a, m[1] * a))
                break
            else:
                break

            ######################################
        if board[y][x].castlingAllowed == True:
            #check short castle
            shortCastle = (False, False)
            
            if board[y][x + 1] == None and board[y][x + 2] == None:
                shortCastle = (True, shortCastle[1])
            if board[y][x + 3] != None:
                if board[y][x + 3].name == "rook" and board[y][x + 3].castlingAllowed == True:
                    shortCastle = (shortCastle[0], True)

            if shortCastle == (True, True):
                moveset.append((2, 0))

            ############################################
            #check long castle
            longCastle = (False, False)
            if board[y][x - 1] == None and board[y][x - 2] == None and board[y][x - 3] == None:
                longCastle = (True, longCastle[1])
            if board[y][x - 4] != None:
                if board[y][x - 4].name == "rook" and board[y][x - 4].castlingAllowed == True:
                    longCastle = (longCastle[0], True)
            if longCastle == (True, True):
                moveset.append((-2, 0))
    ##############################################
    

    for m in moveset:
        if 8 > x + m[0] > -1 and 8 > y + m[1] > -1 and (board[y + m[1]][x + m[0]] == None or board[y + m[1]][x + m[0]].color != turn):
            legalMoves.append((m[0], m[1]))
        
    
    return legalMoves

def drawLegalMoves(board, chosenPiece, turn):
    top, left, squareSize = defineSize()
    legalMoves = findLegalMoves(board, chosenPiece, turn)
    x, y = chosenPiece
   
    for l in legalMoves:
        l = (l[0] + x, l[1] + y)
        center = ((l[0]*squareSize + left + squareSize/2), (l[1]*squareSize + top + squareSize/2))
        pygame.draw.circle(screen, (10, 10, 10), center, squareSize/3)
    
def moveToNotation(moveHistory, notationHistory):
    length = len(moveHistory)
    lastMove = moveHistory[length - 1]
    notation = lastMove[0] + chr(int(lastMove[1]) + 65) + lastMove[2]
    notationHistory.append(notation)
    return notationHistory
    
def main():
    top, left, squareSize = defineSize()
    turn = "white"
    chosenPiece = None
    target = None
    moveHistory = []
    notationHistory = []
    pygame.display.update()
    
    
    board = newBoard()
    drawBoard(board)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == True:
                pos = pygame.mouse.get_pos()
                x, y = pos

               
                if  left + 8*squareSize > x > left and top + 8*squareSize > y > top:
                    x, y = findClickedSquare(pos)

                    

                    if board[y][x] != None:
                        if board[y][x].color == turn:
                            chosenPiece = x, y
                    if chosenPiece != None and board[y][x] != None:
                        if board[y][x].color != turn:
                            target = x, y
                    elif chosenPiece != None and board[y][x] == None:
                            target = x, y

                    if chosenPiece != None:
                        x, y = chosenPiece
                        drawBoard(board)
                        drawLegalMoves(board, chosenPiece, turn)
                        
                        
                        square = ((left + x * squareSize), (top + y * squareSize), squareSize, squareSize)
                        pygame.draw.rect(screen, (0, 200, 0 ), square)
                        
                        drawPieces(board)

                        pygame.display.update()
                        
                    if target != None and chosenPiece != None:
                        x, y = target
                        oldX, oldY = chosenPiece
                        diff = (x - oldX, y- oldY)
                       
                        m = findLegalMoves(board, chosenPiece, turn)

                        if diff in m:
                            moveHistory.append(board[oldY][oldX].notation + str(x) + str(8 - y))
                            notationHistory = moveToNotation(moveHistory, notationHistory)
                            
                            if board[oldY][oldX].name == "king" or board[oldY][oldX].name == "rook":
                                board[oldY][oldX].castlingAllowed = False
                            
                            if board[oldY][oldX].name == "king" and diff == (2, 0):
                                #move rook for short castling
                                board[oldY][oldX + 1] = board[oldY][oldX + 3]
                                board[oldY][oldX + 3] = None
                            elif board[oldY][oldX].name == "king" and diff == (-2, 0):
                                #move rook for long castling
                                board[oldY][oldX - 1] = board[oldY][oldX - 4]
                                board[oldY][oldX - 4] = None

                            board[y][x] = board[oldY][oldX]
                            board[oldY][oldX] = None
                            chosenPiece = None
                            target = None
                            if turn == "white":
                                turn = "black"
                            else:
                                turn = "white"
                            drawBoard(board)
                        elif board[y][x] == None:
                            chosenPiece = None
                            target = None
                            drawBoard(board)
                        
                
            elif event.type == pygame.VIDEORESIZE:
                top, left, squareSize = defineSize()
                screen.fill(color)
                drawBoard(board)
            

main()