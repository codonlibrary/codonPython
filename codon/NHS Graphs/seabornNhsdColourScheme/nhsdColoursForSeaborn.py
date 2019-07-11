"""Sets the seaborn colour palette to the NHS Digital colours
"""
import seaborn as sns

# Set colours
nhsdColours = ["#003087", "#005EB8", "#71CCEF", "#84919C", "#D0D5D6", "#F8F8F8"]
sns.set_palette(nhsdColours)

# Visualise palette
sns.palplot(sns.color_palette())
