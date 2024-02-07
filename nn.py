import argparse
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np

SEED = 12345

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


def generateTrainingDataset():
    colors = [0,1,2,3]
    generatingFunctions = [generateRed, generateGreen, generateBlue, generatePurple]

    points = np.empty(40000, dtype=('int', 2))
    labels = np.empty(40000, dtype='int')

    for i in range(40000):
        labelIndex = i % 4

        x, y = generatingFunctions[labelIndex]()
        label = colors[labelIndex]

        points[i] = x,y
        labels[i] = label


    return points, labels


def buildModel():
    model = keras.models.Sequential()

    model.add(keras.layers.Dense(16, input_shape=(2,), activation='relu'))
    model.add(keras.layers.Dense(32, activation='relu'))
    model.add(keras.layers.Dense(64, activation='relu'))
    model.add(keras.layers.Dense(32, activation='relu'))
    model.add(keras.layers.Dense(4, activation='softmax'))

    model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=['accuracy'])

    return model


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--seed", type=int)
    parser.add_argument("-f", "--fill", action=argparse.BooleanOptionalAction)
    parser.add_argument("--save", action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    if args.seed:
        SEED = args.seed

    print(f"SEED = {SEED}")

    #zadefinovany rovnaky seed kvoli porovnavaniu uspesnosti pre rozne k pri k-NN algoritme
    np.random.seed(SEED)


    train_data, train_labels = generateTrainingDataset()

    model = buildModel()
    model.fit(train_data, train_labels, epochs=3)



    points = np.array([(x, y) for x in range(-5000, 5000, 10) for y in range(-5000, 5000, 10)])

    predictions = model.predict(points, batch_size=64)

    colors = ['red', 'green', 'blue', 'purple']
    predicted_colors = [colors[np.argmax(prediction)] for prediction in predictions]

    x_coords, y_coords = zip(*points)
    plt.scatter(x_coords, y_coords, color=predicted_colors, marker='o', s=1)


    #model.summary()

    if args.save:
        plt.axis('off')
        plt.savefig(f"{SEED}_NN.png", bbox_inches="tight", pad_inches=0)
    else:
        plt.show()

