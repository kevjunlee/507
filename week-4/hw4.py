'''
SI 507 F19 homework 4: Classes and Inheritance

Your discussion section: 003
People you worked with: Iain Graham, Lucy Jiang

######### DO NOT CHANGE PROVIDED CODE ############ 
'''

#######################################################################
#---------- Part 1: Class
#######################################################################

'''
Task A
'''
from random import randrange
class Explore_pet:
    boredom_decrement = -4
    hunger_decrement = -4
    boredom_threshold = 6
    hunger_threshold = 10
    def __init__(self, name="Coco"):
        self.name = name
        self.hunger = randrange(self.hunger_threshold)
        self.boredom = randrange(self.boredom_threshold)

    def mood(self):
        if self.hunger <= self.hunger_threshold and self.boredom <= self.boredom_threshold:
            return "happy"
        elif self.hunger > self.hunger_threshold:
            return "hungry"
        else:
            return "bored"

    def __str__(self):
        state = "I'm " + self.name + '. '
        state += 'I feel ' + self.mood() + '. '
        if self.mood() == 'hungry':
            state += 'Feed me.'
        if self.mood() == 'bored':
            state += 'You can teach me new words.'
        return state
coco = Explore_pet()
#your code begins here . . . 
coco.hunger = 6
coco.boredom = 20
print(coco)

brian = Explore_pet("Brian")
brian.hunger = 11
brian.boredom = 3
print(brian)

'''
Task B
'''
#add your codes inside of the Pet class
class Pet:
    boredom_decrement = -4
    hunger_decrement = -4
    boredom_threshold = 6
    hunger_threshold = 10
    

    def __init__(self, name="Coco"):
        self.word = ["hello"]
        self.name = name
        self.hunger = randrange(self.hunger_threshold)
        self.boredom = randrange(self.boredom_threshold)

    def mood(self):
        if self.hunger <= self.hunger_threshold and self.boredom <= self.boredom_threshold:
            return "happy"
        elif self.hunger > self.hunger_threshold:
            return "hungry"
        else:
            return "bored"

    def __str__(self):
        state = "I'm " + self.name + '. '
        state += 'I feel ' + self.mood() + '. '
        if self.mood() == 'hungry':
            state += 'Feed me.'
        if self.mood() == 'bored':
            state += 'You can teach me new words.'
        return state

    def clock_tick(self):
        self.boredom += 2
        self.hunger += 2
    
    def say(self):
        print("I know how to say ")
        for i in self.word:
            print(i + "\n")

    def teach(self, word):
        self.word.append(word)
        if (self.boredom + self.boredom_decrement < 0):
            self.boredom = 0
        else:
            self.boredom += self.boredom_decrement
    
    def feed(self):
        if self.hunger + self.hunger_decrement < 0:
            self.hunger = 0
        else:
            self.hunger += self.hunger_decrement
        
#'''
#Task C
#'''
    def hi(self):
        x = randrange(len(self.word))
        word = self.word[x]
        print(word)
        

def teaching_session(my_pet, new_words):
    for i in new_words:
        my_pet.teach(i)
        my_pet.hi()
        print(my_pet)
        if my_pet.mood == "hungry":
            my_pet.feed()
        my_pet.clock_tick()
        

new_list =  ['I am sleepy', 'You are the best','I love you, too']
lord = Pet("lord")
teaching_session(lord, new_list)



#######################################################################
#---------- Part 2: Inheritance - subclasses
#######################################################################
'''
Task A: Dog and Cat
'''
#your code begins here . . .
class Dog(Pet):
    def __str__(self):
        state = "I'm " + self.name + ', arrrf! '
        state += 'I feel ' + self.mood() + ', arrrf! '
        if self.mood() == 'hungry':
            state += 'Feed me, arrrf!'
        if self.mood() == 'bored':
            state += 'You can teach me new words, arrrf!'
        return state
    
class Cat(Pet):
    def __init__(self, name, meow_count):
        self.word = ["hello"]
        self.name = name
        self.hunger = randrange(self.hunger_threshold)
        self.boredom = randrange(self.boredom_threshold)
        self.meow_count = meow_count
        
    def hi(self):
        x = randrange(len(self.word))
        word = self.word[x]
        print(word * self.meow_count)
    
'''
Task B: Poodle 
'''
#your code begins here . . .
class Poodle(Dog):
    def dance(self):
        print("Dancing in circles like poodles do!")
        
    def say(self):
        self.dance()
        print("I know how to say ")
        for i in self.word:
            print(i + "\n")

cookie = Poodle("cookie")
print(cookie)
cookie.say()

george = Cat("george", 4)
print(george)
george.hi()



