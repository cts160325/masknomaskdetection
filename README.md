# Helmet & Mask Detection (Webcam)

Dự án mẫu nhận diện đồng thời 4 lớp:
- `Helmet`
- `No Helmet`
- `Mask`
- `No Mask`

Stack: Python, Ultralytics YOLO, OpenCV, MongoDB Atlas.

## 1. Lưu ý quan trọng

Mã nguồn này là bộ khung chạy webcam và ghi sự kiện. Nó **không kèm trọng số đã huấn luyện** và không thể nhận diện đúng 4 lớp nếu chưa có dataset phù hợp và file `models/best.pt`.

Cần có dataset gán nhãn bounding box theo định dạng YOLO, đúng thứ tự class:
0 Helmet
1 No Helmet
2 Mask
3 No Mask

Dataset cần được kiểm tra nhãn, chất lượng, quyền sử dụng và chia train/val/test độc lập. Không dùng tập test để huấn luyện hoặc chỉnh tham số.

## 2. Cài đặt trên Windows

Mở PowerShell trong thư mục dự án:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

Nếu PowerShell chặn activate, chạy:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Có thể dùng Python 3.10 hoặc phiên bản tương thích với PyTorch/Ultralytics đang cài. Nếu cài trên Python mới nhất gặp lỗi, ưu tiên Python 3.10/3.11.

## 3. Chuẩn bị dataset

Tạo cấu trúc:

```text
dataset/
  data.yaml
  images/
    train/
    val/
    test/
  labels/
    train/
    val/
    test/
```

Mỗi ảnh có một file nhãn `.txt` cùng tên. Mỗi dòng nhãn YOLO:
`class_id x_center y_center width height`
Các tọa độ được chuẩn hóa từ 0 đến 1.

Sao chép `data.yaml.example` thành `dataset/data.yaml` và sửa `path` cho phù hợp. Đảm bảo `names` có đúng thứ tự 4 lớp ở trên. Nếu dataset gốc dùng thứ tự khác, phải ánh xạ lại class ID trước khi train.

## 4. Huấn luyện

Ví dụ:
```powershell
py train.py --data dataset/data.yaml --epochs 80 --imgsz 640 --batch 8
```

Nếu có GPU NVIDIA đã cài CUDA tương thích:
```powershell
py train.py --data dataset/data.yaml --epochs 80 --imgsz 640 --batch 8 --device 0
```

Kết quả thường nằm trong:
`runs/helmet_mask/weights/best.pt`

Tạo thư mục `models`, sau đó chép `best.pt` vào `models/best.pt`.

Đánh giá riêng trên tập test (sau khi huấn luyện):
```powershell
yolo detect val model=models/best.pt data=dataset/data.yaml split=test
```

## 5. MongoDB Atlas

1. Tạo cluster và database user trong MongoDB Atlas.
2. Trong Network Access, cho phép IP hiện tại của máy bạn.
3. Chọn Connect > Drivers > Python, sao chép URI.
4. Sao chép `.env.example` thành `.env`.
5. Điền `MONGODB_URI` trong `.env`.

Không đưa URI có mật khẩu lên GitHub hoặc gửi công khai.

Nếu chưa cấu hình MongoDB, chương trình vẫn chạy nhận diện nhưng chỉ in sự kiện ra terminal, không lưu lên Atlas.

## 6. Chạy webcam

```powershell
py main.py
```

Nhấn `Q` hoặc `Esc` để thoát.

Nếu webcam không phải camera số 0, tạo `.env` và thêm:
`CAMERA_INDEX=1`

## 7. Cơ chế chống lưu trùng

Chương trình dùng YOLO tracking (ByteTrack) và chỉ lưu một lần cho mỗi cặp `(track_id, loại vi phạm)` trong một phiên chạy. Nếu người đó rời khung hình rồi quay lại với ID mới, có thể phát sinh sự kiện mới. Cần kiểm thử và tinh chỉnh cho bối cảnh demo.

## 8. Ảnh minh chứng

Ảnh được lưu cục bộ trong `evidence/`. MongoDB lưu đường dẫn cục bộ đó. Đường dẫn này chỉ truy cập được trên máy chạy chương trình; nếu cần xem ảnh từ máy khác, hãy chuyển ảnh lên dịch vụ lưu trữ hoặc GridFS và lưu URL/ID tương ứng.

## 9. Giới hạn

- Chất lượng phụ thuộc dataset, góc camera, ánh sáng, độ che khuất và kích thước vật thể.
- Một mô hình 4 lớp cần dữ liệu được gán nhãn nhất quán. Đặc biệt, nhãn `Mask`/`No Mask` cần là bounding box vùng mặt; `Helmet`/`No Helmet` cần quy tắc gán nhãn rõ ràng.
- Không nên coi kết quả là bằng chứng pháp lý hoặc kết luận tự động về một cá nhân.
- Đánh giá bằng precision, recall, mAP50, mAP50-95 và kiểm thử video thực tế.
