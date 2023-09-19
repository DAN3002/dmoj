```html
<style>
  h2 {
    color: blue;
  }
</style>

<h2></h2>
```

```python
from bs4 import BeautifulSoup, Comment
from dmoj.result import CheckerResult
from dmoj.utils.chrome_driver import get_driver
import re

def check(process_output, judge_output, judge_input, point_value, submission_source, **kwargs):
  input = judge_input.decode('utf-8').strip()

  source = submission_source.decode('utf-8').strip()

  soup = BeautifulSoup(source, 'html.parser')

  # criteria 1
  if input == "Attribute style của phần tử h2 cần được loại bỏ":
    if soup.find("h2", style=True):
      return CheckerResult(False, 0, "")
    return CheckerResult(True, point_value, "")

  # criteria 2
  if input == "Có một phần tử style":
    if len(soup.find_all("style")) == 1:
      return CheckerResult(True, point_value, "")
    return CheckerResult(False, 0, "")

  # criteria 3
  if input == "Phần tử h2 có màu blue":
    driver = get_driver(source)
    h2 = driver.find_element_by_tag_name('h2')
    color = driver.get_computed_style(h2, 'color') if h2 is not None else ""
    driver.quit()

    if color == "rgb(0, 0, 255)":
      return CheckerResult(True, point_value, "")
    return CheckerResult(False, 0, "")

  # criteria 4
  if input == "Khai báo stylesheet cho h2 cần hợp lệ với một dấu chấm phẩy và dấu ngoặc nhọn đóng":
    if len(soup.find_all("style")) != 1:
      return CheckerResult(False, 0, "")

    style_string = re.sub(r"[\t\r\n ]+", "", soup.style.string).strip()

    if re.fullmatch(r"h2\{color:blue;\}", style_string):
      return CheckerResult(True, point_value, "")
    return CheckerResult(False, 0, "")

  # criteria 5
  if input == "Phần tử style cần có thẻ đóng":
    if soup.style and len(soup.find_all("style")) == source.count("</style>"):
     return CheckerResult(True, point_value, "")
    return CheckerResult(False, 0, "")

  return CheckerResult(False, 0, "Lỗi checker")
```
