import Tkinter, tkMessageBox, os, math, sys
from Tkinter import *
from tkMessageBox import *

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

        self.wallFlag = StringVar()
        self.contents1 = StringVar()
        self.contents2 = StringVar()
        self.contents3 = StringVar()
        self.contents4 = StringVar()
        self.contents1.set("Point 1")
        self.contents2.set("Point 2")
        self.contents3.set("InputFileName.txt")
        self.contents4.set("OutputFileName.txt")       
        self.wallFlag.set(" 'N/W' or 'S/E' Profile?")

        
        self.entrythingy = Entry()
        self.entrythingy.pack({"side": "left"})
        self.entrythingy["textvariable"] = self.contents1
        
        self.entrythingy2 = Entry()
        self.entrythingy2.pack({"side": "left"})
        self.entrythingy2["textvariable"] = self.contents2

        self.entrythingy3 = Entry()
        self.entrythingy3.pack({"side": "left"})
        self.entrythingy3["textvariable"] = self.contents3

        self.entrythingy4 = Entry()
        self.entrythingy4.pack({"side": "left"})
        self.entrythingy4["textvariable"] = self.contents4

        self.entrythingy4 = Entry()
        self.entrythingy4.pack({"side": "left"})
        self.entrythingy4["textvariable"] = self.wallFlag
        
        self.input1 = Button(self)
        self.input1["fg"] = "black"
        self.input1["text"] = "Calculate"
        self.input1.pack({"side": "right"})
        self.input1["command"] = self.store_contents

        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.pack({"side": "right"})
        
    def store_contents(self):
        userPointInput1 = self.contents1.get()
        userPointInput2 = self.contents2.get()
        userFileNameInput = self.contents3.get()
        userFileNameOutput = self.contents4.get()
        print self.wallFlag.get()
        SEflag = self.wallFlag.get()
        print SEflag
        parsedPoints = parse_xyz_file(userFileNameInput, self.contents1.get(),self.contents2.get())
        hzpoints = setPerspectiveLine(parsedPoints, SEflag)
        hzpointsfile = open("C:\\Users\\vonpe\\Desktop\\bat stuff\\" + self.contents4.get(), 'w')
        hzpointsfile.writelines(hzpoints)
        hzpointsfile.close()




def getLineLength( (x,y,z), lineCount, yint, SEflag3 ): # gets length of line drawn from (0,y-int) to the argument coordinate
    hypotenuse = math.sqrt( (x*x)+ (y-yint)*(y-yint) )
    if SEflag3 == "S/E":
        newPoint = str(lineCount) + "," + str(hypotenuse - (2 * hypotenuse)) + "," + str(z) + "\n"
    else:
        newPoint = str(lineCount) + "," + str(hypotenuse) + "," + str(z) + "\n"
    return newPoint

def getLineLengthTest( (x1,y1,z1), (x2, y2, z2) ): # gets length of line drawn from (0,0) to the argument coordinate
    hypotenuse = math.sqrt( ((x2-x1) * (x2-x1))+ ((y2-y1) * (y2-y1)) )
    return hypotenuse

def setPerspectiveLine(pointList, SEflag2):
    #store origin and endpoints x and y values
    x1 = pointList[0][0]
    y1 = pointList[0][1]
    x2 = pointList[len(pointList)-1][0]
    y2 = pointList[len(pointList)-1][1]

    #create list to store corrected horizontal/elevation values
    hzpointsList = []
    #gets equation of argument line segment
    #y = mx+b
    #y = 1(0) + b : y=b
    #m = y2-y1 \ x2 -x1
    #b = y-mx
    m1 = (y2 - y1) / (x2 - x1)
    b1 = (y1 - (m1 * x1))

    lineCount = 1
    for coordinate in pointList:

        intersectionPoint = findInverseSlopeIntercept((coordinate[0],coordinate[1],coordinate[2]), m1, b1)
        hzpointsList.append(getLineLength(intersectionPoint, lineCount, b1, SEflag2))
        lineCount = lineCount + 1       

    return hzpointsList
    

def findInverseSlopeIntercept((x, y, z), slope, intercept):
    #finds the inverse line of setPerspectiveLine() based on list of coordinates
    #and returns the perpendicular intersecting coordinate for each point off the line
    #inverse: y = -1(1/m)x +b
    #x = (y-b) / m
    #y = mx + b
    #y = [-(m2/m1)b1 + b2]  /  [ 1 - (m2 / m1) ]
    slope2 = -1 * (1/slope)
    intercept2 = (y - (slope2 * x))


    #find y of perpendicular intersecting point
    intersecty = ( (-1 * (slope2 / slope) * intercept) + intercept2) / (1 - (slope2 / slope))

    intersectx = (intercept2 - intercept) / (slope2 - slope)

    return (intersectx, intersecty, z)



def parse_xyz_file(input_fileName, userInputPoint1, userInputPoint2):   
    #read file
    path = "C:\\Users\\vonpe\\Desktop\\bat stuff\\" + input_fileName
    old_xyzpoints = open( path )
    #store as list variable
    xyzpoints = old_xyzpoints.readlines()
    old_xyzpoints.close() 


    #parse file and store individual values as a (x,y,z) set
    #in loop, and return a parsed float list of specified points within the
    #range given in the argument p1-p2
    new_xyzpoints = []
    x = []
    y = []
    z = []
    pnum = ""
    stringX = ""
    stringY = ""
    stringZ = ""
    commaCount = 0
    userFlag = False
    flag = False

    for line in xyzpoints:
        for char in line:
            if char != "," and commaCount == 0:
                pnum = pnum + char
            elif char == "," and commaCount == 0:
                #test num string for user input
                if pnum == userInputPoint1:
                    commaCount = commaCount + 1
                    userFlag = True
                    pnum = ""
                elif pnum != userInputPoint1 and userFlag == False:
                    pnum = ""
                    break
                elif pnum == str(int(userInputPoint2) + 1):
                    pnum = ""
                    commaCount = 0
                    userFlag = False
                    break
                elif pnum != userInputPoint1 and userFlag == True:
                    pnum = ""
                    commaCount = commaCount + 1

                
            elif char != "," and commaCount == 1:
                x.append(char)
            elif char != "," and commaCount == 2:
                y.append(char)
            elif char != "," and commaCount == 3:
                z.append(char)
            elif commaCount == 4:
                flag = True
                commaCount = 0
                break       
            elif char == ",":
                commaCount = commaCount + 1
        if flag == True:
            for char2 in x:
                stringX = stringX + char2
            for char2 in y:
                stringY = stringY + char2       
            for char2 in z:
                stringZ = stringZ + char2     
            #print stringX + " " + stringY + " " + stringZ
            new_xyzpoints.append( (float(stringX), float(stringY), float(stringZ)) )
            x[:] = []
            y[:] = []
            z[:] = []
            stringX = ""
            stringY = ""
            stringZ = ""
            flag = False

    return new_xyzpoints
        
####### END def parse_xyz_file() ################

userPointInput1 = ""
userPointInput2 = ""
userFileNameInput = ""
userFileNameOutput = ""


root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
