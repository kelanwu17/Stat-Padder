from flask import Flask, render_template, request, redirect, url_for
from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import playerawards, commonplayerinfo,franchisehistory, TeamYearByYearStats, commonteamroster, commonteamyears, commonallplayers, playercareerstats,playergamelog, teamdetails
import json

app = Flask(__name__)

nba_teams = teams.get_teams()
def primaryColor(team):
    if team == "Hawks" or team == "Bulls" or team == "Rockets" or team == "Heat" or team == "Trail Blazers" or team == "Raptors" or team == "Wizards":
        return "DarkRed"
    elif team == "Celtics":
        return "Green"
    elif team == "Nets":
        return "Black"
    elif team == "Hornets":
        return "Teal"
    elif team == "Cavaliers":
        return "Brown"
    elif team == "Mavericks" or team == "Pistons"  or team == "Clippers" or team == "Thunder" or team == "Magic" or team == "76ers":
        return "Blue"
    elif team == "Nuggets" or team == "Timberwolves" or team == "Pelicans" or team == "Jazz":
        return "DarkBlue"
    elif team == "Pacers" or team == "Warriors":
        return "Yellow"
    elif team == "Lakers"  or team == "Kings":
        return "rgb(85, 37, 130)"
    elif team == "Grizzlies":
        return "SkyBlue"
    elif team == "Bucks":
        return "DarkGreen"
    elif team == "Knicks"or team=="Suns":
        return "Orange"
    elif team == "Spurs":
        return "Silver"
    
    




@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        player_input = request.form['player_input']
        return redirect(url_for("playerinfo", player=player_input))
    else:
        return render_template("home.html")
    
@app.route("/<player>", methods = ["GET", "POST"])
def playerinfo(player):
    
        
    
    nba_players = json.loads(commonallplayers.CommonAllPlayers().get_normalized_json())
    player_id = 0;
    player_name = ""
    valid_player = 0
    for i in range(0, len(nba_players['CommonAllPlayers'])):
        if nba_players['CommonAllPlayers'][i]['DISPLAY_FIRST_LAST'].lower() == player.lower():
            player_id = nba_players['CommonAllPlayers'][i]['PERSON_ID']
            player_name = nba_players['CommonAllPlayers'][i]['DISPLAY_FIRST_LAST']
            valid_player = nba_players['CommonAllPlayers'][i]['ROSTERSTATUS']
            break
    if valid_player == 3:
        return "<p> Invalid Player </p>"
    else:
        player_image = f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png'
        player_info = json.loads((commonplayerinfo.CommonPlayerInfo(player_id = player_id)).get_normalized_json())
        player_team = player_info["CommonPlayerInfo"][0]["TEAM_NAME"]
        player_team_id = player_info["CommonPlayerInfo"][0]["TEAM_ID"]
        player_country = player_info["CommonPlayerInfo"][0]["COUNTRY"]
        player_height = player_info["CommonPlayerInfo"][0]["HEIGHT"]
        player_weight = player_info["CommonPlayerInfo"][0]["WEIGHT"]
        team_image = f'https://cdn.nba.com/logos/nba/{player_team_id}/primary/D/logo.svg'
        stats = json.loads(playercareerstats.PlayerCareerStats(player_id = player_id).get_normalized_json())
        careerpts = careergames = careerreb = careerast = 0
        for i in range(0, len(stats['SeasonTotalsRegularSeason'])):
            if stats['SeasonTotalsRegularSeason'][i]['GP'] > 0:
                careergames = careergames + stats['SeasonTotalsRegularSeason'][i]['GP']
            if stats['SeasonTotalsRegularSeason'][i]['PTS'] > 0:
                careerpts = careerpts + stats['SeasonTotalsRegularSeason'][i]['PTS']
            if stats['SeasonTotalsRegularSeason'][i]['REB'] > 0:
                careerreb = careerreb + stats['SeasonTotalsRegularSeason'][i]['REB']
            if stats['SeasonTotalsRegularSeason'][i]['AST'] > 0:
                careerast = careerast + stats['SeasonTotalsRegularSeason'][i]['AST']
                
                
        player_awards = json.loads((playerawards.PlayerAwards(player_id = player_id)).get_normalized_json())        
        all_d = all_nba = fmvp = mvp = roty = dpoy = mip = 0
    
        for i in range(0,len(player_awards["PlayerAwards"])):
            if (player_awards["PlayerAwards"][i]['DESCRIPTION'] == "All-Defensive Team"):
                all_d += 1
            elif (player_awards["PlayerAwards"][i]['DESCRIPTION'] == "All-NBA"):
                all_nba += 1
            elif (player_awards["PlayerAwards"][i]['DESCRIPTION'] == "NBA Finals Most Valuable Player"):
                fmvp += 1
            elif (player_awards["PlayerAwards"][i]['DESCRIPTION'] == "NBA Most Valuable Player"):
                mvp += 1
            elif (player_awards["PlayerAwards"][i]['DESCRIPTION'] == "NBA Rookie of the Year"):
                roty += 1
            elif (player_awards["PlayerAwards"][i]['DESCRIPTION'] == "NBA Defensive Player of the Year"):
                dpoy += 1
            elif (player_awards["PlayerAwards"][i]['DESCRIPTION'] == "NBA Most Improved Player"):
                mip += 1
        all_star = 0
        for i in range(0, len(stats['SeasonTotalsAllStarSeason'])):
            all_star += 1
        
        played_seasons = []
        # Getting played seasons
        for i in range(len(player_info["AvailableSeasons"]) - 1, -1, -1):
            if player_info["AvailableSeasons"][i]['SEASON_ID'][1:] not in played_seasons:
                played_seasons.append(player_info["AvailableSeasons"][i]['SEASON_ID'][1:])
        #for last 5 games
        
        if request.method == "POST":
            specific_year = request.form['season_played']
            game_logs = json.loads(playergamelog.PlayerGameLog(player_id = player_id, season=specific_year).get_normalized_json())
        else:
            specific_year = 2022
            game_logs = json.loads(playergamelog.PlayerGameLog(player_id = player_id).get_normalized_json())
        
        game_date = [] #game date
        match = [] #matchups
        log_pts = [] #points
        log_fg = []
        log_three = []
        log_ft=[]
        log_oreb=[]
        log_dreb=[]
        log_ast=[]
        log_stl=[]
        log_blk=[]
        log_tov=[]
        log_pm = []
        log_wl = []
        log_min = []
        
        season_fgm = 0 #for graphs
        season_fga = 0 #for graphs
        oreb_total = 0
        dreb_total = 0
        threemade = 0
        threeattempt = 0
        total_games = len(game_logs['PlayerGameLog'])
        
        
        for i in range(total_games - 1, -1, -1):
                game_date.append(game_logs['PlayerGameLog'][i]['GAME_DATE'])
                match.append(game_logs['PlayerGameLog'][i]['MATCHUP'])
                log_pts.append(game_logs['PlayerGameLog'][i]['PTS'])
                log_fg.append(str(game_logs['PlayerGameLog'][i]['FGM']) + "/" + str(game_logs['PlayerGameLog'][i]['FGA']))
                log_three.append(str(game_logs['PlayerGameLog'][i]['FG3M']) + "/" + str(game_logs['PlayerGameLog'][i]['FG3A']))
                log_ft.append(str(game_logs['PlayerGameLog'][i]['FTM']) + "/" + str(game_logs['PlayerGameLog'][i]['FTA']))
                log_oreb.append(game_logs['PlayerGameLog'][i]['OREB'])
                log_dreb.append(game_logs['PlayerGameLog'][i]['DREB'])
                log_ast.append(game_logs['PlayerGameLog'][i]['AST'])
                log_stl.append(game_logs['PlayerGameLog'][i]['STL'])
                log_blk.append(game_logs['PlayerGameLog'][i]['BLK'])
                log_tov.append(game_logs['PlayerGameLog'][i]['TOV'])
                log_pm.append(game_logs['PlayerGameLog'][i]['PLUS_MINUS'])
                log_wl.append(game_logs['PlayerGameLog'][i]['WL'])
                log_min.append(game_logs['PlayerGameLog'][i]['MIN'])
                season_fgm = season_fgm + int(game_logs['PlayerGameLog'][i]['FGM'])
                season_fga = season_fga + int(game_logs['PlayerGameLog'][i]['FGA'])
                oreb_total = oreb_total + int(game_logs['PlayerGameLog'][i]['OREB'])
                dreb_total = dreb_total + int(game_logs['PlayerGameLog'][i]['DREB'])
                threemade = threemade + int(game_logs['PlayerGameLog'][i]['FG3M'])
                threeattempt = threeattempt + int(game_logs['PlayerGameLog'][i]['FG3A'])
                
       
        color = primaryColor(player_team)      
                
        return render_template("stats.html", specific_year = specific_year, player_name = player_name, player_image =player_image, player_team = player_team, player_country = player_country, career_pts = round(careerpts/careergames,1), career_ast = round(careerast/careergames,1), career_reb =  round(careerreb/careergames,1), all_d = all_d, all_nba = all_nba, mvp=mvp, fmvp = fmvp,  roty = roty, dpoy = dpoy, mip = mip, player_weight = player_weight, player_height = player_height, all_star = all_star, team_image = team_image, game_date = game_date, match = match, log_pts = log_pts, log_fg = log_fg, log_three = log_three, log_ft = log_ft, log_oreb = log_oreb, log_dreb = log_dreb, log_ast = log_ast, log_stl = log_stl, log_blk = log_blk, log_tov = log_tov, log_pm = log_pm, total_games = total_games, log_wl = log_wl, log_min = log_min, season_fgm = season_fgm, season_fga = season_fga, oreb_total = oreb_total, dreb_total = dreb_total, threemade = threemade, threeattempt = threeattempt, played_seasons = played_seasons, color = color)


@app.route("/history")
def history():
    return render_template("history.html")


if __name__ == "__main__":
    app.run(debug=True)