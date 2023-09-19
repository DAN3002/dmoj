# Các thứ mình đã thay đổi trong dmoj

## Thêm app funix (django-admin startapp funix)
- Thêm app, các views, templates, models, utils cho app này.

## Thêm templates dir của app funix vào dmoj/settings.py
- Thêm `os.path.join(BASE_DIR, 'funix/templates')` vào **TEMPLATES** config 

## Thêm urlconf và custom error pages của app funix vào dmoj/urls.py
```python
urlpatterns += [
    path('beta', include('funix.urls'))
]

from django.conf import settings
DEBUG = settings.DEBUG

if DEBUG == False: 
    handler404 = 'funix.views.error.error404'
    handler403 = 'funix.views.error.error403'
    handler500 = 'funix.views.error.error500'
```

## Thay đổi template gốc của dmoj: site/templates/problem/problem.html
- Thêm nút 'Submit solution beta' và 'Update test data beta'
- Bỏ nút 'Submit solution' cũ đi.

## funix app
### thêm model ProblemTestCaseData, override `save` method của model ProblemTestCase
- Mỗi problem (model **Problem**) có nhiều test cases (model **ProblemTestCase**) (one-to-many).
- Mỗi test case thường sẽ có input data và expected output data, được lưu trong file zip, tương ứng với fields **input_file** và **output_file** của model **ProblemTestCase**. input_file và ouput_file chỉ lưu địa chỉ file.
- Mình thêm model **ProblemTestCaseData** one-to-one với **ProblemTestCase** dùng để lưu input data và expected output data (lấy từ input_file và output_file) cho những test case **công khai**.
- Mình override method của **ProblemTestCase**, khi **save()**, thì sẽ đọc input và output data nếu có, và tạo model **ProblemTestCaseData** tương ứng.

## user story
- Danh sách problems > chọn problem > trang đề bài > click **Submit solution beta** > trang code, có path: /beta/problem/<-problem code->
- Nếu chưa đăng nhập, chỉ hiển thị đề bài, vùng code editor sẽ hiển thị yêu cầu login.
- Trang này sẽ hiển thị source code và kết quả submission lần cuối cùng, nếu chưa submit lần nào thì sẽ trống.
- Viết code > click *submit* nếu chưa submit lần nào, *resubmit* nếu đã có submission trước đó.
- User được chuyển tới path: /beta/problem/<-problem code->/submission/<-submission id-> (giao diện y chang, cùng dùng 1 view), hiển thị loading và sau đó là kết quả submission.

## Iframe của trang 'submit solution beta'
- Để ẩn navigation bar (dùng cho iframe), thêm query vào url: ?iframe=1. Ví dụ: /beta/problem/problem1?iframe=1.
- Khi click 'Submit solution beta' để chuyển tới trang code từ trang đề bài, navigation bar sẽ không ẩn đi. Nếu muốn ẩn ngay từ bước này, chỉ cần vàp site/templates/problem/problem.html, thêm query *?iframe=1* vào sau url là được.
- Hiện tại, nếu user đang ở trang code có navigation bar được hiển thị (iframe != 1), thì khi submit, navigation bar sẽ vẫn được hiển thị. Nếu navigation bar đang ẩn (iframe = 1) thì sau khi submit, navigation bar vẫn sẽ ẩn.
- Sidebar hiện tại chỉ để tượng trưng, nên iframe chưa thống nhất. 

## Update test data beta
- Một số problem không tạo bằng site interface được, ví dụ problem sử dụng customjudge, chỉ có input data, không có expected output data.
- Những problem này do không tạo bằng site interface, nên không có model **ProblemTestCase** được tạo > không có model **ProblemTestCaseData** (đề cập ở trên), do đó không thể hiển thị được input data ở trang code.
- Mình tạo chức năng **Update test data beta**, ở mỗi trang đề bài /problem/<-problem code-> sẽ có nút *Update test data beta*.
- Khi click nút trên > tìm folder trong problem data folder có tên = code của problem > đọc file init.yml > kiểm tra có input hay output file hay không > tạo ProblemTestCase và ProblemTestCaseData từ đó. Sau khi tạo thành công, data có thể được hiển thị.
- Nếu các problem thông thường không tạo bằng site interface (copy từ nơi khác qua chẳng hạn), cũng có thể dùng chức năng này.
