import pandas

# imports the dataframe from the csv file
colnames = ['value', 'name', 'barcode']
data = pandas.read_csv('data.csv', names=colnames, skiprows=[0])

value = data.value.tolist()
names = data.name.tolist()
rawBarcode = data.barcode.tolist()

barcode = []

# for loop cleans up the barcodes by getting rid of anything that is not 0 or 1
for x in range(len(rawBarcode)):
    barcode.append(rawBarcode[x].replace('\n', '').replace('[', '').replace(']', '').replace(' ', ''))


def getIndex():
    # gets the index of the user input for image name

    nameInput = input('Please enter image name: ')
    filetype = '.jpg'
    imgHead = 'img_'
    if filetype not in nameInput:
        nameInput = nameInput + filetype

    if imgHead not in nameInput:
        nameInput = imgHead + nameInput

    for i in range(len(names)):
        if names[i] == nameInput:
            return i


def getDistance(index, indextwo):
    # calculates the hamming distance of two barcodes when given the respective indexes of both images

    distance = 0
    for i in range(len(barcode[index])):  # iterates through length of the barcode to compare
        if barcode[index][i] != barcode[indextwo][i]:
            distance += 1

    return distance


def getAccuracy(index, distancesSortedIndex, y):
    # calculates the accuracy of the top 10 most similar returned images
    counter = 0
    for i in range(1, y):
        if value[index] == value[distancesSortedIndex[i]]:
            counter += 1

    accuracy = counter/(y-1) * 100

    return accuracy


def search_algorithm(index):

    distances = []

    for i in range(len(barcode)):
        distances.append(getDistance(index, i))

    # uses python's sorted function that operates with a O(nlogn) complexity
    # sorts the distances by their index
    distancesSortedIndex = sorted(range(len(distances)), key=lambda k: distances[k])

    # sorts the distances by distance from smallest to largest
    distancesSorted = sorted(distances)

    return distancesSortedIndex, distancesSorted



def main_algorithm():
    # main control algorithm
    cont = 'Y'

    # while loop to control user input
    while cont == 'Y':
        while True:
            userChoice = input("\nPlease enter 1 to search or 2 to find retrieval accuracy: ")

            if userChoice == '1' or userChoice == '2':
                break
            else:
                print("Please enter a valid choice")

        # searches and returns top 10 most similar images
        if userChoice == '1':
            index = getIndex()
            distancesSortedIndex, distancesSorted = search_algorithm(index)

            accuracy = getAccuracy(index, distancesSortedIndex, 11)

            print(f'\nSearching: {names[index]}, value: {value[index]}, index: {index} ')
            print('The 10 most similar images are:\n')

            for i in range(1, 11):
                print(f'{i}. Value: {value[distancesSortedIndex[i]]}, {names[distancesSortedIndex[i]]}, index: {distancesSortedIndex[i]}, distance: {distancesSorted[i]}')

            print(f'The accuracy of the search is: {accuracy}%')

        # finds the overall retrieval accuracy and creates a CSV file with the comparisons
        if userChoice == '2':
            mostSimilarIndex = []
            mostSimilarValue = []
            mostSimilarNames = []
            retrievalData = []
            counter = 0

            for i in range(len(barcode)):
                index = i
                distancesSortedIndex, distancesSorted = search_algorithm(index)
                mostSimilarIndex.append(distancesSortedIndex[1])
                mostSimilarValue.append(value[mostSimilarIndex[i]])
                mostSimilarNames.append(names[mostSimilarIndex[i]])

                if value[i] == mostSimilarValue[i]:
                    counter += 1
                    result = 'hit'
                else:
                    result = 'miss'

                retrievalData.append([names[i], value[i], mostSimilarValue[i], mostSimilarNames[i], result])

            df = pandas.DataFrame(retrievalData, columns=['Searched Image', 'Value', 'Returned Value', 'Returned Image', 'Result'])

            df.to_csv('retrieval_data.csv')

            print(f'The retrieval accuracy is: {counter}%')

        cont = input('Please enter \'Y\' to continue or \'N\' to exit: ')
        cont = cont.upper()

main_algorithm()