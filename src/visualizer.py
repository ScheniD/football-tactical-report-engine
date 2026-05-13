import matplotlib.pyplot as plt
from mplsoccer import Pitch, PyPizza
import pandas as pd
import numpy as np

# --- MODERN SLATE PALETTE ---
BG_COLOR = "#ffffff"
L_GREY = "#f3f4f6"
D_GREY = "#374151"
TEXT_COLOR = "#111827"
# Category Colors (FBref-style)
C_ATTACK = "#ff4b44" # Rose Red
C_POSS = "#00d2d3"   # Modern Teal
C_DEF = "#54a0ff"    # Sky Blue

def plot_zonal_threat(passes, team_name):
    """Generates a clean, technical zonal map."""
    pitch = Pitch(pitch_type='statsbomb', line_zorder=2, pitch_color=BG_COLOR, line_color="#e5e7eb", linewidth=0.5)
    fig, ax = pitch.draw(figsize=(12, 8))
    fig.set_facecolor(BG_COLOR)
    
    bin_statistic = pitch.bin_statistic(passes.x, passes.y, values=passes.xt, statistic='sum', bins=(3, 2))
    total_xt = passes.xt.sum()
    bin_percentages = (bin_statistic['statistic'] / total_xt) * 100
    
    # Use a subtle, sophisticated 'Blues' or 'Greys' to keep it modern
    pcm = pitch.heatmap(bin_statistic, ax=ax, cmap='Greys', edgecolors=BG_COLOR, alpha=0.1)
    
    # Draw clean tactical boxes
    cx = bin_statistic['cx'].flatten()
    cy = bin_statistic['cy'].flatten()
    vals = bin_percentages.flatten()
    
    for i in range(len(cx)):
        if not np.isnan(vals[i]):
            # Use a modern "pill" or "card" look for the numbers
            ax.text(cx[i], cy[i], f'{vals[i]:.1f}%', color=TEXT_COLOR, 
                    fontsize=26, fontweight='300', va='center', ha='center')
            ax.text(cx[i], cy[i]-5, 'THREAT SHARE', color="#9ca3af", 
                    fontsize=8, fontweight='bold', va='center', ha='center')
    
    ax.set_title(f"{team_name.upper()} | ATTACKING INTENSITY", fontsize=18, color=TEXT_COLOR, pad=40, weight='bold', loc='left')
    return fig

def plot_player_pizza(all_events, passes_with_xt, team_name):
    """Generates a multi-color, modern Pizza Chart."""
    top_player_name = passes_with_xt.groupby('player').xt.sum().idxmax()
    
    # Metrics
    p_passes = all_events[(all_events.player == top_player_name) & (all_events.type == 'Pass')]
    p_vol = len(p_passes)
    p_acc = (p_passes.pass_outcome.isna()).mean() * 100
    
    p_xt_data = passes_with_xt[passes_with_xt.player == top_player_name]
    p_xt_total = p_xt_data.xt.sum()
    p_xt_avg = p_xt_data.xt.mean()
    p_fwd = (p_xt_data.end_x > p_xt_data.x).mean() * 100
    
    # Normalized Values (relative to team)
    team_stats = passes_with_xt.groupby('player').agg({'xt': ['count', 'sum', 'mean']})
    values = [
        int(min(100, (p_vol / team_stats['xt']['count'].mean()) * 50)),
        int(p_acc),
        int(min(100, (p_xt_total / team_stats['xt']['sum'].mean()) * 50)),
        int(min(100, (p_xt_avg / team_stats['xt']['mean'].mean()) * 50)),
        int(p_fwd)
    ]
    
    params = ["VOLUME", "ACCURACY", "TOTAL DANGER", "DANGER/PASS", "FORWARD %"]
    slice_colors = [C_POSS, C_POSS, C_ATTACK, C_ATTACK, C_ATTACK]
    
    baker = PyPizza(
        params=params,
        background_color=BG_COLOR,
        straight_line_color="#f3f4f6",
        straight_line_lw=1,
        last_circle_color="#f3f4f6",
        last_circle_lw=1,
        other_circle_lw=1,
        other_circle_ls="-"
    )

    fig, ax = baker.make_pizza(
        values,
        figsize=(8, 8),
        color_blank_space="same",
        slice_colors=slice_colors,
        param_location=115,
        kwargs_slices=dict(edgecolor=BG_COLOR, zorder=2, linewidth=2),
        kwargs_params=dict(color=TEXT_COLOR, fontsize=11, weight='bold'),
        kwargs_values=dict(color=TEXT_COLOR, fontsize=10, weight='bold',
                           bbox=dict(edgecolor="#e5e7eb", facecolor="white", boxstyle="round,pad=0.3"))
    )

    ax.set_title(f"{top_player_name.upper()} | PERFORMANCE PROFILE", fontsize=18, color=TEXT_COLOR, pad=40, weight='bold')
    return fig

def plot_shot_map(events, team_name):
    """Generates a minimalistic, high-end shot map."""
    shots = events[events['type'] == 'Shot'].copy()
    shots['x'] = shots['location'].apply(lambda x: x[0])
    shots['y'] = shots['location'].apply(lambda x: x[1])
    
    pitch = Pitch(pitch_type='statsbomb', line_zorder=2, pitch_color=BG_COLOR, line_color="#e5e7eb", linewidth=0.5)
    fig, ax = pitch.draw(figsize=(12, 8))
    fig.set_facecolor(BG_COLOR)
    
    goals = shots[shots['shot_outcome'] == 'Goal']
    non_goals = shots[shots['shot_outcome'] != 'Goal']
    
    # Modern subtle circles for misses
    pitch.scatter(non_goals.x, non_goals.y, s=non_goals['shot_statsbomb_xg']*1500, 
                  edgecolors="#d1d5db", facecolors='none', linewidth=1, alpha=0.5, ax=ax)
    
    # Bold Rose Red for goals
    pitch.scatter(goals.x, goals.y, s=goals['shot_statsbomb_xg']*1500, 
                  color=C_ATTACK, edgecolors="white", linewidth=1.5, alpha=1, ax=ax, marker='o')
    
    ax.set_title(f"{team_name.upper()} | SHOT CONVERSION", fontsize=18, color=TEXT_COLOR, pad=40, weight='bold', loc='left')
    
    # Legend
    plt.text(115, 85, "● GOAL", color=C_ATTACK, weight='bold', fontsize=10, ha='right')
    plt.text(115, 82, "○ MISS", color="#9ca3af", weight='bold', fontsize=10, ha='right')
    
    return fig
