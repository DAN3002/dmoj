# INSTALLATION

1. Bản này dùng với judge docker. Hiện đang chạy trên nhánh `feature/fe-user-problem`.
2. Làm theo hướng dẫn https://docs.dmoj.ca/#/site/installation, các bước cần lưu ý:

- Thay `git clone https://github.com/DMOJ/site.git` bằng clone bản này về: `git clone https://github.com/uuuuv/dmoj.git`.
- Đổi tên thư mục dmoj > site cho đồng bộ với hướng dẫn: `mv dmoj site`
- `cd site`
- KHÔNG `git checkout v4.0.0`.
- Thay vào đó checkout nhánh đang làm `git switch feature/fe-user-problem` (nhánh `main` chưa có gì)
- Đổi `python3 manage.py loaddata language_small` thành `python3 manage.py loaddata language_all` để cài đặt tất cả các ngôn ngữ lập trình. Nếu chọn small thì chỉ có khoảng 20 ngôn ngữ.
- Do đã có sẵn file cấu hình, nên khi chạy test 'runserver', 'celery', 'bridged' có thể bị lỗi thiếu dependencies. Cuối trang có 2 dependencies, ta cài trước luôn. 
- Bạn cũng có thể xóa các file cấu hình rồi tạo lại theo hướng dẫn.

```shell
  (venv) npm install qu ws simplesets
  (venv) pip3 install websocket-client
```

- Các bước còn lại làm tương tự, sửa lại cấu hình cho phù hợp.
- Cấc trúc thư mục hiện tại của bản này tương ứng với file cấu hình:

/projects  
|\_\_\_\_\_foj  
............|\_\_\_\_\_site  
............|\_\_\_\_\_venv  
............|\_\_\_\_\_static
............|\_\_\_\_\_tmp - chứa file logs, etc.
............|\_\_\_\_\_problems  
............|\_\_\_\_\_cache

# SỦ DỤNG
#### routes mới
1. /beta/problem/<problem code>
2. /beta/problem/<problem code>/submission/<submission id>
3. /beta/problem/<problem code>/comments 
4. /beta/problems
Các route trên, để hiển ẩn thanh navbar để hiển thị trong <iframe>, thêm query `?iframe=1` vào.
Khi vào các trang trên sẽ có thanh sidebar, đều là `iframe=1`

Cách vào các routes trên: 
1. Vào danh sách problem, chọn 1 problem, chọn 'Submit solution beta'
2. Gõ thẳng vào address bar.

# Hardware requirements

From @Xyene:

1. You'll need more hosts for a contest where correct solutions can take several minutes to judge (e.g. IOI (The International Olympiad of Informatics) - style hundreds of test cases).
2. What DMOJ is doing:

- they run dmoj on a baremental host for most of the year:
  6-core (12-thread) AMD Ryzen 5 3600X @ 3.8GHz, with 16 GB 3200 MHz CL16 dual-channel RAM.
- Each judgeruns in a QEMU instance allocated 2GB RAM and 1 physical core (2 threads).
- When they need to run a contest that requireds more judges, they have some scripts to spin some up in the cloud.
- The cloud judges just mount all problem data over NFS (Network File System).
- So, just mount the NFS volume, start docker, and the judge connects.
- If you're planning on running a contest, one thing to keep in mind is that the most load you'll face be at the start of the contest, as everyone rushes to hit the "Join contest" button at the same time. That'll be frontend load more than it will be database load. ton at the same time. That'll be frontend load more than it will be database load. The frontend can render ~ 4 requests/second/core (conservatively, but you should lower bound it at 100ms/req). You can tell how long things take on your setup by reading uwsgi logs.

# Lỗi

1. Nếu gặp lỗi `AttributeError: 'NoneType' object has no attribute 'Redis'`, bạn cần cài thêm Redis cho virtual environment.

```shell
(venv) /projects/foj/site  $ pip3 install Redis
```

2. Khi chạy site trên browser, nếu gặp lỗi "Database returned an invalid datetime value. Are time zone definitions for your database installed", là do MariaDB chưa được cài timezone table.
   Xử lý:

```shell
$ mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql
```

Nếu yêu cầu nhập mật khẩu root của database mà bạn không có, có thể dùng câu lệnh sau để đặt lại mật khẩu, sau đó chạy lại câu lệnh trên.

```shell
$ sudo mysql
<MariaDB> > SET PASSWORD FOR 'root'@localhost = PASSWORD("<mật khẩu>");
<MariaDB> > exit
```
