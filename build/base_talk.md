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

## The Good (3m)

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


```{=latex}
\begin{frame}[fragile]
\frametitle{PyLint: The Bad}

\begin{lstlisting}
$ pylint laptop.py | sed -n '/^laptop/s/[^ ]*: //p'
R0903: Too few public methods (0/2) (too-few-public-methods)
\end{lstlisting}

\end{frame}
```

## The Ugly (3m)

```{=latex}
\begin{frame}[fragile]
\frametitle{PyLint: The Ugly}

"People will just disable the whole check if it's too picky"

PyLint issue 6987, July 3rd, 2022

\end{frame}
```

## Summary (3m)

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

```{=latex}
\begin{frame}
\frametitle{PyLint}

\begin{itemize}
\item Keep the good: \pause
      CI \pause
      Checkers \pause
\item Lose the bad:
      \pause (default deny)
      \pause
\item Avoid the ugly: \pause
      pin
\end{itemize}

\end{frame}
```

```{=latex}
\end{document}
```
