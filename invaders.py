from Tkinter import *

def mousePressed(event):
    redrawAll()

def keyPressed(event):
    if (event.char == "t"):
        doTimerFired()
    elif (event.keysym == "Left"):
        movePaddleLeft()
    elif (event.keysym == "Right"):
        movePaddleRight()
    elif (event.keysym == "space"):
        fireMissile()
    redrawAll()

def movePaddleLeft():
    canvas.data.paddleLeft -= canvas.data.paddleSpeed
    if (canvas.data.paddleLeft < 0):
        canvas.data.paddleLeft = 0

def movePaddleRight():
    canvas.data.paddleLeft += canvas.data.paddleSpeed
    maxLeft = canvas.data.canvasWidth - canvas.data.paddleWidth
    if (canvas.data.paddleLeft > maxLeft):
        canvas.data.paddleLeft = maxLeft

def fireMissile():
    paddleCx = canvas.data.paddleLeft + canvas.data.paddleWidth/2
    canvas.data.missileLeft = paddleCx - canvas.data.missileWidth/2
    canvas.data.missileTop = canvas.data.paddleTop - canvas.data.missileHeight

def doTimerFired():
    moveMissile()
    moveInvaders()

def moveMissile():
    if (canvas.data.missileTop >= 0):
        canvas.data.missileTop -= canvas.data.missileSpeed
    # now check for any collisions with invaders
    for i in xrange(len(canvas.data.invaders)):
        (cx, cy) = canvas.data.invaders[i]
        # find bounding box of missile and bounding box of invader
        # Note that we could do better, testing against the actual
        # circle of the invader rather than the bounding box,
        # but that's assigned on hw6, so we'll stick with bounding boxes here
        mx0 = canvas.data.missileLeft
        mx1 = mx0 + canvas.data.missileWidth
        my0 = canvas.data.missileTop
        my1 = my0 + canvas.data.missileHeight
        r = canvas.data.invaderRadius
        ix0 = cx - r
        ix1 = cx + r
        iy0 = cy - r
        iy1 = cy + r
        if (rectanglesIntersect(mx0, my0, mx1, my1,
                                ix0, iy0, ix1, iy1)):
            # the missile hit the invader!
            # so remove the invader and the missile and return
            canvas.data.invaders.pop(i)
            canvas.data.missileTop = -1
            return

def rectanglesIntersect(mx0, my0, mx1, my1,
                        ix0, iy0, ix1, iy1):
    return ((mx0 <= ix1) and (mx1 >= ix0) and
            (my0 <= iy1) and (my1 >= iy0))

def moveInvaders():
    # set the dx (change in x location)
    dx = canvas.data.invaderSpeed
    if (canvas.data.movingRight == False):
        dx = -dx
    # update the x locations of all invaders
    offBoard = False
    r = canvas.data.invaderRadius
    for i in xrange(len(canvas.data.invaders)):
        (cx,cy) = canvas.data.invaders[i]
        cx += dx
        canvas.data.invaders[i] = (cx,cy)
        if (((cx-r) < 0) or (cx+r > canvas.data.canvasWidth)):
            offBoard = True
    # update the y locations if necessary
    if (offBoard == True):
        canvas.data.movingRight = not canvas.data.movingRight
        dy = 10
        for i in xrange(len(canvas.data.invaders)):
            (cx,cy) = canvas.data.invaders[i]
            cy += dy
            canvas.data.invaders[i] = (cx,cy)

def timerFired():
    doTimerFired()
    redrawAll()
    delay = 25 # milliseconds
    canvas.after(delay, timerFired) # pause, then call timerFired again

def redrawAll():
    canvas.delete(ALL)
    drawInvaders()
    drawPaddle()
    drawMissile()

def drawMissile():
    if (canvas.data.missileTop >= 0):
        x0 = canvas.data.missileLeft
        x1 = x0 + canvas.data.missileWidth
        y0 = canvas.data.missileTop
        y1 = y0 + canvas.data.missileHeight
        canvas.create_rectangle(x0, y0, x1, y1, fill="red")

def drawPaddle():
    x0 = canvas.data.paddleLeft
    x1 = x0 + canvas.data.paddleWidth
    y0 = canvas.data.paddleTop
    y1 = y0 + canvas.data.paddleHeight
    canvas.create_rectangle(x0, y0, x1, y1, fill="blue")
    cannonHeight = canvas.data.paddleHeight/3
    cannonX = (x0 + x1)/2
    cannonY0 = y0 - cannonHeight
    cannonY1 = y0
    canvas.create_line(cannonX, cannonY0, cannonX, cannonY1, width=2)

def drawInvaders():
    r = canvas.data.invaderRadius
    for (cx,cy) in canvas.data.invaders:
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="orange")

def init():
    # set up the paddle
    canvas.data.paddleSpeed = 30
    canvas.data.paddleWidth = 40
    canvas.data.paddleLeft = canvas.data.canvasWidth/2 - canvas.data.paddleWidth/2
    canvas.data.paddleHeight = 15
    paddleMargin = 10
    canvas.data.paddleTop = canvas.data.canvasHeight - paddleMargin - canvas.data.paddleHeight
    # set up the missile
    canvas.data.missileSpeed = 10
    canvas.data.missileTop = -1 # no missile to start
    canvas.data.missileHeight = 10
    canvas.data.missileLeft = -1
    canvas.data.missileWidth = 3
    # set up the invaders
    canvas.data.invaderSpeed = 2
    canvas.data.invaderRadius = 10
    canvas.data.movingRight = True
    # we'll represent the invaders as a 1d list of
    # (x,y) pairs, representing the center of the invaders
    canvas.data.invaders = [ ]
    margin = 10
    r = canvas.data.invaderRadius
    invaderRows = 5
    invaderCols = 10
    colWidth = (canvas.data.canvasWidth*3/4 - 2*margin)/invaderCols
    rowHeight = (canvas.data.canvasHeight/2 - 2*margin)/invaderRows
    for row in xrange(invaderRows):
        for col in xrange(invaderCols):
            cx = margin + r + col * colWidth
            cy = margin + r + row * rowHeight
            canvas.data.invaders += [(cx, cy)]
    redrawAll()

########### copy-paste below here ###########

def run():
    # create the root and the canvas
    global canvas
    root = Tk()
    canvasWidth = 400
    canvasHeight = 400
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.canvasWidth = canvasWidth
    canvas.data.canvasHeight = canvasHeight
    init()
    # set up events
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    timerFired()
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()
