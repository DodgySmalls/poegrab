import subprocess
import re

filename = "formatted.txt"
url = ["http://pathofexile.com/item-data/weapon", "http://pathofexile.com/item-data/armour"]
itemlists = [None]*100

#an optional list to ignore items you probably don't want to filter out, this list is subjective and will require manual ammendments based on preference
#I'm especially neglegent of caster weapons since I include all rare wands/sceptres in my personal filter
bestinslot = ["Thicket Bow", "Ranger Bow", "Assassin Bow", "Spine Bow", "Imperial Bow", "Harbinger Bow", "Maraketh Bow",
			   "Hellion's Paw", "Vaal Claw", "Imperial Claw", "Gemini Claw",
			   "Ambusher", "Imperial Skean", "Sai",
			   "Siege Axe", "Infernal Axe", "Runic Hatchet", "Vaal Hatchet",
			   "Behemoth Mace",
			   "Eternal Sword", "Legion Sword", "Vaal Blade", "Tiger Hook",
			   "Sambar Sceptre",
			   "Lathi", "Eclipse Staff",  #a note that maelstrom staff is not grabbed by my script, "Maelstr" does match the basetype uniquely
			   "Spiraled Foil", "Jewelled Foil", "Dragoon Sword", "Pecoraro",
			   "Vaal Axe", "Despot Axe", "Void Axe", "Ezomyte Axe", "Talon Axe",
			   "Piledriver", "Meatgrinder","Coronal Maul",
			   "Lion Sword","Infernal Sword","Exquisite Blade", 
			   "Imbued Wand", "Profane Wand",
			   "Sacrificial Garb", "Carnal Armour", "Saintly Chainmail", "Assassin's Garb", "Glorious Plate", "Saint's Hauberk", "Sadist Garb", "Vaal Regalia",
			   "Slink Boots", "Murder Boots", "Titan Greaves", "Sorcerer Boots", "Crusader Boots",
			   "Slink Gloves", "Titan Gauntlets", "Sorcerer Gloves", "Dragonscale Gauntlets", "Murder Mitts",
			   "Lion Pelt", "Hubris Circlet", "Eternal Burgonet", "Praetor Crown", "Deicide Mask", "Royal Burgonet", "Ezomyte Burgonet", "Silken Hood",
			   "Colossal Tower Shield", "Supreme Spiked Shield", "Imperial Buckler", "Titanium Spirit Shield", "Harmonic Spirit Shield", "Archon Kite Shield"]

#options to grab a page's source and push it to stdout, leading ' ' is necessary
options = " -q -O -"
	
for page in url:
	command = "wget " + page + options 

	#catch stdout of the above command
	process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
	output = process.communicate()[0]	#output now contains the page's source

	#we're using regex to manually search the string to avoid any more libraries
	#DOTALL is important as a workaround to allow us to grab across the newline character between <td> blocks, as is the (.*?) to avoid matching the entire src
	data = re.findall(r'class="name">([a-zA-Z ]*)</td>.*?<td>([0-9]*)</td>', output, re.DOTALL)

	#data is now a list of tuple's ("item name string", "droplevel") for every entry of the page
	for entry in data:
		if not(bestinslot.__contains__(entry[0])): #exclude items named in our BIS list
			if(itemlists[int(entry[1])] == None):
				itemlists[int(entry[1])] = []
			(itemlists[int(entry[1])]).append(entry[0])
	#now itemlists[droplevel] contains a list of items with a minimum drop level as indicated, so we can generate itemfilter blocks easily for filters

#this sample will generate blocks so that items which are NOT 10 levels below the zone are displayed normally, you may want to write a reverse script where items which ARE below the zone are displayed with special properties
outfile = open(filename, "w")
i = 0
bufferval = 0

while(i<100):
	if itemlists[i] != None:
		sublist = itemlists[i]
		outfile.write("\nShow\n")
		outfile.write("    BaseType")
		
		for e in sublist:
			outfile.write(" \"" + e + "\"")
		
		if(i < 20):							#bracketing the range for acceptable items, higher level gear has less dropoff
			bufferval = 8
		elif(i < 50):
			bufferval = 10
		else:
			bufferval = 12

		outfile.write("\n    ItemLevel <= " + str(i + bufferval))
	i=i+1

outfile.write("\n\n#BIS block\nShow\n    BaseType")

for bis in bestinslot:
	outfile.write(" \"" + bis + "\"")

outfile.close()
print "done"