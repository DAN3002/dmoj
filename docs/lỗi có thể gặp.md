# Lỗi có thể gặp

## Lỗi khi cài đặt

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
