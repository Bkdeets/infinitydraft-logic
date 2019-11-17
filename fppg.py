# Max fppg from draft kings

import os
import csv
import json
import random
import copy
import statistics

limits = {
    'D': 2,
    'M': 2,
    'F': 2,
    'UTIL':1,
    'GK': 1
}
budget = 50000
players = []
#Position,Name + ID,Name,ID,Roster Position,Salary,Game Info,TeamAbbrev,AvgPointsPerGame
fppgsort = []
with open('dksalaries_nov9_game.csv') as file:
    reader = csv.reader(file, delimiter=',')
    for i, col in enumerate(reader):
        if i != -1:
            fppg = float(col[8])
            salary = int(col[5])
            if fppg > 0:
                fppg_ratio = salary/fppg
                fppgsort.append({
                    'Position': col[0],
                    'Name': col[2],
                    'Salary': salary,
                    'AvgPointsPerGame': fppg,
                    'FPPGRatio': fppg_ratio,
                    'Id': col[3]
                })
                players.append({
                    'Position': col[0],
                    'Name': col[2],
                    'Salary': salary,
                    'AvgPointsPerGame': fppg,
                    'FPPGRatio': fppg_ratio,
                    'Id': col[3]
                })
players = sorted(players, key = lambda x : x['FPPGRatio'])
team = []
for player in players:
    position = player.get('Position')
    if position == 'M/F':
        midAvail = limits.get('M') > 0
        forwardAvail = limits.get('F') > 0
        if midAvail:
            position = 'M'
        elif forwardAvail: 
            position = 'F'
        else:
            position = 'UTIL'
    elif limits.get(position) == 0:
        position = 'UTIL'
    
    availableSlot = limits.get(position) > 0
    withinBudget = budget > player.get('Salary')
    if availableSlot and withinBudget:
        team.append(player)
        limits[position] = limits.get(position) - 1
        budget -= player.get('Salary')
        
print(json.dumps(team, sort_keys=True, indent=4))
print(sum([p['AvgPointsPerGame'] for p in team]))
print(json.dumps(limits, sort_keys=True, indent=4))
print(budget)

fppgsort = sorted(fppgsort, key=lambda x: x['FPPGRatio'])


def permute(fppgsort):
    for i in range(0,len(fppgsort)):
        if fppgsort[i]['Position'] == 'M/F':
            fppgsort[i]['Position'] = 'M'
            new_player = copy.copy(fppgsort[i])
            new_player['Position'] == 'F'
            fppgsort.append(new_player)
        
    teams = []
    scores = []
    iterations = 0
    while len(teams) < 100 and iterations < 10000000:
        temp_fppg_sort = fppgsort.copy()
        temp_fppg_sort = temp_fppg_sort[:len(temp_fppg_sort)//2]
        budget = 50000
        limits = {
            'D': 2,
            'M': 2,
            'F': 2,
            'UTIL':1,
            'GK': 1
        }
        team = []
        team_iterations = 0
        while len(team) < 8 and team_iterations < 100000 and iterations < 10000000:
            team_iterations += 1
            iterations += 1
            rand_seed = random.randint(0,len(temp_fppg_sort)-1)
            player = fppgsort[rand_seed]
            inBudget = player['Salary'] < budget
            position = player['Position']
            notInTeam = player not in team
            if limits.get(position) > 0 and inBudget and notInTeam:
                team.append(player)
                limits[position] -= 1
                budget -= player['Salary']
                del temp_fppg_sort[rand_seed]
            elif limits.get('UTIL') > 0 and position != 'GK' and inBudget and notInTeam:
                team.append(player)
                limits['UTIL'] -= 1
                budget -= player['Salary']
                del temp_fppg_sort[rand_seed]
        score = sum([p.get('AvgPointsPerGame') for p in team])
        if len(scores) > 0:
            if score >= max(scores):
                teams.append({
                    'team':team,
                    'score':score
                })
                scores.append(score)
        else:
            teams.append({
                    'team':team,
                    'score':score
                })
            scores.append(score)

    return sorted(teams, key=lambda x: x['score'])

print('Perms baby')
teams = permute(fppgsort)
for team in teams[-10:-1]:
    print(json.dumps(team, sort_keys=True, indent=4))



            
            
            
            



