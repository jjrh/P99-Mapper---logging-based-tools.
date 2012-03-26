import pygame


import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((800,600))

screen.fill((255,255,255))
pygame.display.update()

mapp = []
pPoints = []
p2Points = []
otherPoints = []    
fillSurf = pygame.Surface((800,600))
fillSurf.fill((255,255,255))
backSurf = pygame.Surface((10000,10000))
        
                

class MAP:
        def __init__(self, filename):
                self.mapFull     = []	# The entire map raw.
                self.L_Points    = []	# L type (line points)
                self.P_Points    = []	# P type points
                self.Grid_Points = []	# grid lines, special in that they create a grid when plotted.
                
                self.filename = filename

                self.surface = pygame.Surface((1,1))	# set to 1,1 as default. More there to say this is a surface

        def load(self):
                try:
                        f = open(filename)
                        fail = 0
                        otherFlag = False # when we encounter something unexpected
                        LargestX = 0	# these two are the longest lines, we use this to create a surface that is exactly the right size.
                        LargestY = 0
                        LargestZ = 0	# probably don't actually need this, but might as well calculate it anyways.

                        LargestNegX = 0
                        LargestNegY = 0
                        for line in f.readLines():
                                # get rid of the \n and \r stuff that is in the text file. 
                                processedLine = line.rstrip('\n')
                                processedLine = processedLine.rstrip('\r')
                                processedLine = processedLine.split(',')
                                # we found a line type. 
                                if('L' in processedLine[0]):
                                        fX1 = float(processedLine[1])
                                        fY1 = float(processedLine[2])
                                        fZ1 = float(processedLine[3])
                                        
                                        fX2 = float(processedLine[4])
                                        fY2 = float(processedLine[5])
                                        fZ2 = float(processedLine[6])

                                        # These checks have to do with creating a perfect sized surface.
                                        # we need to find the upper X,Y bounds for when we create the surface. 
                                        if fX1 > LargestX:
                                                LargestX = fX1
                                        if fX2 > LargestX:
                                                LargestX = fX2
                                                
                                        if fY1 > LargestY:
                                                LargestY = fY2
                                        if fY2 > LargestY:
                                                LargestY = fY2
                                                
                                        if fZ1 > LargestZ:
                                                LargestZ = fZ1
                                        if fZ2 > LargestZ:
                                                LargestZ = fZ2

                                        # I should explain why we are doing this:
                                        #	When we are plotting, we need to plot positive numbers.
                                        #	Thus, we need to find what the largest negative value is, then when we draw the map,
                                        #	we add this to what ever we are drawing. 
                                        if fX1 < 0 and fX1*-1 > LargestNegX:
                                                LargestNegX = fX1*-1
                                        if fX2 < 0 and fX2*-1 > LargestNegX:
                                                LargestNegX = fX2*-1

                                        if fY1 < 0 and fY1*-1 > LargestNegY:
                                                LargestNegY = fY1*-1
                                        if fY2 < 0 and fY2*-1 > LargestNegY:
                                                LargestNegY = fY1*-1
                                        
                                        # Create a dictionary and append it to the L_Points list.
                                        vectorLine = {'X1': fX1, 'Y1': fY1, 'Z1': fZ1 , 'X2': fX2, 'Y2': fY2, 'Z2': fZ2}
                                        
                                        self.L_Points.append(vectorLine)

                                
                                                                                                                               
                                                                                                                                                            
                                                                                                                                                              
                                                                                                                                                                                            
                                        
                                        
                                
                except:
                        print "Error with load, most likely a bad filename"
        
                

                

f = open('southro.txt')
fail=0


otherFlag = False
for line in f.readlines():
        l = line.rstrip('\n')
        l = l.rstrip('\r')   
        pt = l[1:].split(',')
        l = l.split(',')
        if( 'L' in l[0]):
                if otherFlag == False:
                        mapp.append(pt)
                else:
                        p2Points.append(pt)
        elif('P' in l[0]):
                otherFlag = True
                pPoints.append(pt)
        else:
                otherFlag = True
                otherPoints.append(l)
                print l[0]
                
#        print pt
        
#        print type(pt[0]),pt[1]
largest_point = 0
for line in mapp:
        for p in line:
                try:
                        if float(p) < 0 and float(p)*-1 > largest_point:
                                largest_point = float(p)*-1
                except:
                        pass
                            
def plotCoreMap(ratio):
        backSurf.fill((255,255,255))
        fail = 0
        for pt in mapp:
                try:
                        
                        x1 = float(pt[0])
                        y1 = float(pt[1])
                        x2 = float(pt[3])
                        y2 = float(pt[4])
                        x1=x1+largest_point
                        y1=y1+largest_point
                        x2 = x2+largest_point
                        y2 = y2+largest_point
                        x1 = x1/ratio
                        x2 = x2/ratio
                        y1 = y1/ratio
                        y2 = y2/ratio
                 
                
                 #       print x1,y1,x2,y2
                        pygame.draw.line(backSurf,(255,0,0),(x1,y1),(x2,y2)) 

                except:
                        fail += 1       

print "failed:", fail
print "largest point:",largest_point





X = 0
Y = 0
EXIT = False
RATIO = 0
MOVE_SPEED = 10


plotCoreMap(RATIO)
screen.blit(fillSurf,(0,0))
screen.blit(backSurf,(X,Y))
pygame.display.flip()
clock = pygame.time.Clock()




while not EXIT:
        clock.tick(60)
        for event in pygame.event.get():
                if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                                EXIT=True
                                
                        elif event.key == K_UP:
                                Y = Y-MOVE_SPEED*RATIO
                        elif event.key == K_DOWN:
                                Y = Y+MOVE_SPEED*RATIO
                        elif event.key == K_LEFT:
                                X = X+MOVE_SPEED*RATIO
                        elif event.key == K_RIGHT:
                                X = X-MOVE_SPEED*RATIO
                        elif event.key == K_q:
                                RATIO = RATIO + 1
                                plotCoreMap(RATIO)
                        elif event.key == K_a:
                                if RATIO > 0:
                                        RATIO = RATIO - 1
                                plotCoreMap(RATIO)
                        else:
                                pass
        
                        screen.blit(fillSurf,(0,0))
                        screen.blit(backSurf,(X,Y))
                        pygame.display.flip()


        
        



