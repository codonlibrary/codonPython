import seaborn as sns
import random


def nhsd_colours():
    """Returns a dictionary full of the different official NHSD colours from the
    style guide:
    https://digital.nhs.uk/about-nhs-digital/corporate-information-and-documents/nhs-digital-style-guidelines/how-we-look/colour-palette

    Parameters
    ----------
    None

    Returns
    --------
    colour_dict : dict (Python dictionary)
      A dictionary containing sets of official NHS Digital branding colours
      (Hexidecimal format) and fonts.
    """

    nhsd_chart_colours = ["#005EB8", "#71CCEF", "#84919C", "#003087", "#D0D5D6"]
    nhsd_chart_background = {"chart_grey_3": "#F8F8F8", "white": "#FFFFFF"}
    nhsd_core_colours = {
        "white": "#ffffff",
        "white_tints": ["#f9fafb", "#f3f5f6", "#edeff1", "#def2e5"],
        "nhs_blue": "#005eb8",
        "blue_tints": ["#337EC6", "#ACCAE8", "#D4E4F3", "#E6EFF8"],
        "nhs_dark_grey": "#425563",
        "grey_tints": [
            "#687784",
            "#98A4AD",
            "#B3BBC1",
            "#DFE2E5",
            "#EDEFF1",
            "#F3F5F6",
            "#F9FAFB",
        ],
        "nhs_mild_grey": "#768692",
        "nhs_warm_yellow": "#FFB81C",
        "warm_yellow_tints": ["#FFE8B4", "#FFF1CC", "#FFF8E8"],
    }
    nhsd_font = ["Frutiger Light", "Frutiger Roman"]
    nhsd_font_backup = ["Arial"]
    colour_dict = {
        "chart": nhsd_chart_colours,
        "chart_background": nhsd_chart_background,
        "core": nhsd_core_colours,
        "font": nhsd_font,
        "font_backup": nhsd_font_backup,
    }
    return colour_dict


def nhsd_seaborn_style():
    """Sets the seaborn style to be inline with NHSD guidlines. This means your
    graphs in Seaborn, or in Matplotlib will come out looking as per the NHSD
    style guide. Simply run this function.

    Parameters
    ----------
    None

    Returns
    ----------
    None"""
    nhs_colours = nhsd_colours()
    chart_background = nhs_colours["chart_background"]
    font_backup = nhs_colours["font_backup"]
    chart_colours = nhs_colours["chart"]

    additional_colours = (
        nhsd_colours()["core"]["blue_tints"]
        + nhsd_colours()["core"]["grey_tints"]
        + nhsd_colours()["core"]["nhs_warm_yellow"]
        + nhsd_colours()["core"]["warm_yellow_tints"]
    )
    random.shuffle(additional_colours)
    nhs_colours = chart_colours + additional_colours

    sns.set_palette(nhs_colours)

    seaborn_style_dict = {
        "axes.axisbelow": True,
        "axes.edgecolor": ".8",
        "axes.facecolor": chart_background["chart_grey_3"],
        "axes.grid": True,
        "axes.labelcolor": ".15",
        "axes.spines.bottom": False,  # no spines
        "axes.spines.left": False,  # no spines
        "axes.spines.right": False,  # no spines
        "axes.spines.top": False,  # no spines
        "figure.facecolor": chart_background["chart_grey_3"],
        "font.family": ["sans-serif"],
        "font.sans-serif": font_backup,
        "grid.color": ".8",
        "grid.linestyle": "-",
        "image.cmap": "rocket",
        "lines.solid_capstyle": "round",
        "patch.edgecolor": "w",
        "patch.force_edgecolor": True,
        "text.color": ".15",
        "xtick.bottom": False,
        "xtick.color": ".15",
        "xtick.direction": "out",
        "xtick.top": False,
        "ytick.color": ".15",
        "ytick.direction": "out",
        "ytick.left": False,
        "ytick.right": False,
    }
    sns.set_style("whitegrid", seaborn_style_dict)
