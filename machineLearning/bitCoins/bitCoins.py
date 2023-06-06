# external libraries
import yfinance as yf
import pandas as pd
import datetime
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

class BitCoin():

    @classmethod
    def youtubeFinanceDataExtractor(cls, parameterDictionary):
        bitcoinSymbol = parameterDictionary.get("symbol")
        bitcoinData = yf.Ticker(bitcoinSymbol)
        bitcoinHistoricalData = bitcoinData.history(start=parameterDictionary.get("start"),
        end=parameterDictionary.get("end"))
        return bitcoinHistoricalData

    @classmethod
    def dataFrameToCsvConverter(cls, parameterDictionary):
        dataF = parameterDictionary.get('dataFrame')
        localPathForTheCsvFile = parameterDictionary.get('localPathForTheCsvFile')
        dataF.to_csv(localPathForTheCsvFile, index=True)
        return dataF

    @classmethod
    def createArrayIndependentVariables(cls, parameterDictionary):
        csvPath = parameterDictionary.get('localPathForTheCsvFile')
        listOfIndependentColumns = parameterDictionary.get('independentColumns')
        csvDataset = pd.read_csv(csvPath)
        arrayIndependentVariables = csvDataset[listOfIndependentColumns].values
        return arrayIndependentVariables

    @classmethod
    def createArrayDependentVariables(cls, parameterDictionary):
        csvPath = parameterDictionary.get('localPathForTheCsvFile')
        listOfDependentColumns = parameterDictionary.get('dependentColumns')
        csvDataset = pd.read_csv(csvPath)
        arrayDependentVariables = csvDataset[listOfDependentColumns].values
        return arrayDependentVariables

    @classmethod
    def dataDivisionTestTraining(cls, parameterDictionary):
        X = parameterDictionary.get('matrixIndependentVariables')
        y = parameterDictionary.get('matrixDependentVariables')
        X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=42)
        response = {
            "X_train": X_train, 
            "X_test": X_test, 
            "y_train": y_train, 
            "y_test": y_test,
        }
        return response

    @classmethod
    def trainingAndPricePrediction(cls, parameterDictionary):
        X_train = parameterDictionary.get('X_train')
        X_test = parameterDictionary.get('X_test')
        y_train = parameterDictionary.get('y_train')
        linearRegressionModel = LinearRegression()
        linearRegressionModel.fit(X_train, y_train)
        prediction = linearRegressionModel.predict(X_test)
        
        response = {
            "model" : prediction, 
            "linearRegressionModel" : linearRegressionModel,
        }
        return response

    @classmethod
    def meanSquarError(cls, parameterDictionary):
        y_test = parameterDictionary.get('y_test')
        y_pred = parameterDictionary.get('model')
        degreeMeanSquarError = mean_squared_error(y_test, y_pred)
        return degreeMeanSquarError

    @classmethod
    def validatePrecisionSelfAdjustingModels(cls, parameterDictionary):
        model = parameterDictionary.get('model')
        X = parameterDictionary.get('X_train')
        y = parameterDictionary.get('y_train') 
        cv = parameterDictionary.get('cv')
        scores = cross_val_score(model, X, y, cv=cv, scoring='neg_mean_squared_error')
        mse_average = scores.mean()

        response = {
            "scores": scores,
            "mse_average": mse_average,
        }
        # Returns negative MSE scores at each iteration
        return response

dataLoadParameters = {
    "symbol":'BTC-USD',
    "start":"2019-01-01",
    "end":"2023-06-06",
}

# 'machineLearning/bitCoins/data/dataFrame.csv'
bitcoinInstance = BitCoin.youtubeFinanceDataExtractor(dataLoadParameters)

savingParametersDataConversion = {
    "dataFrame":bitcoinInstance,
    "localPathForTheCsvFile":'machineLearning/bitCoins/data/dataSet.csv',
}

BitCoin.dataFrameToCsvConverter(savingParametersDataConversion)

parametersCreationTestTrainingSets = {
    "localPathForTheCsvFile":'machineLearning/bitCoins/data/dataSet.csv',
    "independentColumns":['Open', 'High', 'Low', 'Volume'],
    "dependentColumns": ['Close'],
}

arrayDependentVariables = BitCoin.createArrayDependentVariables(parametersCreationTestTrainingSets)
# print(f'variables dependientes:\n {arrayDependentVariables}')

arrayIndependentVariables = BitCoin.createArrayIndependentVariables(parametersCreationTestTrainingSets)
# print(f'variables independientes:\n {arrayIndependentVariables}')

parametersArraysOfVariables = {
    "matrixIndependentVariables": arrayIndependentVariables,
    "matrixDependentVariables": arrayDependentVariables,
}

trainingAndTestData = BitCoin().dataDivisionTestTraining(parametersArraysOfVariables)
# print(f"conjunto X de entrenamiento: {X_train}\n\n conjunto X de test: {X_test}\n\n conjunto y de entrenamiento: {y_train}\n\n conjunto y de test: {y_test}")

trainingAndTestSets = {
    "X_train": trainingAndTestData.get('X_train'),
    "X_test": trainingAndTestData.get('X_test'),
    "y_train": trainingAndTestData.get('y_train'),
    "y_test": trainingAndTestData.get('y_test'),
}

modelAndLineaRegression = BitCoin().trainingAndPricePrediction(trainingAndTestSets)

meanSquarErrorParameters = {
    "y_test": trainingAndTestData.get('y_test'),
    "model": modelAndLineaRegression.get('model'),
}

meanSquarError = BitCoin().meanSquarError(meanSquarErrorParameters)
# print(f"Prediccion de bitcoin:\n\n {modelAndLineaRegression.get('model')}, \n\nerror cuadratico medio de: {meanSquarError}")

print("Predicción de bitcoin:")
for result in modelAndLineaRegression['model']:
    print(result[0])

print("\nError cuadrático medio:", meanSquarError)

precisionValidationParameters = {
    "model" : modelAndLineaRegression.get('linearRegressionModel'),
    "X_train" : trainingAndTestData.get('X_train'),
    "y_train" : trainingAndTestData.get('y_train'),
    "cv" : 5
}

scoresMseAverage = BitCoin().validatePrecisionSelfAdjustingModels(precisionValidationParameters)
# print(f"proporción de la varianza en la variable dependiente: {scoresMseAverage.get('scores')}\npromedio error cuadratico (mse): {scoresMseAverage.get('mse_average')}")