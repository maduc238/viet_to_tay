# Tiếng Việt sang tiếng Tày

![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

Ứng dụng hỗ trợ dịch từ tiếng Việt sang tiếng Tày

## Giới thiệu chung

Tiếng Tày là một ngôn ngữ thuộc nhóm Tày-Thái, trong ngữ hệ Tai-Kadai, được nói chủ yếu ở khu vực miền núi phía Bắc Việt Nam, đặc biệt là các tỉnh Cao Bằng, Lạng Sơn, Bắc Kạn, và Tuyên Quang. Tiếng Tày có một hệ thống âm vị phong phú, bao gồm nhiều thanh điệu, với khoảng sáu thanh điệu chính.

Đặc điểm ngữ pháp của tiếng Tày tương đối đơn giản, không có sự phân biệt giữa giống (nam, nữ) và số (số ít, số nhiều) trong danh từ. Các từ vựng trong tiếng Tày cũng ảnh hưởng nhiều từ tiếng Hán, nhưng vẫn giữ được đặc trưng riêng biệt, phản ánh sự phát triển lâu dài của ngôn ngữ này trong cộng đồng người Tày. Tiếng Tày không chỉ là phương tiện giao tiếp hàng ngày mà còn mang đậm giá trị văn hóa, đặc biệt qua các bài hát, truyền thuyết và lễ hội của người Tày.

Hiện nay, tiếng Tày đang đối mặt với nguy cơ mai một nghiêm trọng, một phần do sự thiếu vắng của nó trong chương trình giáo dục chính thức. Mặc dù là ngôn ngữ của một cộng đồng lớn tại các tỉnh miền núi phía Bắc, nhưng tiếng Tày không được giảng dạy trong các trường học, khiến thế hệ trẻ ngày càng ít có cơ hội tiếp xúc và sử dụng ngôn ngữ mẹ đẻ của mình trong môi trường học thuật. Thay vào đó, tiếng Tày chủ yếu được truyền miệng qua các hoạt động văn hóa trong thôn bản, như các lễ hội, ca hát dân gian, và sinh hoạt gia đình. Điều này dẫn đến sự dần dần mất đi của tiếng Tày trong các thế hệ mới, khi mà các giá trị văn hóa truyền thống không còn được bảo tồn và phát huy như trước.

Hơn nữa, sự phát triển của các ngôn ngữ quốc gia như tiếng Việt cùng với sự phổ biến của các phương tiện truyền thông hiện đại khiến tiếng Tày ngày càng bị lu mờ. Trong khi tiếng Việt là ngôn ngữ chính trong giao tiếp và công việc, tiếng Tày đang dần trở thành ngôn ngữ "dân dã", chỉ còn được sử dụng trong các tình huống giao tiếp hàng ngày trong gia đình và cộng đồng nhỏ. Điều này tạo ra một khoảng cách ngày càng lớn giữa các thế hệ, khiến tiếng Tày không còn là phương tiện giao tiếp chính của người trẻ tuổi.

Để bảo tồn nét văn hóa, ngôn ngữ của đồng bào người Tày, trong dự án này tôi xin giới thiệu công cụ dịch văn bản từ tiếng Việt sang tiếng Tày. Điều này sẽ giúp cho nhiều người dễ dàng tiếp cận được tiếng Tày, cũng như giúp số hóa các tri thức, dữ liệu lưu trữ của tiếng Tày trong thời đại công nghệ số hiện nay.

### Lưu ý

Vì tiếng Tày không có quy chuẩn thống nhất, có nhiều sự khác biệt giữa các vùng miền, nên dự án chỉ tập trung với các từ được công bố trong từ điển Tày-Việt được tham khảo chính để làm chuẩn. Với những từ không tồn tại, bản dịch sẽ mặc định giữ nguyên tiếng Việt để phù hợp với ngữ cảnh giao tiếp đời sống sinh hoạt của người Tày.

## Khởi chạy ứng dụng

### Chạy ứng dụng bằng gunicorn và nginx

Ban đầu chạy bằng `gunicorn` để mở ứng dụng trên cổng 8000.

```commandline
gunicorn --bind 127.0.0.1:8000 wsgi:app
```

Sau khi khởi động, ứng dụng sẽ tạo một web server có đoạn chat riêng tại địa chỉ http://127.0.0.1:8000 (mặc định của Flask):

![img.png](pics/img.png)

Tiếp theo cấu hình `nginx`.

```commandline
sudo vim /etc/nginx/sites-available/myapp
```

Thêm nội dung sau (với *yourdomain.com* là tên miền của trang web đang cần được triển khai):

```
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Lưu lại và liên kết cấu hình:

```commandline
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl reload nginx
```

### Tạo certificate và chạy ứng dụng trên HTTPS

Cài đặt Certbot:

```commandline
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

Lấy chứng chỉ SSL:

```commandline
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Kiểm tra cấu hình HTTPS:

```commandline
sudo systemctl reload nginx
```

Sau đó tiếp tục sửa file `/etc/nginx/sites-available/myapp` như bước trên (với *yourdomain.com* là tên miền của trang web đang cần được triển khai) rồi thêm vào dòng:

```

server {
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Rồi làm lại bước tương tự để liên kết với cấu hình mới:

```commandline
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl reload nginx
```

## Dành cho nhà phát triển

### Thêm nội dung vào từ điển

Để bổ sung các từ ngữ được dịch từ tiếng Việt sang tiếng Tày, thêm nội dung vào các file `csv` tương ứng trong folder `dictionary` theo cấu trúc bảng như sau:

|tieng_viet|tieng_tay|
|-|-|
|một|nừng|
|hai|soong|

### Chạy test bản dịch

Sửa nội dung văn bản cần dịch trong hàm chạy công cụ dịch `translate`.

Sau đó chạy file:

```commandline
python test.py
```

### Gọi API request

Điền nội dung cần dịch vào trường `"message"` trong API POST như sau:

```commandLine
curl -X POST https://<address>/api/translate -H "Content-Type: application/json" -d '{"message": "Xin chào anh em"}'
```

Kết quả trả về trong trường `"translated"`

## Tài liệu tham khảo

[1] Bèn, Lương. "Từ điển Tày-Việt, Nxb Đại học Thái Nguyên." (2011).

[2] Savina, François Marie. *Dictionnaire tày-annamite-français: précédé d'un précis de grammaire tày et suivi d'un vocabulaire français-tày*. Impr. d'Extrême-Orient, 1910.

[3] Hoàng Văn Ma, Lục Văn Pảo, and Hoàng Chí. "Từ điển Tày-Nùng-Việt." (2006).

---

Version 1.2.0
