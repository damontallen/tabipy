import re
import pytest
from tabipy import Table

@pytest.fixture
def t():
    "Returns the table used in the align tests"
    t = Table((1,2,3),
              (4,5,6),
              (7,8,9))
    t.align('Center')
    return t
    
def test_global_align_method_html():
    "This tests that the global align method works in html"
    T = t()
    t1_html = T._repr_html_()
    row_split = re.compile('<\s*tr\s*>')
    lines = row_split.split(t1_html)
    assert len(lines)==4
    col_split = re.compile('>[\s\d\s]*<')
    parts = col_split.split(lines[1])
    cl_check = re.compile('text-align\s*:\s*center')
    assert len(cl_check.findall(parts[0]))>0
    
def test_global_align_method_latex():
    "This tests that the global align method works in latex"
    T = t()
    t1_latex = T._repr_latex_()
    row_split = re.compile(r'\\\\')
    lines = row_split.split(t1_latex)
    assert len(lines)==4
    col_split = re.compile('&')
    parts = col_split.split(lines[0])
    cl_check = re.compile(r'\\begin\s*{\s*tabular\s*}\s*{\s*\*\s*{\s*3\s*}\s*{\s*c\s*}')
    assert len(cl_check.findall(parts[0]))>0
    
def test_cell_align_property_html():
    "This tests that cell align property works in html"
    T = t()
    T.cell(1,1).align = 'Right'
    t1_html = T._repr_html_()
    row_split = re.compile('<\s*tr\s*>')
    lines = row_split.split(t1_html)
    assert len(lines)==4
    col_split = re.compile('>[\s\d\s]*<')
    line_1_parts = col_split.split(lines[1])
    cl_check = re.compile('text-align\s*:\s*center')
    assert len(cl_check.findall(line_1_parts[0]))>0
    line_2_parts = col_split.split(lines[2])
    cl_check = re.compile('text-align\s*:\s*right')
    assert len(cl_check.findall(line_2_parts[2]))>0
    
def test_cell_align_property_latex():
    "This tests that cell align property works in latex"
    T = t()
    T.cell(1,1).align = 'Right'
    t1_latex = T._repr_latex_()
    row_split = re.compile(r'\\\\')
    lines = row_split.split(t1_latex)
    assert len(lines)==4
    col_split = re.compile('&')
    parts = col_split.split(lines[1])
    cl_check = re.compile('\w*\\multicolumn\s*\{\s*1\s*}\s*\{\s*r\s*}')
    assert len(cl_check.findall(parts[1]))>0
