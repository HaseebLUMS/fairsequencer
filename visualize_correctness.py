import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def compute_ras(technique_batches, ground_truth_batches):
    """
    Computes the Rank Agreement Score (RAS) for a given technique compared to the ground truth.
    
    RAS = (Correctly Ordered Pairs - Incorrectly Ordered Pairs) / Total Pairs in Ground Truth
    
    Parameters:
    - technique_batches: List[List[int]], batches assigned by the technique.
    - ground_truth_batches: List[List[int]], true batching order.
    
    Returns:
    - RAS score (float)
    """
    def extract_pairs(batches):
        """Extract all (message_a, message_b) pairs from ordered batches."""
        rank_map = {}
        rank = 0
        for batch in batches:
            for msg in batch:
                rank_map[msg] = rank
            rank += 1
        return rank_map
    
    gt_ranks = extract_pairs(ground_truth_batches)
    tech_ranks = extract_pairs(technique_batches)
    
    messages = list(gt_ranks.keys())
    correct, wrong, total = 0, 0, 0
    
    for i in range(len(messages)):
        for j in range(i + 1, len(messages)):
            m_a, m_b = messages[i], messages[j]
            
            if m_a not in tech_ranks or m_b not in tech_ranks:
                continue  # Ignore missing messages
            
            gt_order = np.sign(gt_ranks[m_a] - gt_ranks[m_b])
            tech_order = np.sign(tech_ranks[m_a] - tech_ranks[m_b])
            
            if gt_order != 0:
                total += 1
                if tech_order == gt_order:
                    correct += 1
                elif tech_order != 0:
                    wrong += 1
    
    return (correct - wrong) / total if total > 0 else 0

def plot_ras_heatmap(output1_list, output2_list, ground_truth_list, labels=None):
    """
    Plots a heatmap comparing the Rank Agreement Score (RAS) of two techniques against the ground truth.
    
    Parameters:
    - output1_list: List of List[List[int]], results from technique 1 across different configurations.
    - output2_list: List of List[List[int]], results from technique 2 across different configurations.
    - ground_truth_list: List of List[List[int]], representing the ground truth batching for each configuration.
    - labels: Optional list of configuration labels.
    """
    assert len(output1_list) == len(output2_list) == len(ground_truth_list), "All inputs must have results for the same number of configurations."
    
    num_configs = len(output1_list)
    
    # Compute Rank Agreement Score (RAS) for each configuration
    ras_1 = np.array([compute_ras(output1_list[i], ground_truth_list[i]) for i in range(num_configs)])
    ras_2 = np.array([compute_ras(output2_list[i], ground_truth_list[i]) for i in range(num_configs)])
    
    # Stack both technique RAS scores for visualization
    ras_matrix = np.vstack([ras_1, ras_2])
    
    fig_width = max(12, num_configs / 50)  # Adaptive width based on number of configurations
    fig_height = 4  # Slightly taller to fit two rows
    plt.figure(figsize=(fig_width, fig_height))
    
    ax = sns.heatmap(ras_matrix, annot=num_configs <= 50, cmap="RdYlGn", center=0, fmt=".2f" if num_configs <= 50 else "",
                      xticklabels=labels if (labels and len(labels) <= 50) else "auto",
                      yticklabels=["Technique 1", "Technique 2"], linewidths=0,
                      vmin=-1, vmax=1, cbar=True)
    
    cbar = ax.collections[0].colorbar
    cbar.set_label("Rank Agreement Score (-1 to 1)")
    cbar.set_ticks([-1, 0, 1])
    cbar.set_ticklabels(["Incorrect", "Random", "Perfect"])  
    
    # plt.title("Comparison of Techniques Against Ground Truth using Rank Agreement Score")
    plt.xlabel("Configuration")
    
    if num_configs > 50:
        xticks = np.linspace(0, num_configs - 1, min(20, num_configs), dtype=int)
        ax.set_xticks(xticks)
        if labels:
            ax.set_xticklabels([labels[i] for i in xticks], rotation=0)
        else:
            ax.set_xticklabels([str(i) for i in xticks], rotation=0)
    else:
        plt.xticks(rotation=0)
    
    plt.savefig("truthfulness.pdf", bbox_inches='tight')