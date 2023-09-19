from bs4 import BeautifulSoup
from dmoj.result import CheckerResult
from dmoj.utils.unicode import utf8text
from dmoj.utils.css_parser import parse_css

def check(process_output, judge_output, judge_input, point_value, submission_source, **kwargs):
    input = judge_input.decode('utf-8').strip()
    
    source = submission_source.decode('utf-8').strip()

    soup = BeautifulSoup(source, 'html.parser')
    
    css = parse_css(soup)
    
    # criteria 1
    if input == "Class flavor có width 75%":
        flavor = css.get(".flavor")
        
        if not flavor: 
            return CheckerResult(False, 0, "Không có .flavor")
        
        width = flavor.get("width")
        if not width: 
            return CheckerResult(False, 0, ".flavor không có width")
        
        if width == '75%':
            return CheckerResult(True, point_value, "")
        else:
            return CheckerResult(False, 0, ".flavor width phải là 75%")
        
    # criteria 2
    if input == "Class price có width 25%":
        price = css.get(".price")
        
        if not price: 
            return CheckerResult(False, 0, "Không có .price")
        
        width = price.get("width")
        if not width: 
            return CheckerResult(False, 0, ".price không có width")
        
        if width == '25%':
            return CheckerResult(True, point_value, "")
        else:
            return CheckerResult(False, 0, ".price width phải là 25%")
        
    return CheckerResult(False, 0, "Lỗi checker")