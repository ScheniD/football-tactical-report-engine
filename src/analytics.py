import numpy as np
import pandas as pd

# Standard 12x8 xT grid (values roughly represent scoring probability change)
# Values adapted from Karun Singh's standard xT model
XT_GRID = np.array([
    [0.00638303, 0.00779616, 0.0084485, 0.00977659, 0.01126267, 0.01248344, 0.01404196, 0.014836, 0.01689468, 0.01935387, 0.02151351, 0.02349751],
    [0.00750056, 0.00870277, 0.0094248, 0.010572, 0.01214681, 0.01384541, 0.01613013, 0.01735647, 0.0211244, 0.02456485, 0.02844199, 0.03361377],
    [0.00888034, 0.00972118, 0.01074523, 0.01216263, 0.01395814, 0.0158231, 0.01843474, 0.02094447, 0.02568682, 0.02968146, 0.03538354, 0.05111162],
    [0.0094059, 0.01021237, 0.01117402, 0.01253046, 0.01449751, 0.01704252, 0.02035772, 0.02384714, 0.02998399, 0.03511107, 0.04761103, 0.10933705],
    [0.0094059, 0.01021237, 0.01117402, 0.01253046, 0.01449751, 0.01704252, 0.02035772, 0.02384714, 0.02998399, 0.03511107, 0.04761103, 0.10933705],
    [0.00888034, 0.00972118, 0.01074523, 0.01216263, 0.01395814, 0.0158231, 0.01843474, 0.02094447, 0.02568682, 0.02968146, 0.03538354, 0.05111162],
    [0.00750056, 0.00870277, 0.0094248, 0.010572, 0.01214681, 0.01384541, 0.01613013, 0.01735647, 0.0211244, 0.02456485, 0.02844199, 0.03361377],
    [0.00638303, 0.00779616, 0.0084485, 0.00977659, 0.01126267, 0.01248344, 0.01404196, 0.014836, 0.01689468, 0.01935387, 0.02151351, 0.02349751]
])

def get_grid_coords(x, y, pitch_length=120, pitch_width=80, grid_x=12, grid_y=8):
    """Maps pitch coordinates (StatsBomb style) to grid indices."""
    xi = int((x / pitch_length) * grid_x)
    yi = int((y / pitch_width) * grid_y)
    
    # Clip to handle boundary values
    xi = min(xi, grid_x - 1)
    yi = min(yi, grid_y - 1)
    return xi, yi

def calculate_xt(events):
    """
    Calculates Expected Threat for successful passes in the events dataframe.
    """
    # Filter for successful passes
    passes = events[(events['type'] == 'Pass') & (events['pass_outcome'].isna())].copy()
    
    # Extract coordinates
    # StatsBomb locations are [x, y]
    passes['x'] = passes['location'].apply(lambda loc: loc[0])
    passes['y'] = passes['location'].apply(lambda loc: loc[1])
    passes['end_x'] = passes['pass_end_location'].apply(lambda loc: loc[0])
    passes['end_y'] = passes['pass_end_location'].apply(lambda loc: loc[1])
    
    xt_values = []
    for _, row in passes.iterrows():
        start_xi, start_yi = get_grid_coords(row['x'], row['y'])
        end_xi, end_yi = get_grid_coords(row['end_x'], row['end_y'])
        
        start_xt = XT_GRID[start_yi, start_xi]
        end_xt = XT_GRID[end_yi, end_xi]
        
        # xT is the difference in scoring probability between start and end
        # We only count positive threat for "attacking" passes
        xt = max(0, end_xt - start_xt)
        xt_values.append(xt)
    
    passes['xt'] = xt_values
    return passes

def get_top_threat_creators(passes):
    """Aggregates xT by player."""
    return passes.groupby('player')['xt'].sum().sort_values(ascending=False).reset_index()
