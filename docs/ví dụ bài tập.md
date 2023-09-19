# Ví dụ bài tập

---

## Bài tập không phải HTML

Nguồn: https://docs.dmoj.ca/#/problem_format/problem_examples

1. **Standard**

Bài tập này có 3 test case.

```yml
archive: aplusb.zip
test_cases:
  - { in: aplusb.1.in, out: aplusb.1.out, points: 5 }
  - { in: aplusb.2.in, out: aplusb.2.out, points: 20 }
  - { in: aplusb.3.in, out: aplusb.3.out, points: 75 }
```

2. **Batched**

Bài tập này có 3 batches, lần lượt là 5, 20, 25 điểm. Mỗi batch có nhiều test case.

```yml
archive: hungry.zip
test_cases:
  - batched:
      - { in: hungry.1a.in, out: hungry.1a.out }
      - { in: hungry.1b.in, out: hungry.1b.out }
      - { in: hungry.1c.in, out: hungry.1c.out }
    points: 5 # trả lời đúng cả 3 test cases trên mới được 5 điểm
  - batched:
      - { in: hungry.2a.in, out: hungry.2a.out }
      - { in: hungry.2b.in, out: hungry.2b.out }
      - { in: hungry.2c.in, out: hungry.2c.out }
      - { in: hungry.2d.in, out: hungry.2d.out }
    points: 20
  - batched:
      - { in: hungry.3a.in, out: hungry.3a.out }
      - { in: hungry.3b.in, out: hungry.3b.out }
      - { in: hungry.3c.in, out: hungry.3c.out }
      - { in: hungry.3d.in, out: hungry.3d.out }
    points: 25
```

3. **Generator**

Ví dụ input là mảng có N \* 1.000.000.000 phần tử.
Lưu trong file thì lớn quá.
Do đó có thể dùng generator: khi thí sinh submit thì mới tạo input output data từ N.

```yml
generator: generator.cpp
points: 5
test_cases:
  - generator_args: [1] # tạo input và output data từ N = 1
  - generator_args: [2]
  - generator_args: [3]
  - generator_args: [4]
```

4. **Custom grading**

Đề bài: viết code tạo infinite loop với độ dài code ngắn nhất có thể.
Điểm = 10/<độ dài code>.
Không viết được infinite loop thì 0 điểm.

```yml
custom_judge: shortest1.py
test_cases:
  - { points: 10 } # không có input output
```

Problem này không có input, output.
Sử dụng custom judge là 1 file python code.
File này đánh giá bằng cách:

- Check nếu code thí sinh chạy bị timed out limit => là vòng lặp vô hạn > trả lời đúng.
- Tính độ dài code N
- Cho điểm = 10/N nếu trả lời đúng, 0 nếu sai.

5. **Interactive**

Đề bài: cho số N. Viết vòng lặp đoán số N bằng cách in ra guess của bạn ở mỗi vòng lặp. Dựa vào guess cao hay thấp so với N, judge sẽ in ra 'cao' nếu guess > N, 'thấp' nếu guess < N, 'bằng' nếu guess = N. Bạn dựa vào đó để đoán tiếp sao cho số lần đoán < 31.

```yml
custom_judge: seed2.py
unbuffered: true
archive: seed2.zip
test_cases:
  - { in: seed2.1.in, points: 20 } # có input, không có output
  - { in: seed2.2.in, points: 20 }
  - { in: seed2.3.in, points: 20 }
  - { in: seed2.4.in, points: 20 }
  - { in: seed2.5.in, points: 20 }
```

seed2.py sẽ chạy như sau:

- Đọc input data là số N.
- Judge sẽ chạy vòng lặp của thí sinh.
- Mỗi vòng lặp seed2.py sẽ đếm số lần, và kiểm tra xem thí sinh đóan đúng chưa bằng cách xem KQ judge in ra 'cao' hay 'thấp' hay 'bằng'
- Nếu số lần >= 31 => 0 điểm.
- Nếu số lần < 31 => đạt điểm.

---

## Bài tập HTML

Xem [Ví dụ bài tập HTML]('./ví dụ bài tập html.md')

Xem các file tại đây để biết rõ thêm các utils: [Judge Server]('https://github.com/uuuuv/judge-server')
