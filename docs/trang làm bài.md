# User story

## User story

### Không Iframe

- Trang chủ > danh sách problem > chọn một problem > Click `Submit solution beta`. Nếu chưa đăng nhập, toàn bộ trang làm bài sẽ được che hết bởi modal yêu cầu đăng nhập.

### Iframe trong lms

- Khi user vào LMS, user sẽ được tự động đăng nhập vào dmoj.

## Giao diện trang làm bài

- User được đưa tới trang làm bài tập. Giao diện và một số chức năng cơ bản:
  - Sidebar: có các navigation sau:
    - Đề bài (+ text editor nếu là bài tập thường) (+ HTML preview nếu là bài tập HTML/CSS)
    - Lịch sử submission
    - Cách giải (Chỉ admin mới xem được)
    - Select box chuyển đổi ngôn ngữ Anh - Việt
  - Topbar:
    - Tên bài tập. Nếu là bài tập ở trong khóa học thì có thêm tên khóa học, tên section của khóa học. User có thể click vào tên khóa học để đi đến trang khóa học.
    - Nếu là bài tập trong khóa, sẽ có thêm các số thứ tự của các bài tập cùng section với bài tập hiện tại. Học viên có thể click vào các button này để đi tới bài tập tương ứng. Các button có các trạng thái:
      - Chưa làm: button chứa số thứ tự của bài.
      - Đang là bài tập hiện tại: button chứa số có backround được highlight.
      - Đã làm, kết quả đúng: button chứa dấu check.
      - Đã làm, kết quả sai: button chứa dấu x.
  - Giao diện đề bài:
    - Với các bài tập HTML thì không có các mục thông tin cùa bài tập như: tác giả, bộ nhớ, thời gian...
  - Giao diện Code Editor:
    - Code ban đầu, độ ưu tiên từ trên xuống:
      - Submission code (nếu có).
      - Initial code (nếu có): có dạng `somecode [...] somecode`, code mẫu để thí sinh điền vào.
      - Template code (nếu có): code đặc hiệu cho mỗi ngôn ngữ.
      - Trống.
    - Expand/Minimize button để phóng to, thu nhỏ Code Editor.
    - Reset button để reset code về code ban đầu.
    - Button nộp bài: nếu user chưa làm bài lần nào thì sẽ là `Submit` (`Nộp bài`), đã làm rồi thì là `Resubmit` (`Nộp bài lại`).
  - Criteria/Test cases:
    - Nếu là bài tập HTML: hiển thị criteria là các yêu cầu user cần đạt được.
    - Nếu là bài tập code khác: hiển thị input, output của thí sinh, expect ouput, thời gian, bộ nhớ nếu là test case công khai.
    - Hiển thị check/x nếu test case/criteria đúng/sai.
  - Console (chỉ ở bài tập không phải HTML):
    - Là kết quả được hiển thị ngắn gọn cho user, gồm đầy đủ các thông tin: kết quả, thời gian, bộ nhớ. Không có input, expected output. Với bài tập có nhiều testcase, user có thể nhìn tổng quan kết quả 1 cách nhanh chóng mà không cần cuộn xuống và click để xem từng test case khi xem ở tab Test case.
  - HTML preview (chỉ ở bài tập HTML): hiển thị nội dung HTML tương ứng của user khi gõ code.
  - Có thể resize ngang, dọc giữa đề bài - editor - HTML preview.

## Chức năng nộp bài

### Code Editor

Với bài tập có code mẫu, user cần điền hết vào vị trí `[...]`. Nếu user thay đổi cấu trúc code mẫu (dựa vào regex), sẽ không cho user submit và alert cho user:

- Nếu không điền hết (còn `[...]`) sẽ thông báo và không cho submit.
- Nếu thay đổi các phần khác sẽ thông báo và không cho submit. ví dụ: `function sayHello() {[...]}`, user nộp `func---tion sayHello(){ console.log('hello'); }` sẽ báo lỗi.

### Phát hiện hành vi paste >= 200 ký tự

- Mỗi lần user paste >= 200 ký tự thì sẽ có alert `Please type your code manually, don't cheat!` và user sẽ được tính là 1 lần có hành vi đáng nghi. Khi nộp bài thì thông tin này sẽ được lưu vào database. Thông tin lưu lại là user, problem, submission, thời gian xảy ra hành vi paste.

### Tính tốc độ gõ bàn phím wpm

- Được lưu cùng với submission.
- Tính theo công thức: số ký tự / 5 / thời gian từ lúc bắt đầu gõ đến lúc nộp bài.
- Nếu số ký tự < 300 và bài tập này user đã làm và submission gần nhất có kết quả wpm, sẽ lấy kết quả này, nếu không sẽ tính mới như công thức trên .

### Thông báo nộp bài đúng

- Nếu user trả lời đúng thì sẽ hiện modal chúc mừng.

## Lịch sử submit

- User có thể xem thông tin các submission cũ, và click view để đi tới trang làm bài với code của submission đó.
