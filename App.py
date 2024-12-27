import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from random import randrange
from GoL import nextStep
import Sounds as s


def start():
    p.playChords(chord)
    root.after(timeStep, stepLoop)

def stepLoop():
    global bitBoard
    if(playing):
        p.stopChords(chord)
        bitBoard = nextStep(bitBoard, boardSize, numNotes, randMel.get())
        loadBoard()
        p.playChords(chord)
        root.after(timeStep, stepLoop)

def loadBoard():
    for i in range(boardSize):
        chord[i] = False

    for i in range(boardSize):
        for j in range(boardSize):
            if(bitBoard[i][j] == 0):
                board[i][j].config(image=sleepImg)
            elif(bitBoard[i][j] == 1):
                board[i][j].config(image=smileImg)
            elif(bitBoard[i][j] == 2):
                board[i][j].config(image=oldImg)
                bitBoard[i][j] = 1
            else:
                board[i][j].config(image=singImg)
                bitBoard[i][j] = 1
                chord[i] = True

def oneStep():
    global bitBoard
    bitBoard = nextStep(bitBoard, boardSize, numNotes, randMel)
    loadBoard()

def buildBoard():
    global sleepImg
    global smileImg
    global singImg
    global oldImg
    global chord
    chord = [False]*boardSize
    
    # Format Images
    bW = int(400 / boardSize)
    resizeSleep = sleepOG.resize((bW,bW))
    sleepImg = ImageTk.PhotoImage(resizeSleep)
    resizeSmile = smileOG.resize((bW,bW))
    smileImg = ImageTk.PhotoImage(resizeSmile)
    resizeSing = singOG.resize((bW,bW))
    singImg = ImageTk.PhotoImage(resizeSing)
    resizeOld = oldOG.resize((bW,bW))
    oldImg = ImageTk.PhotoImage(resizeOld)

    for i in range(boardSize):
        bitBoard.append([])
        board.append([])
        for j in range(boardSize):
            bitBoard[i].append(0)
            board[i].append( tk.Button(gFrame, image=sleepImg, 
                command=lambda a=i, b=j : toggleFace(a,b)) )
            board[i][j].grid(row=i, column=j)

def destroyBoard():
    p.destroy()

    for i in range(boardSize):
        for j in range(boardSize):
            board[0][0].destroy()
            board[0].pop(0)
            bitBoard[0].pop(0)
        board.pop(0)
        bitBoard.pop(0)
            
def submitSize(x):
    global boardSize
    global playing
    global p
    try:
        val = int(sizeField.get())
    except ValueError:
        return

    if(val > 2 and val < 26):
        if(playing):
            togglePlayer()
        destroyBoard()
        boardSize = val
        strSize.set(boardSize)
        buildBoard()
        p = s.Sounds(boardSize)
        setInstr(instrBox.get())

def submitBPM(x):
    global timeStep
    try:
        val = int(bpmField.get())
    except ValueError:
        return

    # I arbitrarily chose 300 as max
    if(val > 0 and val <= 300):
        timeStep = int(60000 / val)
        strBPM.set(val)

def submitNum(x):
    global numNotes
    try:
        val = int(numField.get())
    except ValueError:
        return
    
    if(val > -2 and val <= boardSize):
        numNotes = val
        strNum.set(val)

def toggleFace(i, j):
    if(bitBoard[i][j] == 0):
        board[i][j].config(image=smileImg)
        bitBoard[i][j] = 1
    else:
        board[i][j].config(image=sleepImg)
        bitBoard[i][j] = 0

def togglePlayer():
    global playing
    if(playing):
        playerBtn.config(image=playImg)
        playing = False
        p.stopChords(chord)
    else:
        playerBtn.config(image=pauseImg)
        playing = True
        start()

def clearBoard():
    for i in range(boardSize):
        for j in range(boardSize):
            board[i][j].config(image=sleepImg)
            bitBoard[i][j] = 0

def randomBoard():
    for i in range(boardSize):
        for j in range(boardSize):
            if(randrange(2) == 1):
                toggleFace(i, j)

def setInstr(e):
    p.setInstr(instrBox.get())



if __name__ == '__main__':
    backColor = '#303030'
    foreColor = '#505050'
    boardSize = 10  # App gets weird/breaks when size is too big
    if(boardSize < 3 or boardSize > 25): 
        exit()
    timeStep = 500  # 120 bpm
    numNotes = -1

    p = s.Sounds(boardSize)
    

    root = tk.Tk()
    root.title("Keys of Life")
    root.geometry('900x600')
    root.config(bg=backColor)

    mainFrame = tk.Frame(root)
    mainFrame.pack(fill="both", expand=1)
    canvas = tk.Canvas(mainFrame)
    canvas.pack(side="left", fill="both", expand=1)
    canvas.config(bg=backColor)

    # Create Scrollbar
    scrollbar = ttk.Scrollbar(mainFrame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.config(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.config(scrollregion = canvas.bbox("all")))
    
    innerFrame = tk.Frame(canvas)
    canvas.create_window((0,0), window=innerFrame, anchor="nw")
    innerFrame.config(bg=backColor)


    # Entries
    eFrame = tk.Frame(innerFrame, bg='#505050')
    eFrame.pack()

    # GET board size
    strSize = tk.StringVar(eFrame, boardSize)
    sizeHeader = tk.Label(eFrame, text="Board Length:", 
        bg=foreColor, fg='#FFFFFF')
    sizeField = tk.Entry(eFrame, width=5, 
        bg=foreColor, fg='#FFFFFF')
    sizeBuffer = tk.Label(eFrame, text=" | ", 
        bg=foreColor, fg='#FFFFFF')
    sizeLabel = tk.Label(eFrame, textvariable=strSize, 
        bg=foreColor, fg='#FFFFFF')

    sizeHeader.grid(row=0, column=0)
    sizeField.grid(row=0, column=1)
    sizeBuffer.grid(row=0, column=2)
    sizeLabel.grid(row=0, column=3)
    sizeField.bind("<Return>", submitSize)

    # GET bpm
    strBPM = tk.StringVar(eFrame, int(60000 / timeStep))
    bpmHeader = tk.Label(eFrame, text="BPM:", 
        bg=foreColor, fg='#FFFFFF')
    bpmField = tk.Entry(eFrame, width=5, 
        bg=foreColor, fg='#FFFFFF')
    bpmBuffer = tk.Label(eFrame, text=" | ", 
        bg=foreColor, fg='#FFFFFF')
    bpmLabel = tk.Label(eFrame, textvariable=strBPM, 
        bg=foreColor, fg='#FFFFFF')

    bpmHeader.grid(row=1, column=0)
    bpmField.grid(row=1, column=1)
    bpmBuffer.grid(row=1, column=2)
    bpmLabel.grid(row=1, column=3)
    bpmField.bind("<Return>", submitBPM)

    # GET amount of notes
    strNum = tk.StringVar(eFrame, numNotes)
    numHeader = tk.Label(eFrame, text="Num. Notes:", 
        bg=foreColor, fg='#FFFFFF')
    numField = tk.Entry(eFrame, width=5, 
        bg=foreColor, fg='#FFFFFF')
    numBuffer = tk.Label(eFrame, text=" | ", 
        bg=foreColor, fg='#FFFFFF')
    numLabel = tk.Label(eFrame, textvariable=strNum, 
        bg=foreColor, fg='#FFFFFF')

    numHeader.grid(row=2, column=0)
    numField.grid(row=2, column=1)
    numBuffer.grid(row=2, column=2)
    numLabel.grid(row=2, column=3)
    numField.bind("<Return>", submitNum)

    randMel = tk.IntVar()
    cRandMel = tk.Checkbutton(eFrame, text="Random", variable=randMel, onvalue=1, offvalue=0, 
    bg=foreColor, fg='#FFFFFF', selectcolor=backColor)
    cRandMel.grid(row=2, column=4)

    # GET instrument
    instrHeader = tk.Label(eFrame, text="Instrument:", 
        bg=foreColor, fg='#FFFFFF')
    instrHeader.grid(row=3, column=0)
    
    instrList = []
    for i in range(128):
        instrList.append(i)
    instr = tk.StringVar() 
    instrBox = ttk.Combobox(eFrame, width=15, textvariable=instr) 
    instrBox.config(values=instrList)
    instrBox.bind('<<ComboboxSelected>>', lambda x=instrBox.get() : setInstr(x))
    instrBox.grid(row=3, column=1, columnspan=3)
    instrBox.current(0)
    



    # Game Frame
    gFrame = tk.Frame(innerFrame)
    gFrame.pack()

    # Open images for tiles
    sleepOG = Image.open('Images/sleep.jpg')
    smileOG = Image.open('Images/smiles.jpg')
    singOG = Image.open('Images/sing.jpg')
    oldOG = Image.open('Images/old.jpg')

    # Build game board
    bitBoard = []
    board = []
    buildBoard()


    # Buttons
    btnFrame = tk.Frame(innerFrame)
    btnFrame.pack()

    # Clear button
    clearOG = Image.open('Images/clear.jpg').resize((50,50))
    clearImg = ImageTk.PhotoImage(clearOG)
    clearBtn = tk.Button(btnFrame, image=clearImg, command=clearBoard)
    clearBtn.grid(row=0, column=0)

    # Pause button
    pauseOG = Image.open('Images/pause.jpg').resize((50,50))
    pauseImg = ImageTk.PhotoImage(pauseOG)
    playOG = Image.open('Images/play.jpg').resize((50,50))
    playImg = ImageTk.PhotoImage(playOG)

    playing = False
    playerBtn = tk.Button(btnFrame, image=playImg, command=togglePlayer)
    playerBtn.grid(row=0, column=1)

    # Next step button
    oneStepOG = Image.open('Images/oneStep.jpg').resize((50,50))
    oneStepImg = ImageTk.PhotoImage(oneStepOG)
    oneStepBtn = tk.Button(btnFrame, image=oneStepImg, command=oneStep)
    oneStepBtn.grid(row=0, column=2)
    
    # Randomizer button
    randomOG = Image.open('Images/random.jpg').resize((50,50))
    randomImg = ImageTk.PhotoImage(randomOG)
    randomBtn = tk.Button(btnFrame, image=randomImg, command=randomBoard)
    randomBtn.grid(row=0, column=3)


    
    root.mainloop()