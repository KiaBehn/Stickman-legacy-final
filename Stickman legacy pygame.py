import pygame
import random
import os
import time


class Player:
    def __init__(self, dragon_hp):
        self.coin = 500
        self.dragon_alive = True
        self.dragon_hp = dragon_hp

        self.time = 0
        self.miners = 0
        self.miners_working = 0

        self.swordwraths = 0
        self.archidons = 0
        self.speartons = 0
        self.magikills = 0
        self.giants = 0

        self.army_size = 0
        self.army_num = 1

        self.army_list = []

    def add_miner(self):
        if not self.dragon_alive:
            draw_custom_text("game over")
        elif self.coin < 150:
            draw_custom_text("not enough money")
        elif (self.army_size + 1) > 50:
            draw_custom_text("no room in the army")
        else:
            if self.miners <= 8:
                self.miners_working += 1
                working = True
            else:
                working = False
            self.army_list.append(Troop(self.army_num, working, 100, 0, "Miner", 1, 10, self.time))
            self.miners += 1
            self.army_size += 1
            self.army_num += 1
            self.coin -= 150
            draw_scroll()
            draw_miner_played()
            wait_to_show()

    def add_swordwrath(self):
        if not self.dragon_alive:
            draw_custom_text("game over")
        elif self.coin < 125:
            draw_custom_text("not enough money")
        elif (self.army_size + 1) > 50:
            draw_custom_text("no room in the army")
        else:
            self.army_list.append(Troop(self.army_num, True, 120, 20, "Swordwrath", 1, 1, self.time))
            self.army_size += 1
            self.army_num += 1
            self.swordwraths += 1
            self.coin -= 120
            draw_scroll()
            draw_knight_played()
            wait_to_show()

    def add_archidon(self):
        if not self.dragon_alive:
            draw_custom_text("game over")
        elif self.coin < 300:
            draw_custom_text("not enough money")
        elif (self.army_size + 1) > 50:
            draw_custom_text("no room in the army")
        else:
            self.army_list.append(Troop(self.army_num, True, 80, 10, "Archidon", 1, 1, self.time))
            self.army_size += 1
            self.army_num += 1
            self.archidons += 1
            self.coin -= 300
            draw_scroll()
            draw_archer_played()
            wait_to_show()

    def add_spearton(self):
        if not self.dragon_alive:
            draw_custom_text("game over")
        elif self.coin < 500:
            draw_custom_text("not enough money")
        elif (self.army_size + 2) > 50:
            draw_custom_text("no room in the army")
        else:
            self.army_list.append(Troop(self.army_num, True, 250, 35, "Spearton", 2, 3, self.time))
            self.army_size += 3
            self.army_num += 1
            self.speartons += 1
            self.coin -= 500
            draw_scroll()
            draw_spearman_played()
            wait_to_show()

    def add_magikill(self):
        if not self.dragon_alive:
            draw_custom_text("game over")
        elif self.coin < 1200:
            draw_custom_text("not enough money")
        elif (self.army_size + 4) > 50:
            draw_custom_text("no room in the army")
        else:
            self.army_list.append(Troop(self.army_num, True, 80, 200, "Magikill", 4, 5, self.time))
            self.army_size += 4
            self.army_num += 1
            self.magikills += 1
            self.coin -= 1200
            draw_scroll()
            draw_wizard_played()
            wait_to_show()

    def add_giant(self):
        if not self.dragon_alive:
            draw_custom_text("game over")
        elif self.coin < 1500:
            draw_custom_text("not enough money")
        elif (self.army_size + 4) > 50:
            draw_custom_text("no room in the army")
        else:
            self.army_list.append(Troop(self.army_num, True, 1000, 150, "Giant", 4, 4, self.time))
            self.army_size += 4
            self.army_num += 1
            self.giants += 1
            self.coin -= 1500
            draw_scroll()
            draw_giant_played()
            wait_to_show()

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

    def damage(self, damage_receiver, damage_amount):
        for troop in self.army_list:
            if troop.name == damage_receiver:
                troop.damage_calc_troop(damage_amount)
                if not troop.alive:
                    self.army_size -= troop.size_of_troop
                    if troop.class_type == "Miner":
                        self.miner_death()
                    elif troop.class_type == "Swordwrath":
                        self.swordwrath_death()
                    elif troop.class_type == "Archidon":
                        self.archidon_death()
                    elif troop.class_type == "Spearton":
                        self.speartons_death()
                    elif troop.class_type == "Magikill":
                        self.magikill_death()
                    elif troop.class_type == "Giant":
                        self.giant_death()

                    self.army_list.remove(troop)

    def coin_damage_calc(self):
        total_damage = 0
        for troop in self.army_list:
            if troop.class_type == "Miner":
                self.coin += troop.coin_calc_cycle()
            else:
                total_damage += troop.damage_calc_cycle()
        self.coin += self.government_coin_calc()
        if total_damage != 0:
            draw_custom_text("You dealt " + str(total_damage) + " total damage to the dragon...")
        self.dragon_hp -= total_damage

    def government_coin_calc(self) -> int:
        if self.time % 20 == 0 and not self.time == 0:
            return 180
        else:
            return 0

    def dragon_damage_cycle_calc(self):
        if self.time % 15 == 0 and not self.time == 0:
            damage_rec, damage = self.dragon_damage_calc()
            if damage_rec == -1:
                return
            else:
                for troop in self.army_list:
                    if troop.name == damage_rec:
                        self.damage(damage_rec, damage)
                        return

    def dragon_damage_calc(self):
        if self.army_num == 0:
            return -1, 0
        else:
            damage_rec = random.randrange(0, self.army_num)
            damage = random.randrange(10, 200, 10)
        return damage_rec, damage

    def round_calc(self):
        self.dragon_damage_cycle_calc()
        self.coin_damage_calc()
        if self.dragon_hp <= 0:
            self.dragon_alive = False
        self.time += 1


class Troop:
    def __init__(self, num, working, hp, damage, class_type, size_of_troop, cycle, time_added):
        self.working = working
        self.name = num
        self.working = working
        self.hp = hp
        self.damage = damage
        self.class_type = class_type
        self.size_of_troop = size_of_troop
        self.cycle = cycle
        self.alive = True
        self.time_added = time_added
        self.counter = 0

    def damage_calc_troop(self, damage_amount):
        if self.hp <= damage_amount:
            self.alive = False
            self.hp = 0
            draw_custom_text(self.class_type + " number " + str(self.name) + " died")
            time.sleep(1)
        else:
            self.hp -= damage_amount
            draw_custom_text(self.class_type + " number " + str(self.name) + " received " + str(damage_amount) +
                             " damage")
            time.sleep(1)

    def damage_calc_cycle(self):
        self.counter += 1
        if self.counter % self.cycle == 0:
            draw_custom_text(self.class_type + " number " + str(self.name) + " dealt " + str(self.damage))
            return self.damage
        else:
            return 0

    def coin_calc_cycle(self) -> int:
        self.counter += 1
        if self.counter % self.cycle == 0 and self.working:
            return 150
        else:
            return 0


def read_from_game_setting_file():
    with open("Game setting.txt", mode="r") as game_setting:
        for lines in game_setting:
            temp, dragon_hp = lines.split()
            return int(dragon_hp)


player = Player(read_from_game_setting_file())
pygame.init()

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickman legacy")


WHITE = (255, 255, 255)

FPS = 60

CARD_WIDTH = 152
CARD_HEIGHT = 200


# image_loading
BACKGROUND_IMAGE = pygame.image.load(os.path.join('Pictures', 'medieval pixel art.png'))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (1280, 720))

BACKGROUND_DETAILS_IMAGE = pygame.image.load(os.path.join('Pictures', 'background details.png'))
BACKGROUND_DETAILS = pygame.transform.scale(BACKGROUND_DETAILS_IMAGE, (1280, 720))

BACKGROUND_BARRACKS = pygame.image.load(os.path.join('Pictures', 'scroll_background.png'))

MINER_CARD_IMAGE = pygame.image.load(os.path.join("Pictures", "miner card.jpg"))
MINER_CARD_IMAGE_SELECT = pygame.image.load(os.path.join("Pictures", "miner card select.jpg"))
MINER_CARD = pygame.transform.scale(MINER_CARD_IMAGE, (CARD_WIDTH, CARD_HEIGHT))
MINER_CARD_SELECT = pygame.transform.scale(MINER_CARD_IMAGE_SELECT, (CARD_WIDTH, CARD_HEIGHT))

SKIP_CARD_IMAGE = pygame.image.load(os.path.join("Pictures", "Skip card.jpg"))
SKIP_CARD_IMAGE_SELECT = pygame.image.load(os.path.join("Pictures", "skip card select.jpg"))
SKIP_CARD = pygame.transform.scale(SKIP_CARD_IMAGE, (CARD_WIDTH, CARD_HEIGHT))
SKIP_CARD_SELECT = pygame.transform.scale(SKIP_CARD_IMAGE_SELECT, (CARD_WIDTH, CARD_HEIGHT))

KNIGHT_CARD_IMAGE = pygame.image.load(os.path.join("Pictures", "knight card.jpg"))
KNIGHT_CARD_IMAGE_SELECT = pygame.image.load(os.path.join("Pictures", "knight card select.jpg"))
KNIGHT_CARD = pygame.transform.scale(KNIGHT_CARD_IMAGE, (CARD_WIDTH, CARD_HEIGHT))
KNIGHT_CARD_SELECT = pygame.transform.scale(KNIGHT_CARD_IMAGE_SELECT, (CARD_WIDTH, CARD_HEIGHT))

ARCHER_CARD_IMAGE = pygame.image.load(os.path.join("Pictures", "archer card.jpg"))
ARCHER_CARD_IMAGE_SELECT = pygame.image.load(os.path.join("Pictures", "archer card select.jpg"))
ARCHER_CARD = pygame.transform.scale(ARCHER_CARD_IMAGE, (CARD_WIDTH, CARD_HEIGHT))
ARCHER_CARD_SELECT = pygame.transform.scale(ARCHER_CARD_IMAGE_SELECT, (CARD_WIDTH, CARD_HEIGHT))

SPEARMAN_CARD_IMAGE = pygame.image.load(os.path.join("Pictures", "spearman card.jpg"))
SPEARMAN_CARD_IMAGE_SELECT = pygame.image.load(os.path.join("Pictures", "spearman card select.jpg"))
SPEARMAN_CARD = pygame.transform.scale(SPEARMAN_CARD_IMAGE, (CARD_WIDTH, CARD_HEIGHT))
SPEARMAN_CARD_SELECT = pygame.transform.scale(SPEARMAN_CARD_IMAGE_SELECT, (CARD_WIDTH, CARD_HEIGHT))

WIZARD_CARD_IMAGE = pygame.image.load(os.path.join("Pictures", "wizard card.jpg"))
WIZARD_CARD_IMAGE_SELECT = pygame.image.load(os.path.join("Pictures", "wizard card select.jpg"))
WIZARD_CARD = pygame.transform.scale(WIZARD_CARD_IMAGE, (CARD_WIDTH, CARD_HEIGHT))
WIZARD_CARD_SELECT = pygame.transform.scale(WIZARD_CARD_IMAGE_SELECT, (CARD_WIDTH, CARD_HEIGHT))

GIANT_CARD_IMAGE = pygame.image.load(os.path.join("Pictures", "giant card.jpg"))
GIANT_CARD_IMAGE_SELECT = pygame.image.load(os.path.join("Pictures", "giant card select.jpg"))
GIANT_CARD = pygame.transform.scale(GIANT_CARD_IMAGE, (CARD_WIDTH, CARD_HEIGHT))
GIANT_CARD_SELECT = pygame.transform.scale(GIANT_CARD_IMAGE_SELECT, (CARD_WIDTH, CARD_HEIGHT))

DRAGON_CARD_IMAGE = pygame.image.load(os.path.join("Pictures", "dragon card.jpg"))
DRAGON_CARD = pygame.transform.scale(DRAGON_CARD_IMAGE, (CARD_WIDTH, CARD_HEIGHT))

SCROLL = pygame.image.load(os.path.join("Pictures", "scrolls.png"))


COIN_IMAGE = pygame.image.load(os.path.join("Pictures", "coin.png"))
COIN = pygame.transform.scale(COIN_IMAGE, (50, 50))


# Font
FONT_BIG_BIG = pygame.font.Font('Fonts/alagard.ttf', 64)
FONT_BIG = pygame.font.Font('Fonts/alagard.ttf', 34)
FONT = pygame.font.Font('Fonts/alagard.ttf', 26)
FONT_MEDIUM = pygame.font.Font('Fonts/alagard.ttf', 30)

DEFAULT_CARD_POSITION_X = 50
DEFAULT_CARD_POSITION_Y = 500
CARD_POS_CHANGE = 50


miner_price = 150
swordwrath_price = 125
archer_price = 300
spearton_price = 500
magikill_price = 1200
giant_price = 1500


def game_over_screen():
    WIN.blit(BACKGROUND_BARRACKS, (0, 30))
    counter_line = 200
    text_troop = FONT_BIG_BIG.render("GAME OVER...", True, (0, 0, 0))
    WIN.blit(text_troop, (350, counter_line))
    if player.dragon_alive:
        text_troop = FONT.render("YOU LOST", True, (0, 0, 0))
    else:
        text_troop = FONT.render("YOU WON THE DRAGON IS DEAD", True, (0, 0, 0))
    WIN.blit(text_troop, (350, counter_line + 100))


def draw_army_screen():
    WIN.blit(BACKGROUND_BARRACKS, (0, 30))
    counter_line = 160
    for troop in player.army_list:

        if troop.class_type == "Miner":
            text_troop = FONT.render("Miner: " + str(troop.name) + " " + str(troop.hp) + " HP", True, (0, 0, 0))

        elif troop.class_type == "Swordwrath":
            text_troop = FONT.render("Knight: " + str(troop.name) + " " + str(troop.hp) + " HP", True, (0, 0, 0))

        elif troop.class_type == "Archidon":
            text_troop = FONT.render("Archer: " + str(troop.name) + " " + str(troop.hp) + " HP", True, (0, 0, 0))

        elif troop.class_type == "Spearton":
            text_troop = FONT.render("Spearman: " + str(troop.name) + " " + str(troop.hp) + " HP", True, (0, 0, 0))

        elif troop.class_type == "Magikill":
            text_troop = FONT.render("Wizard: " + str(troop.name) + " " + str(troop.hp) + " HP", True, (0, 0, 0))

        elif troop.class_type == "Giant":
            text_troop = FONT.render("Giant: " + str(troop.name) + " " + str(troop.hp) + " HP", True, (0, 0, 0))

        WIN.blit(text_troop, (350, counter_line))
        counter_line += 20


def draw_background():
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(BACKGROUND_DETAILS, (0, 0))


def draw_coins_details():
    WIN.blit(COIN, (0, 0))
    overall_coins = FONT_BIG_BIG.render("COINS: " + str(player.coin), True, (0, 0, 0))
    WIN.blit(overall_coins, (60, 0))

    overall_time = FONT_BIG.render("ROUND: " + str(player.time), True, (0, 0, 0))
    WIN.blit(overall_time, (80, 60))

    price_txt = FONT.render("Price: " + str(player.coin), True, (0, 0, 0))
    WIN.blit(price_txt, (DEFAULT_CARD_POSITION_X, DEFAULT_CARD_POSITION_Y + 30))

    hp_txt = FONT.render(str(player.miners), True, (0, 0, 0))
    WIN.blit(hp_txt, (DEFAULT_CARD_POSITION_X + 230, DEFAULT_CARD_POSITION_Y - 170))

    hp_txt = FONT.render(str(player.swordwraths), True, (0, 0, 0))
    WIN.blit(hp_txt, (DEFAULT_CARD_POSITION_X + 390, DEFAULT_CARD_POSITION_Y - 170))

    hp_txt = FONT.render(str(player.archidons), True, (0, 0, 0))
    WIN.blit(hp_txt, (DEFAULT_CARD_POSITION_X + 550, DEFAULT_CARD_POSITION_Y - 170))

    hp_txt = FONT.render(str(player.speartons), True, (0, 0, 0))
    WIN.blit(hp_txt, (DEFAULT_CARD_POSITION_X + 710, DEFAULT_CARD_POSITION_Y - 170))

    hp_txt = FONT.render(str(player.magikills), True, (0, 0, 0))
    WIN.blit(hp_txt, (DEFAULT_CARD_POSITION_X + 870, DEFAULT_CARD_POSITION_Y - 170))

    hp_txt = FONT.render(str(player.giants), True, (0, 0, 0))
    WIN.blit(hp_txt, (DEFAULT_CARD_POSITION_X + 1030, DEFAULT_CARD_POSITION_Y - 170))


def draw_card_selected(index):
    if index == 0:
        WIN.blit(SKIP_CARD_SELECT, (DEFAULT_CARD_POSITION_X, DEFAULT_CARD_POSITION_Y - 10))
    elif index == 1:
        WIN.blit(MINER_CARD_SELECT, (DEFAULT_CARD_POSITION_X + 160, DEFAULT_CARD_POSITION_Y - 10))
    elif index == 2:
        WIN.blit(KNIGHT_CARD_SELECT, (DEFAULT_CARD_POSITION_X + 320, DEFAULT_CARD_POSITION_Y - 10))
    elif index == 3:
        WIN.blit(ARCHER_CARD_SELECT, (DEFAULT_CARD_POSITION_X + 480, DEFAULT_CARD_POSITION_Y - 10))
    elif index == 4:
        WIN.blit(SPEARMAN_CARD_SELECT, (DEFAULT_CARD_POSITION_X + 640, DEFAULT_CARD_POSITION_Y - 10))
    elif index == 5:
        WIN.blit(WIZARD_CARD_SELECT, (DEFAULT_CARD_POSITION_X + 800, DEFAULT_CARD_POSITION_Y - 10))
    elif index == 6:
        WIN.blit(GIANT_CARD_SELECT, (DEFAULT_CARD_POSITION_X + 960, DEFAULT_CARD_POSITION_Y - 10))


def draw_card(index):
    if not index == 0:
        WIN.blit(SKIP_CARD, (DEFAULT_CARD_POSITION_X, DEFAULT_CARD_POSITION_Y))
    if not index == 1:
        WIN.blit(MINER_CARD, (DEFAULT_CARD_POSITION_X + 160, DEFAULT_CARD_POSITION_Y))
    if not index == 2:
        WIN.blit(KNIGHT_CARD, (DEFAULT_CARD_POSITION_X + 320, DEFAULT_CARD_POSITION_Y))
    if not index == 3:
        WIN.blit(ARCHER_CARD, (DEFAULT_CARD_POSITION_X + 480, DEFAULT_CARD_POSITION_Y))
    if not index == 4:
        WIN.blit(SPEARMAN_CARD, (DEFAULT_CARD_POSITION_X + 640, DEFAULT_CARD_POSITION_Y))
    if not index == 5:
        WIN.blit(WIZARD_CARD, (DEFAULT_CARD_POSITION_X + 800, DEFAULT_CARD_POSITION_Y))
    if not index == 6:
        WIN.blit(GIANT_CARD, (DEFAULT_CARD_POSITION_X + 960, DEFAULT_CARD_POSITION_Y))
    if player.dragon_alive:
        WIN.blit(DRAGON_CARD, (520, 50))


def wait_to_show():
    pygame.display.update()
    time.sleep(1)


def draw_scroll():
    WIN.blit(SCROLL, (0, 0))


def draw_tutorial_hud():
    text_to_show = FONT.render("Press escape for army info...", True, (0, 0, 0))
    WIN.blit(text_to_show, (0, 225))


def draw_skip():
    text_to_show = FONT_BIG.render("You skipped a round...", True, (0, 0, 0))
    WIN.blit(text_to_show, (150, 225))


def draw_miner_played():
    text_to_show = FONT_BIG.render("You added a miner to your army...", True, (0, 0, 0))
    WIN.blit(text_to_show, (150, 225))


def draw_knight_played():
    text_to_show = FONT_BIG.render("You added a knight to your army...", True, (0, 0, 0))
    WIN.blit(text_to_show, (150, 225))


def draw_archer_played():
    text_to_show = FONT_BIG.render("You added an archer to your army...", True, (0, 0, 0))
    WIN.blit(text_to_show, (150, 225))


def draw_spearman_played():
    text_to_show = FONT_BIG.render("You added a spearman to your army...", True, (0, 0, 0))
    WIN.blit(text_to_show, (150, 225))


def draw_wizard_played():
    text_to_show = FONT_BIG.render("You added a wizard to your army...", True, (0, 0, 0))
    WIN.blit(text_to_show, (150, 225))


def draw_giant_played():
    text_to_show = FONT_BIG.render("You added a giant to your army...", True, (0, 0, 0))
    WIN.blit(text_to_show, (150, 225))


def draw_dragon_hp():
    dragon_hp = FONT_BIG.render(str(player.dragon_hp), True, (0, 0, 0))
    WIN.blit(dragon_hp, (950, 75))


def draw_custom_text(text_to_show):
    draw_scroll()
    text_to_show = FONT_BIG.render(text_to_show, True, (0, 0, 0))
    WIN.blit(text_to_show, (150, 225))
    wait_to_show()


def play_card(index):
    if index == 0:
        player.round_calc()
        draw_scroll()
        draw_skip()
        wait_to_show()

    elif index == 1:
        player.add_miner()
    elif index == 2:
        player.add_swordwrath()
    elif index == 3:
        player.add_archidon()
    elif index == 4:
        player.add_spearton()
    elif index == 5:
        player.add_magikill()
    elif index == 6:
        player.add_giant()


def main():
    game_over_flag = False
    army_menu_flag = False
    card_index = 0
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if game_over_flag and pygame.K_SPACE:
                    run = False
                if event.key == pygame.K_LEFT and not game_over_flag:
                    if card_index != 0:
                        card_index -= 1
                if event.key == pygame.K_RIGHT and not game_over_flag:
                    if card_index != 6:
                        card_index += 1
                if event.key == pygame.K_SPACE and not game_over_flag:
                    play_card(card_index)
                if event.key == pygame.K_ESCAPE and not game_over_flag:
                    if army_menu_flag:
                        army_menu_flag = False
                    else:
                        army_menu_flag = True

        if not player.dragon_alive:
            game_over_flag = True

        if game_over_flag:
            game_over_screen()
            pygame.display.update()

        elif not army_menu_flag:
            draw_background()
            draw_coins_details()
            draw_card(card_index)
            draw_dragon_hp()
            draw_card_selected(card_index)
            draw_tutorial_hud()
            pygame.display.update()

        elif army_menu_flag:
            draw_army_screen()
            pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
