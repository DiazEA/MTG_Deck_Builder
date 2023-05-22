import pandas as pd
import csv
import pathlib
from pathlib import Path

df = pd.read_csv("cards_updated.csv", sep = ",")

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
def add_card_to_deck(card_index):
    name = df.at[card_index, 'name']
    print(name)

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
    card_index = df['UID'].loc[df["name"] == card_name].item()
    print(card_index)
    return card_index

color_identity = ''

def add_commander_to_deck(card_index, deck):
    name = df['name'].loc[df['UID'] == card_index].item()
    description = df['text'].loc[df['UID'] == card_index].item()
    type = df['type'].loc[df['UID'] == card_index].item()
    card_type = df['types'].loc[df['UID'] == card_index].item()
    power = df['power'].loc[df['UID'] == card_index].item()
    toughness = df['toughness'].loc[df['UID'] == card_index].item()
    commander = True
    mana_cost = df['manaCost'].loc[df['UID'] == card_index].item()
    color_identity = df['colorIdentity'].loc[df['UID'] == card_index].item()
    deck.loc[0, ['Name', 'Description', 'Type', 'Sub-type',
                 'Power', 'Toughness', 'Commander', 'Mana_Cost',
                 'Color_Identity']] = [name, description, type, card_type, power, toughness,commander, mana_cost, color_identity]
    #print(name, description, type, card_type, color_identity, commander, mana_cost, power, toughness)
    print(deck)
    
def add_lands():
    land_count = input('How many lands would you like to run?')
    card_name = input('Enter a non-basic land card name.')
    card_index = get_card_index(card_name)
    check_non_basic(card_index)
    
def check_non_basic(card_index):
    type = df.at[card_index, 'supertypes']
    is_land = df.at[card_index, 'type']
    if type != 'Basic' and is_land == 'Land':
        add_card_to_deck(card_index)
    print(type)
 
    
def add_non_basic_land(land_count):
    print('Lets add non-basic lands first')
    
    
#def color_identity_check(card_index):
    
    
choice = main_menu()

if choice == "1":
    deck = make_deck()
    commander_name = commander()
    card_index = get_card_index(commander_name)
    add_commander_to_deck(card_index, deck)
    add_lands()
    
else:
    print("working on it")
    
    