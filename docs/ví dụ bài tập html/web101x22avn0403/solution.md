### Freecodecamp

```html
<style>
  .center {
    text-align: center;
  }

  .justify {
    text-align: justify;
  }
</style>
<h4 class="center"></h4>
<p class="justify"></p>
```

```html
<style>
  h4 {
    text-align: center;
  }

  p {
    text-align: justify;
  }
</style>
<h4></h4>
<p></p>
```

```html
<h4 style="text-align: center"></h4>
<p style="text-align: justify"></p>
```

### DMOJ

Code mẫu có thẻ `<style>` cùng với selector `p` và `h4` có sẵn nên mình chỉ check set css bằng selectors `p` và `h4`

```html
<style>
  h4 {
    text-align: center;
  }

  p {
    text-align: justify;
  }
</style>
<h4></h4>
<p></p>
```

```python
from bs4 import BeautifulSoup
from dmoj.result import CheckerResult
from dmoj.utils.css_parser import parse_css

def check(process_output, judge_output, judge_input, point_value, submission_source, **kwargs):
  input = judge_input.decode('utf-8').strip()

  source = submission_source.decode('utf-8').strip()

  soup = BeautifulSoup(source, 'html.parser')

  css = parse_css(soup)

  # criteria 1
  if input == "Sử dụng property text-align với giá trị là center cho thẻ h4":
    if soup.h4 and css.get("h4") and css.get("h4").get("text-align") == "center":
      return CheckerResult(True, point_value, "")
    return CheckerResult(False, 0, "")

  # criteria 2
  if input == "Sử dụng property text-align với giá trị justify cho thẻ p":
    if soup.p and css.get("p") and css.get("p").get("text-align") == "justify":
      return CheckerResult(True, point_value, "")
    return CheckerResult(False, 0, "")

  return CheckerResult(False, 0, "Lỗi checker")
```
