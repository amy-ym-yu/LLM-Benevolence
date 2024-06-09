import pandas as pd
import matplotlib.pyplot as plt
import textwrap
import numpy as np
from itertools import product

# Notes
# ------------------------------------------------------------------------------------------------------------------------------------------------------------
# python3 -m venv env; source env/bin/activate; pip install pandas matplotlib product 
# python3 dataplot.py 

# Function to wrap labels
def wrap_labels(labels, width):
    return ['\n'.join(textwrap.wrap(label, width)) for label in labels]

# ------------------------------------------------------------------------------------------------------------------------------------------------------------

def conditionsbarplot(data, y_columns, x_columns):
    
    # Plot
    plt.rcParams.update({'font.size': 14, 'axes.titlesize': 18, 'axes.labelsize': 16, 'xtick.labelsize': 14, 'ytick.labelsize': 14, 'legend.fontsize': 14})
    for y in y_columns:
        for x in x_columns:
            plt.figure(figsize=(18, 10))
            means = data.groupby([x, 'Source'])[y].mean().unstack().reset_index()
            n_bars = len(means)
            labels = means[x].astype(str)
            wrapped_labels = wrap_labels(labels, 10)
            x_pos = range(len(means))
            bar_width = 0.35
            bars1 = plt.bar(x_pos, means['GPT'], width=bar_width, label='GPT', color=plt.cm.Blues(0.6))
            bars2 = plt.bar([p + bar_width for p in x_pos], means['Claude'], width=bar_width, label='Claude', color=plt.cm.Greens(0.6))

            for bar in bars1:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}', ha='center', va='bottom')

            for bar in bars2:
                height = bar.get_height()
                plt.text(bar.get_x() + bar_width / 2, height, f'{height:.2f}', ha='center', va='bottom')

            plt.xlabel(x)
            plt.ylabel(y)
            plt.title(f'{y} by {x}')
            plt.xticks([p + bar_width / 2 for p in x_pos], wrapped_labels, rotation=0)
            plt.legend()
            plt.tight_layout()
            plt.show()

# Load and Combine GPT/Calude Data
gpt_file = "gpt_responses_enum.csv"
gpt_data = pd.read_csv(gpt_file)
gpt_data['Source'] = 'GPT'
claude_file = "claude_responses_enum.csv"
claude_data = pd.read_csv(claude_file)
claude_data['Source'] = 'Claude'
combined_data = pd.concat([gpt_data, claude_data])
y_columns = ['Overall Score', 'Minutes Waited']
x_columns = ['Age', 'Gender', 'Race', 'Option']

# Plot Scores / Times by feature
conditionsbarplot(combined_data, y_columns, x_columns)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------

def comparescoresbarplot(data, features):
    
    # Plot
    plt.rcParams.update({'font.size': 14, 'axes.titlesize': 18, 'axes.labelsize': 16,'xtick.labelsize': 14, 'ytick.labelsize': 14, 'legend.fontsize': 14})
    fig, ax = plt.subplots(figsize=(18, 10))
    bar_width = 0.35
    r = np.arange(len(features))
    colors = {'GPT': plt.cm.Blues(0.6), 'Claude': plt.cm.Greens(0.6)}

    for i, source in enumerate(data['Source'].unique()):
        means = []
        for feature in features:
            mean_score = data[data['Source'] == source].groupby(feature)['Overall Score'].mean().mean()
            means.append(mean_score)
        bars = ax.bar(r + i * bar_width, means, color=colors[source], width=bar_width, edgecolor='white', label=f'{source}')
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

    ax.set_title('Average Overall Score by Category')
    ax.set_xlabel('Categories')
    ax.set_ylabel('Average Score')
    ax.set_xticks(r + bar_width / 2)
    ax.set_xticklabels(features, rotation=0)
    ax.legend()
    plt.tight_layout()
    plt.show()

# Load and Combine GPT/Calude Data
gpt_file = "gpt_responses_enum.csv"
gpt_data = pd.read_csv(gpt_file)
gpt_data['Source'] = 'GPT'
claude_file = "claude_responses_enum.csv"
claude_data = pd.read_csv(claude_file)
claude_data['Source'] = 'Claude'
combined_data = pd.concat([gpt_data, claude_data])

# Plot Comparison of All Average Scores / Feature
features = ['Age', 'Gender', 'Race', 'Option']
comparescoresbarplot(combined_data, features)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------

def actionsbarplot(average_gpt_score, average_claude_score, average_survey_scores):

    # Increase Font
    plt.rcParams.update({'font.size': 14, 'axes.titlesize': 18, 'axes.labelsize': 16, 'xtick.labelsize': 14, 'ytick.labelsize': 14, 'legend.fontsize': 14})
    
    # Plot
    plt.figure(figsize=(18, 10))
    combined_scores = pd.DataFrame({'Action': ['GPT', 'Claude'] + list(average_survey_scores.index),'Average Score': [average_gpt_score, average_claude_score] + list(average_survey_scores.values)})
    colors = ['blue', 'green'] + ['orange'] * len(average_survey_scores)
    bars = plt.bar(combined_scores['Action'], combined_scores['Average Score'], color=colors, alpha=0.6, width=0.6)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}', ha='center', va='bottom')

    labels = wrap_labels(combined_scores['Action'], 10)
    plt.xticks(ticks=range(len(labels)), labels=labels, rotation=0, ha='right')
    plt.xlabel('Actions')
    plt.ylabel('Average Score')
    plt.title('Average Benevolence Scores: Claude vs GPT vs Google Survey')
    plt.legend([bars[0], bars[1], bars[2]], ['GPT Actions Score', 'Claude Actions Score', 'Survey Actions Score'])
    plt.tight_layout()
    plt.show()

# Get average scores from gpt/claude/survey data 
gpt_file = "gpt_responses_enum.csv"
gpt_data = pd.read_csv(gpt_file)
average_gpt_score = gpt_data['Overall Score'].mean()
claude_file = "claude_responses_enum.csv"
claude_data = pd.read_csv(claude_file)
average_claude_score = claude_data['Overall Score'].mean()
survey_file = "BenevolenceSurveyResponses.csv"
survey_data = pd.read_csv(survey_file)
survey_data = survey_data.iloc[:, 1:]
average_survey_scores = survey_data.mean() * 10

# Plot scores by action
actionsbarplot(average_gpt_score, average_claude_score, average_survey_scores)
