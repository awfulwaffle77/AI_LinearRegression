import turicreate

data =  turicreate.SFrame('/content/training.csv')
tests = turicreate.SFrame('/content/test.csv')
feats = ["Readme", "Interfaces", "Virt_functions", "Classes", "Diagrams", "Lines"]
model = turicreate.linear_regression.create(data, target='Grade', features=feats)
coefficients = model.coefficients
predictions = model.predict(data)
results = model.evaluate(data)

res_tests = model.predict(tests)
print("Results: ",res_tests)