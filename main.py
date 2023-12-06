import numpy as np
import matplotlib.pyplot as plt
import argparse

from collections import Counter

import kdtree
from point import Point


#set sluzi na hladaniu duplikatov
points = set()

#k-d tree sluzi na hladanie k-NN
kd_tree = kdtree.KDNode

remainingPoints = list()


NUMBER_OF_POINTS = 40000
SEED = 12345
K = 1

#zadefinovany rovnaky seed kvoli porovnavaniu uspesnosti pre rozne k pri k-NN algoritme
np.random.seed(SEED)

#funkcie na generaciu bodov pre jednotlive farby
def generateRed():
    chance = np.random.randint(1, 101)

    if chance == 1:
        x = np.random.randint(-5000, 5001)
        y = np.random.randint(-5000, 5001) 

    else:
        x = np.random.randint(-5000, 501)
        y = np.random.randint(-5000, 501)

    return [x, y]

def generateGreen():
    chance = np.random.randint(1, 101)

    if chance == 1:
        x = np.random.randint(-5000, 5001)
        y = np.random.randint(-5000, 5001) 

    else:
        x = np.random.randint(-500, 5001)
        y = np.random.randint(-5000, 501)

    return [x, y]

def generateBlue():
    chance = np.random.randint(1, 101)

    if chance == 1:
        x = np.random.randint(-5000, 5001)
        y = np.random.randint(-5000, 5001) 
    
    else:
        x = np.random.randint(-5000, 501)
        y = np.random.randint(-500, 5001)

    return [x, y]

def generatePurple():
    chance = np.random.randint(1, 101)

    if chance == 1:
        x = np.random.randint(-5000, 5001)
        y = np.random.randint(-5000, 5001) 
    
    else:
        x = np.random.randint(-500, 5001)
        y = np.random.randint(-500, 5001)

    return [x, y]


def generatePoints():
    global points, kd_tree

    colors = ["red", "green", "blue", "purple"]
    generatingFunctions = [generateRed, generateGreen, generateBlue, generatePurple]

    colorIndex = 0

    succesful = 0


    while len(points) != NUMBER_OF_POINTS + 20:

        color = colors[colorIndex]
        
        #generacia bodu, podla farby
        x,y = generatingFunctions[colorIndex]()

        #postupne iteruje cez farby
        colorIndex += 1

        if colorIndex > 3:
            colorIndex = 0
            
    
        point = Point(x, y, color)

        if point not in points:
            if color == clasify(point):
                succesful += 1

            points.add(point)
            kd_tree.add(point)


    successRate = succesful / NUMBER_OF_POINTS * 100

    return successRate




def clasify(newPoint: Point) -> str:
    global points
    
    #najde k-NN v k-d tree
    nearest_points = kd_tree.search_knn(newPoint, K)

    #upravi data, aby to bol list farieb
    nearest_points = list(map(lambda pointDistTuple: pointDistTuple[0].data.color, nearest_points))

    #ak je K > 1, tak zisti, ktora farba je najcastejsie
    newPoint.color = Counter(nearest_points).most_common()[0][0]


    return newPoint.color
    

    

def fillPlot():

    global remainingPoints
    blankColor = "blank"


    remainingPoints = [Point(x, y, clasify(Point(x, y, blankColor))) for x in range(-5000, 5000, 10) for y in range(-5000, 5000, 10)]





def readStartingPoints():
    global points

    with open("starting_points.txt", "r") as f:
        lines = f.readlines()

    formatedLines = []
    for line in lines:
        line = line.split(', ')

        # Convert the values to integers
        formatedLines.append([int(value) for value in line])

    red, green, blue, purple = formatedLines


    red = [Point(red[i], red[i + 1], "red") for i in range(0, len(red), 2)]
    green = [Point(green[i], green[i + 1], "green") for i in range(0, len(green), 2)]
    blue = [Point(blue[i], blue[i + 1], "blue") for i in range(0, len(blue), 2)]
    purple = [Point(purple[i], purple[i + 1], "purple") for i in range(0, len(purple), 2)]


    points = set(red + green + blue + purple)



if __name__ == "__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument("-k", type=int)
    parser.add_argument("-s", "--seed", type=int)
    parser.add_argument("-f", "--fill", action=argparse.BooleanOptionalAction)
    parser.add_argument("--save", action=argparse.BooleanOptionalAction)


    args = parser.parse_args()

    if args.k:
        K = args.k

    if args.seed:
        SEED = args.seed

    print(f"K = {K}\tSEED = {SEED}")




    #nacitanie pociatocnych bodov
    readStartingPoints()


    # vytvorenie k-d tree z pociatocnych bodov
    kd_tree = kdtree.create(list(points))

    #generacia + klasifikacia dalsich 40000 bodov
    successRate = generatePoints()

    print("Initial classification was complete")
    print(f"Success rate for classificator is {successRate:.2f} %")


    #vyfarbenie celej plochy
    if args.fill:
        print("Waiting for remaining points to be classified")
        fillPlot()


    print("Classification was complete, waiting for points to be plotted")
    

    #vizualizacia bodov
    plt.rcParams['toolbar'] = 'None'
    
    plt.xlim(-5000, 5000)
    plt.ylim(-5000, 5000)

    plt.scatter([point.x for point in points], [point.y for point in points], color=[point.color for point in points], marker='o', s=1)
    plt.scatter([point.x for point in remainingPoints], [point.y for point in remainingPoints], color=[point.color for point in remainingPoints], marker='o', s=5)

    plt.xlabel(f"Success rate is {successRate:.2f} %", fontsize = 15)


    if args.save:
        plt.savefig(f"{SEED}_{K}.png")
    else:
        plt.show()