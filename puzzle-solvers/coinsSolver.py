from random import shuffle

cp = ["red", "corroded", "shiny", "concave", "blue"]
p = [2, 3, 5, 7, 9]

while True:
    r = list(range(5))
    shuffle(r)
    result = p[r[0]] + p[r[1]]*p[r[2]]**2 + p[r[3]]**3 - p[r[4]]
    if result == 399:
        print("Result found!")
        print("{} + {} * {}^2 + {}^3 - {} = 399".format(p[r[0]], p[r[1]], p[r[2]],
                                                        p[r[3]], p[r[4]]))

        print("Coins:")
        for i in range(5):
            print("\t{}\n".format(cp[r[i]]))
        break