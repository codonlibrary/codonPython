import numpy as np, pandas as pd
from matplotlib import pyplot as plt

# There's a bit of a backlash against pie charts
# e.g. https://www.perceptualedge.com/articles/visual_business_intelligence/save_the_pies_for_dessert.pdf
# It's normally recommended to use a bar chart or just a table instead
# If you really want to show proportions of a whole visually, a stacked bar is usually better choice
# This will make one!

# Replace the labels and values for each section of the bar
# The top item in this list will appear at the bottom of the chart
# Make sure your values add up to 1

df = pd.DataFrame({
    'Merged - no contact needed (2, 3%)': pd.Series([0.0333333333333333], index=['']),
    'Does not need to submit (3, 5%)': pd.Series([0.05], index=['']),
    'Differences resolved - remaining difference accounted for': pd.Series([0.0666666666666667], index=['']),
    'Differences resolved - small or no difference remains': pd.Series([0.383333333333333], index=['']),
    'Trust contacted - they have identified the problem and are working on a fix (13, 22%)': pd.Series([0.216666666666667], index=['']),
    'Trust contacted - they are investigating the issue (2, 3%)': pd.Series([0.0333333333333333], index=['']),
    'Greater than 5% difference remains - trust not yet contacted (3, 5%)': pd.Series([0.05], index=['']),
    'Very large difference remains (5, 8%)': pd.Series([0.0833333333333333], index=['']),
    'Non-submitters (5, 8%)': pd.Series([0.0833333333333333], index=['']),
})

# Define a color for each section, corresponding to the bars you set up above.

pal=[
    '#a9d38e',
    '#a9d38e',
    '#a9d38e',
    '#a9d38e',
    '#ffcf63',
    '#ffcf63',
    '#ffcf63',
    '#ff7169',
    '#ff7169',
    '#ff7169',
]

# edgecolor here is the line colour of the bars
ax = df.plot.bar(title="", legend=False, figsize=(10,5), width=10, stacked=True, color=pal, edgecolor="#34495e", linewidth=0.5)

#set the distance between the y axis ticks with the "step" values below
major_yticks = np.arange(0, 1.01, step=0.1)
minor_yticks = np.arange(0, 1.01, step=0.05)

ax.set_yticks(major_yticks)
ax.set_yticks(minor_yticks, minor = True)
ax.grid(which = 'minor', alpha = 0)
ax.grid(which = 'major', alpha = 0)
ax.set_ylim([0,1])
ax.set_xlim([0,1])

ax.set_yticklabels(['{:,.0%}'.format(x) for x in ax.get_yticks()])

def annotateBars(row, ax=ax):
    cumulative_height = 0
    bar = 0
    # each bar (starting from the bottom of the chart) is indexed as "bar" in the loop below, so if bar = 0 that's the bottom bar, bar = 1 is the one above, and so on. If you want to change the font size, position, colour or whatever of an individual label, add an elif below, add in whatever conditions you need. Use the else for your default setting.
    for col in row.index:
        if bar == 0:
            label_height = 3
            label_fontsize = 7
        elif bar == 5:
            label_height = 3
            label_fontsize = 7
        elif bar == 6:
            label_height = 3
            label_fontsize = 7
        else:
            label_height = 2.3
            label_fontsize = 7
        if (str(cumulative_height) != 'nan'):
            ax.text(0.5, cumulative_height + (row[col] / label_height), col, horizontalalignment='center', fontsize=label_fontsize, weight='normal')
        cumulative_height += row[col]
        bar += 1

df.apply(annotateBars, ax=ax, axis=1)

fig1 = plt.gcf()

plt.figure(figsize=(10,10))

# Set the filename here, the facecolor is the background color behind the chart
fig1.savefig("Stacked-bar.png", bbox_inches='tight', dpi=300, facecolor='#ffffff')