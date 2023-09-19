If you make the width of the page preview smaller, you will notice at some point, some of the text on the left starts wrapping around to the next line. This is because the width of the `p` elements on the left side can only take up `50%` of the space.

Since you know the prices on the right have significantly fewer characters, change the `flavor` class `width` value to be `75%` and the `price` class `width` value to be `25%`.

---

Nếu bạn làm cho chiều rộng của trang xem trước nhỏ hơn, bạn sẽ nhận thấy tại một số điểm, một số văn bản bên trái bắt đầu bao quanh dòng tiếp theo. Điều này là do chiều rộng của các phần tử `p` ở phía bên trái chỉ có thể chiếm `50%` không gian.

Vì bạn biết giá ở bên phải có ít ký tự hơn đáng kể, hãy thay đổi giá trị `width` của lớp `flavour` thành `75%` và giá trị `width` của lớp `price` thành `25%`.

---

```html
<html>
  <style>
    .flavor {
      text-align: left;
      width: 10%;
    }

    .price {
      text-align: right;
      width: 10%;
    }
  </style>
  <body>
    <p>some html code</p>
  </body>
</html>
```
