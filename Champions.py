class Champions:
    def __init__(self, hp, rp, ap, name, title, code, rp_name, attack_list, specials_list):
        #Health Point
        self.hp = hp
        #Resource Point
        self.rp = rp
        #Attack Power
        self.ap = ap
        #Set name
        self.name = name
        #Set Title
        self.title = title
        #Set Code
        self.code = code
        #Resource Power Name
        self.rp_name = rp_name
        #Possible attacks List
        self.attack_list = attack_list
        #Possible Special Abilities List
        self.specials_list = specials_list
#Tanks:
#MNK
MONK = Champions(2000, 100, 150, 'Feramon, the Monk', "Monk", "MNK", "Focus", ["Palm Strike", "Leg Sweep"], ["Harmonize", "Pressure Points"])
#BBR
BARBARIAN = Champions(2250, 100, 150, 'Baralor, the Barbarian', "Barbarian", "BBR", "Rage", ["Bloodthirst", "Pulverize"], ["Challenging Shout", "Impactful Boast"])
#VBG
VETERAN_BODYGUARD = Champions(2000, 0, 150, 'Hecutis, the Veteran Bodyguard', "Veteran Bodyguard", "VBG", "null", ["Shield Bash", "Trainwreck"], ["Fortification", "Block"])
#MTF
MASTER_FENCER = Champions(2000, 0, 150, 'Lorelai, the Master Fencer', "Fencer", "MTF", "null", ["Pierce", "Disruptive Slash"], ["Parry", "Elusive Measures"])

#DPS:

#Melee
#BKR
BERSERKER = Champions(1000, 100, 400, 'Kelzarg, the Berserker', "Berserkser", "BKR", "Rage", ["Raging Blow", "Rampage"], ["Enrage", "Reckless Flurry"])
#RGE
ROGUE = Champions(1000, 0, 400, 'Ryker, the Rogue', "Rogue", "RGE", "null", ["Serrated Slash", "Eviscerate"], ["Garrote", "Exploit Weakness"])
#SRV
SURVIVALIST = Champions(1000, 0, 400, 'Mally, the Survivalist', "Survivalist", "SRV", "null", ["Spear Thrust", "Scrap Bomb"], ["Play Dead", "Rushed Rest"])
#BST
BRAWLIST = Champions(1250, 0, 400, 'George, the Brawlist', "Brawlist", "BST", "null", ["Tactical Punch", "Uppercut"], ["Defensive Stance", "Rushdown"])

#Magic
#ADM
ACADEMIC_MAGE = Champions(1000, 200, 400, 'Tulip, the Academic Mage', "Academics Mage", "ADM", "Mana", ["Frost Bolt", "Fireball"], ["Arcane Brilliance", "Magical Barrier"])
#DRD
DRUID = Champions(1000, 200, 400, 'Fuds, the Druid', "Druid", "DRD", "Mana", ["Venus-fly Snap", "Vine-Swipe"], ["Thorns", "Prickle Arena"])
#WRK
WARLOCK = Champions(1000, 200, 400, "Sol'ghar, the Warlock", "Warlock", "WRK", "Mana", ["Black Bolt", "Void Infusion"], ["Wound Fissure", "Soul Tap"])
#BDM
BLOODMANCER = Champions(1000, 0, 400, 'Flynn, the Bloodmancer', "Bloodmancer", "BDM", "Health", ["Drain Life", "Blood Spike"], ["Blood Boil", "Enharden Nerves"])

#Mixed
#PLD
PALADIN = Champions(1000, 0, 400, 'Olig, the Paladin', "Paladin", "PLD", "null", ["Overhand Justice", "Righteous Blow"], ["Aura of Power", "Aura of Protection"])
#CLR
CASTLE_RANGER = Champions(1000, 0, 400, 'Brad, the Castle Ranger', "Ranger", "CLR", "null", ["Steady Shot", "Power Opt"], ["Equip Iron-cast Arrows", "Equip Tracker-tipped Arrows"])
#THD
THUNDER_APPRENTICE = Champions(1000, 0, 400, "Kel'ther, the Thunders Apprentice", "Thunderous Apprentice", "THD", "null", ["Lightning Bolt", "Chain Lightning"], ["Crashing Boom", "Thunderous Vigor"])
#PWC
POWER_CONDUIT = Champions(1000, 3, 0, 'Power Conduit', "Power Conduit", "PWC", "Charges", [], ["Muscle Enlarger", "Mistic Bloom", "Power Surge", "Full Potential"])

#Healers:
#ESP
EARTH_SPEAKER = Champions(1000, 200, 150, "Delmanar, the Earth's Speaker", "Earth Speaker", "ESP", "Mana", ["Rock Barrage"], ["Healing Surge", "Rejuvenating Whirlpool", "Boulder Cocoon"])
#PRS
PRIEST_OF_THE_DEVOTED = Champions(1000, 200, 150, 'Sethuk, Priest of the Devoted', "Priest", "PRS", "Mana", ["Shimmering Bolt", "Divine Smite"], ["Healing Light", "Diffracting Nova"])
#TWK
TIME_WALKER = Champions(1000, 200, 150, 'Zaqner, the Time Walker', "Time Walker", "TWK", "Mana", ["Cybernetic Blast"], ["Nanoheal Bots", "Reverse Wounds", "Alter Time"])
#FDM
CHILD_OF_MEDICINE = Champions(1000, 0, 150, 'Curie, a Child of Medicine', "Field Medic", "FDM", "null", ["Throw Scissors"], ["Bandage Wound", "Perfected Herbal Tea", "G.3.T  J.A.X.D"])