# How to contribute

First off, thank you for taking the time to contribute! If you have a functionality that you would like to see in codon, we have a few standards and guidelines so we can merge your pull request quicker.

## Basic idea

1. [Fork](https://help.github.com/en/articles/fork-a-repo) codonPython on GitHub.

2. Write your documented function and tests (:heart_eyes:) on a new branch, coding in line with our **coding conventions**.

3. Submit a [pull request](https://help.github.com/en/articles/creating-a-pull-request) to codonPython with a clear description of what you have done.

We suggest you make sure all of your commits are atomic (one feature per commit). Please make sure that non-obvious lines of code are commented, and variable names are as clear as possible. Please do not send us undocumented code as we will not accept it. Including tests to your pull request will bring tears of joy to our eyes, and will also probably result in a faster merge.

## Coding conventions

We use the industry standard [PEP 8](https://www.python.org/dev/peps/pep-0008/) styling guide within the `codonPython` package. **Therefore, it’s imperative that you use the coding standards found within PEP 8 when creating or modifying any code within the `codonPython` package**. Autoformatters for PEP8, for instance [autopep8](https://pypi.org/project/autopep8/), can easily ensure compliance. The reason we use PEP 8 coding standards is to make sure there is a layer of consistency across our codebase. This reduces the number of decisions that you need to make when styling your code, and also makes code easier to read when switching between functions etc.

While you are creating code, we recommend that you understand the style guide standards for the following topics:

* [Code layout](https://www.python.org/dev/peps/pep-0008/#code-lay-out) – Indentation, tabs or spaces, maximum line length, blank lines, source file encoding, imports & module level Dunder name
* [String quotes](https://www.python.org/dev/peps/pep-0008/#string-quotes)
* [Whitespace in expressions and statements](https://www.python.org/dev/peps/pep-0008/#whitespace-in-expressions-and-statements) – Pet Peeves, alternative recommendations
* [When to use trailing commas](https://www.python.org/dev/peps/pep-0008/#when-to-use-trailing-commas)
* [Comments](https://www.python.org/dev/peps/pep-0008/#comments) – Block comments, inline comments & documentation strings (docstrings)
* [Naming conventions](https://www.python.org/dev/peps/pep-0008/#naming-conventions) – Naming styles, naming conventions, names to avoid, ASCII compatibility, package and module names, class names, type variable names, exception names, global variable names, function and variable names, function and method arguments, method names and instance variables, constants & designing for inheritance
* [Programming recommendations](https://www.python.org/dev/peps/pep-0008/#programming-recommendations) – Function annotations & variable annotations

We also use docstrings and we try to follow [`numpy`'s docstring standards](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard).

Start reading our code to get a feel for it but most importantly, remember that this is open source software - consider the people who will read your code, and make it look nice for them.

* We use [PEP8](https://www.python.org/dev/peps/pep-0008/). Autoformatters for PEP8, for instance [autopep8](https://pypi.org/project/autopep8/), can easily ensure compliance.
* We use docstrings and we try to (loosely) follow [`numpy`'s docstring standards](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard).
* This is open source software. Consider the people who will read your code, and make it look nice for them.

## Code of Conduct

As a contributer you can help us keep the Codon community open and inclusive. Please read and follow our [Code of Conduct](https://github.com/codonlibrary/code-of-conduct/tree/master). By contributing to it, you agree to comply with it.

:clinking_glasses: Thank you!
Team codon