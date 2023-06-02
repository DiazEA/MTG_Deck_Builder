import pandas as pd
import csv
import pathlib
from pathlib import Path

df = pd.read_csv("cards_updated.csv", sep = ",")
df['colorIdentity'] = df['colorIdentity'].fillna('C')

## ask for user name
def user_name():
    name = input("Enter your name: ")
    return name
##name the deck
def name_deck():
    deck_name = input("Enter the name of the deck: ")
    
## what type of deck
def commander():
    commander_name = input("Enter your commander's name: ")
    commander_name = commander_checks(commander_name)
    return commander_name
    
##check if the commander is legendary
def check_legendary(card_name):
    if (((df['supertypes'].loc[df["name"] == card_name]) == "Legendary").any()) == True:
        print("Commander is a Legendary Creature")
        return card_name
    else:
        print("Please enter a Legendary Creature as your commander")
        commander()
    
       
## check if commander exists
def commander_checks(commander_name):
    commander_name = check_legendary(commander_name)
    commander_name = card_exists(commander_name)
    return commander_name

## ask or card name
def card_name():
    card_name = input("Enter your card name: ")
    return card_name

## check if card exists
def card_exists(card_name):
    if ((card_name in df["name"].values) == True):
        print(card_name, " exists")
        return card_name
    else:
        print(card_name, " does not exist")
        ask_card_name()
        
    
## add card to deck
def add_land_to_deck(card_index, land_inc):
    index_slot = land_inc + 1
    name = df.at[card_index, 'name']
    description = df.at[card_index, 'text']
    type = df.at[card_index, 'type']
    card_type = df.at[card_index, 'types']
    power = df.at[card_index, 'power']
    toughness = df.at[card_index, 'toughness']
    commander = False
    mana_cost = df.at[card_index, 'manaCost']
    color_identity = df.at[card_index, 'colorIdentity']
    deck.loc[index_slot, ['Name', 'Description', 'Type', 'Sub-type',
                 'Power', 'Toughness', 'Commander', 'Mana_Cost',
                 'Color_Identity']] = [name, description, type, card_type, power, toughness,commander, mana_cost, color_identity]
    land_inc += 1
    print(name)
    print(deck)
    return land_inc
    

##ask for a card name
def ask_card_name():
    card_name = input("What card would you like to add to your deck: ")
    ##check if card exists
    card_exists(card_name)
    return card_name
    

##make a deck
def make_deck():
    deck = pd.DataFrame(columns = ['Name', 'Description', 'Type', 
                                   'Sub-type', 'Power', 'Toughness', 
                                   'Commander', 'Mana_Cost', 'Color_Identity'])
    print(deck)
    print("Deck created successfully")
    return deck
    

def main_menu():
    print("Welcome")
    print("1: Create a new deck")
    print("2: Load an existing deck")
    choice = input("select an option:")
    choice = valid_choice(choice)
    return choice
    
def valid_choice(choice):
    if choice == "1":
        return choice
    else:
        print("Please select a valid option.")
        main_menu()

def get_card_index(card_name):
    card_index = df.index[df['name'] == card_name].item()
    print(card_index)
    return card_index

color_identity = ''

def add_commander_to_deck(card_index):
    name = df.at[card_index, 'name']
    description = df.at[card_index, 'text']
    type = df.at[card_index, 'type']
    card_type = df.at[card_index, 'types']
    power = df.at[card_index, 'power']
    toughness = df.at[card_index, 'toughness']
    commander = True
    mana_cost = df.at[card_index, 'manaCost']
    color_identity = df.at[card_index, 'colorIdentity']
    deck.loc[0, ['Name', 'Description', 'Type', 'Sub-type',
                 'Power', 'Toughness', 'Commander', 'Mana_Cost',
                 'Color_Identity']] = [name, description, type, card_type, power, toughness,commander, mana_cost, color_identity]
    #print(name, description, type, card_type, color_identity, commander, mana_cost, power, toughness)
    print(deck)
    return color_identity
    
def add_nonbasic_lands(land_inc):
    card_name = input('Enter a non-basic land card name.')
    card_index = get_card_index(card_name)
    is_basic = check_non_basic(card_index)
    color_match = check_color_identity(card_index)
    if is_basic == False and land_inc < land_count and color_match == True:
        land_inc = add_land_to_deck(card_index, land_inc)
        ask_for_more_lands = input("Add another non-basic Land card? y/n:")
        print(land_inc)
        if ask_for_more_lands == 'y':
            land_inc = add_nonbasic_lands(land_inc)
        else:
            print(land_inc)
            return land_inc
    else:
        print('Land is not a non-basic land card or doesnt match your color identity')
        add_nonbasic_lands(land_inc)
        
    return land_inc
    
def check_non_basic(card_index):
    type = df.at[card_index, 'supertypes']
    is_land = df.at[card_index, 'type']
    if type != 'Basic' and is_land == 'Land':
        is_basic = False
        # add_land_to_deck(card_index, land_count)
    else:
        is_basic = True
    return is_basic

def check_color_identity(card_index):
    print(card_index)
    card_identity = df.at[card_index, 'colorIdentity']
    card_identity_list = card_identity.split(",")
    color_match = True
    for i in card_identity_list:
       if i in color_identity_check and color_match == True:
           print("within color identity")
       else:
           print('card identity not within the color identity of your commander')
           color_match = False
           #add_nonbasic_lands(land_inc)
    return color_match
    
def land_menu():
    print("Which basic land would you like to start with?")
    if 'G' in color_identity_check:
        print("Forest")
    if 'B' in color_identity_check:
        print("Swamp")
    if 'W' in color_identity_check:
        print('Plains')
    if 'U' in color_identity_check:
        print('Island')
    if 'R' in color_identity_check:
        print('Mountain')
    print('Wastes')
    
def check_land_name(land_name):
    valid_lands = ['Mountain', 'Wastes', 'Island', 'Swamp',
                   'Plains', 'Forest']
    if land_name in valid_lands:
        print('Valid choice')
    else:
        print('Please select a valid choice')
        add_basic_lands()
    return land_name
 
def check_number_of_lands():
    number_to_add = input("how many of this basic land would you like to add")
    number_to_add = int(number_to_add)
    if number_to_add > (land_count - land_inc):
        print('You do not have enough land slots left')   
        check_number_of_lands()
    else:
        return number_to_add
    
def loop_in_lands(land_index, number_to_add, land_inc):
    x = 0
    while x != number_to_add and land_inc <= land_count:
        land_inc = add_land_to_deck(land_index, land_inc)
        x += 1
    print(deck)

def add_basic_lands(land_inc):
    print(land_inc)
    print("Now we will add any basic lands")
    land_menu()
    land_name = input('Enter a name from the list of basic lands available')
    valid_land_name = check_land_name(land_name)
    land_index = get_card_index(land_name)
    number_to_add = check_number_of_lands()
    loop_in_lands(land_index, number_to_add, land_inc)
    
    
    
def color_identity_to_list():
    deck_color_identity1 = deck_color_identity.split(',')
    print(deck_color_identity1)
    return deck_color_identity1
    
choice = main_menu()

df.set_index('UID', inplace =True)
deck_size = 99 # excludes commander
land_inc = 0 #incramenter to count lands

if choice == "1":
    deck = make_deck()
    commander_name = commander()
    card_index = get_card_index(commander_name)
    deck_color_identity = add_commander_to_deck(card_index)
    color_identity_check = color_identity_to_list()
    color_identity_check.append('C')
    land_count = input('How many lands would you like to run?')
    land_count = int(land_count)
    deck_size = deck_size - land_count
    print('Lets start with non-basic lands')
    xyz = add_nonbasic_lands(land_inc)
    print(xyz)
    add_basic_lands(xyz)
    
else:
    print("working on it")
    
    