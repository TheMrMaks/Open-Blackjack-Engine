import random

# Setting the inital number of decks
Shoe_decks = 8

# Setting number of players at the table
# this value should not affect odds and is aimed at 
# analtical purposes of the code itself
players = 1

# initializing the running count
running_count = 0

# Setting a dictionary of cards and their values
# the format is CARD : VALUE
card_values = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": "ACE"
}

# Creating a card face list
card_face_list = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]

# Creating a list of all cards in the shoe
shoe_cards_left ={
    "2": 4*Shoe_decks,
    "3": 4*Shoe_decks,
    "4": 4*Shoe_decks,
    "5": 4*Shoe_decks,
    "6": 4*Shoe_decks,
    "7": 4*Shoe_decks,
    "8": 4*Shoe_decks,
    "9": 4*Shoe_decks,
    "10": 4*Shoe_decks,
    "J": 4*Shoe_decks,
    "Q": 4*Shoe_decks,
    "K": 4*Shoe_decks,
    "A": 4*Shoe_decks
}

# number of cards left in the deck
shoe_nr = 52*Shoe_decks

# defining a function for finfing the real count
def real_count():
    real_count = running_count/(shoe_nr/52)

# Defining a function determining if the player is bust
def over21(sum,VERBOSE = False):
    if sum > 21:
        Bust = True
    else:
        Bust = False
    if VERBOSE == True: # Troubleshooting mode 
        print(str(Bust))

    return Bust


# defining the function that updates the running count
def HI_LO(value,VERBOSE = False):
    if str(value) == "ACE" : # ace - subtracting 1
        count_append = -1
    elif value >=2 and value <= 6 : # low card - subtracting 1
        count_append = 1
    elif value >= 7 and value <=9 : # 7 to 10 - doing nothing
        count_append = 0 
    elif value == 10 : # high card - adding 1
        count_append = -1
    if VERBOSE == True: # Troubleshooting mode 
        print(str(count_append))

    return count_append

# defining the function that deals a card from the leftover shoe randomly
def deal():
    c = random.randint(1, shoe_nr) # getting a random number to pick a card
    
    findingcard = True
    loop = 0 # initializing loop iteration of the while loop to 0
    while findingcard:
        
        if c <= shoe_cards_left[card_face_list[loop]]:  # checking if the currently considered card type is the one
            card_face = card_face_list[loop] # setting card_face - our random card to the currently looped type

            findingcard = False # exiting loop
        else:
            c -= shoe_cards_left[card_face_list[loop]] # subtracting the number of checked cards from random number
            
            loop +=1 # looping through next type of card
    
    return card_face


# dealing the whole game 
for i in range(0,shoe_nr):
    card_face = deal() # pulling a card
    
    shoe_cards_left[card_face] -= 1 # subtracting 1 from the number of cards of the type left
    
    shoe_nr -= 1 # subtracting 1 from cards in the shoe
    
    value = card_values[card_face] # getting card value
    
    running_count += HI_LO(value) # updating count

    print("run nr.",i+1,' the card is ',card_face,', running count at :',running_count)

print(shoe_cards_left)



