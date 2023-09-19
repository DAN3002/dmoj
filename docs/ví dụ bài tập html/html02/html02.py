from bs4 import BeautifulSoup
from dmoj.result import CheckerResult

def check(process_output, judge_output, judge_input, point_value, submission_source, **kwargs):
    input = judge_input.decode('utf-8').strip()
    source = submission_source.decode('utf-8').strip()

    soup = BeautifulSoup(source, 'html.parser')
    h1s = soup.find_all('h1')
    if not h1s:
        return CheckerResult(False, 0, "Thiếu thẻ h1")
    
    if len(h1s) > 1:
        return CheckerResult(False, 0, "Quá nhiều thẻ h1")
    
    h1 = h1s[0]
    
    if h1.text != 'CatPhotoApp':
        return CheckerResult(False, 0, "Nội dung thẻ h1 phải là CatPhotoApp")
    
    h2 = h1.find_next_sibling('h2')
    
    if not h2:
        return CheckerResult(False, 0, "Thiếu thẻ h2 phía sau h1")
    
    if h2.text != 'Cat Photos':
        return CheckerResult(False, 0, "Nội dung thẻ h2 phải là Cat Photos")

        
    return CheckerResult(True, point_value, "Chính xác")