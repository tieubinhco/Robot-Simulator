import Controllers.JoystickController
import pygame
import math

class Point:
    def __init__(self, x,y ):
        self.x = x
        self.y = y
    def dot(self, point):
        return self.x * point.x + self.y * point.y
    def mag(self):
        return (self.x**2 + self.y**2)**0.5
    def normalize(self):
        return Point(self.x/self.mag(), self.y/self.mag())
    def __sub__(self, point):
        return Point(self.x - point.x, self.y - point.y)
    def __add__(self, point):
        return Point(self.x + point.x, self.y + point.y)
    def __str__(self):
        return str(self.x) + ", " + str(self.y)
    def __mul__(self, other):
        return Point(self.x * other, self.y * other)
    def __truediv__(self, other):
        return Point(self.x/other, self.y/other)
    def __abs__(self):
        return Point(abs(self.x), abs(self.y))

    __rmul__ = __mul__


class PurePersuitController:
    def __init__(self, lookAhead):
        self.points = []
        self.lookAhead = lookAhead
        self.lookAheadPoint = Point(0, 0)
        self.curvature = 1
        self.maxVelo = None
        self.jsTest = Controllers.JoystickController.JoystickController()
        self.loc = None
        self.side = 1
        self.robotTheta = 0
        return

    def addPoint(self, x, y):
        self.points.append(Point(x, y))

    def calculateIntersect(self, loc, start, end): #calculate using parametric subsitution to find intersections https://stackoverflow.com/questions/1073336/circle-line-segment-collision-detection-algorithm/1084899#1084899
        E = start
        L = end
        C = loc
        r = self.lookAhead
        d = L - E
        f = E - C

        a = d.dot(d)
        b = 2 * f.dot(d)
        c = f.dot(f) - r ** 2
        discriminant = b ** 2 - 4 * a * c

        if (discriminant < 0):
            return None
        else:  # limit discriminant somehow?
            discriminant = discriminant ** 0.5
            t1 = (-b - discriminant) / (2 * a)
            t2 = (-b + discriminant) / (2 * a)

            canidates = {}
            if (t1 >= 0 and t1 <= 1.0):
                canidates[t1] = E + d * t1
            if (t2 >= 0 and t2 <= 1.0):
                canidates[t2] = E + d * t2

            if (len(canidates.keys()) > 0):
                intersect = canidates[max(canidates.keys())]
                return intersect
            else:
                return None

    def getLookAheadPoint(self, loc):
        self.loc = loc
        # get closest path point
        distance = float("inf")
        closest = 0
        for i in range(len(self.points)-1, -1, -1):
            d = ((loc.x-self.points[i].x)**2+(loc.y-self.points[i].y)**2)**0.5
            if(d < distance):
                closest = i
                distance = d

        #print(str(self.points[closest]))

        E = self.points[closest]
        L = None
        try:
            L = self.points[closest+1]
        except:
            L = self.points[closest] + (self.points[closest]-self.points[closest-1]).normalize() * self.lookAhead


        p = self.calculateIntersect(loc, E, L)
        #print(self.lookAheadPoint)
        if(p == None):
            p = self.calculateIntersect(loc, self.points[closest-1], self.points[closest])
            if(p != None):
                self.lookAheadPoint = p
        else:
            self.lookAheadPoint = p

        #alternatively, get lookahead by picking closest path point, then going one lookahead up that segment

    def calculateArc(self, p):
        try:
            r = (self.lookAhead**2)/(2*p.x)
            self.curvature = 1/r

            #get side
            self.side = math.sin(self.robotTheta) * (self.lookAheadPoint.x - self.loc.x) - math.cos(self.robotTheta) * (self.lookAheadPoint.y - self.loc.y)

        except:
            return 0
        return self.curvature

    def removePassedPoints(self):
        return

    def smoothPath(self):
        #for i in range(len(self.points)):
        return

    def update(self, pos): #optional param sim
        loc = Point(pos[0], pos[1])
        self.robotTheta = pos[2]
        self.getLookAheadPoint(loc)
        self.calculateArc(self.lookAheadPoint-loc)
        #print(self.curvature)
        return self.jsTest.update()

    def visualDebug(self, g):

        for i in range(len(self.points)-1):
            p1 = g.translatePoint(self.points[i])
            p2 = g.translatePoint(self.points[i+1])
            pygame.draw.line(g.screen, (0, 255, 0), p1, p2, 4)

        pygame.draw.circle(g.screen, (255, 0, 0), g.translatePoint(self.loc), int(g.translateDim(self.lookAhead, 0)[0]), 4)
        pygame.draw.circle(g.screen, (0, 255, 255), g.translatePoint(self.lookAheadPoint), 4, 0)

        #calculate center of desired travel arc
        midPoint = (self.lookAheadPoint-self.loc)/2
        perpLen = ((1/self.curvature)**2 - midPoint.mag()**2) ** 0.5
        perpVec = (Point(-midPoint.y, midPoint.x)/midPoint.mag()) * perpLen
        if(self.side < 0):
            perpVec *= -1
        center = (self.loc+midPoint) - perpVec
        #pygame.draw.line(g.screen, (0, 255, 0), g.translatePoint(self.loc), g.translatePoint(self.loc+midPoint), 4)

        #pygame.draw.line(g.screen, (0, 255, 0), g.translatePoint(self.loc+midPoint), g.translatePoint(center), 4)
        #pygame.draw.circle(g.screen, (0, 255, 255), g.translatePoint(center), int(g.translateDim(abs(1/self.curvature), 0)[0]), 2)

        try:
            robotAngle = 180 / math.pi * math.atan2(self.loc.y - center.y, self.loc.x - center.x)
            lookAheadPointAngle = 180 / math.pi * math.atan2(self.lookAheadPoint.y - center.y, self.lookAheadPoint.x - center.x)
            if (self.side <= 0):
                lookAheadPointAngle = lookAheadPointAngle + robotAngle
                robotAngle = lookAheadPointAngle - robotAngle
                lookAheadPointAngle = lookAheadPointAngle - robotAngle

            g.drawCircleArc((255, 255, 0), g.translatePoint(center), int(g.translateDim(abs(1/self.curvature), 0)[0]), lookAheadPointAngle, robotAngle, 4)
        except:
            return
        return
