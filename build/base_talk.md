```{=latex}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{listings}
\usepackage{textcomp}
\usepackage{fancyvrb}

\newcommand{\passthrough}[1]{\lstset{mathescape=false}#1\lstset{mathescape=true}}
\newcommand{\tightlist}{}
```

```{=latex}
\title{PyLint: The Good, The Bad, and the Ugly}
\author{Moshe Zadka -- https://cobordism.com}
\date{}

\begin{document}
\begin{titlepage}
\maketitle
\end{titlepage}

\frame{\titlepage}
```

```{=latex}
\begin{frame}
\frametitle{Acknowledgement of Country}

Belmont (in San Francisco Bay Area Peninsula)

Ancestral homeland of the Ramaytush Ohlone people

\end{frame}
```

I live in Belmont,
in the San Francisco Bay Area Peninsula.
I wish to acknowledge it as the
ancestral homeland
of the
Ramaytush Ohlone people.

## The Good

Hot take:
PyLint is good actually!

"PyLint can save your life"
is an exaggeration,
for the most part.
But not as much as you might think!

PyLint can keep you from
*really*
*really*
hard to find,
complicated,
bugs.

At worst,
it will save you the time of a test run.
At best,
it can help you avoid complicated production mistakes.

```{=latex}
\begin{frame}[fragile]
\frametitle{PyLint}

\pause
...is good actually.
\end{frame}
```

### Redefine function

```{=latex}
\begin{frame}[fragile]
\frametitle{Redefining functions}
```


```python
def test_add_small():
    # Math, am I right?
    assert 1 + 1 == 3
    
def test_add_large():
    assert 5 + 6 == 11
    
def test_add_small():
    assert 1 + 10 == 11
```


```{=latex}
\end{frame}
```

I...am embarassed to say how common this can be.
Naming tests is weird:
*nothing cares about the names*
and there's often not a natural name.

### Test works

```{=latex}
\begin{frame}[fragile]
\frametitle{Test works!}

\begin{lstlisting}
collected 2 items                                                                         

test.py .. 
2 passed 
\end{lstlisting}
```


```{=latex}
\end{frame}
```

But,
and here is the kicker,
if you override a name,
the testing infrastructure will happily just skip over the test!

In reality,
these files can be hundreds of lines long,
and the person adding the new test might not be aware
of all the names.
Unless someone is looking at test output carefully everything looks
fine.

Worst of all,
the
*addition of the overriding test*,
the
*breakage of the overridden test*,
and the
*problem that results in prod*
can be apart by
days,
months,
or even your years.

### Pylint finds it

```{=latex}
\begin{frame}[fragile]
\frametitle{PyLint: The Good}

\begin{lstlisting}
test.py:8:0: E0102: function already defined line 1
     (function-redefined)
\end{lstlisting}

\end{frame}
```

But like a good friend,
PyLint is there for you
when the test becomes moo.
Moo,
like a cow's opinion:
it doesn't matter.

## The Bad

```{=latex}
\begin{frame}[fragile]
\frametitle{PyLint: The Bad}
```


```python
"""Inventory abstractions"""

import attrs

@attrs.define
class Laptop:
    """A laptop"""
    ident: str
    cpu: str
```


```{=latex}
\end{frame}
```

But,
like a 90s sitcom,
the more you get into
PyLint,
the more it becomes problematic.

This is completely reasonable code
for an inventory modeling program.
Yet,
PyLint has opinions formed in the 90s,
and is not afraid to state them as facts.

But,
like a 90s sitcom,
the more you get into
PyLint,
the more it becomes problematic.

This is completely reasonable code
for an inventory modeling program.
Yet,
PyLint has opinions formed in the 90s,
and is not afraid to state them as facts.


```{=latex}
\begin{frame}[fragile]
\frametitle{PyLint: The Bad}

\begin{lstlisting}
$ pylint laptop.py | sed -n '/^laptop/s/[^ ]*: //p'
R0903: Too few public methods (0/2) (too-few-public-methods)
\end{lstlisting}

\end{frame}
```

OK,
PyLint.
You do you.

## The Ugly

```{=latex}
\begin{frame}[fragile]
\frametitle{PyLint: The Ugly}

"People will just disable the whole check if it's too picky"

PyLint issue 6987, July 3rd, 2022

\end{frame}
```

Ever wanted to add your own
unvetted opinion
to a tool used by millions?
PyLint has 12 million monthly downloads.

The attitude it takes towards adding a test with potentially many false positives is
"eh".

## Summary

### Pin


```{=latex}
\begin{frame}[fragile]
\frametitle{Pin PyLint}

\begin{lstlisting}
# pyproject.toml

[project.optional-dependencies]
pylint = ["pylint"]
\end{lstlisting}

\end{frame}
```

```{=latex}
\begin{frame}[fragile]
\frametitle{Pin PyLint}
```


```python
# noxfile.py
...
@nox.session(python=VERSIONS[-1])
def refresh_deps(session):
    """Refresh the requirements-*.txt files"""
    session.install("pip-tools")
    for deps in [..., "pylint"]:
        session.run(
            "pip-compile",
            "--extra",
            deps,
            "pyproject.toml",
            "--output-file",
            f"requirements-{deps}.txt",
        )
```

```{=latex}
\end{frame}
```

PyLint is fine,
but you need to interact with it carefully.
Pin the PyLint version you use
to avoid any surprises!

## Default deny

```{=latex}
\begin{frame}[fragile]
\frametitle{Default Deny}
```

```python
# noxfile.py
...
@nox.session(python="3.10")
def lint(session):
    files = ["src/", "noxfile.py"]
    session.install("-r", "requirements-pylint.txt")
    session.install("-e", ".")
    session.run(
        "pylint",
        "--disable=all",
        *(f"--enable={checker}" for checker in checkers)
        "src",
    )
```

```{=latex}
\end{frame}
```

Disable all checks.
Then enable ones that you think have a high
value-to-false-positive
ratio.
(Not just false-negative-to-false-positive ratio!)

### A Few of My Favorite Things

```{=latex}
\begin{frame}[fragile]
\frametitle{A few of my favorite things}
```


```python
checkers = [
    "missing-class-docstring",
    "missing-function-docstring",
    "missing-module-docstring",
    "function-redefined",
]

```

```{=latex}
\end{frame}
```

These are some of the ones I like.
Enforce consistency in the project,
avoid some obvious mistakes

```{=latex}
\begin{frame}
\frametitle{PyLint}

\begin{itemize}
\item Keep the good: \pause
      CI \pause
      Checkers \pause
\item Lose the bad:
      \pause Default deny
      \pause
\item Avoid the ugly: \pause
      Pin
\end{itemize}

\end{frame}
```

Take the good parts of PyLint:
run it in CI to keep consistency,
use the highest value checkers.

Lose the bad parts of PyLint:
default deny checkers.

Avoid the ugly parts:
pin the version to avoid surprises.

Unlike the facts of life,
here we get to only take the good parts!
And there you have the facts of PyLint.






```{=latex}
\end{document}
```
