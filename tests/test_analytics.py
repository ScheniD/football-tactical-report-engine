import pandas as pd
import pytest
from src.analytics import calculate_xt

def test_calculate_xt_basic():
    # Erstelle minimale Testdaten
    data = {
        'type': ['Pass', 'Pass'],
        'location': [[10, 10], [50, 50]],
        'pass_end_location': [[20, 20], [60, 60]],
        'outcome': [float('nan'), float('nan')], # Erfolgreiche Pässe
        'team': ['Test Team', 'Test Team']
    }
    df = pd.DataFrame(data)
    
    # Führe Berechnung aus
    # Hinweis: Da calculate_xt ein Modell lädt, testen wir hier primär, 
    # ob die Spalten korrekt hinzugefügt werden, ohne das Modell zu simulieren.
    try:
        result = calculate_xt(df)
        assert 'xT' in result.columns
        assert len(result) == 2
    except Exception as e:
        pytest.fail(f"calculate_xt failed: {e}")
