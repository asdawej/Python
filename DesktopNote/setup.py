import pickle

f = open('note.dat', 'wb')
pickle.dump([], f)
f.close()
