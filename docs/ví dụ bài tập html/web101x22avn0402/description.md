With CSS, there are hundreds of CSS properties that you can use to change the way an element looks on your page.

When you entered `<h2 style="color: red;">CatPhotoApp</h2>`, you were styling that individual `h2` element with inline CSS, which stands for Cascading Style Sheets.

That's one way to specify the style of an element, but there's a better way to apply CSS.

At the top of your code, create a `style` block like this:

```html
<style></style>
```

Inside that style block, you can create a CSS selector for all `h2` elements. For example, if you wanted all `h2` elements to be red, you would add a style rule that looks like this:

```html
<style>
  h2 {
    color: red;
  }
</style>
```

Note that it's important to have both opening and closing curly braces (`{` and `}`) around each element's style rule(s). You also need to make sure that your element's style definition is between the opening and closing style tags. Finally, be sure to add a semicolon to the end of each of your element's style rules.

---

Delete your h2 element's style attribute, and instead create a CSS style block. Add the necessary CSS to turn all h2 elements blue.

---

Với CSS, có hàng trăm thuộc tính CSS mà bạn có thể sử dụng để thay đổi giao diện của một phần tử trên trang của bạn.

Khi bạn nhập `<h2 style="">CatPhotoApp</h2>`, bạn đang tạo style cho từng phần tử h2 bằng CSS inline, viết tắt của Cascading Style Sheets.

Đó là một cách để chỉ định style cho một phần tử, nhưng có một cách tốt hơn để áp dụng CSS.

Ở phần mở đầu, hãy tạo một khối `style` như sau:

```html
<style></style>
```

Bên trong khối `style` đó, bạn có thể tạo bộ chọn CSS cho tất cả các phần tử `h2`. Ví dụ: nếu bạn muốn tất cả các phần tử `h2` có màu đỏ, bạn sẽ thêm quy tắc style giống như sau:

```html
<style>
  h2 {
    color: red;
  }
</style>
```

Lưu ý phải có cả dấu ngoặc nhọn mở và đóng (`{` và `}`) xung quanh quy tắc style của mỗi phần tử. Đảm bảo rằng việc tạo style cho phần tử nằm giữa thẻ mở và thẻ đóng của thẻ style. Cuối cùng, hãy thêm dấu chấm phẩy vào cuối mỗi quy tắc style.

---

Xóa thuộc tính style ở phần tử `h2` và thay vào đó tạo một khối `style` CSS. Thêm CSS cần thiết để chuyển tất cả các phần tử `h2` thành màu xanh lam.

```html
<h2 style="color: red;">CatPhotoApp</h2>
<main>
  <p>Click here to view more <a href="#">cat photos</a>.</p>

  <a href="#"
    ><img
      src="https://cdn.freecodecamp.org/curriculum/cat-photo-app/relaxing-cat.jpg"
      alt="A cute orange cat lying on its back."
  /></a>

  <div>
    <p>Things cats love:</p>
    <ul>
      <li>cat nip</li>
      <li>laser pointers</li>
      <li>lasagna</li>
    </ul>
    <p>Top 3 things cats hate:</p>
    <ol>
      <li>flea treatment</li>
      <li>thunder</li>
      <li>other cats</li>
    </ol>
  </div>

  <form action="https://freecatphotoapp.com/submit-cat-photo">
    <label><input type="radio" name="indoor-outdoor" checked /> Indoor</label>
    <label><input type="radio" name="indoor-outdoor" /> Outdoor</label><br />
    <label><input type="checkbox" name="personality" checked /> Loving</label>
    <label><input type="checkbox" name="personality" /> Lazy</label>
    <label><input type="checkbox" name="personality" /> Energetic</label><br />
    <input type="text" placeholder="cat photo URL" required />
    <button type="submit">Submit</button>
  </form>
</main>
```
