
from ultralytics import YOLO
from pathlib import Path
import argparse
import torch


# Thu muc goc cua du an
ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(
        description="Huấn luyện YOLO nhận diện mũ bảo hiểm và khẩu trang"
    )

    parser.add_argument(
        "--data",
        default=str(ROOT / "data.yaml"),
        help="Đường dẫn file data.yaml"
    )

    parser.add_argument("--model", default="yolo11n.pt")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--imgsz", type=int, default=416)
    parser.add_argument("--batch", type=int, default=2)
    parser.add_argument("--device", default="0")

    args = parser.parse_args()

    # Kiem tra file dataset
    data_file = Path(args.data)

    if not data_file.is_absolute():
        data_file = ROOT / data_file

    if not data_file.exists():
        raise FileNotFoundError(
            f"Khong tim thay file data.yaml: {data_file}"
        )

    # Kiem tra GPU
    if args.device != "cpu":
        if not torch.cuda.is_available():
            raise RuntimeError(
                "CUDA khong kha dung. Hay kiem tra lai PyTorch va GPU."
            )

        print("GPU:", torch.cuda.get_device_name(0))
        print("CUDA:", torch.version.cuda)

    print("\n========== CAU HINH HUAN LUYEN ==========")
    print("Dataset:", data_file)
    print("Model:", args.model)
    print("Epochs:", args.epochs)
    print("Image size:", args.imgsz)
    print("Batch size:", args.batch)
    print("Device:", args.device)
    print("=========================================\n")

    # Tai mo hinh YOLO11n
    model = YOLO(args.model)

    # Cau hinh huan luyen
    results = model.train(
        data=str(data_file),
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        project=str(ROOT / "runs"),
        name="helmet_mask",
        patience=15,
        workers=2,
        plots=True,
        save=True,
        cache=False,
        exist_ok=True
    )

    best = ROOT / "runs" / "helmet_mask" / "weights" / "best.pt"

    print("\n========== HOAN THANH ==========")
    print("Huấn luyện đã kết thúc.")

    if best.exists():
        print("Model tốt nhất:", best)
        print("Hãy sao chép best.pt vào thư mục models/")
    else:
        print("Chưa tìm thấy best.pt. Hãy kiểm tra thư mục runs.")


if __name__ == "__main__":
    main()
