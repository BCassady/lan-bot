import pickle

f = open("output.csv", "r")

link_options = []

for line in f.readlines():
    useful = line.split(';')[0]
    if "/wiki/" in useful and "navigation" not in useful and ".png" not in useful:
        link_options.append(useful)

pickle.dump( link_options, open( "realmeye.p", "wb" ) )

