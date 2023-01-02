from django.shortcuts import render

import mysql.connector
import datetime

#connexion au base de données
db = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "",
  database = "BE_Basket_MLD"
)

cur = db.cursor()


titles = []
titles += ["Les 10 joueurs qui ont marqué le plus grand nombre de points avec leur équipe national sont :"]
titles += ["Les 3 joueurs avec le meilleur pourcentage de lancer franc dans une final de championnat européen sont :"]
titles += ["Le club avec la plus haute moyenne de taille est : "]
titles += ["Le sponsor qui a sponsorisé le plus d'équipe nationale qui ont gagné les championnats du monde est : "]
titles += ["Pour chaque club le joueur qui a le meilleur pourcentage de 3 points dans la saison actuelle est : "]
titles += ["Pour un club particulier: le CSKA Moscou, le joueur qui a le plus d'assist par game est : "]
titles += ["Voici la liste des club qui ont gagné l'euroleague au moins 3 fois : "]


def questions(request):
    values = []
    values += [(getQuestion1(), titles[0], 1, "", "qui a marqué :", "points.", "")]
    values += [(getQuestion2(), titles[1], 2, "", "avec un pourcentage de :", ".", "")]
    values += [(getQuestion3(), titles[2], 3, "", "qui a une moyenne de taille de :", "cm.", "")]
    values += [(getQuestion4(), titles[3], 4, "", "avec :", "sponsorisation lors de finale.", "")]
    values += [(getQuestion5(), titles[4], 5, "", "qui a un pourcentage de 3 points de :", "avec :", ".")]
    values += [(getQuestion6(), titles[5], 6, "", "avec :", "assists.", "")]
    values += [(getQuestion7(), titles[6], 7, "", "qui a gagné les championnats du monde :", "fois.", "")]

    return render(request, 'questions.html', {"values": values})  





def getSql(sql):
  cur.execute(sql)
  value = cur.fetchall()
  return value

def getQuestion1():
  sql_10_player_total_point_for_national = "SELECT Name, SUM(2_pts*2+3_pts*3+free_throws) AS total_pts FROM player INNER JOIN game_stat ON player.IdPlayer = game_stat.IdPlayer WHERE game_stat.country IS NOT NULL GROUP BY player.IdPlayer ORDER BY total_pts DESC LIMIT 10;"
  return getSql(sql_10_player_total_point_for_national)

def getQuestion2():
  sql_3_player_freeThrowsPourcentage = "SELECT Name, (free_throws/free_throws_try) AS pourcentage FROM player INNER JOIN game_stat ON player.IdPlayer = game_stat.IdPlayer INNER JOIN game ON game_stat.IdGame = game.IdGame WHERE game.match_category = 'Final' AND game.league = 'Euroleague' ORDER BY pourcentage DESC LIMIT 3;"
  return getSql(sql_3_player_freeThrowsPourcentage)

def getQuestion3():
  sql_avg_height = "SELECT club.Name, AVG(player.height) AS avg_height FROM club INNER JOIN game_stat ON club.IdClub = game_stat.IdClub INNER JOIN player ON game_stat.IdPlayer = player.IdPlayer GROUP BY club.IdClub ORDER BY avg_height DESC LIMIT 1;"
  return getSql(sql_avg_height)

def getQuestion4():
  sql_sponsor_won_world_with_national = "SELECT sponsor_NTeam.name, COUNT(*) AS numberWinSponsor FROM sponsor_NTeam INNER JOIN (SELECT Final_matchs.GameCountry as Country FROM (SELECT game_stat.Country as GameCountry, game.IdGame as GameId, SUM(2_pts*2+3_pts*3+free_throws) AS total_pts FROM game_stat INNER JOIN game on game_stat.IdGame = game.IdGame WHERE game.league = 'World Cup' AND game.match_category = 'Final' GROUP BY game.IdGame, game_stat.Country ) AS Final_Matchs WHERE Final_matchs.total_pts = (SELECT MAX(Final_Matchs2.total_pts) FROM (SELECT game_stat.Country as GameCountry, game.IdGame as GameId, SUM(2_pts*2+3_pts*3+free_throws) AS total_pts FROM game_stat INNER JOIN game on game_stat.IdGame = game.IdGame WHERE game.league = 'World Cup' AND game.match_category = 'Final' GROUP BY game.IdGame, game_stat.Country ) AS Final_Matchs2 WHERE Final_Matchs2.GameId = Final_Matchs.GameId GROUP BY Final_Matchs2.GameId)) AS countryWinners ON sponsor_NTeam.Country = countryWinners.Country GROUP BY sponsor_Nteam.Name ORDER BY numberWinSponsor DESC LIMIT 1"
  return getSql(sql_sponsor_won_world_with_national)

def getQuestion5():
  sql_avg_3_pts_2022 = "SELECT player.Name, playerPourcentages.avg_3_pts, club.Name FROM player INNER JOIN (SELECT player.IdPlayer AS playerId, club.IdClub AS clubId, AVG(3_pts/3_pts_try) AS avg_3_pts FROM club INNER JOIN game_stat ON club.IdClub = game_stat.IdClub INNER JOIN player ON game_stat.IdPlayer = player.IdPlayer INNER JOIN game ON game_stat.IdGame = game.IdGame WHERE YEAR(game.Date) = 2022 GROUP BY player.IdPlayer, club.IdClub ) AS playerPourcentages ON player.IdPlayer = playerPourcentages.playerId INNER JOIN club ON club.IdClub = playerPourcentages.clubId WHERE playerPourcentages.avg_3_pts=(SELECT MAX(playerPourcentages2.avg_3_pts) FROM (SELECT player.IdPlayer AS playerId, club.IdClub AS clubId, AVG(3_pts/3_pts_try) AS avg_3_pts FROM club INNER JOIN game_stat ON club.IdClub = game_stat.IdClub INNER JOIN player ON game_stat.IdPlayer = player.IdPlayer INNER JOIN game ON game_stat.IdGame = game.IdGame WHERE YEAR(game.Date) = 2022 GROUP BY player.IdPlayer, club.IdClub ) AS playerPourcentages2 WHERE playerPourcentages2.clubId = playerPourcentages.clubId GROUP BY playerPourcentages2.clubId)"
  # "SELECT playerPourcentages.playerName, playerPourcentages.clubName, playerPourcentages.avg_3_pts FROM (SELECT player.Name AS playerName, club.Name AS clubName, AVG(3_pts/3_pts_try) AS avg_3_pts FROM club INNER JOIN game_stat ON club.IdClub = game_stat.IdClub INNER JOIN player ON game_stat.IdPlayer = player.IdPlayer INNER JOIN game ON game_stat.IdGame = game.IdGame WHERE YEAR(game.Date) = 2022 GROUP BY player.IdPlayer, club.name) AS playerPourcentages WHERE playerPourcentages= (SELECT MAX(playerPourcentages2.avg_3_pts) FROM (SELECT AVG(3_pts/3_pts_try) AS avg_3_pts FROM club INNER JOIN game_stat ON club.IdClub = game_stat.IdClub INNER JOIN player ON game_stat.IdPlayer = player.IdPlayer INNER JOIN game ON game_stat.IdGame = game.IdGame WHERE YEAR(game.Date) = 2022 AND player.IdPlayer = playerPourcentages.IdPlayer GROUP BY player.IdPlayer, club.name) AS playerPourcentages2"
  return getSql(sql_avg_3_pts_2022)

def getQuestion6():
  sql_player_most_assistPerGame_for_club = "SELECT player.Name, AVG(assists) AS avg_assistsPerGame FROM club INNER JOIN game_stat on club.IdClub = game_stat.IdGame INNER JOIN player ON game_stat.IdPlayer = player.IdPlayer WHERE club.Name = 'CSKA Moscou' GROUP BY player.IdPlayer ORDER BY avg_assistsPerGame DESC LIMIT 1;"
  return getSql(sql_player_most_assistPerGame_for_club)

def getQuestion7():
  sql_club_won_3_euroleague = "SELECT club.Name, COUNT(*) AS numberWinClub FROM club INNER JOIN (SELECT Final_matchs.GameClub as IdClub FROM (SELECT game_stat.IdClub as GameClub, game.IdGame as GameId, SUM(2_pts*2+3_pts*3+free_throws) AS total_pts FROM game_stat INNER JOIN game on game_stat.IdGame = game.IdGame WHERE game.league = 'Euroleague' AND game.match_category = 'Final' GROUP BY game.IdGame, game_stat.IdClub ) AS Final_Matchs WHERE Final_matchs.total_pts = (SELECT MAX(Final_Matchs2.total_pts) FROM (SELECT game_stat.IdClub as GameClub, game.IdGame as GameId, SUM(2_pts*2+3_pts*3+free_throws) AS total_pts FROM game_stat INNER JOIN game on game_stat.IdGame = game.IdGame WHERE game.league = 'Euroleague' AND game.match_category = 'Final' GROUP BY game.IdGame, game_stat.IdClub ) AS Final_Matchs2 WHERE Final_Matchs2.GameId = Final_Matchs.GameId GROUP BY Final_Matchs2.GameId) ) AS winnerEuro ON club.IdClub = winnerEuro.IdClub GROUP BY club.Name HAVING numberWinClub > 2"
  return getSql(sql_club_won_3_euroleague)
