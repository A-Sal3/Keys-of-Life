import copy
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
    chord.clear()

    for i in range(boardSize):
        for j in range(boardSize):
            if(bitBoard[i][j] == 0):
                board[i][j].config(image=blackImg)
            elif(bitBoard[i][j] == 1):
                board[i][j].config(image=whiteImg)
            else:
                board[i][j].config(image=blueImg)
                bitBoard[i][j] = 1
                chord.append([i,j])

def oneStep():
    global bitBoard
    bitBoard = nextStep(bitBoard, boardSize, numNotes, randMel)
    loadBoard()

def buildBoard():
    global blackImg
    global whiteImg
    global blueImg
    global prevBoard
    chord.clear()
    
    # Format Images
    bW = int(400 / boardSize)
    resizeBlack = blackOG.resize((bW,bW))
    blackImg = ImageTk.PhotoImage(resizeBlack)
    resizeWhite = whiteOG.resize((bW,bW))
    whiteImg = ImageTk.PhotoImage(resizeWhite)
    resizeBlue = blueOG.resize((bW,bW))
    blueImg = ImageTk.PhotoImage(resizeBlue)

    for i in range(boardSize):
        bitBoard.append([])
        board.append([])
        for j in range(boardSize):
            bitBoard[i].append(0)
            board[i].append( tk.Button(gFrame, image=blackImg,
                command=lambda a=i, b=j : toggleFace(a,b)) )
            board[i][j].grid(row=i, column=j)
    prevBoard = bitBoard

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
    global boardNotes
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
        p = s.Sounds(boardSize, dist, fret)
        boardNotes = p.getBoardNotes()
        setInstr(instrBox.get())

def submitBPM(x):
    global timeStep
    try:
        val = int(bpmField.get())
    except ValueError:
        return

    # Arbitrarily set max to 300
    if(val > 0 and val <= 300):
        timeStep = int(60000 / val)
        strBPM.set(val)

def submitNum(x):
    global numNotes
    try:
        val = int(numField.get())
    except ValueError:
        return
    
    if(val >= -1 and val <= boardSize):
        numNotes = val
        strNum.set(val)

def toggleFace(i, j):
    if(bitBoard[i][j] == 0):
        board[i][j].config(image=whiteImg)
        bitBoard[i][j] = 1
    else:
        board[i][j].config(image=blackImg)
        bitBoard[i][j] = 0

def togglePlayer():
    global playing
    global prevBoard
    if(playing):
        playerBtn.config(image=playImg)
        playing = False
        p.stopChords(chord)
    else:
        playerBtn.config(image=pauseImg)
        playing = True
        prevBoard = bitBoard
        start()

def goBack():
    global bitBoard
    bitBoard = prevBoard
    if(not playing):
        loadBoard()

def clearBoard():
    for i in range(boardSize):
        for j in range(boardSize):
            board[i][j].config(image=blackImg)
            bitBoard[i][j] = 0

def randomBoard():
    for i in range(boardSize):
        for j in range(boardSize):
            if(randrange(2) == 1):
                toggleFace(i, j)

def setInstr(e):
    p.setInstr(instrBox.get())

def chngDistSel():
    val = int(distSelect.get())
    if(val):
        distField.config(state='normal')
        dScaleBox.config(state='disabled')
        submitDist(0)
    else:
        distField.config(state='disabled')
        dScaleBox.config(state='normal')
        setDistScale(0)

def setDistScale(x):
    global dist
    dist = dScaleBox.get()
    p.setBoardNotes(boardSize, dist, fret)

def chngFretSel():
    val = int(fretSelect.get())
    if(val):
        fretField.config(state='normal')
        fScaleBox.config(state='disabled')
        submitFret(0)
    else:
        fretField.config(state='disabled')
        fScaleBox.config(state='normal')
        setFretScale(0)


def setFretScale(x):
    global fret
    fret = fScaleBox.get()
    p.setBoardNotes(boardSize, dist, fret)

def submitDist(x):
    global dist
    global p
    global boardNotes
    try:
        val = int(distField.get())
    except ValueError:
        return

    # Arbitrarily set max to 12
    if(val >= 0 and val <= 12):
        dist = val
        strDist.set(val)
        p.setBoardNotes(boardSize, dist, fret)

def submitFret(x):
    global fret
    global p
    global boardNotes
    try:
        val = int(fretField.get())
    except ValueError:
        return
    
    # Arbitrarily set max to 12
    if(val >= 0 and val <= 12):
        fret = val
        strFret.set(val)
        p.setBoardNotes(boardSize, dist, fret)


if __name__ == '__main__':
    backColor = '#303030'
    foreColor = '#505050'
    boardSize = 10  # App gets weird/breaks when size is too big
    if(boardSize < 3 or boardSize > 25): 
        exit()
    timeStep = 500  # 120 bpm
    numNotes = -1

    dist = "Pentatonic"
    fret = 0
    p = s.Sounds(boardSize, dist, fret)
    boardNotes = p.getBoardNotes()
    

    root = tk.Tk()
    root.title("Keys of Life")
    root.geometry('500x600')
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
    instrBox = ttk.Combobox(eFrame, width=10, textvariable=instr) 
    instrBox.config(values=instrList)
    instrBox.bind('<<ComboboxSelected>>', setInstr)
    instrBox.grid(row=3, column=1, columnspan=3)
    instrBox.current(0)



    # Game Frame
    gFrame = tk.Frame(innerFrame)
    gFrame.pack()

    # Open images for tiles
    blackOG = Image.open('Images/black.jpg')
    whiteOG = Image.open('Images/white.jpg')
    blueOG = Image.open('Images/blue.jpg')

    # Build game board
    bitBoard = []
    board = []
    chord = []
    buildBoard()


    # Buttons
    btnFrame = tk.Frame(innerFrame)
    btnFrame.pack()

    # Clear button
    clearOG = Image.open('Images/clear.jpg').resize((50,50))
    clearImg = ImageTk.PhotoImage(clearOG)
    clearBtn = tk.Button(btnFrame, image=clearImg, command=clearBoard)
    clearBtn.grid(row=0, column=0)

    # Go Back button
    goBackOG = Image.open('Images/goBack.jpg').resize((50,50))
    goBackImg = ImageTk.PhotoImage(goBackOG)
    goBackBtn = tk.Button(btnFrame, image=goBackImg, command=goBack)
    goBackBtn.grid(row=0, column=1)

    # Pause/Play button
    pauseOG = Image.open('Images/pause.jpg').resize((50,50))
    pauseImg = ImageTk.PhotoImage(pauseOG)
    playOG = Image.open('Images/play.jpg').resize((50,50))
    playImg = ImageTk.PhotoImage(playOG)

    playing = False
    playerBtn = tk.Button(btnFrame, image=playImg, command=togglePlayer)
    playerBtn.grid(row=0, column=2)

    # Next step button
    oneStepOG = Image.open('Images/oneStep.jpg').resize((50,50))
    oneStepImg = ImageTk.PhotoImage(oneStepOG)
    oneStepBtn = tk.Button(btnFrame, image=oneStepImg, command=oneStep)
    oneStepBtn.grid(row=0, column=3)
    
    # Randomizer button
    randomOG = Image.open('Images/random.jpg').resize((50,50))
    randomImg = ImageTk.PhotoImage(randomOG)
    randomBtn = tk.Button(btnFrame, image=randomImg, command=randomBoard)
    randomBtn.grid(row=0, column=4)


    # More Entries
    eFrame2 = tk.Frame(innerFrame, bg='#505050')
    eFrame2.pack()

    scaleList = ["Pentatonic"]
    # GET string distance
    distSelect = tk.StringVar(eFrame2, 0)
    distHeader = tk.Label(eFrame2, text="String:", 
        bg=foreColor, fg='#FFFFFF')
    distRad1 = tk.Radiobutton(eFrame2, text="Scale:",
        bg=foreColor, fg='#FFFFFF', selectcolor=backColor, command=chngDistSel,
        variable=distSelect, value=0)

    dScale = tk.StringVar() 
    dScaleBox = ttk.Combobox(eFrame2, width=10, textvariable=dScale,
        values=scaleList)
    dScaleBox.bind('<<ComboboxSelected>>', setDistScale)
    dScaleBox.current(0)

    strDist = tk.StringVar(eFrame2, 2)
    distRad2 = tk.Radiobutton(eFrame2, text="Interval:",
        bg=foreColor, fg='#FFFFFF', selectcolor=backColor, command=chngDistSel,
        variable=distSelect, value=1)
    distField = tk.Entry(eFrame2, width=5,
        bg=foreColor, fg='#FFFFFF')
    distField.insert(0, "2")
    distField.config(state='disabled')
    distBuffer = tk.Label(eFrame2, text=" | ", 
        bg=foreColor, fg='#FFFFFF')
    distLabel = tk.Label(eFrame2, textvariable=strDist, 
        bg=foreColor, fg='#FFFFFF')

    distHeader.grid(row=0, column=1)
    distRad1.grid(row=1, column=0, sticky='w')
    dScaleBox.grid(row=1, column=1, columnspan=3)
    distRad2.grid(row=2, column=0, sticky='w')
    distField.grid(row=2, column=1)
    distBuffer.grid(row=2, column=2)
    distLabel.grid(row=2, column=3)
    distField.bind("<Return>", submitDist)

    # GET fret distance
    fretSelect = tk.StringVar(eFrame2, 1)
    fretHeader = tk.Label(eFrame2, text="Fret:", 
        bg=foreColor, fg='#FFFFFF')
    fretRad1 = tk.Radiobutton(eFrame2, text="Scale:",
        bg=foreColor, fg='#FFFFFF', selectcolor=backColor, command=chngFretSel,
        variable=fretSelect, value=0)

    fScale = tk.StringVar() 
    fScaleBox = ttk.Combobox(eFrame2, width=10, textvariable=fScale,
        values=scaleList)
    fScaleBox.config(state='disabled')
    fScaleBox.bind('<<ComboboxSelected>>', setFretScale)
    fScaleBox.current(0)

    strFret = tk.StringVar(eFrame2, 0)
    fretRad2 = tk.Radiobutton(eFrame2, text="Interval:",
        bg=foreColor, fg='#FFFFFF', selectcolor=backColor, command=chngFretSel,
        variable=fretSelect, value=1)
    fretField = tk.Entry(eFrame2, width=5,
        bg=foreColor, fg='#FFFFFF')
    fretField.insert(0, "0")
    fretBuffer = tk.Label(eFrame2, text=" | ", 
        bg=foreColor, fg='#FFFFFF')
    fretLabel = tk.Label(eFrame2, textvariable=strFret, 
        bg=foreColor, fg='#FFFFFF')

    tk.Label(eFrame2, text="Buffer", bg=foreColor, fg=foreColor).grid(row=0, column=6)
    fretHeader.grid(row=0, column=8)
    fretRad1.grid(row=1, column=7, sticky='w')
    fScaleBox.grid(row=1, column=8, columnspan=3)
    fretRad2.grid(row=2, column=7, sticky='w')
    fretField.grid(row=2, column=8)
    fretBuffer.grid(row=2, column=9)
    fretLabel.grid(row=2, column=10)
    fretField.bind("<Return>", submitFret)


    
    root.mainloop()