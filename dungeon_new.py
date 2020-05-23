#================================================================#
# DUNGEON GAME                                                   #
# Intro To Computer Science, Final Project                       #
# Michael Shaten                                                 #
#                                                                #
# CODE IS ORGANIZED IN FOLLOWING ORDER:                          #
# 1. Classes                                                     #
# 2. Functions (only one function exists outside of a class)     #
# 3. Lists and Dictionaries                                      #
#                                                                #
# CREDITS FOR ARTWORK ARE FOUND AT THE BOTTOM                    #
#================================================================#

import tkinter as tk
import os
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter.font as tkFont
from tkinter import simpledialog
# from PIL import Image, ImageTk
import random
import operator

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        #-------------------------------------------------------#
        #                       CLASSES                         #  
        #-------------------------------------------------------#    


# shop class
class Shop:
    def __init__(self,stock={}, prices={}):
        self.stock = stock
        self.prices = prices
    def add_item(self,item,stock=1): #adds item to shop, modifies base price from item_prices
        price = random_price(item_prices[item])
        if item in self.stock:
            self.stock[item] += 1
        if item not in self.stock:
            self.stock[item] = 1
            self.prices[item] = price          
    def remove_item(self,item): #removes item from shop
        if self.stock[item] > 0:
            self.stock[item] -= 1     

# player class
class Player:
    def __init__(self,gold=10,hp=10,name="player_name",inventory={},prices={}):
        self.hp = hp #health points
        self.gold = gold #can be spent in shop, or gained from selling items
        self.inventory = inventory #contains items that player collects
        self.prices = prices #prices for items, found in item_prices dictionary
        self.name = name
    def add_item(self,item,stock=1): #adds item to player inventory, modifies base price from item_prices
        price = random_price(item_prices[item])
        if item in self.inventory:
            self.inventory[item] += 1
        if item not in self.inventory:
            self.inventory[item] = 1
            self.prices[item] = price   
    def remove_item(self,item): #removes item from player inventory
        if self.inventory[item] > 0:
            self.inventory[item] -= 1
        if self.inventory[item] == 0:
            self.inventory.pop(item)
    def take_damage(self, damage_taken): #reduces player hp when attacked
        self.hp -= damage_taken
    def attack(self, enemy): #outputs damage to enemy
        random_damage = random.randrange(0,5)
        if "silver sword" in self.inventory:
            random_damage = random.randrange(5,10)
        if "emerald sword" in self.inventory:
            random_damage = random.randrange(8,12)
        if "gold sword" in self.inventory:
            random_damage = random.randrange(10,15)
        damage_given = random_damage
        enemy.take_damage(damage_given)
    def goldup(self,amt): #increases gold
        self.gold += amt
    def golddown(self,amt): #decreases gold
        self.gold -= amt
        if self.gold < 0:
            self.gold = 0
    def buy_item(self,item,shop): #adds item to player.inventory, removes gold price from player.gold
        price = shop.prices[item]
        self.golddown(price)
        self.add_item(item)
        shop.remove_item(item)
    def sell_item(self,item,shop): #removes item, adds gold
        price = self.prices[item]
        self.goldup(price)
        self.remove_item(item)
        shop.add_item(item)      

# monster class
class Monster:
    def __init__(self,name,hp=10,gold=0,loot=["health potion","emerald"]):
        self.hp = hp
        self.name = name
        self.loot = loot
        self.gold = gold
    def take_damage(self, damage_taken):
        self.hp -= damage_taken
    def attack(self, enemy,random_damage):
        damage_given = random_damage
        enemy.take_damage(damage_given)
    def drop_loot(self,enemy):
        enemy.goldup(self.gold)
        for item in self.loot:
            enemy.add_item(item)     

#npc class (will be used in later development)
class npc:
    def __init__(self,name,gold=0,helped=0,bag={}):
        self.name = name
        self.gold = gold
        self.bag = bag
    def give_item(self,player,item):
        player.add_item(item)

# main window class, is created when program is run
class App:
    def __init__(self):  
        #opens main (root) window 
        self.window = tk.Tk()  
        self.window.title("Dungeon Game") #window title
        self.iconFile = "assets/images/misc/torch.ico"
        self.window.wm_iconbitmap(self.iconFile) #icon image for window
        image = tk.PhotoImage(file="assets/images/misc/hallway.png") #background image for window
        label = tk.Label(image=image)
        label.pack()
        w = tk.Label(self.window,text="Welcome to the Dungeon",fg="red",font=('Old English Text MT', 25, 'bold'),) #welcome label
        w.place(y=30,x=256,anchor=CENTER) 
                             
        #------------------PLAYER NAME INPUT--------------------#
        #window for player to input character name
        self.enter_name = Toplevel()
        self.enter_name.wm_iconbitmap(self.iconFile) #icon image for windo
        self.enter_name.geometry("300x45")
        self.enter_name.grab_set() #disables parent window until closed
        self.enter_name.title("Name your character") #window title
        self.enter_name.rowconfigure((0,1),weight=1)

        #open entry widget inside the window
        name = Entry(self.enter_name)
        name.pack()
        name.focus_set()

        #after player hits button, this assigns the input to the name in player1, enter_name window is destroyed
        def complete():
            character_name = name.get() 
            self.player1.name = character_name         
            self.enter_name.destroy()        

        #calls complete function
        b = Button(self.enter_name,text='OK',command=complete,cursor="hand2")
        b.pack(side='bottom')
        #-------------------------------------------------------#


        #-------------------------------------------------------#
        #                   MAIN WINDOW BUTTONS                 #  
        #-------------------------------------------------------# 


        #styling for buttons
        style = Style() 
        style.configure('TButton', font = ('algerian', 10, 'bold'),  borderwidth = '4') 

        # enter_dungeon button, command dungeon method will open dungeon window
        btn_dungeon = Button(self.window,text="Enter Dungeon", command=self.dungeon,cursor="hand2")
        btn_dungeon.place(x=35,y=100)


        # visit shop button, command shop_visit method will open the shop window
        btn_shop = Button(self.window, text = "Visit Shop ",command = self.shop_visit,cursor="hand2")
        btn_shop.place(x = 35, y = 130)


        # view inventory button, command view_invneotry will open the inventory window
        btn_inventory = Button(self.window, text="View Inventory", command = self.view_inventory,cursor="hand2")
        btn_inventory.place(x = 35, y = 160)

        # exits the window
        btn_exit = Button(self.window, text="exit", command=self.window.quit,cursor="X_cursor")
        btn_exit.place(x =35, y = 190)


        #-------------------------------------------------------#
        #            CREATE SHOP AND PLAYER  OBJECTS            #  
        #-------------------------------------------------------#  


        self.player1 = Player() #assign player to class
        self.shop1 = Shop() #assign shop to class

        #add starting items to shop
        self.shop1.add_item("gold sword")
        self.shop1.add_item("staff")
        self.shop1.add_item("staff")
        self.shop1.add_item("ring")

        #---------------------#
        self.window.mainloop()
        #---------------------#
        

#-------------------------------------------------------#
#              DEFINE MAIN WINDOW FUNCTIONS             #  
#-------------------------------------------------------#  


    # open dungeon window and pick random function from the function list
    def dungeon(self):
        dungeon_window = Toplevel()
        dungeon_window.wm_iconbitmap(self.iconFile)
        dungeon_window.title("Dungeon Game | Dungeon")
        dungeon_window.grab_set() #disables parent window until closed
        dungeon_window.grid_columnconfigure((0,1), weight=1)


        #-------------------------------------------------------#
        #               DUNGEON WINDOW FUNCTIONS                #  
        #-------------------------------------------------------#          
        

        #####################      FINDING TREASURE   #######################
        # randomizer below determines whether to call regular or rare treasure find 
        def treasure(self):

            #--------------REGULAR TREASURE--------------------#  
            # normal window and items
            def regular():
                randomizer = random.randrange(len(list(item_list)))# pick random treasure from list
                item = list(item_list)[randomizer]

                # narration
                text = Label(dungeon_window,text=f"You found some treasure!\n\nHere's what you found:",font=("Bodoni MT",10))
                text.grid(row=0, column=0, columnspan=2)
                text.configure(anchor="center")

                # image of item
                image_file = "assets/images/items/" + item_images[item]
                photo = PhotoImage(file=image_file)
                labelphoto = tk.Label(dungeon_window,image=photo,)
                labelphoto.image = photo
                labelphoto.grid(row=1,column=0,columnspan=2)

                #narration
                text2 = Label(dungeon_window,text=f"{item}",font=("Bodoni MT",10))
                text2.grid(row=2,column=0,columnspan=2)
                text2.configure(anchor="center")

                # exit window
                btn_collect = Button(dungeon_window,text="Collect Item",command=dungeon_window.destroy,cursor="hand2")
                btn_collect.grid(row=3,column=0,columnspan=2)

                self.player1.add_item(item) #add item to player inventory

                #consumables change player hp, are removed from inventory
                if item == "health potion":
                    self.player1.remove_item(item)
                    self.player1.hp += 3
                if item == "bread":
                    self.player1.remove_item(item)
                    self.player1.hp += 1
            #-----------------------------------------------------#                      

            #--------------RARE TREASURE (CHEST)------------------#  
            # small chance to show chest, runs open_chest function if player has the key
            def rare():
                
                # function if player has key to the chest and presses button
                def open_chest():
                    chest_window = Toplevel() # new window
                    chest_window.wm_iconbitmap(self.iconFile)
                    chest_window.title("Dungeon Game | Chest")
                    chest_window.grab_set()
                    chest_window.grid_columnconfigure((0,1),weight=1)

            
                    randomizer = random.randrange(len(list(rare_item_list)))# pick random treasure from list
                    item = list(rare_item_list)[randomizer]

                    # narration
                    text = Label(chest_window,text=f"You found some treasure!\n\nHere's what you found:",font=("Bodoni MT",10))
                    text.grid(row=0, column=0, columnspan=2)
                    text.configure(anchor="center")

                    # image of item
                    image_file = "assets/images/items/" + item_images[item]
                    photo = PhotoImage(file=image_file)
                    labelphoto = tk.Label(chest_window,image=photo,)
                    labelphoto.image = photo
                    labelphoto.grid(row=1,column=0,columnspan=2)

                    #change chest image to open
                    image_file = "assets/images/misc/openChest.png"
                    photo = PhotoImage(file=image_file)
                    labelphoto = tk.Label(dungeon_window,image=photo,)
                    labelphoto.image = photo
                    labelphoto.grid(row=1,column=0,columnspan=2)

                    #narration
                    text2 = Label(chest_window,text=f"{item}",font=("Bodoni MT",10))
                    text2.grid(row=2,column=0,columnspan=2)
                    text2.configure(anchor="center")

                    #exit dungeon window
                    btn_unlock = Button(dungeon_window,text="Leave Dungeon",command=dungeon_window.destroy,cursor="hand2")
                    btn_unlock.grid(row=3,column=0,columnspan=2)

                    # exit chest window
                    btn_collect = Button(chest_window,text="Collect Item",command=chest_window.destroy,cursor="hand2")
                    btn_collect.grid(row=3,column=0,columnspan=2)

                    self.player1.add_item(item) #add item to player inventory
                    self.player1.inventory.pop("rusty key") # remove rusy key after use          

                # show button to open chest if player has key, button to exit if not
                if "rusty key" in self.player1.inventory:
                    # narration
                    text = Label(dungeon_window,text=f"You found chest!",font=("Bodoni MT",10))
                    text.grid(row=0, column=0, columnspan=2)
                    text.configure(anchor="center")

                    # chest image
                    image_file = "assets/images/misc/lockedChest.png"
                    photo = PhotoImage(file=image_file)
                    labelphoto = tk.Label(dungeon_window,image=photo,)
                    labelphoto.image = photo
                    labelphoto.grid(row=1,column=0,columnspan=2)

                    # narration
                    text2 = Label(dungeon_window,text="Looks like you have a key!",font=("Bodoni MT",10))
                    text2.grid(row=2,column=0,columnspan=2)
                    text2.configure(anchor="center")

                    # open chest window
                    btn_unlock = Button(dungeon_window,text="Unlock Chest",command=open_chest,cursor="hand2")
                    btn_unlock.grid(row=3,column=0,columnspan=2)
                else:
                    # narration
                    text = Label(dungeon_window,text=f"You found chest!",font=("Bodoni MT",10))
                    text.grid(row=0, column=0, columnspan=2)
                    text.configure(anchor="center")

                    # chest image
                    image_file = "assets/images/misc/lockedChest.png"
                    photo = PhotoImage(file=image_file)
                    labelphoto = tk.Label(dungeon_window,image=photo,)
                    labelphoto.image = photo
                    labelphoto.grid(row=1,column=0,columnspan=2)

                    # narration
                    text2 = Label(dungeon_window,text="Looks like it needs a key!",font=("Bodoni MT",10))
                    text2.grid(row=2,column=0,columnspan=2)
                    text2.configure(anchor="center")

                    #exit window
                    btn_unlock = Button(dungeon_window,text="Leave Dungeon",command=dungeon_window.destroy,cursor="hand2")
                    btn_unlock.grid(row=3,column=0,columnspan=2)
            #-----------------------------------------------------#                      

            #--------------REGULAR OR RARE TREASURE---------------#      
            # generating random numbers
            rare1 = random.randrange(0,5)
            rare2 = random.randrange(0,1)
                
            # calls rare function for chest if random numbers are equal (reducing chance of rare) 
            if rare1 == rare2:
                rare()
            else:
                regular()
            #-----------------------------------------------------#                 
        #####################################################################  

        #####################      MEETING AN NPC     #######################
        # npc method, player can meet and talk with npcs, may provide items/info 
        def npc(self):

            #--------------CREATING THE NPC--------------------#  
            randomizer1 = random.randrange(len(npc_list))# pick random npc from list
            npc = npc_list[randomizer1]

            randomizer2 = random.randrange(len(dialogue_list)) # asssigning random dialogue from list
            dialogue = dialogue_list[randomizer2]

            # narration
            text = Label(dungeon_window,text=f"You meet another traveler in the dungeon!",font=("Bodoni MT",10))
            text.grid(row=0, column=0, columnspan=2)
            text.configure(anchor="center")

            # image of npc
            image_file = "assets/images/npc/"+npc_images[npc]
            photo = PhotoImage(file=image_file)
            labelphoto = tk.Label(dungeon_window,image=photo,)
            labelphoto.image = photo
            labelphoto.grid(row=1,column=0,columnspan=2)

            #npc dialogue
            text2 = Label(dungeon_window,text=f"'{dialogue}'",font=("Bodoni MT",10))
            text2.grid(row=2, column=0, columnspan=2)
            text2.configure(anchor="center")
            #--------------------------------------------------#

            #--------------PLAYER DIALOGUE OPTIONS-------------#
            # if statements for dialogue options    
            if dialogue_list.index(dialogue) == 0:
                def interact():
                    random_gold = random.randrange(1,3)
                    self.player1.golddown(random_gold) 
                    dungeon_window.destroy()
                # exit window
                btn_leave = Button(dungeon_window,text="Not a chance",command=dungeon_window.destroy,cursor="hand2")
                btn_leave.grid(row=3,column=0,sticky=E)
                # interact button
                btn_collect = Button(dungeon_window,text="Sure, I'll help you",command=interact,cursor="hand2")
                btn_collect.grid(row=3,column=1,sticky=W)
            if dialogue_list.index(dialogue) == 1:
                def interact():   
                    dungeon_window.destroy()
                # exit window
                btn_leave = Button(dungeon_window,text="Get a map",command=dungeon_window.destroy,cursor="hand2")
                btn_leave.grid(row=3,column=0,sticky=E)
                # interact button
                btn_collect = Button(dungeon_window,text="Of course, follow me",command=interact,cursor="hand2")
                btn_collect.grid(row=3,column=1,sticky=W)                
            if dialogue_list.index(dialogue) == 2:
                def interact():   
                    self.player1.add_item("rusty key")
                    dungeon_window.destroy()
                # exit window
                btn_leave = Button(dungeon_window,text="No, you need it more than me",command=dungeon_window.destroy,cursor="hand2")
                btn_leave.grid(row=3,column=0,sticky=E)
                # interact button
                btn_collect = Button(dungeon_window,text="Why thank you!",command=interact,cursor="hand2")
                btn_collect.grid(row=3,column=1,sticky=W)                
            if dialogue_list.index(dialogue) == 3:
                def interact():   
                    dungeon_window.destroy()
                # exit window
                btn_leave = Button(dungeon_window,text="No it's not",command=dungeon_window.destroy,cursor="hand2")
                btn_leave.grid(row=3,column=0,sticky=E)
                # interact button
                btn_collect = Button(dungeon_window,text="It sure is",command=interact,cursor="hand2")
                btn_collect.grid(row=3,column=1,sticky=W)
            #--------------------------------------------------#   
        #####################################################################       

        #####################      MONSTER APPEARS    #######################
        # battle method, random monster appears, player can fight mosnter or flee
        def battle(self):
            dungeon_window.geometry("360x300")

            #--------------CREATING THE MONSTER-----------------#        
            # randomly selecting monster, assigning image to monster
            randomizer1 = random.randrange(len(list(monster_list))) #assign random number from listified monster dictionary
            monster = list(monster_list)[randomizer1] #grabbing random monster from the list
            image_file = "assets/images/monsters/" + monster_list[monster] #finds monster image file in values from monster dicionary

            # assign monster to Monster() class, generate monster stats
            random_gold = random.randrange(1,5)
            self.monster1 = Monster(monster,gold=random_gold) #assigning monster to the Monster class, giving it a name and gold

            # randomly selecting monster description (adjectives)
            randomizer2 = random.randrange(len(monster_discription)) #assign random number
            description = monster_discription[randomizer2] #calls random description from the list

            # randomly selecting monster pose
            randomizer3 = random.randrange(len(monster_pose)) #assign random number
            pose = monster_pose[randomizer3] #calls random pose from list

            # narration
            text = Label(dungeon_window,text=f"A{description} {monster} {pose}! ",font=("Bodoni MT",10))
            text.grid(row=0, column=0, columnspan=2)
            text.configure(anchor="center")

            # image of the random monster
            photo = PhotoImage(file=image_file)
            labelphoto = tk.Label(dungeon_window,image=photo,)
            labelphoto.image = photo
            labelphoto.grid(row=1,column=0,columnspan=2)
            #------------------------------------------------------# 
          
            #--------------FIGHTING THE MONSTER--------------------#  
            # function mosnter fight if player chooses to fight
            def fight(monster):
                # simulate 50/50 coin flip to see who goes first
                def coin_flip():
                    flip = random.randint(1,100)
                    if flip <= 50:
                        return "monster"
                    elif flip >= 51:
                        return "player"

                first_attack = coin_flip() #variable for who goes first, calls coin flip function 

                # conditional statements based on who goes first and remaining health points; object changes and new windows appaer basd on conditional paths
                if first_attack == "monster": #monster goes first
                    random_damage = random.randrange(0,5) #picking random damage
                    self.monster1.attack(self.player1,random_damage) #call method to damage player1
                    if self.player1.hp <= 0: #special window if player dies
                        battle_end = Toplevel()# new window after round of fight
                        battle_end.wm_iconbitmap(self.iconFile)
                        battle_end.title("Dungeon Game | Battle has Ended")
                        battle_end.grab_set()
                        battle_end.grid_columnconfigure((0,1),weight=1)
                        #narration
                        text = Label(battle_end,text=f"The {self.monster1.name} has defeated you.",font=("Bodoni MT",10))
                        text.grid(row=2,column=0,columnspan=2)
                        text.configure(anchor="center")
                        text2 = Label(battle_end,text="GAME OVER!",font=("Bodoni MT",10))
                        text2.grid(row=3,column=0,columnspan=2)
                        text2.configure(anchor="center")

                        #record how player died in a text file
                        try:
                            file = open("assets/text/character_deaths.txt","a")
                            try:
                                file.write(f"{self.player1.name} was defeated by a{description} {monster}\n\n")
                            finally:
                                file.close()
                        except IOError:
                            messagebox.showinfo("Error","Trouble writing character death to file. File does not exist or cannot be opened.")

                        # button to close entire program if monster wins
                        btn_collect = Button(battle_end,text="Exit",command=self.window.destroy,cursor="hand2")
                        btn_collect.grid(row=4,column=0,columnspan=2)
                    elif self.player1.hp == 1 and random_damage > 0: #special window if monster has 1 health point remaining, only opens if this was caused damage for this round of fighting
                        battle_end = Toplevel()# new window after round of fight
                        battle_end.wm_iconbitmap(self.iconFile)
                        battle_end.title("Dungeon Game | Battle has Ended")
                        battle_end.grab_set()
                        battle_end.grid_columnconfigure((0,1),weight=1)
                        #narration
                        text = Label(battle_end,text=f"The {self.monster1.name} inflicts a massive amount of damage! You have {self.player1.hp} health point left!",font=("Bodoni MT",10))
                        text.grid(row=2,column=0,columnspan=2)
                        text.configure(anchor="center")
                        # button to close current window
                        btn_collect = Button(battle_end,text="OK",command=battle_end.destroy,cursor="hand2")
                        btn_collect.grid(row=3,column=0,columnspan=2)
                    else:
                        if self.player1.hp == 1: #window to display if player has 1 health point, but this happened in an earlier round of fighting, also string "point" is singular
                            battle_end = Toplevel()# new window after round of fight
                            battle_end.wm_iconbitmap(self.iconFile)
                            battle_end.title("Dungeon Game | Battle has Ended")
                            battle_end.grab_set()
                            battle_end.grid_columnconfigure((0,1),weight=1)
                            #narration
                            text = Label(battle_end,text=f"The {self.monster1.name} attacks!\n{self.player1.name} has {self.player1.hp} health point left",font=("Bodoni MT",10))
                            text.grid(row=2,column=0,columnspan=2)
                            text.configure(anchor="center")
                            # button to close current window
                            btn_collect = Button(battle_end,text="OK",command=battle_end.destroy,cursor="hand2")
                            btn_collect.grid(row=3,column=0,columnspan=2)
                        else:
                            battle_end = Toplevel()# new window after round of fight
                            battle_end.wm_iconbitmap(self.iconFile)
                            battle_end.title("Dungeon Game | Battle has Ended")
                            battle_end.grab_set()
                            battle_end.grid_columnconfigure((0,1),weight=1)
                            #narration
                            text = Label(battle_end,text=f"The {self.monster1.name} attacks!\n{self.player1.name} has {self.player1.hp} health points left",font=("Bodoni MT",10))
                            text.grid(row=2,column=0,columnspan=2)
                            text.configure(anchor="center")
                            # button to close current window
                            btn_collect = Button(battle_end,text="OK",command=battle_end.destroy,cursor="hand2")
                            btn_collect.grid(row=3,column=0,columnspan=2)
                elif first_attack == "player": #picking random damage
                    self.player1.attack(self.monster1) #call method to damage monster
                    if self.monster1.hp <= 0: #speical window if monster dies
                        battle_end = Toplevel()# new window after round of fight
                        battle_end.wm_iconbitmap(self.iconFile)
                        battle_end.title("Dungeon Game | Battle has Ended")
                        battle_end.grab_set()
                        battle_end.grid_columnconfigure((0,1),weight=1)
                        
                        def destroy_windows(): #close all but main window
                            battle_end.destroy()
                            dungeon_window.destroy()

                        # create list of monster loot that will dislay if player wins
                        display_loot = " "
                        for item in self.monster1.loot:
                            display_loot = f"{item}\n"
                        self.monster1.drop_loot(self.player1)         

                        #narration  
                        text = Label(battle_end,text=f"VICTORY! WE HAVE VICTORY!\n\nThe {self.monster1.name} dropped:\n\n{display_loot}\n{self.monster1.gold} gold",font=("Bodoni MT",10))# gives player info about monster loot they collected
                        text.grid(row=2,column=0,columnspan=2)
                        text.configure(anchor="center")
                        #close dungeon window if player wins
                        btn_collect = Button(battle_end,text="Exit Dungeon",command=destroy_windows,cursor="hand2")
                        btn_collect.grid(row=3,column=0,columnspan=2)                        
                    elif self.monster1.hp == 1: #special window if monster has 1 health point remaining
                        battle_end = Toplevel()# new window after round of fight
                        battle_end.wm_iconbitmap(self.iconFile)
                        battle_end.title("Dungeon Game | Battle has Ended")
                        battle_end.grab_set()
                        battle_end.grid_columnconfigure((0,1),weight=1)
                        #narration
                        text = Label(battle_end,text=f"{self.player1.name} inflicts a massive amount of damage! The {self.monster1.name} appears to be very badly wounded!",font=("Bodoni MT",10))
                        text.grid(row=2,column=0,columnspan=2)
                        text.configure(anchor="center")
                        # button to close current window
                        btn_collect = Button(battle_end,text="OK",command=battle_end.destroy,cursor="hand2")
                        btn_collect.grid(row=3,column=0,columnspan=2)
                    else:
                        if self.player1.hp == 1:
                            battle_end = Toplevel()# window to display if player has 1 health point, to adjust string "point" to singular
                            battle_end.wm_iconbitmap(self.iconFile)
                            battle_end.title("Dungeon Game | Battle has Ended")
                            battle_end.grab_set()
                            battle_end.grid_columnconfigure((0,1),weight=1)
                            #narration
                            text = Label(battle_end,text=f"{self.player1.name} attacks the {self.monster1.name}!\n{self.player1.name} has {self.player1.hp} health point left",font=("Bodoni MT",10))
                            text.grid(row=2,column=0,columnspan=2)
                            text.configure(anchor="center")
                            # button to close current window
                            btn_collect = Button(battle_end,text="OK",command=battle_end.destroy,cursor="hand2")
                            btn_collect.grid(row=3,column=0,columnspan=2)                          
                        else:
                            battle_end = Toplevel()# new window after round of fight, displays player health points
                            battle_end.wm_iconbitmap(self.iconFile)
                            battle_end.title("Dungeon Game | Battle has Ended")
                            battle_end.grab_set()
                            battle_end.grid_columnconfigure((0,1),weight=1)
                            #narration
                            text = Label(battle_end,text=f"{self.player1.name} attacks the {self.monster1.name}!\n{self.player1.name} has {self.player1.hp} health points left",font=("Bodoni MT",10))
                            text.grid(row=2,column=0,columnspan=2)
                            text.configure(anchor="center")
                            # button to close current window
                            btn_collect = Button(battle_end,text="OK",command=battle_end.destroy,cursor="hand2")
                            btn_collect.grid(row=3,column=0,columnspan=2)
            #------------------------------------------------------#                                  

            #-----------------------FLEE---------------------------#     
            # give player option to fight monster or flee (exit dungeon window)
            def choice(self):
                # narration
                label = Label(dungeon_window,text="What will you do? ",font=("Bodoni MT",10))
                label.grid(row=2, column=0, columnspan=2)
                label.configure(anchor="center")

                # fight button, initiates the fight method
                btn_fight = Button(dungeon_window,text="FIGHT", command=lambda  a=monster: fight(a), cursor="pirate")
                btn_fight.grid(row=3,column=0,sticky=E)

                # flee button, exits the dungeon window
                btn_flee = Button(dungeon_window,text="FLEE",command=dungeon_window.destroy,cursor="trek")
                btn_flee.grid(row=3,column=1,sticky=W)
        
            # pause after image appears, then displays choice method
            dungeon_window.after(2000,lambda: choice(self))
        #----------------------------------------------------------------#
        #########################################################################


        # CHOOSE RANDOM DUNGEON FUNCTION FROM LIST #
        function_list = [treasure,npc,battle]      #
        random.choice(function_list)(self)         #
        #------------------------------------------#


        #-------------------------------------------------------#
        #                    SHOP WINDOW FUNCTION               #
        #-------------------------------------------------------# 


    # opens shop window
    def shop_visit(self):
        # Frame that opens when Visit Shop button is selected 
        shop_window = Toplevel()
        shop_window.wm_iconbitmap(self.iconFile)
        shop_window.title("Dungeon Game | Shop")
        shop_window.geometry("350x350")
        shop_window.grab_set() #disables parent window until closed
        
        def close():
            shop_window.destroy()
            for items in range(len(self.shop1.stock)):
                if self.shop1.stock[item] == 0:
                    self.shop1.stock.pop(item)  

        photo = PhotoImage(file="assets/images/misc/coin.png")
        labelphoto = Label(shop_window,image=photo)
        labelphoto.image = photo
        labelphoto.grid(row=0,column=0)

        boldStyle = Style()
        boldStyle.configure("Bold.Label", font=('Bodoni MT','15'), borderwidth=2)

        gold_label = Label(shop_window,text=f"Gold: {self.player1.gold}") #displays current gold from player1.gold
        gold_label.grid(row=0, column=0, columnspan=3)

        btn_exit = Button(shop_window, text="Exit", command=close,cursor="X_cursor")
        btn_exit.grid(row=0, column=3)

        lbl_top = Label(shop_window,text="Items for Sale: ",font=('Bodoni MT','20','bold'),borderwidth=2)
        lbl_top.grid(row=1, column=0, columnspan=3)
   
        #----------------------PURCHASE ITEM---------------------------#   
        # purchase method for when player hits 'buy item' button
        def purchase(item, shop, stocklabel): #args used to identify "row" activated

            #set item_price equal to the key in shop_prices. key is the item passed to purchase() from the itembutton 
            if shop.stock[item] == 0: #error if item is out of stock
                error = Toplevel()
                error.wm_iconbitmap(self.iconFile)
                error.title("Dungeon Game | Error")
                error.grab_set()
                error.grid_columnconfigure((0,1),weight=1)

                message = Label(error,text="This item is out of stock!",font=("Bodoni MT",10))
                message.grid(row=0,column=1,columnspan=2)

                ok_button = Button(error,text="OK",command=error.destroy,cursor="hand2")
                ok_button.grid(row=3,column=1)
  
            elif shop.prices[item] > self.player1.gold: #error for player selecting item that is more than their gold
                error = Toplevel()
                error.wm_iconbitmap(self.iconFile)
                error.title("Dungeon Game | Error")
                error.grab_set()
                error.grid_columnconfigure((0,1),weight=1)

                message = Label(error,text="You do not have enough gold to purchase this item!",font=("Bodoni MT",10))
                message.grid(row=0,column=1,columnspan=2)

                ok_button = Button(error,text="OK",command=error.destroy,cursor="hand2")
                ok_button.grid(row=3,column=1)

            else:
                self.player1.buy_item(item,shop) #calls buy_item method, passes in item and shop name
                gold_label.config(text=f"Gold: {self.player1.gold}") #updates player gold label
                stocklabel.config(text=f"{shop.stock[item]}") #updates stock of item

            ##### DISABLE THE BUTTON IF STOCK IS EMPTY, work in progress#####
                # if shop.stock[item] == 0:
                #     itembutton.btn_id["state"] = DISABLED
        #--------------------------------------------------------------#

        boldStyle = Style()# styleing for labels
        boldStyle.configure("Bold.Label", font = ('Bodoni MT','15'), borderwidth=2)

        #setting up grid headers for shop window
        nameheader = Label(shop_window, text="Item name  ",style="Bold.Label")
        nameheader.grid(row=2, column=0)
        priceheader = Label(shop_window, text="Price  ",style="Bold.Label")
        priceheader.grid(row=2, column=1)
        stockheader = Label(shop_window, text="Stock",style="Bold.Label")
        stockheader.grid(row=2, column=2)

        # iterates through shop_prices and shop_stock dicionaries to display items, prices, stocks, purchase buttons
        for i in range(len(self.shop1.stock)):
            item = list(self.shop1.prices.keys())[i]
            itemlabel = Label(shop_window, text=f"{item}",relief="groove")
            itemlabel.grid(row=i + 3, column=0)
            itemprice = Label(shop_window, text=f"{self.shop1.prices[item]}")
            itemprice.grid(row=i + 3, column=1)
            itemstock = Label(shop_window, text=f"{self.shop1.stock[item]}")
            itemstock.grid(row=i + 3, column=2)

            # lambda used to pass variables to purchase method 
            itembutton = Button(shop_window,text=f"Purchase",command=lambda  a=item, b=self.shop1, c=itemstock: purchase(a, b, c), state=NORMAL,cursor="hand2")
            itembutton.grid(row=i + 3, column=3)


        #-------------------------------------------------------#
        #                   INVENTORY WINDOW                    #  
        #-------------------------------------------------------#


    # Opens window to view player's inventory
    def view_inventory(self):
        inv_w = Toplevel()
        inv_w.wm_iconbitmap(self.iconFile) 
        inv_w.title("Dungeon Game | Inventory")
        inv_w.grab_set() #disables parent window until closed
        inv_w.grid_columnconfigure((0,1,2), weight=1)

        boldStyle = Style()# styling for label
        boldStyle.configure("Bold.Label", font = ('Matura MT Script Capitals','20'), borderwidth=0)

        # if inventory dictionary is empty, display this label, else display items in player1.inventory 
        if self.player1.inventory == {}:
            lbl_top = Label(inv_w,text="Your inventory is empty! ",style="Bold.Label")
            lbl_top.grid(row=0,column=1)
        else:
            lbl_top = Label(inv_w,text="Inventory: ",style="Bold.Label")
            lbl_top.grid(row=0,column=1)

        # iterate through the inventory dicitionary and display each key and value as a lable
        for key in self.player1.inventory:
            lbl = Label(inv_w,text=f"{key} ({self.player1.inventory[key]})\n",relief="groove")
            lbl.grid(column=1)

        #image of player's inventory bag
        photo = PhotoImage(file="assets/images/misc/bag.png")
        labelphoto = Label(inv_w,image=photo)
        labelphoto.image = photo
        labelphoto.grid(row=0,rowspan=100,columnspan=2,column=2)

        # image of coin
        photo = PhotoImage(file="assets/images/misc/coin.png")
        labelphoto = Label(inv_w,image=photo)
        labelphoto.image = photo
        labelphoto.grid(row=101,column=2)

        #displays current gold from player1.gold
        gold_label = Label(inv_w,text=f"Gold: {self.player1.gold}") 
        gold_label.grid(row=101, column=2, columnspan=2)

        # conditional heart images based on player health
        if self.player1.hp >= 10:
            photo = PhotoImage(file="assets/images/misc/heartFull.png") # image of heart
            labelphoto = Label(inv_w,image=photo)
            labelphoto.image = photo
            labelphoto.grid(row=102,column=2)
        elif self.player1.hp >= 5 and self.player1.hp < 10:
            photo = PhotoImage(file="assets/images/misc/heartHalf.png") # image of heart
            labelphoto = Label(inv_w,image=photo)
            labelphoto.image = photo
            labelphoto.grid(row=102,column=2)
        else:
            photo = PhotoImage(file="assets/images/misc/heartEmpty.png") # image of heart
            labelphoto = Label(inv_w,image=photo)
            labelphoto.image = photo
            labelphoto.grid(row=102,column=2)

        #displays current health from player1.hp
        health_label = Label(inv_w,text=f"Health: {self.player1.hp}") 
        health_label.grid(row=102, column=2, columnspan=2)

        # button to exit inventory window
        btn_exit = Button(inv_w, text="exit", command=inv_w.destroy,cursor="X_cursor")
        btn_exit.grid(row=50,column=1)
        
        #space filler labels
        lbl_left = Label(inv_w,text="                            ")
        lbl_left.grid(column=0)
        lbl_right = Label(inv_w,text="                           ")
        lbl_right.grid(column=3)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


#-------------------------------------------------------#
#                       FUNCTIONS                       #
#-------------------------------------------------------# 


# function that adds or subtracts a random modifier to item's base price
def random_price(base_price):
    base_price = base_price
    operators = [operator.add,operator.sub]
    random_operator = random.choice(operators)
    random_number = 0
    if base_price < 4:
        new_price = base_price
    elif base_price >= 4 and base_price <= 10:
        random_number = random.randrange(1,4)       
    elif base_price >= 11 and base_price <= 30:
        random_number = random.randrange(1,6)
    elif base_price >= 31:
        random_number = random.randrange(1,7)         
    new_price = random_operator(base_price,random_number)
    return new_price

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


#-------------------------------------------------------#
#                 DICTIONARIES AND LISTS                #
#-------------------------------------------------------# 

#----------------------ITEMS---------------------------#   
#item lists
item_list = ["health potion","silver sword","emerald sword","diamond","gold sword","bread","staff","emerald staff","ring","waterproof candle","emerald"]
rare_item_list = ["armor of dragon scales","diamond staff","crystal ball","ancient tome","double-edged sword"]

#item prices dictionary
item_prices = {
    "health potion": 3,
    "silver sword": 15,
    "emerald sword": 25,
    "diamond": 20,
    "gold sword": 10,
    "bread": 1,
    "staff": 15,
    "emerald staff" : 25,
    "rusty key": 8,
    "ring": 8,
    "waterproof candle": 6,
    "emerald" : 18,
    "armor of dragon scales": 38, 
    "diamond staff" : 35,
    "crystal ball" : 25,
    "ancient tome" : 30,
    "double-edged sword" : 33, 
}


# item images dictionary
item_images = {
    "health potion" : "healthPotion.png",
    "crystal ball" : "crystalBall.png",
    "silver sword" : "silverSword.png",
    "emerald sword" : "emeraldSword.png",
    "diamond" : "diamond.png",
    "gold sword" : "goldSword.png",
    "bread" : "bread.png",
    "staff" : "staff.png",
    "diamond staff" : "diamondStaff.png",
    "emerald staff" : "emeraldStaff.png", 
    "ancient tome" : "ancientTome.png",
    "ring" : "ring.png",
    "waterproof candle" : "candle.png",
    "rusty key" : "key.png",
    "armor of dragon scales" : "armorOfDragonScales.png",
    "double-edged sword" : "doubleEdgedSword.png",
    "emerald" : "emerald.png"
}

#------------------------------------------------------#   

#---------------------MONSTERS-------------------------#   
# dictionary of monsters and their image directories, used for battle in the dungeon
monster_list = {
    "three headed dog": "dog.png",
    "flying skull" : "flyingSkull.png",
    "minotaur" : "minotaur.png",
    "reaper" : "reaper.png",
    "griffin" : "griffin.png",
    "werewolf" : "werewolf.png",
    "goblin" : "goblin.png",
    "skeleton" : "skeleton.png",
    "headless knight" : "headlessKnight.png",
    "vampire" : "vampire.png",
    "ghoul" : "ghoul.png",
    "zombie" : "zombie.png",
    "undead dwarf" : "undeadDwarf.png",
    "stone golem" : "stoneGolem.png"
}

# list of mosnter descriptions, used for battle in the dungeon
monster_discription = [" terrifying"," disgusting"," demonic","n evil"," freaky"," hideous"," horrific","n intimidating"," monstrous"," nightmarish"," menacing"," nasty","n ominous"," sinister"," spine-chilling"," threatening","n ugly"," spooky"," hellish"," grotesque"," repulsive"," revolting","n atrocious"," vicious"," frightening"," diabolical"," foul"," deformed"]

# list of monster poses, used for battle in the dungeon
monster_pose = ["appears before you","blocks your path","emerges form the darkness","looms ahead of you","is waiting for you","is ready to nibble on your bones","looks hungry","is ready to fight","thirsts for your blood","is snarling at you","is about to attack","doesn't look very friendly","is looking for some fresh meat","wants to sink its teeth into you","is prowling up ahead","thinks you look tasty","just wants a mouthful","wants a bit off the flank",]
#------------------------------------------------------#

#-----------------------NPCs---------------------------#
# list of npc
npc_list = ["old man","kenobi","young boy"]

# list of dialogue options
dialogue_list = ["Could you spare some change?","I'm lost, will you help me find my way out?","Here, take this, I don't need it anymore","It's nice to see another living soul after all this time"]

# images for npc
npc_images = {
    "old man" : "oldMan.png",
    "kenobi" : "kenobi.png",
    "young boy" : "youngBoy.png"
}
#------------------------------------------------------#

if __name__ == "__main__":
    App()
        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CREDITS FOR ARTWORK~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


#BACKGROUND ART: by Harold Bell, found at https://codepen.io/hbellatcodepen/pen/PjRdrG
#NPCS PHOTOS: © 2016 - 2020 TowardsThePantheon, found at https://www.deviantart.com/towardsthepantheon/art/Towards-The-Pantheon-villager-NPCs-641005237
#MONSTER PHOTOS: found at https://www.bynogame.com/pazar/steam-oyunlari/pixel-art-monster--color-by-number
#ITEM PHOTOS: by AntyGRaphics for the game Nebulosa found at https://www.reddit.com/r/PixelArt/comments/cfessw/pixel_art_items/
#MORE IMAGES: benhickling.deviantart.com, Denis Samokhvalov and Niccolo Favari from https://80.lv/articles/pixel-art-game-production-for-mobile/, VectorPixelStar from https://www.shutterstock.com/es/image-vector/gold-coin-bitcoin-cryptocurrency-symbol-pixel-751722985, PixelCod from https://www.deviantart.com/pixelcod/art/Bread-Loaf-Icon-598473493, bakcpack image found at https://www.pinterest.com/pin/459156124498191395/, itzkreator from https://www.fiverr.com/itzkreator/create-high-quality-pixel-art-sprites-tilesets-and-icons, Mr5ombra found at https://www.reddit.com/r/PixelArt/comments/5sepaa/oc_ruby_ring/, https://www.pngkit.com/view/u2q8a9i1u2i1y3y3_heart-pixel-png-pixel-heart/

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #




