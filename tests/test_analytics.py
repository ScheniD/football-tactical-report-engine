import pandas as pd
import pytest
from src.analytics import calculate_xt

def test_calculate_xt_basic():
    # Korrigierte Testdaten (pass_outcome statt outcome)
    data = {
        'type': ['Pass', 'Pass'],
        'location': [[10, 10], [50, 50]],
        'pass_end_location': [[20, 20], [60, 60]],
        'pass_outcome': [float('nan'), float('nan')], 
        'team': ['Test Team', 'Test Team'],
        'player': ['Player 1', 'Player 2']
    }
    df = pd.DataFrame(data)
    
    result = calculate_xt(df)
    
    # Prüfen, ob xT berechnet wurde
    assert 'xt' in result.columns
    assert len(result) == 2
    assert result['xt'].iloc[1] >= 0
