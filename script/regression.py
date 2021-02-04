import turicreate

data = turicreate.SFrame('/content/training_*.csv')  # unde * va fi inlocuita cu numarul csv-ului respectiv
tests = turicreate.SFrame('/content/test_*.csv')
feats = ["Readme", "Interfaces", "Virt_functions", "Classes", "Diagrams", "Lines"]
model = turicreate.linear_regression.create(data, target='Grade', features=feats)
coefficients = model.coefficients
predictions = model.predict(data)
results = model.evaluate(data)

print(model.summary())

res_tests = model.predict(tests)

rounded_res = []
for x in res_tests:
    x = round(x, 2)
    rounded_res.append(x)
res = dict(zip(tests["Student"], rounded_res))
print(res)
