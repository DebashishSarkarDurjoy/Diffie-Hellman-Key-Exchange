import random
# p=11, g=7, xA=3 and xB=4, k=5
# p=97, g=5, xA=36 and xB=58, k=75
# p=5, g=2, xA=3 and xB=2, k=4

random.seed(100)

#display the options
# option 1 for Random numbers
# option 2 for manual input of numbers
def menu():

    print("1. Random.")
    print("2. Manual.")
    option = int(input(">> "))
    if option == 1:
        randomNumber() #call randomNumber() for option 1
    elif option == 2:
        manualNumber() #call manualNumber() for option 2

    return 0

#this function generates random numbers for p and g
#this function uses Node.computeXa() to generate random numbers for Xa and Xb
def randomNumber():
    p = random.randint(2, 100) #generate random number between 2 and 100
    while isPrime(p) == False and p > 2: # p should be greater than 2 and prime
        p = random.randint(2, 101) # keep looping until a proper value is set

    g = random.randint(2, p) # now get g based on p
    while isPrimitiveRoot(g, p) == False or p == g: # must be primite and p != g
        g = random.randint(2, p)
        try: # catch any value error
            g = random.randint(2, p)
        except ValueError:
            continue # reset g
    print(f"random g: {g}\nrandom p: {p}") # show g and p

    print()

    #if g and p are set properly, continue
    if isPrimitiveRoot(g, p) and isPrime(p):
        alice = Node(g, p)
        bob = Node(g, p)
        alice.computeXa() # generates random Xa value
        alice.computePublicKey() # computes the public key of A

        print("Alice Xa: ", alice.getXa()) # shows the value of Xa
        print("Alice publicKey: ", alice.getPublicKey()) # shows the value of Xb
        print()
        bob.computeXa() # compute Xb
        # if g == 2 or p == 3: # if g or p is too low set Xa of bob to 2
        #     bob.Xa = 2
        while bob.getXa() == alice.getXa(): # Xa and Xb should not be same
            bob.computeXa()
        bob.computePublicKey() # compute public key of B
        print("Bob Xb: ", bob.getXa()) # show Xb
        print("Bob publicKey", bob.getPublicKey()) # show public key of B

        print()
        # compute private key of Alice using public key of Bob
        alice.computePrivateKey(bob.getPublicKey())
        # compute private key of Bob using public key of Alice
        bob.computePrivateKey(alice.getPublicKey())
        # show the private keys of Alice and Bob
        print("Alice privateKey: ", alice.getPrivateKey())
        print("Bob privateKey: ", bob.getPrivateKey())

#this function asks user for manual entry of p, g, Xa and Xb
def manualNumber():
    # ask user for g and p
    g = int(input("Enter g: "))
    p = int(input("Enter p: "))

    print()
    if isPrimitiveRoot(g, p) and isPrime(p):
        # ask user for Xa and Xb
        Xa = int(input("Alice Xa: "))
        Xb = int(input("Bob Xb: "))
        if (Xa == Xb): # Xa and Xb can not be same
            print("Not Xa and Xb are same. Not valid entry")
            return 0 # terminate program is same

        alice = Node(g, p, Xa) # make an object of Alice from Node class
        bob = Node(g, p, Xb) # make an object of Bob from Node class

        alice.computePublicKey() # compute the public key of Alice
        print("alice Xa: ", alice.getXa()) # show Xa
        print("alice publicKey: ", alice.getPublicKey()) # show public key
        print()

        bob.computePublicKey() # compute public key of Bob
        print("bob Xb: ", bob.getXa()) # show Xa
        print("bob publicKey", bob.getPublicKey()) # show public key

        print()
        # Alice computes the private key using Bob's public key
        alice.computePrivateKey(bob.getPublicKey())
        # Bob computes the private key using Alice's public key
        bob.computePrivateKey(alice.getPublicKey())

        # show the private keys, they should match
        print("alice privateKey: ", alice.getPrivateKey())
        print("bob privateKey: ", bob.getPrivateKey())
    else:
        # if inputs are not valid (not primitive), show the msg and quit
        print("Not valid entry")
        return 0

# function to check if a number n is prime
def isPrime(n):
    if n == 2: # if n is 2 it is prime, return true
        return True
    if n % 2 == 0: # if n is divisible by 2, it is not prime, return False
        return False
    # check all number from 2 till n/2, n is divisible by any number in this
    # range then it is not prime
    for i in range(2, int(n/2)):
        if n % i == 0:
            return False
    return True

# function to calculate the result of n^p
def power(n, p):
    result = 1
    for i in range(0, p): # loop p times
        result = result * n # multiply result with n for p times

    return result

# a class to represent the two entities Alice and Bob.
class Node:
    def __init__(self, g, p, Xa = None):
        # sets the initial values
        self.Xa = Xa
        self.publicKey = None
        self.privateKey = None
        self.p = p
        self.g = g

    # getter for Xa
    def getXa(self):
        return self.Xa

    # getter for public key
    def getPublicKey(self):
        return self.publicKey

    # getter for private key
    def getPrivateKey(self):
        return self.privateKey

    # this method sets a random Xa based on this condition 1 < Xa < p
    def computeXa(self):
        if self.p == 1 or self.p == 2: # if p is too low, set Xa as 1
            self.Xa = 1
            return
        Xa = random.randint(2, self.p) # 1 < Xa < p
        while isPrimitiveRoot(Xa, self.p) == False:
            Xa = random.randint(2, self.p)
        self.Xa = Xa

    # method to calculate public key, formula: g^Xa mod p
    def computePublicKey(self):
        self.publicKey = power(self.g, self.Xa) % self.p

    # method to calculate private key, formula: B^Xa mod p
    def computePrivateKey(self, B): # B is the public key of the other entity
        self.privateKey = power(B, self.Xa) % self.p


# a function to check if g and p are primitive root
def isPrimitiveRoot(g, p):
    remainders = []
    for i in range(p):
        #appends remainder of g^i mod p to the remainder list
        remainders.append(power(g, i) % p)
    remainders.pop(0) # pops the first value
    for i in range(0, len(remainders)): # checks if any number is repeating
        if remainders.count(remainders[i]) > 1:
            #if any number has count more than 1, then g and p are not primitive
            return False
    # if there are no repeating remainders, then g and p are primitive roots
    return True


#this starts the program
menu()
