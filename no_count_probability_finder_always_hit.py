import random
import pandas as pd
import numpy as np

# setting number of monte carlo loops
mc_loop_nr = 100

# Setting the inital number of decks
Shoe_decks = 6

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

# function that salculates the "Soft sum" of a player/dealer
def Soft_sum(sum,ace_count):
    if ace_count == 0:
        S_Sum = sum
    if ace_count > 0:
        new_ace_count = ace_count - 1 # updating the number of aces we can "SWAP" from 11 to 1
    
    return S_Sum, new_ace_count


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
    elif value >= 7 and value <=9 : # 7 to 9 - doing nothing
        count_append = 0 
    elif value >= 10 : # high card - adding 1
        count_append = -1
    else:
        print("HI_LO error! Value = ", value)
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

# function determining the winner in our form of game simulation - we deal all cards at once, not per player.
def Winner(player_sum,player_ace_count,dealer_sum,dealer_ace_count):
    player_isbust = False
    dealer_isbust = False
    player_no_blackjack = False
    dealer_no_blackjack = False
    # checking if the player is bust
    if player_sum > 21 and player_ace_count == 0: # case where the player simply goes bust.
        player_isbust = True
    elif player_sum > 21 and player_ace_count > 0: # we are over 21 but have a ace
        while player_sum > 21 and player_ace_count > 0: # subtracting as long as we need to or as long as we can
            player_sum -= 10
            player_ace_count -= 1
            player_no_blackjack = True # you still can have 21, but you cannot have a blackjack
        if player_sum > 21:
            player_isbust = True
    
    # checking if dealer is bust
    if dealer_sum > 21 and dealer_ace_count == 0:
        dealer_isbust = True
    elif dealer_sum > 21 and dealer_ace_count > 0: # we are over 21 but have a ace
        while dealer_sum > 21 and dealer_ace_count > 0: # subtracting as long as we need to or as long as we can
            dealer_sum -= 10
            dealer_ace_count -= 1
            dealer_no_blackjack = True # you still can have 21, but you cannot have a blackjack
        if dealer_sum > 21:
            dealer_isbust = True
    
    # checking the outcome of showdown
    if player_isbust: # player went bust. this always looses
        winner = "D"
    elif dealer_isbust: # player is not bust and the dealer is
        winner = "P"
    elif player_sum == dealer_sum: # draw/push
        winner = "PUSH"
    elif player_sum == 21 and not player_no_blackjack: # does the player have a blackjack. The case of a draw has been covered in the previous statement
        winner = "Blackjack"
    elif player_sum > dealer_sum: # player has higher sum than dealer
        winner = "P"
    elif player_sum < dealer_sum:
        winner = "D"
    else:
        print("Error in showdown evaluation! Check your code")

    return winner


# Create a numpy array for always hiiting. the vertical axis is teh dealer and the horizontal axis is the player.

always_hit_win = np.zeros((22,12))
always_hit_loss = np.zeros((22,12))
always_hit_draw = np.zeros((22,12))
always_hit_blackjack = np.zeros((22,12))



for i in range(mc_loop_nr):
    # initializing the first 3 cards and then always hitting once
    for player_card_face in card_face_list:
        player_ace_count = 0
        player_sum = 0
        ### begin repetable segment ### for player
        player_card_value = card_values[player_card_face] # getting card value
        if str(player_card_value) == "ACE":
            player_ace_count += 1 # The variable to destinguish if and how many aces the player has
            player_card_value = 11
        player_sum += player_card_value # set the players sum
        ### finish repetable segment ###

        # second card now O(n^2)
        for player_card_face in card_face_list:
            player_ace_count2 = 0
            player_sum2 = 0
            ### begin repetable segment ### for player
            player_card_value = card_values[player_card_face] # getting card value
            if str(player_card_value) == "ACE":
                player_ace_count2 = player_ace_count + 1 # The variable to destinguish if and how many aces the player has
                player_card_value = 11
            player_sum2 = player_sum + player_card_value # set the players sum
            ### finish repetable segment ###

            #finding if first sum is ace. this would otherwise register as initial 22
            if player_sum2 == 22:
                player_sum2 = 12
                player_ace_count2 -= 1

            # finding the row to save data in - cruicial element
            player_first_sum = player_sum2
        
            # third card now O(n^3)
            for dealer_card_face in card_face_list:
                dealer_ace_count = 0
                dealer_sum = 0 
                ### begin repetable segment ### for dealer
                dealer_card_value = card_values[dealer_card_face] # getting card value
                if str(dealer_card_value) == "ACE":
                    dealer_ace_count += 1 # The variable to destinguish if and how many aces the dealer has
                    dealer_card_value = 11
                dealer_sum += dealer_card_value # set the dealers sum
                ### finish repetable segment ###

                # finding column to save data in the chart - cruicial element
                first_dealer_card = dealer_card_value 

                ### finding win probability with always hitting. with dealer stopping on soft 17 ###

                # fourth card now O(n^4)
                for player_card_face in card_face_list:

                    # potentially loop here if monte carlo was used.

                    player_ace_count3 = 0
                    player_sum3 = 0

                    ### begin repetable segment ### for player
                    player_card_value = card_values[player_card_face] # getting card value
                    if str(player_card_value) == "ACE": # in case of ace
                        player_ace_count3 = player_ace_count2 + 1 # The variable to destinguish if and how many aces the player has
                        player_card_value = 11
                    player_sum3 = player_sum2 + player_card_value # set the players sum
                    ### finish repetable segment ###
                    
                    #### the player here is done.
                    
                    

                    ### now dealer plays till soft 17 ###
                    dealer_sum2 = 0
                    loop = 0
                    dealer_ace_count2 = 0
                    while dealer_sum2 < 17:
                        
                        # here my brain just melted from imagining depth and functions, so i decided to run 
                        # it with the deal() function. i will run it 100 times and I will see what happens
                        
                        
                        ### begin repetable segment ### for dealer
                        dealer_card_face = deal()
                        dealer_card_value = card_values[dealer_card_face] # getting card value
                        if str(dealer_card_value) == "ACE":
                            if loop == 0:
                                dealer_ace_count2 = dealer_ace_count + 1 # The variable to destinguish if and how many aces the dealer has
                            else:
                                dealer_ace_count2 += 1
                            dealer_card_value = 11
                        if loop == 0:
                            dealer_sum2 = dealer_sum + dealer_card_value # set the dealers sum    
                        else:           
                            dealer_sum2 += dealer_card_value
                        loop =+ 1
                        ### finish repetable segment ###
                    
                    showdown = Winner(player_sum3,player_ace_count3,dealer_sum2,dealer_ace_count2)
                    if showdown == "P":
                        always_hit_win[player_first_sum,first_dealer_card] += 1
                    if showdown == "D":
                        always_hit_loss[player_first_sum,first_dealer_card] += 1
                    if showdown == "Blackjack":
                        always_hit_blackjack[player_first_sum,first_dealer_card] += 1
                    if showdown == "PUSH":
                        always_hit_draw[player_first_sum,first_dealer_card] += 1
                    
                    
                # 4th card nest
            # 3rd card nest
            
        # 2nd card nest
    # 1st card nest
                    
                

# Initialize a numpy array to store the win rates
win_rate_array = np.zeros((22, 12))

# Loop through each row and column
for row in range(22):
    for col in range(12):
        # Calculate the win rate for the current cell location
        win_rate = (always_hit_win[row, col] + 1.5*always_hit_blackjack[row, col]) / (always_hit_win[row, col] + always_hit_loss[row, col] + always_hit_blackjack[row, col])

        # Store the win rate in the win_rate_arr numpy array
        win_rate_array[row, col] = win_rate

print(always_hit_win)
print(always_hit_loss)
print(win_rate_array)

win_rate_df = pd.DataFrame(win_rate_array)
win_df = pd.DataFrame(always_hit_win)
loss_df = pd.DataFrame(always_hit_loss)
blackjack_df = pd.DataFrame(always_hit_blackjack)
draw_df = pd.DataFrame(always_hit_draw)


# Create a Pandas Excel writer using xlsxwriter as the engine
writer = pd.ExcelWriter(f"always_hit_winrate_{mc_loop_nr}.xlsx", engine='xlsxwriter')

# Write each DataFrame to a separate worksheet in the Excel file
win_rate_df.to_excel(writer, sheet_name='Win_rate')
win_df.to_excel(writer, sheet_name='Always Hit Wins')
loss_df.to_excel(writer, sheet_name='Always Hit Losses')
blackjack_df.to_excel(writer, sheet_name='Always Hit Blackjacks')
draw_df.to_excel(writer, sheet_name='Always Hit Blackjacks')
# Close the Pandas Excel writer and save the Excel file
writer.save()





