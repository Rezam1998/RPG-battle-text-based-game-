from classes.game import person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


# Create Black magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizard = Spell("Blizard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 12, 140, "black")

# Create White Magic
cure = Spell("Cure", 25, 600, "White")
cura = Spell("Cura", 32, 1500, "White")
curaga = Spell("Curaga", 50, 6000, "white")

# Create smoe Items:
potion = Item("potion", "potion", "Heals 50 Hp", 50)
hipotion = Item("Hi-potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixer", "potion", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizard, meteor, quake, cura, cure]
enemy_spells = [fire, meteor, curaga]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5}, 
				{"item": superpotion, "quantity": 5},{"item": elixer, "quantity": 5}, 
				{"item": hielixer, "quantity": 2},{"item": grenade, "quantity": 5}]
# Instantiate People
player1 = person("Reza :", 3260, 132, 300, 34, player_spells, player_items)
player2 = person("Hadis:", 4160, 188, 300, 34, player_spells, player_items)
player3 = person("Robot:", 3089, 174, 300, 34, player_spells, player_items)


enemy1 = person("Imp1 ", 1250, 130, 560, 325, enemy_spells, [])
enemy2 = person("Magus", 11200, 221, 525, 25, enemy_spells, [])
enemy3 = person("Imp2 ", 1250, 130, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]
running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS" + bcolors.ENDC)

while running:
	print("=========================")
	print("\n\n")
	print("NAME             HP                      MP")
	for player in players:
		
		player.get_stat()
	print("\n")

	for enemy in enemies:
		enemy.get_enemy_stat()

	for player in players :
		
		player.choose_action()
		choice = input("    Choose Action:")
		index = int(choice) - 1

		if index == 0:
			dmg = player.generate_damage()
			enemy = player.choose_target(enemies)
			enemies[enemy].take_dmg(dmg)
			print("You atacked" + enemies[enemy].name.replace(" ", "") + "for", dmg, "points of damage")
			if enemies[enemy].get_hp() == 0:
				print (enemies[enemy].name.replace(" ", "") +" has died!!")
				del enemies[enemy]

		elif index == 1 :
			player.choose_magic()
			magic_choice = int(input("    choose magic:")) - 1

			if magic_choice == -1 :
				continue


			spell = player.magic[magic_choice]
			magic_dmg = spell.generate_damage()


			current_mp = player.get_mp()

			if spell.cost > current_mp:
				print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
				continue


			player.reduce_mp(spell.cost)

			if spell.type == "White":
				player.heal(magic_dmg)
				print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), ".HP", bcolors.ENDC)
			elif spell.type == "black":
				enemy = player.choose_target(enemies)
				enemies[enemy].take_dmg(magic_dmg)

				print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)
			if enemies[enemy].get_hp() == 0:
				print (enemies[enemy].name.replace(" ", "") +" has died!!")
				del enemies[enemy]

		elif index == 2 :
			player.choose_item()
			item_choice = int(input("    Choose item: ")) - 1	

			if item_choice == -1:
				continue	
				
			item = player.items[item_choice]["item"]
			if player.items[item_choice]["quantity"] == 0:
				print(bcolors.FAIL + "\n" + "None Left ..." + bcolors.ENDC)
				continue		
			player.items[item_choice]["quantity"] -= 1


			if item.type == "potion":
				player.heal(item.prop)
				print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop) + "HP", bcolors.ENDC)

			elif item.type == "elixer":
				if item.name == "MegaElixer":
					for i in players:
						i.hp = i.maxhp
						i.mp = i.maxmp
					else:
						player.hp = player.maxhp
						player.mp = player.maxmp
				print (bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
			
			elif item.type == "attack":
				enemy = player.choose_target(enemies)
				enemies[enemy].take_dmg(item.prop)

				print (bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "point of damage to " + enemies[enemy].name + bcolors.ENDC)

				if enemies[enemy].get_hp() == 0:
					print (enemies[enemy].name.replace(" ", "") +" has died!!")
					del enemies[enemy]

	# check the battle is over or not
	defeated_enemies = 0
	defeated_players = 0

	for enemy in enemies :
		if enemy.get_hp() == 0:
			defeated_enemies += 1

	for player in players :
		if player.get_hp() == 0:
			defeated_enemies += 1

	# check if player won
	if defeated_enemies == 2:
		print(bcolors.OKGREEN + "YOU WIN!" + bcolors.ENDC)
		running = False

	# check if enemies won
	elif defeated_players == 2:
		print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
		running = False
	print("\n")
	# enemy attack phase 
	for enemy in enemies:
		enemy_choice = random.randrange (0, 2)

		if enemy_choice == 0:
			target = random.randrange (0 ,3)
			enemy_dmg = enemies[0].generate_damage()
			players[target].take_dmg(enemy_dmg)
			print(enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "") + " for", enemy_dmg)
				

		elif enemy_choice == 1:
			spell, magic_dmg = enemy.choose_enemy_spell()
			
			enemy.reduce_mp(spell.cost)
			if spell.type == "White":
				enemy.heal(magic_dmg)
				print(bcolors.OKBLUE  + spell.name + " heals " + enemy.name + " for", str(magic_dmg), ".HP", bcolors.ENDC)
			elif spell.type == "black":
				target = random.randrange (0 ,3)
				players[target].take_dmg(magic_dmg)

				print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + "'s" + spell.name + " deals", str(magic_dmg), "points of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)
			if players[target].get_hp() == 0:
				print (players[target].name.replace(" ", "") + " has died!!")
				del players[target]
			print("Enemy chose ", spell.name, "damage is ", magic_dmg)





