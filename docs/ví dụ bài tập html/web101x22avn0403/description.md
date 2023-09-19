This section of the curriculum focuses on Applied Visual Design. The first group of challenges build on the given card layout to show a number of core principles.

Text is often a large part of web content. CSS has several options for how to align it with the `text-align` property.

`text-align: justify;` spaces the text so that each line has equal width.

`text-align: center;` centers the text

`text-align: right;` right-aligns the text

And `text-align: left;` (the default) left-aligns the text.

---

Align the `h4` tag's text, which says "Google", to the center. Then justify the paragraph tag which contains information about how Google was founded.

---

Phần này tập trung vào Thiết kế Trực quan . Nhóm thử thách đầu tiên xây dựng dựa trên bố cục thẻ đã cho để chỉ ra một số nguyên tắc cốt lõi.

Văn bản thường chiếm một phần lớn của nội dung web. CSS có một số tùy chọn về cách căn chỉnh văn bản với thuộc tính `text-align`

`text-align: justify;` chiều rộng của mỗi dòng văn bản bằng nhau.

`text-align: center;` căn giữa văn bản

`text-align: right;` căn phải văn bản

Và `text-align: left;` (mặc định) căn trái văn bản.

---

Căn chỉnh văn bản của `h4`, nội dung "Google" nằm ở chính giữa. Sau đó, căn chỉnh thẻ paragraph có chứa thông tin về cách Google được thành lập.

```html
<style>
  h4 {
  }
  p {
  }
  .links {
    margin-right: 20px;
  }
  .fullCard {
    border: 1px solid #ccc;
    border-radius: 5px;
    margin: 10px 5px;
    padding: 4px;
  }
  .cardContent {
    padding: 10px;
  }
</style>
<div class="fullCard">
  <div class="cardContent">
    <div class="cardText">
      <h4>Google</h4>
      <p>
        Google was founded by Larry Page and Sergey Brin while they were Ph.D.
        students at Stanford University.
      </p>
    </div>
    <div class="cardLinks">
      <a
        href="https://en.wikipedia.org/wiki/Larry_Page"
        target="_blank"
        class="links"
        >Larry Page</a
      >
      <a
        href="https://en.wikipedia.org/wiki/Sergey_Brin"
        target="_blank"
        class="links"
        >Sergey Brin</a
      >
    </div>
  </div>
</div>
```
