from flask import Flask, render_template, request, redirect, url_for
from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import playerawards, commonplayerinfo,franchisehistory, TeamYearByYearStats, commonteamroster, commonteamyears, commonallplayers, playercareerstats
import json




# print(player)

# player_awards = playerawards.PlayerAwards(player_id = player_id)
# player_json = player_awards.get_normalized_json()
# player_json_loads = json.loads(player_json)
# print(json.dumps(player_json_loads, indent = 4))
# all_defense_team = 0
# all_nba = 0
# fmvp = 0
# mvp = 0
# roty = 0


app = Flask(__name__)
@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        player_input = request.form.get('player_input')
        return redirect(url_for("playerinfo", player=player_input))
    else:
        return render_template("index.html")
    
@app.route("/<player>")
def playerinfo(player):
        
        nba_players = json.loads(commonallplayers.CommonAllPlayers().get_normalized_json())
        player_id = 0;
        player_name = ""

        for i in range(0, len(nba_players['CommonAllPlayers'])):
            if nba_players['CommonAllPlayers'][i]['DISPLAY_FIRST_LAST'].lower() == player.lower():
                player_id = nba_players['CommonAllPlayers'][i]['PERSON_ID']
                player_name = nba_players['CommonAllPlayers'][i]['DISPLAY_FIRST_LAST']
                break
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
            
        return render_template("awards.html", player_name = player_name, player_image =player_image, player_team = player_team, player_country = player_country, career_pts = round(careerpts/careergames,1), career_ast = round(careerast/careergames,1), career_reb =  round(careerreb/careergames,1), all_d = all_d, all_nba = all_nba, mvp=mvp, fmvp = fmvp,  roty = roty, dpoy = dpoy, mip = mip, player_weight = player_weight, player_height = player_height, all_star = all_star, team_image = team_image)
    
if __name__ == "__main__":
    app.run(debug=True)