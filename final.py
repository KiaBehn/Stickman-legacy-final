class Player:
    """
    This class is for handling things related to player during game
    """
    def __init__(self, dragon_hp):
        self.coin = 500
        self.dragon_alive = True
        self.dragon_hp = dragon_hp
        self.time = 0

        self.army_size = 0
        self.army_num = 1
        self.miners = 0
        self.miners_working = 0

        self.swordwraths = 0
        self.archidons = 0
        self.speartons = 0
        self.magikills = 0
        self.giants = 0

        self.army_list = []

    def add_miner(self):
        if not self.dragon_alive:
            print("game over")
            write_in_file("game over")
        elif self.coin < 150:
            print("not enough money")
            write_in_file("not enough money")
        elif (self.army_size + 1) > 50:
            print("too many army")
            write_in_file("too many army")
        else:
            if self.miners <= 8:
                self.miners_working += 1
                working = True
            else:
                working = False
            self.army_list.append(Troop(self.army_num, working, 100, 0, "Miner", 1, 10))
            self.miners += 1
            self.army_size += 1
            self.army_num += 1
            self.coin -= 150

    def add_swordwrath(self):
        if not self.dragon_alive:
            print("game over")
            write_in_file("game over")
        elif self.coin < 125:
            print("not enough money")
            write_in_file("not enough money")
        elif (self.army_size + 1) > 50:
            print("too many army")
            write_in_file("too many army")
        else:
            self.army_list.append(Troop(self.army_num, True, 120, 20, "Swordwrath", 1, 1))
            self.army_size += 1
            self.army_num += 1
            self.swordwraths += 1
            self.coin -= 120

    def add_archidon(self):
        if not self.dragon_alive:
            print("game over")
            write_in_file("game over")
        elif self.coin < 300:
            print("not enough money")
            write_in_file("not enough money")
        elif (self.army_size + 1) > 50:
            print("too many army")
            write_in_file("too many army")
        else:
            self.army_list.append(Troop(self.army_num, True, 80, 10, "Archidon", 1, 1))
            self.army_size += 1
            self.army_num += 1
            self.archidons += 1
            self.coin -= 300

    def add_spearton(self):
        if not self.dragon_alive:
            print("game over")
            write_in_file("game over")
        elif self.coin < 500:
            print("not enough money")
            write_in_file("not enough money")
        elif (self.army_size + 2) > 50:
            print("too many army")
            write_in_file("too many army")
        else:
            self.army_list.append(Troop(self.army_num, True, 250, 35, "Spearton", 2, 3))
            self.army_size += 3
            self.army_num += 1
            self.speartons += 1
            self.coin -= 500

    def add_magikill(self):
        if not self.dragon_alive:
            print("game over")
            write_in_file("game over")
        elif self.coin < 1200:
            print("not enough money")
            write_in_file("not enough money")
        elif (self.army_size + 4) > 50:
            print("too many army")
            write_in_file("too many army")
        else:
            self.army_list.append(Troop(self.army_num, True, 80, 200, "Magikill", 4, 5))
            self.army_size += 4
            self.army_num += 1
            self.magikills += 1
            self.coin -= 1200

    def add_giant(self):
        if not self.dragon_alive:
            print("game over")
            write_in_file("game over")
        elif self.coin < 1500:
            print("not enough money")
            write_in_file("not enough money")
        elif (self.army_size + 4) > 50:
            print("too many army")
            write_in_file("too many army")
        else:
            self.army_list.append(Troop(self.army_num, True, 1000, 150, "Giant", 4, 4))
            self.army_size += 4
            self.army_num += 1
            self.giants += 1
            self.coin -= 1500

    def miner_death(self):
        if self.miners <= 8:
            self.miners -= 1
            self.miners_working -= 1
            return
        for troop in self.army_list:
            if troop.name == "Miner" and not troop.working:
                troop.working = True
                self.miners -= 1
                return
        self.miners -= 1
        self.miners_working -= 1
        return

    def swordwrath_death(self):
        self.swordwraths -= 1

    def archidon_death(self):
        self.archidons -= 1

    def speartons_death(self):
        self.speartons -= 1

    def magikill_death(self):
        self.magikills -= 1

    def giant_death(self):
        self.giants -= 1

# This handles the damage that was given to troops by dragon
    def damage(self, damage_receiver, damage_amount):
        for troop in self.army_list:
            if troop.name == damage_receiver:
                death_flag, size_of_troop_flag, hp, class_type = troop.damage_calc(damage_amount)
                if death_flag:
                    self.army_list.remove(troop)
                    self.army_size -= size_of_troop_flag
                    if class_type == "Miner":
                        self.miner_death()
                    elif class_type == "Swordwrath":
                        self.swordwrath_death()
                    elif class_type == "Archidon":
                        self.archidon_death()
                    elif class_type == "Spearton":
                        self.speartons_death()
                    elif class_type == "Magikill":
                        self.magikill_death()
                    elif class_type == "Giant":
                        self.giant_death()
                    return
                else:
                    print(hp)
                    write_in_file(str(hp))
                    return
        print("no matter")
        write_in_file("no matter")

    def enemy_status(self):
        if not self.dragon_alive:
            print("game over")
            write_in_file("game over")
            return
        else:
            print(int(self.dragon_hp))
            write_in_file(str(int(self.dragon_hp)))

    def army_status(self):
        if not self.dragon_alive:
            print("game over")
            write_in_file("game over")
            return
        else:
            print(self.miners, self.swordwraths, self.archidons, self.speartons, self.magikills, self.giants)
            text_to_show = str(self.miners) + " " + str(self.swordwraths) + " " + str(self.archidons) + " "
            text_to_show += str(self.speartons) + " " + str(self.magikills) + " " + str(self.giants)
            write_in_file(text_to_show)

    def money_status(self):
        if not self.dragon_alive:
            print("game over")
            write_in_file("game over")
            return
        else:
            print(int(self.coin))
            write_in_file(str(int(self.coin)))

    # calculates the money that was given to us by government
    def government_money_calc(self, initial_time, end_time) -> int:
        cycle_gov = 20
        time_spent = end_time - initial_time
        cycle_counter_gov = initial_time % cycle_gov
        return 180 * ((time_spent + cycle_counter_gov) // cycle_gov)

    # calculates the money and damages from troops
    def money_damage_calc(self, initial_time, end_time):
        total_money = total_damage = 0
        for troop in self.army_list:
            if troop.class_type == "Miner":
                total_money += troop.money_calc_cycle(initial_time, end_time)
            else:
                total_damage += troop.damage_calc_cycle(initial_time, end_time)
        total_money += self.government_money_calc(initial_time, end_time)
        self.coin += total_money
        self.dragon_hp -= total_damage
        if self.dragon_hp <= 0:
            self.dragon_alive = False


class Troop:
    """
    This class is for troops and handling them
    """
    def __init__(self, num, working, hp, damage, class_type, size_of_troop, cycle):
        self.name = num
        self.working = working
        self.hp = hp
        self.damage = damage
        self.class_type = class_type
        self.size_of_troop = size_of_troop
        self.cycle = cycle
        self.cycle_counter = 1
        self.show()

    # Calculates the damage that was given to troops by dragon
    def damage_calc(self, damage_amount):
        if self.hp <= damage_amount:
            print("dead")
            write_in_file("dead")
            self.hp = 0
            return True, self.size_of_troop, 0, self.class_type
        else:
            self.hp -= damage_amount
            return False, 0, self.hp, self.class_type

    # calculates the damage that will be done to dragon each cycle
    def damage_calc_cycle(self, initial_time, end_time):
        time_spent = end_time - initial_time
        self.cycle_counter = initial_time % self.cycle
        return self.damage * ((time_spent + self.cycle_counter) // self.cycle)

    def money_calc_cycle(self, initial_time, end_time):
        time_spent = end_time - initial_time
        self.cycle_counter = initial_time % self.cycle
        return 100 * ((time_spent + self.cycle_counter) // self.cycle)

    def show(self):
        print(self.name)
        write_in_file(str(self.name))


def truncate_float(float_number, decimal_places):
    multiplier = 10 ** decimal_places
    return int(float_number * multiplier) / multiplier


# changes the file numbers into time
def time_file_to_number(time_to_number) -> int:
    mins_str, secs_str, mil_secs_str = time_to_number.split(":")
    mins = int(mins_str)
    secs = int(secs_str)
    mil_secs = int(mil_secs_str)
    return mins * 60 + secs + (mil_secs / 1000)


def read_from_file(init_time):
    initial_time = init_time
    first_flag = True
    with open("commands.txt", mode="r") as commands:
        for command in commands:
            if first_flag:
                command_numbers_str, dragon_hp_str = command.split()
                command_numbers = int(command_numbers_str)
                dragon_hp = int(dragon_hp_str)
                player = Player(dragon_hp)
                first_flag = False
            else:
                if "add" in command:
                    command_part, role, timestamp = command.split()
                    end_time = time_file_to_number(timestamp)
                    if role == "miner":
                        player.money_damage_calc(initial_time, end_time)
                        player.add_miner()
                    elif role == "swordwrath":
                        player.money_damage_calc(initial_time, end_time)
                        player.add_swordwrath()
                    elif role == "archidon":
                        player.money_damage_calc(initial_time, end_time)
                        player.add_archidon()
                    elif role == "spearton":
                        player.money_damage_calc(initial_time, end_time)
                        player.add_spearton()
                    elif role == "magikill":
                        player.money_damage_calc(initial_time, end_time)
                        player.add_magikill()
                    elif role == "giant":
                        player.money_damage_calc(initial_time, end_time)
                        player.add_giant()
                    initial_time = end_time

                elif "money-status" in command:
                    command_part, timestamp = command.split()
                    end_time = time_file_to_number(timestamp)
                    player.money_damage_calc(initial_time, end_time)
                    player.money_status()
                    initial_time = end_time

                elif "army-status" in command:
                    command_part, timestamp = command.split()
                    end_time = time_file_to_number(timestamp)
                    player.money_damage_calc(initial_time, end_time)
                    player.army_status()
                    initial_time = end_time

                elif "enemy-status" in command:
                    command_part, timestamp = command.split()
                    end_time = time_file_to_number(timestamp)
                    player.money_damage_calc(initial_time, end_time)
                    player.enemy_status()
                    initial_time = end_time

                elif "damage" in command:
                    command_part, recieve_id, damage_amount, timestamp = command.split()
                    end_time = time_file_to_number(timestamp)
                    player.damage(int(recieve_id), int(damage_amount))
                    player.money_damage_calc(initial_time, end_time)
                    initial_time = end_time


def write_in_file(text_to_write):
    text_to_file.write(text_to_write + "\n")


text_to_file = open("output.txt", mode="w")
initial_time_overall = 0
read_from_file(initial_time_overall)
