import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

plt.rcParams.update({'font.size': 14})  # Adjust the number to your preferred size

def plot_fairness_heatmap(output1_list, output2_list, labels=None):
    """
    Plots a heatmap of the fairness score between two techniques across different configurations.
    
    Fairness Score = (Batches in Technique 1 - Batches in Technique 2) / max(Batches in Technique 1, Batches in Technique 2)
    
    Parameters:
    - output1_list: List of List[List[int]], results from technique 1 across different configurations.
    - output2_list: List of List[List[int]], results from technique 2 across different configurations.
    - labels: Optional list of configuration labels.
    """
    assert len(output1_list) == len(output2_list), "Both techniques must have results for the same number of configurations."
    
    num_configs = len(output1_list)
    batches_1 = np.array([len(config) for config in output1_list])
    batches_2 = np.array([len(config) for config in output2_list])
    
    # Compute fairness score
    fairness_scores = (batches_1 - batches_2) / np.maximum(batches_1, batches_2)
    
    # Reshape to 1 row for heatmap visualization
    fairness_matrix = fairness_scores.reshape(1, -1)
    
    fig_width = max(12, num_configs / 50)  # Adaptive width based on number of configurations
    fig_height = 2  # Fixed height to avoid excessive stretching
    plt.figure(figsize=(fig_width, fig_height))
    
    ax = sns.heatmap(fairness_matrix, annot=num_configs <= 50, cmap="RdYlGn", center=0, fmt=".2f" if num_configs <= 50 else "",
                      xticklabels=labels if (labels and len(labels) <= 50) else "auto",
                      yticklabels=["Fairness Score"], linewidths=0,  # Removed column borders
                      vmin=-1, vmax=1, cbar=True)
    
    cbar = ax.collections[0].colorbar
    # cbar.set_label("Fairness Score (-1 to 1)")
    cbar.set_ticks([-1, 0, 1])
    cbar.set_ticklabels(["TrueTime Wins", "Neutral", "Tommy Wins"])  # Add labels at -1 and 1
    
    # plt.title("Fairness Score Heatmap (More Positive = Green, More Negative = Red)")
    plt.xlabel("Configurations")
    
    # Make x ticks sparse and horizontal
    if num_configs > 50:
        xticks = np.linspace(0, num_configs - 1, min(20, num_configs), dtype=int)  # Reduce number of ticks
        ax.set_xticks(xticks)
        if labels:
            ax.set_xticklabels([labels[i] for i in xticks], rotation=0)  # Keep labels horizontal
        else:
            ax.set_xticklabels([str(i) for i in xticks], rotation=0)  # Use only numeric indices, horizontal
    else:
        plt.xticks(rotation=0)
    
    plt.savefig("tmp.pdf", bbox_inches='tight')
    # plt.show()

# Example usage:
# plot_fairness_heatmap([[[1], [2, 3]], [[4, 5], [6]]], [[[1, 2], [3]], [[4], [5, 6]]])