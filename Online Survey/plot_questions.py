import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import os

# Latex adaption for the plot 
figsize = (2.24, 1.75) # For 3 plots in a row
# figsize = (1.88, 1.5) # For 4 plots in a row
# figsize = (1.68, 1.5) # For 4 plots in a row
# figsize = (3.75, 2.92) # For slides

# Find the fonts 
font_names = mpl.font_manager.get_font_names()
print(font_names)

rc_dict = {
        'figure.figsize': figsize, # For 3 plots in a row
        'font.size': 8,
        'grid.linewidth': 0.8,
        'grid.alpha': 0.7,
        'font.size': 8,
        'font.family': 'serif',
        'font.serif': 'Times',
    }


font = {'family' : 'serif', 'weight': 'normal', 'size': 8}

#color_palaette = ["#4c72b0", "#55a868", "#c44e52", "#8172b2", "#ccb974", "#64b5cd"]

# color_palaette = ["#293462", "#F7D716", "#2B8A3E", "#5F3DC4", "#EC9B3B", "#F24C4C", "#0B7285"]

color_palette = ["#0887FE"] # AirGuard blue 
color_palette = ["#00B4FC"] # AirGuard light blue
color_palette = ["#057EFD", "#295D94"] # AirGuard dark blue


def set_size(width, fraction=1):
    """Set figure dimensions to avoid scaling in LaTeX.

    Parameters
    ----------
    width: float
            Document textwidth or columnwidth in pts
    fraction: float, optional
            Fraction of the width which you wish the figure to occupy

    Returns
    -------
    fig_dim: tuple
            Dimensions of figure in inches
    """
    # Width of figure (in pts)
    fig_width_pt = width * fraction

    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Golden ratio to set aesthetic figure height
    # https://disq.us/p/2940ij3
    golden_ratio = (5**.5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio

    fig_dim = (fig_width_in, fig_height_in)

    return fig_dim

def plot_choice_question(question_df: pd.DataFrame, question: str, survey_set: str, percentage: bool=True, out_dir="../Results/Eval/Plots", latex_width=241):

    # Set the style for the plot
    rc_dict["figure.figsize"] = set_size(latex_width)
    sns.set(style="whitegrid", font="Times", font_scale=0.8, rc=rc_dict)

    sns.set_palette(color_palette)

    # Create a barplot
    # ax = sns.barplot(x="answers", y="count", data=question_df)
    ax = sns.barplot(x="answers", y="count", data=question_df, orient="y")

    # Set the title and labels
    ax.set_xlabel(None)
    
    num_answers = len(question_df['answers'])
    # Check the length of the answers and decide if we need to replace them with a shorter version
    max_length = question_df['answers'].str.len().max()
    print(f"Max length: {max_length}")
    print(f"Num answers: {num_answers}")
    ax.set_xticks(ax.get_xticks())
    if max_length < 10 and num_answers < 5:
        # Just set them without rotation
        ax.set_xticklabels(question_df['answers'], rotation=0)
    elif max_length <= 5 and num_answers >= 5:
        ax.set_xticklabels(question_df['answers'], rotation=90) 
    elif max_length > 10 and max_length <= 17 and num_answers >= 5:
        # Set them with rotation 
        # Move the ticks a bit to the left
        ax.set_xticklabels(question_df['answers'], rotation=45, ha="right")
    else: 
        # Replace all answers with alphabetic characters, like a), b), c), ...
        
        # Create a list of alphabetic characters
        alphabet = list("abcdefghijklmnopqrstuvwxyz")
        # Get the first num_answers characters from the alphabet
        labels = alphabet[:num_answers]
        # Add the closing bracket for each 
        labels = [f"{label})" for label in labels]
        # Set the labels
        ax.set_xticklabels(labels, rotation=0)

    ax.tick_params(axis='both', which='major', pad=0)

    if percentage: 
        ax.yaxis.set_major_formatter(mpl.ticker.PercentFormatter())
        ax.set_ylabel(None)
        count_list = question_df["count"].values.tolist()
        # print(f"Containers {ax.containers[0]}")
        # print(f"Bar labels: {labels}")
        # Format as percentage with only two decimals
        if num_answers <= 10: 
            if num_answers <= 6:
                labels = [f"{label:.2f}%" for label in count_list]
            elif num_answers <= 10:
                labels = [f"{round(label)}%" for label in count_list]

            ax.bar_label(ax.containers[0], labels, fontsize=7)
            # Set a higher y limit
            ylim = ax.get_ylim()
            ax.set_ylim(ylim[0], min((ylim[1] + 5), 100))

    # plt.show()
    # Convert question to file name
    name = question.replace(" ", "_")
    name = name.replace("?", "")
    name = name.replace("/", "")
    name = os.path.normpath(f"{name}_{survey_set}.pdf")
    path = os.path.join(out_dir, name)
    print(f"Saving figure to {path}")
    plt.savefig(path,bbox_inches='tight', pad_inches=0.01)
    plt.show()
    plt.close()

def get_fig_size(width, no_of_answers:int=0, fraction=1):
    normalized_size = set_size(width, fraction)

    # Now we want to make sure its not too high for the number of answers
    max_height = normalized_size[1]
    height = min(max_height, 0.25 + 0.25 * no_of_answers)

    figsize = (normalized_size[0], height)
    return figsize

def plot_choice_question_horizontal(question_df: pd.DataFrame, question: str, survey_set: str, percentage: bool=True, out_dir="../Results/Eval/Plots", latex_width=241):
    num_answers = len(question_df['answers'])

    figsize = get_fig_size(latex_width, num_answers)
    print(f"Figsize: {figsize}")
    rc_dict["figure.figsize"] = figsize
    # Set the style for the plot
    sns.set(style="whitegrid", font="Times", font_scale=0.8, rc=rc_dict)

    sns.set_palette(color_palette)

    # Create a barplot
    # ax = sns.barplot(x="answers", y="count", data=question_df)
    ax = sns.barplot(y="answers", x="count", data=question_df, orient="h")

    # # Set the title and labels
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    
    
    # # Check the length of the answers and decide if we need to replace them with a shorter version
    # max_length = question_df['answers'].str.len().max()
    # print(f"Max length: {max_length}")
    # print(f"Num answers: {num_answers}")
    # ax.set_xticks(ax.get_xticks())
    # ax.tick_params(axis='both', which='major', pad=0)

    if percentage: 
        ax.xaxis.set_major_formatter(mpl.ticker.PercentFormatter())
        ax.set_ylabel(None)
        count_list = question_df["count"].values.tolist()
        max_percentage = question_df["count"].max()
        # print(f"Containers {ax.containers[0]}")
        # print(f"Bar labels: {labels}")
        # Format as percentage with only two decimals
        
        if num_answers <= 10: 
            labels = [f"{label:.2f}%" for label in count_list]
            # if num_answers <= 6:
            #     labels = [f"{label:.2f}%" for label in count_list]
            # elif num_answers <= 10:
            #     labels = [f"{round(label)}%" for label in count_list]

            ax.bar_label(ax.containers[0], labels, fontsize=7, padding=1.2)
            # Set a higher y limit
            xlim = ax.get_xlim()
            ax.set_xlim(xlim[0], (max_percentage + 2 + max_percentage * 0.16))

    # plt.show()
    # Convert question to file name
    name = question.replace(" ", "_")
    name = name.replace("?", "")
    name = name.replace("/", "")
    # Max file name length should be 20 characters
    if len(name) > 20:
        name = name[:20]
    name = os.path.normpath(f"{name}_{survey_set}")
    path = os.path.join(out_dir, name + ".pdf")
    plt.tight_layout()
    print(f"Saving figure to {path}")
    plt.savefig(path,bbox_inches='tight', pad_inches=0.01)
    plt.show()
    plt.close()
    path_csv = os.path.join(out_dir, name + ".csv")
    question_df.to_csv(path_csv)