import importlib

from robots.short_sighted_steve import ShortSightedSteve

RamboTheRando = importlib.import_module("robots.coding-challenge-bot-template.rambo_the_rando").RamboTheRando
DanielsRobot = importlib.import_module("robots.DanielsRobot.Daniels_Bot").Daniels_Bot
JorikAtilla = importlib.import_module("robots.jorik.atilla").AtillaTheAttacker
TheCluelessAfrican = importlib.import_module("robots.jp.The_no_clue_African").TheCluelessAfrican
BigAssBot = importlib.import_module("robots.mahmoud.big_ass_bot").BigAssBot
ch34tsRus = importlib.import_module("robots.lewie.ch34tsRus").ch34tsRus
RickbrandtVanRijn = importlib.import_module("robots.rick.RickbrandtVanRijn").RickbrandtVanRijn
Vector = importlib.import_module("robots.ishu.vector").Vector
Greedy = importlib.import_module("robots.rayman.greedy").Greedy
id10plus_bot = importlib.import_module("robots.tim.id10+_bot").id10plus_bot
ShortSpanDog = importlib.import_module("robots.felipe.short_span_dog").ShortSpanDog
LearoundoDaVinci = importlib.import_module("robots.hein-leo.learoundo_da_vinci").LearoundoDaVinci
RapidRothko = importlib.import_module("robots.jorik.rapid").RapidRothko
Kadabra = importlib.import_module("robots.rayman.astar").Kadabra
Alakazam = importlib.import_module("robots.rayman.astar").Alakazam
FurryBot = importlib.import_module("robots.furbot.furbot").FurryBot
Schumi = importlib.import_module("robots.furbot.furbot").Schumi
LeonardoDaVidi = importlib.import_module("robots.bram.leonardo_da_vidi").LeonardoDaVidi
Rokusho = importlib.import_module("robots.rokus.rokusho").Rokusho
SwiftSweeper = importlib.import_module("robots.jerrel.swift_sweeper").SwiftSweeper
HarryPlotter = importlib.import_module("robots.bram.harry_plotter").HarryPlotter
ChasingBots = importlib.import_module("robots.jerrel2.chasingbots").ChasingBots

# Add new bots to the bottom of this list
# to maintain the same colours as much as possible
BotList = [
    FurryBot,
    LeonardoDaVidi,
    DanielsRobot,
    JorikAtilla,
    TheCluelessAfrican,
    BigAssBot,
    ch34tsRus,
    SwiftSweeper,
    RickbrandtVanRijn,
    Vector,
    Alakazam, # A bot has evolved!
    id10plus_bot,
    ShortSpanDog,
    LearoundoDaVinci,
    RapidRothko,
    Kadabra,
    Schumi,
    Rokusho,
    HarryPlotter,
    ChasingBots,

    # Template bots are not part of the finals
    # RamboTheRando,
    # ShortSightedSteve,
]