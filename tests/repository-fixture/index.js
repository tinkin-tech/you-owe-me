const sumTwoNumbers = (numA, numB) => {
    return numA + numB
}

const getCommonElements = (arrayA, arrayB) => {
    return arrayA.filter(
        (element) => arrayB.find((elementB) => elementB === element)
    )
}

const generateRandomNumber = (min, max) => {
  return Math.floor(Math.random() * (max - min))
}