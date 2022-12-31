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

sql = "SELECT Name FROM player"

sql_10_player_total_point_for_national = "SELECT Name, SUM(2_pts*2+3_pts*3+free_throws) AS total_pts FROM player INNER JOIN game ON player.IdPlayer = game.IdPlayer WHERE game.country IS NOT NULL GROUP BY player.IdPlayer ORDER BY total_pts LIMIT 10;"
sql_3_player_freeThrowsPourcentage = "SELECT Name, (free_throws/free_throws_try) AS pourcentage FROM player INNER JOIN game ON player.IdPlayer = game.IdPlayer WHERE game.match_category = 'final_euro' ORDER BY pourcentage LIMIT 3;"
sql_avg_height = "SELECT club.Name, AVG(player.height) AS avg_height FROM club INNER JOIN game ON club.IdClub = game.IdClub INNER JOIN player ON game.IdPlayer = player.IdPlayer GROUP BY club.IdClub ORDER BY avg_height LIMIT 1;"
sql_sponsor_won_world_with_national = "SELECT sponsor_NTeam.Name COUNT(game.Id) AS sum_win FROM sponsor_NTeam JOIN game ON sponsor_NTeam.Country = game.Country WHERE game.Win = true GROUP BY sponsor_NTeam.Name ORDER BY sum_win;"
sql_avg_3_pts_2022 = "SELECT player.Name, AVG(3_pts/3_pts_try) AS avg_3_pts FROM club INNER JOIN game ON club.IdClub = game.IdClub INNER JOIN player ON game.IdPlayer = player.IdPlayer WHERE YEAR(game.Date) = 2022 GROUP BY player.IdPlayer;"
sql_player_most_assistPerGame_for_club = "SELECT player.Name, AVG(assists) AS avg_assistsPerGame FROM club INNER JOIN game on club.IdClub = game.IdGame INNER JOIN player ON game.IdPlayer = player.IdPlayer WHERE club.Name = 'test' GROUP BY player.IdPlayer ORDER BY avg_assistsPerGame LIMIT 1;"
sql_club_won_3_euroleague = "SELECT club.Name, COUNT(*) AS numberWin FROM club INNER JOIN game ON club.IdClub = game.IdClub WHERE SELECT DISTINCT game.win = true"



#exécuter le curseur avec la méthode executemany() et transmis la requéte SQL
cur.execute(sql)

value = cur.fetchall()

def hello(request):
    bands = []
    for val in value:
        bands += [{"name": val[0]}]
    return render(request, 'hello.html', {"bands": bands})


titles = []
titles += ["Les 10 joueurs qui ont marqué le plus grand nombre de points avec leur équipe national sont :"]
titles += ["Les 3 joueurs avec le meilleur pourcentage de lancer franc dans une final de championnat européen sont :"]
titles += ["Le club avec la plus haute moyenne de taille est : "]
titles += ["Le sponsor qui a sponsorisé le plus d'équipe nationale qui ont gagné les championnats du monde est : "]
titles += ["Pour chaque club le joueur qui a le meilleur pourcentage de 3 points dans la saison actuelle est : "]
titles += ["Pour un club particulier, le joueur qui a le plus d'assist par game est : "]
titles += ["Voici la liste des club qui ont gagné l'euroleague au moins 3 fois : "]


def questions(request):
    bands = []
    for val in value:
        bands += [{"name": val[0]}]
    values = []
    # for i in range(7):
    #   values += [(value, titles[i], (i+1))]
    values += [(getQuestion1(), titles[0], 1)]
    values += [(getQuestion2(), titles[1], 2)]
    values += [(getQuestion3(), titles[2], 3)]
    # values += [(getQuestion4(), titles[3], 4)]
    values += [(getQuestion5(), titles[4], 5)]
    values += [(getQuestion6(), titles[5], 6)]
    # values += [(getQuestion7(), titles[6], 7)]

    return render(request, 'questions.html', {"values": values})





def getSql(sql):
  cur.execute(sql)
  value = cur.fetchall()
  return value

def getQuestion1():
  sql_10_player_total_point_for_national = "SELECT Name, SUM(2_pts*2+3_pts*3+free_throws) AS total_pts FROM player INNER JOIN game ON player.IdPlayer = game.IdPlayer WHERE game.country IS NOT NULL GROUP BY player.IdPlayer ORDER BY total_pts LIMIT 10;"
  return getSql(sql_10_player_total_point_for_national)

def getQuestion2():
  sql_3_player_freeThrowsPourcentage = "SELECT Name, (free_throws/free_throws_try) AS pourcentage FROM player INNER JOIN game ON player.IdPlayer = game.IdPlayer WHERE game.match_category = 'final_euro' ORDER BY pourcentage LIMIT 3;"
  return getSql(sql_3_player_freeThrowsPourcentage)

def getQuestion3():
  sql_avg_height = "SELECT club.Name, AVG(player.height) AS avg_height FROM club INNER JOIN game ON club.IdClub = game.IdClub INNER JOIN player ON game.IdPlayer = player.IdPlayer GROUP BY club.IdClub ORDER BY avg_height LIMIT 1;"
  return getSql(sql_avg_height)

def getQuestion4():
  sql_sponsor_won_world_with_national = "SELECT sponsor_NTeam.Name COUNT(game.Id) AS sum_win FROM sponsor_NTeam JOIN game ON sponsor_NTeam.Country = game.Country WHERE game.Win = true GROUP BY sponsor_NTeam.Name ORDER BY sum_win;"
  return getSql(sql_sponsor_won_world_with_national)

def getQuestion5():
  sql_avg_3_pts_2022 = "SELECT player.Name, AVG(3_pts/3_pts_try) AS avg_3_pts FROM club INNER JOIN game ON club.IdClub = game.IdClub INNER JOIN player ON game.IdPlayer = player.IdPlayer WHERE YEAR(game.Date) = 2022 GROUP BY player.IdPlayer;"
  return getSql(sql_avg_3_pts_2022)

def getQuestion6():
  sql_player_most_assistPerGame_for_club = "SELECT player.Name, AVG(assists) AS avg_assistsPerGame FROM club INNER JOIN game on club.IdClub = game.IdGame INNER JOIN player ON game.IdPlayer = player.IdPlayer WHERE club.Name = 'test' GROUP BY player.IdPlayer ORDER BY avg_assistsPerGame LIMIT 1;"
  return getSql(sql_player_most_assistPerGame_for_club)

def getQuestion7():
  sql_club_won_3_euroleague = "SELECT club.Name, COUNT(*) AS numberWin FROM club INNER JOIN game ON club.IdClub = game.IdClub WHERE SELECT DISTINCT game.win = true"
  return getSql(sql_club_won_3_euroleague)