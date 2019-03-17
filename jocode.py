import joserial
import time
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    portName = '/dev/ttyACM0'
    baudRate = 115200

    nbMeasure = 10
    nbSample = 100
    waitTime = 1000
    pwm = 220

    # Define the format of the structure of data sent
    structFormatConfig = ['uint8', 'uint16', 'uint16', 'uint8']
    structFormatMeasure = ['uint32', 'uint32', 'float']

    timestamps = np.zeros((nbMeasure, nbSample))
    positions = np.zeros((nbMeasure, nbSample))
    speeds = np.zeros((nbMeasure, nbSample))
    test = joserial.Connection()

    # Wait for the arduino to initilize
    time.sleep(2)
    # Write some data to the arduino
    test.writeData(structFormatConfig, [nbMeasure, nbSample, waitTime, pwm])
    print(test.readData(structFormatConfig))
    for i in range(nbMeasure):
        print(i+1, '/', nbMeasure)
        for j in range(nbSample):
            timestamps[i, j], positions[i, j], speeds[i, j] = test.readData(structFormatMeasure)

    speed = np.mean(speeds, axis=0)
    t = [i*0.01 for i in range(0, len(speed))]

    plt.plot(t, speed)
    plt.xlabel("Time in seconds")
    plt.ylabel("Speed in steps/seconds")
    plt.show()
