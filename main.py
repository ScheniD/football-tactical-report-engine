from src.data_loader import get_events, get_matches, get_competitions
from src.analytics import calculate_xt, get_top_threat_creators
from src.visualizer import plot_zonal_threat, plot_player_pizza, plot_shot_map
from src.pdf_generator import create_report
import os

def main(match_id, team_name, comp_id, season_id):
    # 1. Fetch Data
    print(f"--- Processing Match {match_id} for {team_name} ---")
    events = get_events(match_id)
    
    # Get match info
    matches = get_matches(competition_id=comp_id, season_id=season_id)
    match_info_row = matches[matches['match_id'] == match_id].iloc[0]
    match_info = match_info_row.to_dict()
    
    # Find competition name
    comps = get_competitions()
    comp_name = comps[(comps.competition_id == comp_id) & (comps.season_id == season_id)].competition_name.iloc[0]
    match_info['competition'] = comp_name
    
    team_events = events[events['team'] == team_name]
    
    # 2. Analytics
    print("Calculating advanced metrics (xT)...")
    passes_with_xt = calculate_xt(team_events)
    top_creators = get_top_threat_creators(passes_with_xt)
    
    # 3. Visualization
    print("Generating tactical visualizations...")
    os.makedirs('data', exist_ok=True)
    heatmap_path = 'data/temp_heatmap.png'
    radar_path = 'data/temp_radar.png'
    shotmap_path = 'data/temp_shotmap.png'
    
    fig_heatmap = plot_zonal_threat(passes_with_xt, team_name)
    fig_heatmap.savefig(heatmap_path, bbox_inches='tight', dpi=300)
    
    fig_pizza = plot_player_pizza(events, passes_with_xt, team_name)
    fig_pizza.savefig(radar_path, bbox_inches='tight', dpi=300)
    
    fig_shotmap = plot_shot_map(team_events, team_name)
    fig_shotmap.savefig(shotmap_path, bbox_inches='tight', dpi=300)
    
    # 4. PDF Generation
    print("Assembling Modern Technical Dossier...")
    os.makedirs('reports', exist_ok=True)
    report_filename = f"reports/{team_name.replace(' ', '_')}_CL_Final_Report_{match_id}.pdf"
    
    create_report(match_info, top_creators, heatmap_path, radar_path, shotmap_path, report_filename)
    
    print(f"--- Success! Report ready at {report_filename} ---")

if __name__ == "__main__":
    # AS Monaco vs FC Porto | Champions League Final 2003/2004
    main(match_id=3752619, team_name='FC Porto', comp_id=16, season_id=44)
