Now let's change the color of some of our text.

We can do this by changing the `style` of your `h2` element.

The property that is responsible for the color of an element's text is the `color` style property.

Here's how you would set your `h2` element's text color to blue:

```html
<h2 style="color: blue;">CatPhotoApp</h2>
```

Note that it is a good practice to end inline `style` declarations with a `;` .

---

Change your `h2` element's style so that its text color is red.

---

Hãy thay đổi màu của một số văn bản.

Chúng ta có thể làm điều này bằng cách thay đổi `style` của phần tử `h2`.

Thuộc tính chịu trách nhiệm về màu sắc của văn bản là thuộc tính `color`.

Đây là cách bạn đặt màu văn bản của phần tử `h2` thành màu xanh lam:

```html
<h2 style="color: blue;">CatPhotoApp</h2>
```

Lưu ý rằng bạn nên kết thúc các khai báo inline `style` bằng dấu `;`.

---

Thay đổi màu văn bản của phần tử `h2` thành màu đỏ.

```html
<h2>CatPhotoApp</h2>
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
