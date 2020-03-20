import math
import numpy as np
import random

def probabilisticHoughTransform(edgeImg, colCount, rowCount, rho, theta, threshold, lineLength, lineGap, linesMax):
    lines = []
    numAngleCells = round(np.pi / theta)
    numrho = round(((colCount + rowCount) * 2 + 1) / rho)

    accum = np.zeros(numAngleCells)
    accum2 = [None]*numAngleCells
    print(accum2)
    mask = np.zeros((rowCount , colCount))
    nonZeroPoints = []

    cosTable = []
    sinTable = []
    for targetIndex in range(0, numAngleCells):
        cosTable.append(math.cos(targetIndex * theta) / rho)
        sinTable.append(math.sin(targetIndex * theta) / rho)
    
    # stage 1. collect non-zero image points
    for y in range(0, rowCount):
        for x in range(0, colCount):
            if edgeImg[y][x]:
                nonZeroPoints.append([y, x])
                mask[y][x] = 1

    # Shuffle the array randomly
    random.shuffle(nonZeroPoints)    

    # stage 2. process all the points in random order
    for index in range(len(nonZeroPoints) - 1, -1, -1):
        print(index)
        row, col = nonZeroPoints[index]

        # check if it has been excluded already (i.e. belongs to some other line)
        if not mask[row][col]:
            continue

        maxVal = threshold - 1
        maxThetaIndex = 0
        # update accumulator, find the most probable line
        for thetaIndex in range(0, numAngleCells):
            rho = round(col * cosTable[thetaIndex] + row * sinTable[thetaIndex])
            rho += (numrho - 1) / 2
            print(rho)
            
            if not accum[thetaIndex]:
                accum[thetaIndex] = []
            
            if not accum[thetaIndex][rho]:
                accum[thetaIndex][rho] = 1
            else:
                accum[thetaIndex][rho] += 1

            val = accum[thetaIndex][rho]

            if maxVal < val:
                maxVal = val
                maxThetaIndex = thetaIndex

        # if it is too "weak" candidate, continue with another point
        if maxVal < threshold:
            continue

        # from the current point walk in each direction
        # along the found line and extract the line segment
        lineEnds = np.one(2)
        shift = 16
        a = -sinTable[maxThetaIndex]
        b = cosTable[maxThetaIndex]
        x0 = col
        y0 = row
        if abs(a) > abs(b):
            isWalkingX = True
            if a > 0:
                dx0 = 1
            else:
                dx0 = -1
            dy0 = round(b * (1 << shift) / abs(a))
            y0 = (y0 << shift) + (1 << (shift - 1))
        else:
            isWalkingX = False
            if b > 0:
                dy0 = 1
            else:
                dy0 = -1
            dx0 = round(a * (1 << shift) / abs(b))
            x0 = (x0 << shift) + (1 << (shift - 1))

        for k in range(0 ,2):
            gap = 0
            x = x0
            y = y0
            dx = dx0
            dy = dy0

            # Walk in the opposite direction for the second point
            if (k > 0):
                dx = -dx
                dy = -dy
          
            # walk along the line using fixed-point arithmetics,
            while True:
                x += dx
                y += dy
                if isWalkingX:
                    j1 = x
                    i1 = y >> shift
                else:
                    j1 = x >> shift
                    i1 = y

                # stop at the image border or in case of too big gap
                if j1 < 0 or j1 >= colCount or i1 < 0 or i1 >= rowCount: 
                    break

                # for each non-zero point:
                #    update line end,
                #    clear the mask element
                #    reset the gap
                if mask[i1 * colCount + j1]:
                    gap = 0
                    lineEnds[k] = [j1, i1] # x, y of kth point
                elif gap + 1 > lineGap:
                    break

        goodLine = abs(lineEnds[1][0] - lineEnds[0][0]) >= lineLength or abs(lineEnds[1][1] - lineEnds[0][1]) >= lineLength

        for k in range(0 ,2):
            x = x0
            y = y0
            dx = dx0
            dy = dy0

            if (k > 0):
                dx = -dx
                dy = -dy

        # walk along the line using fixed-point arithmetics,
        # stop at the image border or in case of too big gap
            while True:
                x += dx
                y += dy
                if isWalkingX:
                    j1 = x
                    i1 = y >> shift
                else:
                    j1 = x >> shift
                    i1 = y

                # for each non-zero point:
                #    update line end,
                #    clear the mask element
                #    reset the gap
                if mask[i1 * colCount + j1]: 
                    if goodLine:
                    # Since we decided on this line as authentic, remove this pixel's
                    # weights for all possible angles from the accumulator array
                        for thetaIndex in range(0 ,numAngleCells):
                            rho = round(j1 * cosTable[thetaIndex] + i1 * sinTable[thetaIndex])
                            rho += (numrho - 1) / 2
                            if accum[thetaIndex] and accum[thetaIndex][rho]:
                                accum[thetaIndex][rho] -= 1

                        mask[i1 * colCount + j1] = 0

                if i1 == lineEnds[k][1] and j1 == lineEnds[k][0]:
                    break

        if goodLine:
            # x1, y1, x2, y2
            lines.append([lineEnds[0][0], lineEnds[0][1], lineEnds[1][0], lineEnds[1][1]])
            if len(lines) >= linesMax:
                return lines

    return lines