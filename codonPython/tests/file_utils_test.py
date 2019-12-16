from codonPython.file_utils import compare
from codonPython.file_utils import file_search
from codonPython.file_utils import import_files
import numpy as np
import pytest
import pandas as pd

df1 = pd.DataFrame(
    {
        "A": [1, 5, 6, 1, 8, 5, 9],
        "B": [2, 8, 5, 2, 21, 3, 5],
        "C": [3, 4, 5, 3, 1, 5, 9],
        "D": [2, 8, 5, 2, 4, 6, 2],
        "E": [1, 2, 6, 1, 3, 5, 5],
    }
)

df2 = pd.DataFrame(
    {
        "A": [1, 5, 6, 1, 9, 5, 9],
        "B": [2, 9, 5, 2, 21, 3, 5],
        "C": [3, 4, 5, 3, 1, 35, 9],
        "D": [2, 8, 7, 2, 4, 6, 2],
        "E": [1, 2, 46, 1, 3, 8, 5],
    }
)

dict_test = {
    "same_values": pd.DataFrame(
        np.array([[1, 2, 3, 2, 1], [9, 5, 9, 2, 5]]), columns=["A", "B", "C", "D", "E"]
    ),
    "df1_not_df2": pd.DataFrame(
        np.array([[5, 8, 4, 8, 2], [6, 5, 5, 5, 6], [8, 21, 1, 4, 3], [5, 3, 5, 6, 5]]),
        columns=["A", "B", "C", "D", "E"],
    ),
    "df2_not_df1": pd.DataFrame(
        np.array(
            [[5, 9, 4, 8, 2], [6, 5, 5, 7, 46], [9, 21, 1, 4, 3], [5, 3, 35, 6, 8]]
        ),
        columns=["A", "B", "C", "D", "E"],
    ),
    "df1_dups": pd.DataFrame(
        np.array([[1, 2, 3, 2, 1]]), columns=["A", "B", "C", "D", "E"]
    ),
    "df2_dups": pd.DataFrame(
        np.array([[1, 2, 3, 2, 1]]), columns=["A", "B", "C", "D", "E"]
    ),
    "Same": False,
}


@pytest.mark.parametrize(
    "x, y, names, dups, same, expected",
    [
        (
            pd.DataFrame(
                {
                    "A": [1, 5, 6, 1, 8, 5, 9],
                    "B": [2, 8, 5, 2, 21, 3, 5],
                    "C": [3, 4, 5, 3, 1, 5, 9],
                    "D": [2, 8, 5, 2, 4, 6, 2],
                    "E": [1, 2, 6, 1, 3, 5, 5],
                }
            ),
            pd.DataFrame(
                {
                    "A": [1, 5, 6, 1, 9, 5, 9],
                    "B": [2, 9, 5, 2, 21, 3, 5],
                    "C": [3, 4, 5, 3, 1, 35, 9],
                    "D": [2, 8, 7, 2, 4, 6, 2],
                    "E": [1, 2, 46, 1, 3, 8, 5],
                }
            ),
            ["df1", "df2"],
            True,
            True,
            dict_test,
        )
    ],
)
def test_compare_BAU(x, y, names, dups, same, expected):
    dict_test1 = compare(x, y, names=["df1", "df2"], dups=True, same=True)
    for i in expected.keys():
        if i == "Same":
            assert dict_test1[i] == expected[i]
        else:
            for j in expected[i]:
                list_test1 = list(dict_test1[i][j])
                list_exp = list(expected[i][j])
                assert list_test1 == list_exp


@pytest.mark.parametrize(
    "doctype, like, strict, expected", [("md", ["README"], True, ["README.md"])]
)
def test_file_search_BAU(doctype, like, strict, expected):
    assert file_search(doctype=doctype, like=like, strict=strict) == expected


@pytest.mark.parametrize("expected", [({})])
def test_import_files_BAU(expected):
    assert import_files() == expected


@pytest.mark.parametrize("subdir, expected", [(True, {})])
def test_import_files_BAU_2(subdir, expected):
    assert import_files(subdir=subdir) == expected


@pytest.mark.parametrize("strict,subdir, expected", [(True, True, {})])
def test_import_files_BAU_3(strict, subdir, expected):
    assert import_files(strict=strict, subdir=subdir) == expected


# ----------------Console output-------------------------


@pytest.mark.parametrize(
    "x, y, names, dups, same, comment",
    [
        (
            pd.DataFrame(
                {
                    "A": [1, 5, 6, 1, 8, 5, 9],
                    "B": [2, 8, 5, 2, 21, 3, 5],
                    "C": [3, 4, 5, 3, 1, 5, 9],
                    "D": [2, 8, 5, 2, 4, 6, 2],
                    "E": [1, 2, 6, 1, 3, 5, 5],
                }
            ),
            pd.DataFrame(
                {
                    "A": [1, 5, 6, 1, 9, 5, 9],
                    "B": [2, 9, 5, 2, 21, 3, 5],
                    "C": [3, 4, 5, 3, 1, 35, 9],
                    "D": [2, 8, 7, 2, 4, 6, 2],
                    "E": [1, 2, 46, 1, 3, 8, 5],
                }
            ),
            ["df1", "df2"],
            True,
            True,
            True,
        )
    ],
)
def test_compare_console(x, y, names, dups, same, comment, capsys):
    dict_test1 = compare(
        x, y, names=["df1", "df2"], dups=True, same=True, comment=comment
    )
    captured = capsys.readouterr()
    assert (
        captured.out
        == "\nThere are "
        + str(dict_test1["same_values"].shape[0])
        + " same values\nThere are "
        + str(dict_test1[names[0] + "_not_" + names[1]].shape[0])
        + " outliers in "
        + str(names[0])
        + "\nThere are "
        + str(dict_test1[names[1] + "_not_" + names[0]].shape[0])
        + " outliers in "
        + str(names[1])
        + "\nThere are "
        + str(dict_test1[names[0] + "_dups"].shape[0])
        + " duplicates in "
        + str(names[0])
        + "\nThere are "
        + str(dict_test1[names[1] + "_dups"].shape[0])
        + " duplicates in "
        + str(names[1])
        + "\nDataFrames are not the same\n"
    )

# -------------ValueError tests-----------------

# -------------File Search----------------------


@pytest.mark.parametrize("like", [("txt")])
def test_file_search_ValueError_1(like):

    with pytest.raises(ValueError):

        file_search(like=like)


@pytest.mark.parametrize("path", [(1)])
def test_file_search_ValueError_2(path):

    with pytest.raises(ValueError):

        file_search(path=path)


@pytest.mark.parametrize("doctype", [(["txt"])])
def test_file_search_ValueError_3(doctype):

    with pytest.raises(ValueError):

        file_search(doctype=doctype)


@pytest.mark.parametrize("strict", [("True")])
def test_file_search_ValueError_4(strict):

    with pytest.raises(ValueError):

        file_search(strict=strict)


# -----------------Import files-------------------------


@pytest.mark.parametrize("like", [("txt")])
def test_import_files_ValueError_1(like):

    with pytest.raises(ValueError):

        import_files(like=like)


@pytest.mark.parametrize("subdir", [("True")])
def test_import_files_ValueError_2(subdir):

    with pytest.raises(ValueError):

        import_files(subdir=subdir)


@pytest.mark.parametrize("doctype", [(["txt"])])
def test_import_files_ValueError_3(doctype):

    with pytest.raises(ValueError):

        import_files(doctype=doctype)


@pytest.mark.parametrize("sheet", [(1)])
def test_import_files_ValueError_4(sheet):

    with pytest.raises(ValueError):

        import_files(sheet=sheet)


@pytest.mark.parametrize("path", [(["Desktop"])])
def test_import_files_ValueError_5(path):

    with pytest.raises(ValueError):

        import_files(path=path)


@pytest.mark.parametrize("strict", [("True")])
def test_import_files_ValueError_6(strict):

    with pytest.raises(ValueError):

        import_files(strict=strict)


# ---------------Compare--------------------------


@pytest.mark.parametrize("names", [("txt")])
def test_compare_ValueError_1(names):

    with pytest.raises(ValueError):

        compare(df1, df2, names=names)


@pytest.mark.parametrize("x", [([1, 2, 3])])
def test_compare_ValueError_2(x):

    with pytest.raises(ValueError):

        compare(x, df2, names=["x", "df2"])


@pytest.mark.parametrize("dups", [("True")])
def test_compare_ValueError_3(dups):

    with pytest.raises(ValueError):

        compare(df1, df2, names=["df1", "df2"], dups=dups)


@pytest.mark.parametrize("same", [("True")])
def test_compare_ValueError_4(same):

    with pytest.raises(ValueError):

        compare(df1, df2, names=["df1", "df2"], same=same)


@pytest.mark.parametrize("comment", [("True")])
def test_compare_ValueError_5(comment):

    with pytest.raises(ValueError):

        compare(df1, df2, names=["df1", "df2"], comment=comment)


@pytest.mark.parametrize("y", [([1, 2, 3])])
def test_compare_ValueError_6(y):

    with pytest.raises(ValueError):

        compare(df1, y, names=["df1", "y"])
