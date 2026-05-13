from statsbombpy import sb
import pandas as pd

def get_competitions():
    """Fetch all available free competitions."""
    return sb.competitions()

def get_matches(competition_id, season_id):
    """Fetch all matches for a specific competition and season."""
    return sb.matches(competition_id=competition_id, season_id=season_id)

def get_events(match_id):
    """Fetch all events for a specific match."""
    return sb.events(match_id=match_id)

if __name__ == "__main__":
    # Test script to see available data
    comps = get_competitions()
    print("Available Competitions (First 5):")
    print(comps[['competition_name', 'season_name', 'competition_id', 'season_id']].head())

    print("\nMatches for Bundesliga 23/24:")
    matches = get_matches(competition_id=9, season_id=281)
    print(matches[['match_id', 'home_team', 'away_team', 'match_date']].head())
