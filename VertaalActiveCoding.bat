REM Vertaal ActiveCoding in Windows

latexmk -pdf ActiveCoding.tex

bibtext activeCoding

makeindex activeCoding.glo -s nomencl.ist -o activeCoding.gls


latexmk -pdf ActiveCoding.tex

bibtext activeCoding

latexmk -pdf ActiveCoding.tex