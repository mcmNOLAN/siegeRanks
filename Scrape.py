import os

from bs4 import BeautifulSoup
import requests
import pandas as pd

users = ["MARKcmn", "markxk", "GIGOligaLO", "MarkyDJM", "Killz%20n%20Thrills", "xcharlieMAsheen"]  # Users being queried
gamertags = []
user_ranks = []  # Empty list storing ranks
user_mmr = []  # Empty list storing mmr
top_attacker = []
top_defender = []
KillDeath = []
killsMatch = []
winPercentage = []
textFile = open('Siege Ranks.txt',"w+")


def getUserRank(user):
    webPage = requests.get("https://r6.tracker.network/profile/xbox/" + user)  # Getting web page
    soup = BeautifulSoup(webPage.content, "html.parser")  # Creating "Beautiful Soup" object from web page
    name = soup.find(attrs={'class': 'trn-profile-header__name'}).findChild().get_text()  # pulling back username
    mmr = soup.find(attrs={'class': 'r6-season-rank__progress-fill'}).findChild().get_text()  # pulling back mmr
    rank = soup.find(attrs={'class': 'trn-text--dimmed trn-text--center'}).get_text()  # pulling back rank
    gamertags.append(name)
    user_ranks.append(rank)
    user_mmr.append(mmr)

def getTops(user):
    webPage = requests.get("https://r6.tracker.network/profile/xbox/" + user + "/operators?seasonal=1")  # Getting web page
    soup = BeautifulSoup(webPage.content, "html.parser")  # Creating "Beautiful Soup" object from web page
    attacker = soup.find(attrs={'style': 'display: flex; align-items: center;'}).findChildren()[1].get_text()  # pulling back top attacker
    defender = soup.find(attrs={'id': 'operators-Defenders'}).findChildren()[16].get_text()  # pulling back top defender
    top_attacker.append(attacker)
    top_defender.append(defender.replace("\n", ""))

def getStats(user):
    webPage = requests.get("https://r6.tracker.network/profile/xbox/" + user + "/seasons")  # Getting web page
    soup = BeautifulSoup(webPage.content, "html.parser")  # Creating "Beautiful Soup" object from web page
    kd = soup.findAll(attrs={'class': 'trn-defstat__value'})[0].get_text()  # pulling back top k/d
    killsPerMatch = soup.findAll(attrs={'class': 'trn-defstat__value'})[1].get_text()  # pulling back Kills/match
    winPercent = soup.findAll(attrs={'class': 'trn-defstat__value'})[4].get_text()  # pulling back top win %
    KillDeath.append(kd)
    killsMatch.append(killsPerMatch)
    winPercentage.append(winPercent)

for user in users:  # Iterating through users array
    getUserRank(user)  # Saving returned values from function to list
    getTops(user)
    getStats(user)

myDataFrame = pd.DataFrame({"Gamertag": gamertags, "Rank": user_ranks, "MMR": user_mmr, "Top Attacker": top_attacker, "Top Defender": top_defender, "K/D": KillDeath, "Kills/Match": killsMatch, "Win %": winPercentage})  # Creating a data frame from the dictionary
textFile.write(myDataFrame.to_string())
textFile.close()
