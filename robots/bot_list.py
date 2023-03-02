import importlib  

from robots.short_sighted_steve import ShortSightedSteve

RamboTheRando = importlib.import_module("robots.coding-challenge-bot-template.rambo_the_rando").RamboTheRando
DanielsRobot = importlib.import_module("robots.DanielsRobot.Daniels_Bot").Daniels_Bot

# Add new bots to the bottom of this list
# to maintain the same colours as much as possible
BotList = [
    RamboTheRando,
    ShortSightedSteve,
    DanielsRobot
]