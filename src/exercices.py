#Branis AINOUZ
def exo1(n):
    print("Exercice 1")  

    a = (n+4)**3
    print(a)
    b = a**0.5
    print(b)
    c = a//n
    print(c)
    d = a%n
    print(d)
    e = (a+5) % (n-1)
    print(e)
    f = a * c * d * e
    print(f)

def exo2(prixHt,TVA):
    print("Exercice 2")  

    ttc = prixHt + (prixHt * TVA)/100
    print(ttc)  


def exo3(year):
    print("Exercice 3")  

    if((year%4==0) and (year%100!=0 or year%400==0 )):
        print("bisextile")
    else:
        print("pas bisextile")


def exo4(t,n):
    print("Exercice 4")  

    if(n == 0):
        print("conversion de %d degres Celsius en Fahrenheit : " % (t))
        res = (t * 9/5) + 32
    else:
        print("conversion de %d degres Fahrenheit en Celsius : " % (t))
        res = (t - 32) * 5/9
    print(round(res,3))


def exo5():
    print("Exercice 5")  

    texte = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean at accumsan nisl, ac aliquet tellus. Sed maximus leo lacus, nec pulvinar purus maximus vel. Morbi sagittis suscipit risus, sed luctus metus bibendum vitae. Sed ac odio dignissim, efficitur ipsum eu, imperdiet ante."
    voy = 'aeiouy'

    cpt = 0
    for i in voy:
        cpt += texte.count(i)
    print(cpt)

def exo6():
    print("Exercice 6")  

    voy = 'aeiouy'
    ma_liste = ["maths", "info", "python", "exposant", "alpha", "fonction", "parabole", "equilateral", "orthogonal", "cercle", "isocèle" ]
    print("Mots commencant par une voyelle")
    for i in voy:
        for mot in ma_liste:
            if(mot[0] == i):
                print(mot)

    print("Modifier premier mot de la liste par music et afficher la liste")
    ma_liste[0] = "music"
    print(ma_liste)

    print("Afficher la liste des mots de la liste donnée qui se terminent par un e")
    for mot in ma_liste:
        if(mot[len(mot) -1] == "e"):
            print(mot)

exo1(5)
exo2(14,20)
exo3(2020)
exo4(21,0)
exo5()
exo6()
