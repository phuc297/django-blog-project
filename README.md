﻿# django-blog-project
  
**project settings folder**: config

**apps folders**: users, blog, interactions


# Sinh Dữ Liệu
```bash
pip install -r .\requirements.txt
```

vào file **`fake.py`** để tùy chỉnh:

|  |  |
| :--- | :--- |
| **`NUMBER_OF_USERS`** | Số lượng **User** mới được tạo. |
| **`NUMBER_OF_POSTS`** | Số lượng **Bài viết** sẽ được tạo. |
| **`NUMBER_OF_COMMENTS`** | Tổng số **Bình luận** được tạo. |
| **`NUMBER_OF_CATEGORIES`** | Số lượng **Danh mục** sẽ được tạo. |
| **`MIN_FOLLOWERS_PER_USER`** | Số lượng **Follower tối thiểu** mỗi user có. |
| **`MAX_FOLLOWERS_PER_USER`** | Số lượng **Follower tối đa** mỗi user có. |

```bash
python manage.py shell
```

```shell
from fake import Fake
```

```shell
Fake() 
```

```bash
exit()
```


```
python -m venv venv
```

```
.\venv\Scripts\activate
```

```
python -m pip install --upgrade pip
```

```
pip install -r .\requirements.txt
```

```
python .\manage.py migrate
```









