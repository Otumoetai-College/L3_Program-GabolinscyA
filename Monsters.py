class Monsters:
    def __init__(self, hp, ap, rp, rp_name, name, nickname, enter_word, attack_list, ai_spawned):
        #Health Point
        self.hp = hp
        # Attack Power
        self.ap = ap
        #Resource Point
        self.rp = rp
        # Resource Power Name
        self.rp_name = rp_name
        #Set name
        self.name = name
        #Set Nickname
        self.nickname = nickname
        #Set Combat Entry Word
        self.enter_word = enter_word
        #Set Code
        self.attack_list = attack_list
        #Set the amount of AI enemies there will be
        self.ai_spawned = ai_spawned

GROTHAK_THE_DESTROYER = Monsters(3000, 100, 0, "null", "Grothak the Destroyer", "Grothak", "", ["Club Slam"], 1)

WORMPULP_BROTHERS = Monsters(1500, 50, 100, "Scent", "Wormpulp Brothers", "Wormpulp Brother", "the", ["Violent Thrash"], 2)

SIREN_TRIPLETS = Monsters(1000, 33, 200, "Mana", "Siren Triplets", "Triplet", "the", ["Twilight Beam"], 3)

VEMONSKIN_TROGGIES = Monsters(750, 25, 0, "null", "Venomskin Troggies", "Venomskin Troggie", "a gang of", ["Spear Thrust"], 4)

GIANT_LOCUST_SWARM = Monsters(600, 20, 0, "null", "Giant Locust Swarm", "Giant Locust", "a", ["Bite"], 5)