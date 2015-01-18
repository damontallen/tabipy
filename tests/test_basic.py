from tabipy import Table, TableRow, TableCell, TableHeaderRow, TableHeader
import re

def test_simple():
    # For now, this is little more than a smoke test to check that it's not
    # erroring out.
    t = Table(TableHeaderRow('a','b','c'),
          (1,  2,  3),
          (2,  4,  6),
         )
    
    html = t._repr_html_()
    assert '<th' in html
    assert '<td' in html
    
    latex = t._repr_latex_()
    assert r'\hline' in latex

def test_tableheader():
    t = Table((TableHeader('a'), 1, 2),
              (TableHeader('b'), 3, 4),
              (TableHeader('c'), 5, 6))

    html = t._repr_html_()
    assert html.count('<th') == 3

    latex = t._repr_latex_()
    assert latex.count(r'\bf') == 3

def test_escape():
    inp_expected = (('', ''),
                    ('&', r'\&'),
                    ('\\', r'{\textbackslash}'),
                    ('~', r'{\textasciitilde}'),
                    ('$', '\$'),
                    ('\n', r'{\linebreak}'),
                    ('\r', r'{\linebreak}'),
                    ('\r\n', r'{\linebreak}'),
                    ('_', r'\_'),
                    ('{', '\{'),
                    ('}', '\}'),
                    ('body & mind & r&d', r'body \& mind \& r\&d'),
                    (r'\_/~\_/', 
                     r'{\textbackslash}\_/{\textasciitilde}'
                     r'{\textbackslash}\_/'),
                    ('~_$\r\n{}', 
                     r'{\textasciitilde}\_\${\linebreak}\{\}'))
    for inp, expected in inp_expected:
        cell = TableCell(inp)
        assert cell._repr_latex_() == expected

def col_span_table():
    "Returns the table used in the col_span tests"
    t = Table((1,2,3),
      (4,5,6),
      (7,8,9))
    cell_1_1 = t.rows[0].cells[0]
    cell_1_1.col_span = 2
    return t

def test_col_span_html():
    "This test col_span works in html"
    t = col_span_table()
    t1_html = t._repr_html_()
    row_split = re.compile('<\s*tr\s*>')
    lines = row_split.split(t1_html)
    assert len(lines)==4
    col_split = re.compile('>[\s\d\s]*<')
    parts = col_split.split(lines[1])
    cl_check = re.compile('colspan\s*=\s*"\s*2\s*"')
    assert len(cl_check.findall(parts[0]))>0
    #print("pass")

def test_col_span_latex():
    "This test col_span works in latex"
    t = col_span_table()    
    t1_latex = t._repr_latex_()
    row_split = re.compile(r'\\\\')
    lines = row_split.split(t1_latex)
    assert len(lines)==4
    col_split = re.compile('&')
    parts = col_split.split(lines[0])
    cl_check = re.compile('\w*\\multicolumn\s*\{\s*2\s*}')
    assert len(cl_check.findall(parts[0]))>0
    #print("pass")
