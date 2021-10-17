import pieces
import sys
import pygame
import socket
import pickle

pygame.init()

size = [1600, 900]
inMenu = True
top = size[1]/10
left = (size[0] - (size[1] - 2*top)) / 2
squareSize = int((size[1] - 2*top) / 8)

screen = pygame.display.set_mode(size, pygame.RESIZABLE)
color = (0, 0, 0)
white = (255, 255, 255)
screen.fill(color)

brown = (153, 102, 51)
lightBrown = (236, 217, 198)


def defineSize():
    size = screen.get_size()
    top = size[1]/10
    left = (size[0] - (size[1] - 2*top)) / 2
    squareSize = int((size[1] - 2*top) / 8)
    return int(top), int(left), int(squareSize)


def drawMenu():
    top, left, squareSize = defineSize()
    screen.fill(color)
    x, y = screen.get_size()
    heightLetters = 35
    textFont = pygame.font.SysFont("calibri", heightLetters, True)

    text1 = textFont.render("Schach lokal spielen", True, white)
    text2 = textFont.render("Schach online spielen", True, white)

    text3 = textFont.render("Schachvariante lokal spielen", True, white)
    text4 = textFont.render("Schachvariante online spielen", True, white)
    texts = [text1, text2, text3, text4]
    maxWidth = text4.get_size()[0]

    image = pygame.image.load("Sprites/chess_position.png")
    image = pygame.transform.smoothscale(image, (y, y))
    screen.blit(image, ((x-y)/2, 0))

    for a in range(4):
        width = texts[a].get_size()[0]

        surface = pygame.Surface((maxWidth + 40, heightLetters + 10))
        surface.fill(brown)
        surface.blit(texts[a], ((maxWidth-width)/2 + 20, 5))
        surface.set_alpha(200)
        screen.blit(surface, (x/2-maxWidth/2 - 20,
                    (top + squareSize + 2*a*squareSize - heightLetters/2 - 5)))


def chooseVariant(x, y):
    top, left, squareSize = defineSize()
    xVal, yVal = screen.get_size()
    if x > xVal/2 - 239 and x < xVal/2 + 239:
        if y > top + squareSize - 35/2 - 5 and y < top + squareSize - 35/2 - 5 + 45:
            return 0
        elif y > top + squareSize + 2*squareSize - 35/2 - 5 and y < top + squareSize + 2*squareSize - 35/2 - 5 + 45:
            return 1
        elif y > top + squareSize + 4*squareSize - 35/2 - 5 and y < top + squareSize + 4*squareSize - 35/2 - 5 + 45:
            return 2
        elif y > top + squareSize + 6*squareSize - 35/2 - 5 and y < top + squareSize + 6*squareSize - 35/2 - 5 + 45:
            return 3


def drawBoard(board, turn):
    if inMenu:
        drawMenu()
    else:
        top, left, squareSize = defineSize()

        screen.fill(color)

        for a in range(8):
            for b in range(8):

                if (a + b) % 2 == 1:
                    square = ((left + a * squareSize), (top + b *
                              squareSize), squareSize, squareSize)
                    pygame.draw.rect(screen, brown, square)

                else:
                    square = ((left + a * squareSize), (top + b *
                              squareSize), squareSize, squareSize)
                    pygame.draw.rect(screen, lightBrown, square)

        if inCheck(board, turn):
            drawCheck(board, turn)
        else:
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
                spriteOfPiece = pygame.image.load(board[b][a].sprite)
                image = pygame.transform.smoothscale(
                    spriteOfPiece, (squareSize, squareSize))
                screen.blit(image, coord)
    pygame.display.update()


def drawChosenPiece(board, x, y):
    top, left, squareSize = defineSize()

    square = ((left + x * squareSize), (top + y *
              squareSize), squareSize, squareSize)
    pygame.draw.rect(screen, (0, 200, 0), square)

    coord = ((left + squareSize * x), (top + squareSize * y))
    spriteOfPiece = pygame.image.load(board[y][x].sprite)
    image = pygame.transform.smoothscale(
        spriteOfPiece, (squareSize, squareSize))
    screen.blit(image, coord)
    pygame.display.update()


def findLegalMoves(board, chosenPiece, turn):
    x, y = chosenPiece
    moveset = []

    mov = list(board[y][x].moves)

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

        # capture sideways
        if board[y][x].color == "black":
            yDir = -1
        else:
            yDir = 1

        if 8 > x + 1 > -1 and 8 > y - 1 * yDir > -1 and board[y - 1 * yDir][x + 1] != None and board[y - 1 * yDir][x + 1].color != turn:
            legalMoves.append((1, - yDir))

        if 8 > x - 1 > -1 and 8 > y - 1 * yDir > -1 and board[y - 1 * yDir][x - 1] != None and board[y - 1 * yDir][x - 1].color != turn:
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
            if 8 > x + m[0] > -1 and 8 > y + m[1] > -1 and board[y + m[1]][x + m[0]] == None:
                moveset.append((m[0], m[1]))
            elif 8 > x + m[0] > -1 and 8 > y + m[1] > -1 and board[y + m[1]][x + m[0]].color != turn:
                moveset.append((m[0], m[1]))

            ######################################
        if board[y][x].castlingAllowed == True:
            # check short castle
            shortCastle = (False, False)

            if x + 2 < 8 and board[y][x + 1] == None and board[y][x + 2] == None:
                shortCastle = (True, shortCastle[1])
            if x + 3 < 8 and board[y][x + 3] != None:
                if board[y][x + 3].name == "rook" and board[y][x + 3].castlingAllowed == True:
                    shortCastle = (shortCastle[0], True)

            if shortCastle == (True, True):
                moveset.append((2, 0))

            ############################################
            # check long castle
            longCastle = (False, False)
            if x - 3 > -1 and board[y][x - 1] == None and board[y][x - 2] == None and board[y][x - 3] == None:
                longCastle = (True, longCastle[1])
            if x - 4 > -1 and board[y][x - 4] != None:
                if board[y][x - 4].name == "rook" and board[y][x - 4].castlingAllowed == True:
                    longCastle = (longCastle[0], True)
            if longCastle == (True, True):
                moveset.append((-2, 0))
    ##############################################
    if board[y][x].name == "knight":
        for m in mov:
            if 8 > x + m[0] > -1 and 8 > y + m[1] > -1 and board[y + m[1]][x + m[0]] == None:
                moveset.append((m[0], m[1]))
            elif 8 > x + m[0] > -1 and 8 > y + m[1] > -1 and board[y + m[1]][x + m[0]].color != turn:
                moveset.append((m[0], m[1]))

    for m in moveset:
        if 8 > x + m[0] > -1 and 8 > y + m[1] > -1 and (board[y + m[1]][x + m[0]] == None or board[y + m[1]][x + m[0]].color != turn):
            legalMoves.append((m[0], m[1]))

    return legalMoves


def drawLegalMoves(board, chosenPiece, turn):
    top, left, squareSize = defineSize()
    # findLegalMoves -> findAllLegalMoves
    legalMoves = findAllLegalMoves(board, chosenPiece, turn)
    x, y = chosenPiece

    for l in legalMoves:
        l = (l[0] + x, l[1] + y)
        center = ((l[0]*squareSize + left + squareSize/2),
                  (l[1]*squareSize + top + squareSize/2))
        pygame.draw.circle(screen, (10, 10, 10), center, squareSize/3)


def moveToNotation(moveHistory, notationHistory):
    length = len(moveHistory)
    lastMove = moveHistory[length - 1]
    notation = lastMove[0] + chr(int(lastMove[1]) + 65) + lastMove[2]
    notationHistory.append(notation)
    return notationHistory


def getPawnPromotion(x, y):
    top, left, squareSize = defineSize()
    width, heigth = screen.get_size()

    x = int((x - width/2 + 2*squareSize)/squareSize)
    y = int((y - heigth/2 + squareSize/2)/squareSize)

    if y == 0:
        if x == 0:
            return "queen"
        elif x == 1:
            return "rook"
        elif x == 2:
            return "bishop"
        elif x == 3:
            return "knight"
        else:
            return 0
    else:
        return 0


def findKing(board, turn):
    for y in range(8):
        for x in range(8):
            if board[y][x] != None and board[y][x].name == "king" and board[y][x].color == turn:
                return x, y


def inCheck(board, turn):
    a, b = findKing(board, turn)

    # we want to know whether the black king is in check after white moved, therefore we need to find the legal moves of white(def findLegalMove).
    # But turn would be black because white just moved, so we switch turn.
    if turn == "white":
        turn = "black"
    else:
        turn = "white"

    for y in range(8):
        for x in range(8):
            # this turn and the turn in the next line need to be the same
            if board[y][x] != None and board[y][x].color == turn:
                lMoves = findLegalMoves(board, (x, y), turn)
                for m in lMoves:
                    if m[0] + x == a and m[1] + y == b:
                        return True
    return False


def drawCheck(board, turn):
    top, left, squareSize = defineSize()
    x, y = findKing(board, turn)
    square = (left + x * squareSize, top + y *
              squareSize, squareSize, squareSize)
    pygame.draw.rect(screen, (255, 0, 0), square)
    drawPieces(board)


def drawPromotion(c):
    screen.fill(color)
    brown = (153, 102, 51)
    lightBrown = (236, 217, 198)
    top, left, squareSize = defineSize()
    width, height = screen.get_size()

    promotionPieces = ["queen", "rook", "bishop", "knight"]

    for a in range(4):
        left = width/2 + (a - 2) * squareSize
        top = height/2 - squareSize/2
        square = (left, top, squareSize, squareSize)
        if a % 2 == 0:
            sColor = lightBrown
        else:
            sColor = brown

        pygame.draw.rect(screen, sColor, square)

        name = promotionPieces[a]

        image1 = pygame.image.load("Sprites/" + c + "_" + name + ".png")
        image1 = pygame.transform.smoothscale(image1, (squareSize, squareSize))
        screen.blit(image1, (left, top))

        pygame.display.update()

###############################################


def castleThroughCheck(board, a, b, legalMoves, turn):
    print(legalMoves)

    print(turn)
    print(board[b][a])
    if (2, 0) in legalMoves:

        for add in range(0, 2):
            virtualBoard = []
            for q in range(8):
                virtualBoard.append(list(board[q]))
            virtualBoard[b][a] = None
            virtualBoard[b][a + add] = pieces.King(turn)
            if inCheck(virtualBoard, turn):
                legalMoves.remove((2, 0))
                break

    if (-2, 0) in legalMoves:
        print(legalMoves)
        for add in range(0, -2, -1):
            virtualBoard = []
            for q in range(8):
                virtualBoard.append(list(board[q]))
            virtualBoard[b][a] = None
            virtualBoard[b][a + add] = pieces.King(turn)
            if inCheck(virtualBoard, turn):
                legalMoves.remove((-2, 0))
                break

    return legalMoves


def removeMovesDueToCheck(board, a, b, turn, legalMoves):
    if board[b][a] != None and board[b][a].color == turn:
        if board[b][a].name == "king" and board[b][a].castlingAllowed == True:
            legalMoves = castleThroughCheck(board, a, b, legalMoves, turn)
        virtualBoard = []
        lMovesCopy = list(legalMoves)
        for m in lMovesCopy:
            virtualBoard = []
            for q in range(8):
                virtualBoard.append(list(board[q]))
            virtualBoard[b + m[1]][a + m[0]] = virtualBoard[b][a]
            virtualBoard[b][a] = None
            if inCheck(virtualBoard, turn):
                legalMoves.remove(m)
    return legalMoves


def findAllLegalMoves(board, chosenPiece, turn):
    a, b = chosenPiece
    legalMoves = findLegalMoves(board, chosenPiece, turn)
    return removeMovesDueToCheck(board, a, b, turn, legalMoves)


def variant(board, target, turn):
    x, y = target

    if board[y][x].name == "queen":
        board[y][x] = pieces.Queen(turn)
    elif board[y][x].name == "rook":
        board[y][x] = pieces.Rook(turn)
    elif board[y][x].name == "bishop":
        board[y][x] = pieces.Bishop(turn)
    elif board[y][x].name == "knight":
        board[y][x] = pieces.Knight(turn)


def displayIP():
    heightLetters = 35
    x, y = screen.get_size()

    textFont = pygame.font.SysFont("calibri", heightLetters, True)
    self_ip = str(socket.gethostbyname(socket.gethostname()))
    self_ip = f"your IP: {self_ip}"
    text_ip = textFont.render(self_ip, True, white)

    w, h = text_ip.get_size()

    surface = pygame.Surface((w + 40, h + 10))
    surface.fill(brown)
    surface.blit(text_ip, (20, 5))
    surface.set_alpha(200)

    screen.blit(surface, (x/2-w/2-20, y/3 - h/2 - 5))

    # host menu button
    w, h = 700, 100
    l, t = x/2 - w/2, (2*y)/3 - h/2
    button = pygame.Rect(l, t, w, h)
    text1 = 'Host Game'  # 160, 35
    text2 = 'You dont need to enter an IP to host a Game'  # 650, 35
    textButton1 = textFont.render(text1, True, white)
    textButton2 = textFont.render(text2, True, white)

    surface = pygame.Surface((w, h))
    surface.fill(color)
    surface.blit(textButton1, (700/2 - 160/2, 10))
    surface.blit(textButton2, (700/2 - 650/2, 10 + 35 + 10))
    surface.set_alpha(200)

    screen.blit(surface, (l, t))
    # give l, t, w, h to inputField


def inputField():
    x, y = screen.get_size()
    textFont = pygame.font.SysFont("calibri", 35, True)
    w, h = 500, 50
    left = (screen.get_size()[0] - w)/2
    top = (screen.get_size()[1] - h)/2 + 10
    inputField = pygame.Rect(left, top, w, h)
    clicked = True
    inputFinished = False
    opponent_ip = ''
    dimension = 700, 100,  x/2 - w/2, (2*y)/3 - h/2
    button = pygame.Rect(dimension[0], dimension[1],
                         dimension[2], dimension[3])

    while not inputFinished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == True:
                x, y = pygame.mouse.get_pos()
                if inputField.collidepoint((x, y)):
                    clicked = True
                elif button.collidepoint(x, y):
                    print(11111111111111, 12432421, x, y, button)
                    hosting = True
                    return hosting
                else:
                    clicked = False
            elif event.type == pygame.KEYDOWN:
                if clicked:
                    if event.key == pygame.K_RETURN:
                        return opponent_ip
                    elif event.key == pygame.K_BACKSPACE:
                        opponent_ip = opponent_ip[:-1]
                    else:
                        opponent_ip += event.unicode

        x, y = screen.get_size()
        screen.fill((0, 0, 0))
        image = pygame.image.load("Sprites/chess_position.png")
        image = pygame.transform.smoothscale(image, (y, y))
        screen.blit(image, ((x-y)/2, 0))

        displayIP()

        inputF = textFont.render(opponent_ip, True, color)
        if inputF.get_size()[0] + 15 > w:
            w = inputF.get_size()[0] + 15
            inputField = pygame.Rect(left, top, w, h)
        screen.blit(inputF, (left + 10, top + 7))
        pygame.draw.rect(screen, color, inputField, 5)
        pygame.display.update()

def checkStalemate(board, turn):
    isStalemate = True
    for a in range(8):
        for b in range(8):
            if board[b][a] != None and board[b][a].color == turn:
                if findAllLegalMoves(board, (a, b), turn) != []:
                    isStalemate = False
                    break
    if inCheck(board, turn):
        isStalemate = False
    return isStalemate

def stalemate():
    msg = f'Stalemate, press enter'
    textFont = pygame.font.SysFont("calibri", 50, True)
    winMsg = textFont.render(msg, True, white)

    wid = winMsg.get_size()[0]

    surf = pygame.Surface((wid + 20, 70))
    surf.fill(brown)
    surf.set_alpha(200)
    size = screen.get_size()
    surf.blit(winMsg, (10, 10))
    screen.blit(surf, (size[0]/2 - wid/2 - 10, size[1]/2 - 35))
    pygame.display.update()
    pressedEscape = False
    while pressedEscape == False:
        for event2 in pygame.event.get():
            if event2.type == pygame.KEYDOWN and event2.key == pygame.K_RETURN:
                pressedEscape = True
            elif event2.type == pygame.QUIT: 
                sys.exit()
    
def checkForCheckmate(board, turn):
    if inCheck(board, turn):
        saved = False
        for b in range(8):
            for a in range(8):
                if board[b][a] != None and board[b][a].color == turn:
                    lMoves = findLegalMoves(board, (a, b), turn)
                    virtualBoard = []
                    lMovesCopy = list(lMoves)
                    for m in lMovesCopy:
                        virtualBoard = []
                        for q in range(8):
                            virtualBoard.append(list(board[q]))
                        virtualBoard[b + m[1]][a + m[0]] = virtualBoard[b][a]
                        virtualBoard[b][a] = None
                        if not inCheck(virtualBoard, turn):
                            saved = True
                        else:
                            lMoves.remove(m)
                    #print(lMoves, board[b][a].name, (a, b))
        return saved
    return True

def checkmateMessage(turn):
    if turn == 'white':

        winner = 'black'
    else:
        winner = 'white'

    msg = f'Checkmate, {winner} won. press enter'
    textFont = pygame.font.SysFont("calibri", 50, True)
    winMsg = textFont.render(msg, True, white)

    wid = winMsg.get_size()[0]

    surf = pygame.Surface((wid + 20, 70))
    surf.fill(brown)
    surf.set_alpha(200)
    size = screen.get_size()
    surf.blit(winMsg, (10, 10))
    screen.blit(surf, (size[0]/2 - wid/2 - 10, size[1]/2 - 35))
    pygame.display.update()
    pressedEscape = False
    while pressedEscape == False:
        for event2 in pygame.event.get():
            if event2.type == pygame.KEYDOWN and event2.key == pygame.K_RETURN:
                pressedEscape = True
            elif event2.type == pygame.QUIT: 
                sys.exit()
        
stalemateBoard = [[None for i in range(8)] for i in range(8)]
stalemateBoard[0][0] = pieces.King("black")
stalemateBoard[1][3] = pieces.Queen("white")
stalemateBoard[7][7] = pieces.King("white")

def main():
    global inMenu
    NotOpen = True
    playerColor = 'both'
    chosenVariant = 4
    top, left, squareSize = defineSize()
    turn = "white"
    chosenPiece = None
    target = None
    moveHistory = []
    notationHistory = []
    pygame.display.update()
    
    
    board = newBoard()
    #board = stalemateBoard
    drawBoard(board, turn)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 59822))#(IP, Port)
    s.listen(5) #queue size

    while True:
        if chosenVariant == 0 or chosenVariant == 2:
            s.close()
        if (chosenVariant == 1 or chosenVariant == 3) and playerColor != turn and playerColor != 'both':
            
            full_msg = b''
            new_msg = True
            msglen = 0
            while len(full_msg)-8 != msglen:
                socketOPPONENT, address = s.accept()
                opponentIP = address[0]
                print(f"Connection from {address} has been established")
                """
                data = socketOPPONENT.recv(5096)
                print(data, len(data))
                msg = pickle.loads(data)
                """
                msg = socketOPPONENT.recv(16)
                if new_msg:
                    print("new msg len:",msg[:8])
                    msglen = int(msg[:8])
                    new_msg = False

                print(f"full message length: {msglen}")

                full_msg += msg

                print(len(full_msg))

                
            print("full msg recvd")
            print(full_msg[8:])
            print(pickle.loads(full_msg[8:]))
            
            board = full_msg[8:]

            turn = playerColor
            drawBoard(board, turn)
            if not checkForCheckmate(board, turn):
                checkmateMessage(turn)
                inMenu = True
                turn = "white"
                board = newBoard()
                moveHistory = []
                notationHistory = []
                drawBoard(board, turn)

                print("Checkmate, ", turn, " loses")
            if checkStalemate(board, turn):
                drawBoard(board, turn)

                stalemate()

                inMenu = True
                board = newBoard()
                moveHistory = []
                notationHistory = []
                turn = "white"
            pygame.display.update()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == True:

                if inMenu:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    x, y = pos
                    if chooseVariant(x, y) == 0 or chooseVariant(x, y) == 2:
                        playerColor = 'both'
                        inMenu = False
                        chosenVariant = chooseVariant(x, y)
                        screen.fill(color)
                        drawBoard(board, turn)
                    elif chooseVariant(x, y) == 1 or chooseVariant(x, y) == 3:
                        chosenVariant = chooseVariant(x, y)
                        opponentIP = inputField()
                        if opponentIP == True:
                            playerColor = 'black'
                            opponentIP = ''
                        else:
                            playerColor = 'white'
                        print(opponentIP)
                        inMenu = False
                        drawBoard(board, turn)
                    
                else:
                    top, left, squareSize = defineSize()
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

                            drawBoard(board, turn)
                            drawChosenPiece(board, x, y)
                            drawLegalMoves(board, chosenPiece, turn)
                            
                            pygame.display.update()
                            
                        if target != None and chosenPiece != None:#check whether you can capture the target piece
                            x, y = target
                            oldX, oldY = chosenPiece
                            diff = (x - oldX, y - oldY)
                        
                            m = findAllLegalMoves(board, chosenPiece, turn)

                            if diff in m:#capture piece
                                moveHistory.append(board[oldY][oldX].notation + str(x) + str(8 - y))
                                notationHistory = moveToNotation(moveHistory, notationHistory)
                                print(notationHistory)
                                # TODO: add Checks, castling, captures and promotion to notation
                                
                                if board[oldY][oldX].name == "king" or board[oldY][oldX].name == "rook":
                                    board[oldY][oldX].castlingAllowed = False
                                
                                if board[oldY][oldX].name == "king" and diff == (2, 0):
                                    # move rook for short castling
                                    board[oldY][oldX + 1] = board[oldY][oldX + 3]
                                    board[oldY][oldX + 3] = None
                                elif board[oldY][oldX].name == "king" and diff == (-2, 0):
                                    # move rook for long castling
                                    board[oldY][oldX - 1] = board[oldY][oldX - 4]
                                    board[oldY][oldX - 4] = None

                                #########################################
                                # promotion
                                undidMove = False #for control later on
                                if board[oldY][oldX].name == "pawn" and (y == 7 or y == 0):
                                    # promotion
                                    drawPromotion(board[oldY][oldX].color)

                                    if inCheck(board, turn):
                                        drawCheck(board, turn)
                                    # pygame.display.update()

                                    promoteTo = None
                                    

                                    while promoteTo != "queen" and promoteTo != "rook" and promoteTo != "knight" and promoteTo != "bishop" and promoteTo != 0:
                                        for event in pygame.event.get():
                                            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == True:
                                                x1, y1 = pygame.mouse.get_pos()
                                                promoteTo = getPawnPromotion(x1, y1)
                                            ###########################    
                                            elif event.type == pygame.VIDEORESIZE:
                                                drawPromotion(board[oldY][oldX].color)
                                            ###########################
                                            elif event.type == pygame.QUIT: 
                                                sys.exit()

                                    if promoteTo == "queen": 
                                        board[oldY][oldX] = pieces.Queen(turn)
                                    elif promoteTo == "rook": 
                                        board[oldY][oldX] = pieces.Rook(turn)
                                    elif promoteTo == "bishop": 
                                        board[oldY][oldX] = pieces.Bishop(turn)
                                    elif promoteTo == "knight": 
                                        board[oldY][oldX] = pieces.Knight(turn)
                                    else:
                                        undidMove = True
                                #######################################################
                                
                                if undidMove == False: #if not promoted
                                    # variant
                                    if board[oldY][oldX].name == "pawn" and board[target[1]][target[0]] != None and board[target[1]][target[0]].name != "pawn" and (chosenVariant == 2 or chosenVariant == 3):
                                        variant(board, target, turn)
                                    else:
                                        board[y][x] = board[oldY][oldX]
                                    
                                    board[oldY][oldX] = None
                                    chosenPiece = None
                                    target = None

                                    if turn == "white":
                                        turn = "black"
                                    else:
                                        turn = "white"

                                    if chosenVariant == 1 or chosenVariant == 3:
                                        # send new board to opponent
                                        msg = pickle.dumps(board)
                                        msg = bytes(f"{len(msg):<{8}}", 'utf-8')+msg
                                        print(msg, len(msg))
                                        sOpponent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                        sOpponent.connect((opponentIP, 59822))#(IP, Port)
                                        sOpponent.send(msg)
                                        
                                        
                                    # check for stalemate
                                    if checkStalemate(board, turn):
                                        drawBoard(board, turn)

                                        stalemate()

                                        inMenu = True
                                        board = newBoard()
                                        moveHistory = []
                                        notationHistory = []
                                        turn = "white"

                                    drawBoard(board, turn)
                                else:
                                    target = None
                                    drawBoard(board, turn)

                            elif board[y][x] == None or board[y][x].color != turn:
                                chosenPiece = None
                                target = None
                                drawBoard(board, turn)

                            if not checkForCheckmate(board, turn):
                                checkmateMessage(turn)
                                inMenu = True
                                turn = "white"
                                board = newBoard()
                                moveHistory = []
                                notationHistory = []
                                drawBoard(board, turn)

                                print("Checkmate, ", turn, " loses")
                        
                        
                
            elif event.type == pygame.VIDEORESIZE:
                top, left, squareSize = defineSize()
                screen.fill(color)
                drawBoard(board, turn)
            

main()
