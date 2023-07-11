import pandas as pd
import csv
import pathlib
from pathlib import Path
import pdb

df = pd.read_csv("cards_updated.csv", sep = ",")
df['colorIdentity'] = df['colorIdentity'].fillna('C')
df_search = df[['UID', 'name']].copy()
df_search['name'] = df_search['name'].str.lower().replace(",",'', regex = True)
df_search.set_index("UID", inplace = True)

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
    commander_name = card_exists(commander_name)
    card_index = get_card_index(commander_name)
    card_index =check_legendary(card_index)
    # commander_name = commander_checks(commander_name)
    return card_index
    
##check if the commander is legendary
def check_legendary(card_index):
    if df.at[card_index, 'supertypes'] == "Legendary":
        print("Commander is a Legendary Creature")
        return card_index
    else:
        print("Please enter a Legendary Creature")
        card_index = commander()


    
       
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
    if ((card_name in df_search["name"].values) == True):
        print(card_name, " exists")
    else:
        print(card_name, " does not exist")
        card_name = ask_card_name()
    return card_name    
        
    
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
    converted_mana_cost = df.at[card_index, 'convertedManaCost']
    color_identity = df.at[card_index, 'colorIdentity']
    deck.loc[index_slot, ['Name', 'Description', 'Type', 'Sub-type',
                 'Power', 'Toughness', 'Commander', 'Mana_Cost', "CMC",
                 'Color_Identity']] = [name, description, type, card_type, power, toughness,commander, mana_cost, converted_mana_cost, color_identity]
    land_inc += 1
    print(name)
    print(deck)
    return land_inc
    

##ask for a card name
def ask_card_name():
    card_name = input("What card would you like to add to your deck: ")
    ##check if card exists
    card_name = card_exists(card_name)
    return card_name
    

##make a deck
def make_deck():
    deck = pd.DataFrame(columns = ['Name', 'Description', 'Type', 
                                   'Sub-type', 'Power', 'Toughness', 
                                   'Commander', 'Mana_Cost', 'CMC', 'Color_Identity'])
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
    if choice == "1" or choice == "2":
        return choice
    else:
        print("Please select a valid option.")
        main_menu()

def get_card_index(card_name):
    card_index = (df_search.index[df_search['name'] == card_name]).item()
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
    converted_mana_cost = df.at[card_index, 'convertedManaCost']
    color_identity = df.at[card_index, 'colorIdentity']
    deck.loc[0, ['Name', 'Description', 'Type', 'Sub-type',
                 'Power', 'Toughness', 'Commander', 'Mana_Cost', 'CMC',
                 'Color_Identity']] = [name, description, type, card_type, power, toughness,commander, mana_cost, converted_mana_cost, color_identity]
    print(deck)
    return color_identity
    
def add_nonbasic_lands(land_inc):
    card_name = input('Enter a non-basic land card name.(lowercase no commas)')
    card_name = card_exists(card_name)
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
        land_inc = add_nonbasic_lands(land_inc)
        
    return land_inc
    
def check_non_basic(card_index):
    type = df.at[card_index, 'supertypes']
    is_land = df.at[card_index, 'type']
    if type != 'Basic' and 'Land' in is_land:
        is_basic = False
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
    return color_match
    
def land_menu():
    print("Which basic land would you like to start with?")
    if 'G' in color_identity_check:
        print("forest")
    if 'B' in color_identity_check:
        print("swamp")
    if 'W' in color_identity_check:
        print('plains')
    if 'U' in color_identity_check:
        print('island')
    if 'R' in color_identity_check:
        print('Mountain')
    print('Wastes')
    
def check_land_name(land_name):
    valid_lands = ['mountain', 'wastes', 'island', 'swamp',
                   'plains', 'forest']
    if land_name in valid_lands:
        print('Valid choice')
        return land_name
    else:
        print('Please select a valid choice')
        land_name = ask_card_name()
        land_name = check_land_name(land_name)
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
    while x != number_to_add and land_inc < land_count:
        land_inc = add_land_to_deck(land_index, land_inc)
        x += 1
    print(deck)
    return land_inc
    
def check_land_count(land_inc):
    print('You are running {} lands'.format(land_inc))
    print('You originally wanted to add {} lands'.format(land_count))
    repeat = input('would you like to add more lands? (y/n')
    if repeat == 'y':
        land_option = input('basic or nonbasic?')
        if land_option == 'basic':
            land_inc = add_basic_lands(land_inc)
        elif land_option == 'nonbasic':
            land_inc = add_nonbasic_lands(land_inc)
        else:
            print("Please select a valid option")
            check_land_count(land_inc)
    elif repeat == 'n':
        return land_inc
    else:
        print("Please select a valid option")
        land_inc = check_land_count(land_inc)
        return land_inc
        
            
def ask_for_more_lands(land_inc):
    more_lands = input('would you like to add more basic lands? (y/n')
    if more_lands == 'y':
        land_inc = add_basic_lands(land_inc)
    else:
        land_inc = check_land_count(land_inc)
        return land_inc
      
    

def add_basic_lands(land_inc):
    print(land_inc)
    land_menu()
    land_name = input('Enter a name from the list of basic lands available')
    valid_land_name = check_land_name(land_name)
    print(valid_land_name)
    land_index = get_card_index(valid_land_name)
    number_to_add = check_number_of_lands()
    land_inc = loop_in_lands(land_index, number_to_add, land_inc)
    land_inc = ask_for_more_lands(land_inc)
    return land_inc
   
    
def color_identity_to_list():
    deck_color_identity1 = deck_color_identity.split(',')
    print(deck_color_identity1)
    return deck_color_identity1

def add_card(card_index, card_inc):
    index_slot = card_inc + 1
    name = df.at[card_index, 'name']
    description = df.at[card_index, 'text']
    type = df.at[card_index, 'type']
    card_type = df.at[card_index, 'types']
    power = df.at[card_index, 'power']
    toughness = df.at[card_index, 'toughness']
    commander = False
    mana_cost = df.at[card_index, 'manaCost']
    converted_mana_cost = df.at[card_index, 'convertedManaCost']
    color_identity = df.at[card_index, 'colorIdentity']
    deck.loc[index_slot, ['Name', 'Description', 'Type', 'Sub-type',
                 'Power', 'Toughness', 'Commander', 'Mana_Cost', 'CMC', 
                 'Color_Identity']] = [name, description, type, card_type, power, toughness,commander, mana_cost, converted_mana_cost, color_identity]
    card_inc += 1
    print(deck)
    return card_inc
   
def check_if_unique(card_index):
    already_exists = False
    if ((df.at[card_index, 'name'] in deck['Name'].values) == True):
        print('This card is already in the deck')
        already_exists = True
        return already_exists
    else:
        return already_exists
       
def add_card_to_deck(card_inc):
    card_name = ask_card_name()
    card_index = get_card_index(card_name)
    already_exists = check_if_unique(card_index)
    color_match = check_color_identity(card_index)
    if already_exists == False and color_match == True and card_inc < deck_size:
        card_inc = add_card(card_index, card_inc)
        if card_inc != deck_size:
            add_card_to_deck(card_inc)
        else:
            print(card_inc)
            return card_inc
    else:
        print('This card already exists or doesnt match you color identity')    
        card_inc = add_card(card_index, card_inc)
    return card_inc

def create_csv():
    deck_name = input('Enter the name of the deck')
    print('exporting to csv file...')
    deck.to_csv('{}.csv'.format(deck_name))
    
def count_colors():
    i = 0
    white, blue, black, green, red = 0 , 0 , 0 , 0 , 0
    while i<99:
        deck['Mana_Cost'] = deck['Mana_Cost'].astype(str)
        if deck.at[i, 'Mana_Cost'] == 'NaN':
            i += 1
        else:
            white += deck.at[i, 'Mana_Cost'].count('W')
            blue += deck.at[i, 'Mana_Cost'].count('U')
            black += deck.at[i, 'Mana_Cost'].count('B')
            green += deck.at[i, 'Mana_Cost'].count('G')
            red += deck.at[i, 'Mana_Cost'].count('R') 
            i+= 1
    color_intensity_list = [white, blue, black, green, red]
    print(color_intensity_list)
    return color_intensity_list
            
def load_deck():
    deck_name = input('please enter the name of the deck you want to load')
    deck = pd.read_csv('{}.csv'.format(deck_name))
    return deck   

def land_production():
    deck['Description'] = deck['Description'].astype(str)
    i = 0
    makes_white, makes_blue, makes_black, makes_green, makes_red = 0,0,0,0,0
    while i < 99:
        if deck.at[i, 'Sub-type'] == 'Land':
            makes_white += deck.at[i, 'Description'].count('W')
            makes_blue += deck.at[i, 'Description'].count('U')
            makes_black += deck.at[i, 'Description'].count('B')
            makes_green += deck.at[i, 'Description'].count('G')
            makes_red += deck.at[i, 'Description'].count('R')
            i += 1
        else:
            i += 1
    land_produces_list = [makes_white, makes_blue, 
                          makes_black, makes_green, makes_red]
    print(land_produces_list)
    return land_produces_list

def make_color_dframe(color_intensity_list, land_produces_list):
    color_df = pd.DataFrame(columns = ['color', 'intensity', 'land_production'])
    color_df['color'] = ['White', 'Blue', 'Black', 'Green', 'Red']
    color_df['intensity'] = color_intensity_list
    color_df['land_production'] = land_produces_list
    color_df.set_index('color')
    print(color_df)
    return color_df

def create_excel_file():
    file_name = input("Enter the name of the deck")
    with pd.ExcelWriter("{}.xlsx".format(file_name)) as writer:
        deck.to_excel(writer, sheet_name = 'Sheet_name_1')
        color_df.to_excel(writer, sheet_name = 'Sheet_name_2')
    #deck.to_excel('{}.xlsx'.format(file_name), sheet_name = 'Sheet_name_1')   

def color_to_excel():
    color_df.to_excel('deck_color_data.xlsx', sheet_name = 'Sheet_name_2')
    
def deck_color_data():
    color_intensity_list = count_colors()
    land_produces_list = land_production()
    color_df = make_color_dframe(color_intensity_list, land_produces_list)
    return color_df
 
choice = main_menu()

df.set_index('UID', inplace =True)
deck_size = 99 # excludes commander
land_inc = 0 #incramenter to count lands

if choice == "1":
    deck = make_deck()
    card_index = commander()
    deck_color_identity = add_commander_to_deck(card_index)
    color_identity_check = color_identity_to_list()
    color_identity_check.append('C')
    land_count = input('How many lands would you like to run?')
    land_count = int(land_count)
    print('Lets start with non-basic lands')
    xyz = add_nonbasic_lands(land_inc)
    print(xyz)
    land_inc = add_basic_lands(xyz)
    card_inc = deck.index[-1].item()
    print(card_inc)
    print("you have {} card slots remaining for the rest of your deck.".format(99-card_inc))
    card_inc = add_card_to_deck(card_inc)
    color_df = deck_color_data()
    create_excel_file()
    #create_csv()
    
    
    
elif choice == '2':
    deck = load_deck()
    print(deck)
    color_intensity_list = count_colors()
    land_produces_list = land_production()
    color_df = make_color_dframe(color_intensity_list, land_produces_list)
    create_excel_file()
    
else:
    print("working on it")
       