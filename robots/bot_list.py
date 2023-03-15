import importlib  

from robots.short_sighted_steve import ShortSightedSteve

RamboTheRando = importlib.import_module("robots.coding-challenge-bot-template.rambo_the_rando").RamboTheRando
DanielsRobot = importlib.import_module("robots.DanielsRobot.Daniels_Bot").Daniels_Bot
JorikAtilla = importlib.import_module("robots.jorik.atilla").AtillaTheAttacker
TheCluelessAfrican = importlib.import_module("robots.jp.The_no_clue_African").TheCluelessAfrican
BigAssBot = importlib.import_module("robots.mahmoud.big_ass_bot").BigAssBot
ch34tsRus = importlib.import_module("robots.lewie.ch34tsRus").ch34tsRus
Aslan = importlib.import_module("robots.hakan.aslan").Aslan

# Add new bots to the bottom of this list
# to maintain the same colours as much as possible
BotList = [
    RamboTheRando,
    ShortSightedSteve,
    DanielsRobot,
    JorikAtilla,
    TheCluelessAfrican,
    BigAssBot,
    ch34tsRus,
    Aslan,
]