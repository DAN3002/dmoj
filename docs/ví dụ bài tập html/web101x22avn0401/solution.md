```html
<h2 style="color: red;"></h2>
```

```python
from bs4 import BeautifulSoup, Comment
from dmoj.result import CheckerResult
from dmoj.utils.css_parser import parse_inline_css

def check(process_output, judge_output, judge_input, point_value, submission_source, **kwargs):
  input = judge_input.decode('utf-8').strip()

  source = submission_source.decode('utf-8').strip()

  soup = BeautifulSoup(source, 'html.parser')

  # criteria 1
  if input == "Phần tử h2 có khai báo attribute style":
    if soup.find("h2", style=True):
      return CheckerResult(True, point_value, "")
    return CheckerResult(False, 0, "")

  # criteria 2
  if input == "Phần tử h2 có color được đặt giá trị là red":

    if len(soup.find_all("h2")) != 1:

      return CheckerResult(False, 0, "")

    if soup.h2.get("style") is None:

      return CheckerResult(False, 0, "")

    css = parse_inline_css(soup.h2)

    if css.get("color") == "red":
      return CheckerResult(True, point_value, "")

    return CheckerResult(False, 0, "")

  # criteria 3
  if input == "Khai báo style phải kết thúc với một dấu ;":

    if len(soup.find_all("h2")) != 1:

      return CheckerResult(False, 0, "")

    style = soup.h2.get("style")

    if style is None:

      return CheckerResult(False, 0, "")

    if style.count(";") > 0 and style.strip().rfind(";") == len(style.strip()) - 1:

      return CheckerResult(True, point_value, "")
    return CheckerResult(False, 0, "")

  return CheckerResult(False, 0, "Lỗi checker")
```
