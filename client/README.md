# ログイン

## Cài đặt và chạy project

```bash
# cài đặt các package cần thiết
$ yarn install

# gen các file đa ngôn ngữ (được định nghĩa tại https://docs.google.com/spreadsheets/d/1Ig_DFnj1a_bBn4uw7Mbor-pRXK5zrB6vvzX-ArsAThY)
$ yarn message

# chạy project
$ yarn dev

# build
$ yarn build
$ yarn start

# generate
$ yarn generate
```

## Các thư mục quan trọng

### `pages`

Đây là thư mục quan trọng nhất, chứa các đường dẫn và các màn hình của hệ thống.
Phần lớn thời gian khi code sẽ dành cho thư mục này.

Xem thêm tại [đây](https://nuxtjs.org/docs/directory-structure/pages).

### `components`

Đây là thư mục chứa tất cả các component của hệ thống và có thể được tái sử dụng ở nhiều chỗ khác nhau.
Nuxt.js sẽ tự động import các component trong thư mục này khi cần thiết, nghĩa là không cần phải import thủ công.

Xem thêm tại [đây](https://nuxtjs.org/docs/directory-structure/components).

### `assets`

Đây là thư mục để chứa các assets chưa được compile như styles, ảnh, font.
Các assets này sẽ được tác động (xử lí) bởi webpack (ví dụ SASS, SCSS sẽ được webpack chuyển thành CSS thuần, ảnh sẽ được tối ưu dung lượng, ...).

Xem thêm tại [đây](https://nuxtjs.org/docs/directory-structure/assets).

### `layouts`

Đây là thư mục để chứa các layout của hệ thống.
Một layout có thể được dùng chung cho nhiều màn hình khác nhau.

Xem thêm tại [đây](https://nuxtjs.org/docs/directory-structure/layouts).

### `plugins`

Đây là thư mục chứa các thư viện sẽ được chạy trước khi khởi tạo Vue app.

Xem thêm tại [đây](https://nuxtjs.org/docs/directory-structure/plugins).

### `static`

Đây là thư mục chứa các file tĩnh. Các file này sẽ không bị tác động bởi webpack và sẽ không thay đổi trong suốt thời gian hệ thống chạy.
Mỗi file trong thư mục này sẽ được map bởi `/`.

Ví dụ: `/static/robots.txt` sẽ được map thành `/robots.txt`.

Xem thêm tại [đây](https://nuxtjs.org/docs/directory-structure/static).

### `store`

Đây là thư mục chứa các file store của Vuex.

Xem thêm tại [đây](https://nuxtjs.org/docs/directory-structure/store).

### `constants`

Đây là thư mục chứa các biến để lưu các giá trị không thay đổi trong suốt thời gian hệ thống chạy.

### `css`

Đây là thư mục chứa các style chung của hệ thống.

### `locales`

Đây là thư mục chứa các file đa ngôn ngữ.

### `middlewware`

Đây là thư mục chứa các middleware được gọi trước khi chạy một số màn hình của hệ thống.

Ví dụ: xác thực người dùng.

### `utils`

Đây là thư mục chứa các tool, các đoạn code để giúp ích và đơn giản hoá việc code.

Ví dụ: function để parse date.
