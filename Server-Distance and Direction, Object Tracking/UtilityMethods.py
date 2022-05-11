import pickle

# input as flat text
a = ["Ford", "Volvo", "BMW"]

pickle.dump(a, open("save.p", "wb"))

x = pickle.dumps(a)

#x = pickle.load(open("save.p", "rb"))

print(x)

print(pickle.loads(x))