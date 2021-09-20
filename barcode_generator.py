import cv2
import numpy
import os
import pandas

# Locates the folder containing the dataset of images
folders = os.listdir('./MNIST_DS')

pandas.set_option("display.max_rows", None, "display.max_columns", None)


def sharpenImage(img):
    # Sharpens the image by removing array values of less than 20

    for row in range(len(img)):
        for column in range(len(img[0])):
            if img[row][column] < 20:
               img[row][column] = 0


def projectionArrays(p1, p2, p3, p4, img):
    # Creates the projections p1, p2, p3, and p4 when given the array of the image

    # Projection 1 - 0 degrees
    rowsum = 0
    for row in range(len(img)):
        for column in range(len(img[0])):
            rowsum += img[row][column]

        p1.append(rowsum)
        rowsum = 0

    # Projection 2 - 45 degrees
    for i in range(len(img)):
        p2.append(numpy.trace(img, offset=1+i-len(img)))

    for i in range(1, len(img)):
        p2.append(numpy.trace(img, offset=i))

    # Projection 3 - 90 degrees
    colsum = 0
    for column in range(len(img[0])):
        for row in range(len(img)):
            colsum += img[row][column]

        p3.append(colsum)
        colsum = 0

    # Projection 4 - 135 degrees
    flipimg = numpy.fliplr(img) # flips the image on vertical axis and finds the trace
    for i in range(len(img)):
        p4.append(numpy.trace(flipimg, offset=len(img)-1-i))
    for i in range(1, len(img)):
        p4.append(numpy.trace(flipimg, offset=0-i))


def calculateThreshold(projection):
    # Calculates the threshold by taking the sum of the projection array
    # and dividing it by the length of the array to get the average

    projection_sum = numpy.sum(projection)
    projection_average = projection_sum / len(projection)

    return projection_average


def generateCodeFragment(projection, threshold):
    # Generates a binary code fragment for the projection angle and its respective threshold

    codeFragment = []


    for i in range(len(projection)):
        if projection[i] < threshold:
            codeFragment.append(0) # if the projection segment is less than threshold then append 0
        else:
            codeFragment.append(1) # otherwise append 1
    return codeFragment


def concatenateFragments(fragment1, fragment2, fragment3, fragment4):
    # Combines the 4 code fragments into one large binary barcode

    RBC = numpy.concatenate([fragment1, fragment2, fragment3, fragment4])
    return RBC


def createBarcodeDataframe():
    # Main function that calls and creates and exports the dataframe to a .csv file

    data = []

    for i in range(len(folders)):
        imageName = os.listdir(f'./MNIST_DS/{i}')

        for x in range(len(imageName)):
            img = cv2.imread(f'./MNIST_DS/{i}/{imageName[x]}', 0)
            img = numpy.array(img)

            p1 = []
            p2 = []
            p3 = []
            p4 = []

            sharpenImage(img)
            projectionArrays(p1, p2, p3, p4, img)

            # The following threshold multipliers were found to maximize the retrieval accuracy
            th_p1 = calculateThreshold(p1) * 1.4
            th_p2 = calculateThreshold(p2) * 1.5
            th_p3 = calculateThreshold(p3) * 2.5
            th_p4 = calculateThreshold(p4) * 1.5

            c1 = generateCodeFragment(p1, th_p1)
            c2 = generateCodeFragment(p2, th_p2)
            c3 = generateCodeFragment(p3, th_p3)
            c4 = generateCodeFragment(p4, th_p4)

            barcode = concatenateFragments(c1, c2, c3, c4)

            data.append([i, imageName[x], barcode])



    df = pandas.DataFrame(data, columns=['Integer', 'Name', 'Barcode'])


    return df


dataframe = createBarcodeDataframe()
dataframe.to_csv('data.csv')

print(dataframe)
