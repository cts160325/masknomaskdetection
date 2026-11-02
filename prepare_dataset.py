
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent

SOURCE = ROOT / "dataset_source"
DEST = ROOT / "dataset_4class"

# ID gốc -> ID mới
class_mapping = {
    0: 0,
    1: 2,
    2: 1,
    3: 3
}

splits = ["train", "valid", "test"]

for split in splits:
    image_dir = SOURCE / split / "images"
    label_dir = SOURCE / split / "labels"

    new_image_dir = DEST / split / "images"
    new_label_dir = DEST / split / "labels"

    new_image_dir.mkdir(parents=True, exist_ok=True)
    new_label_dir.mkdir(parents=True, exist_ok=True)

    if not image_dir.exists() or not label_dir.exists():
        raise FileNotFoundError(
            f"Khong tim thay images hoac labels trong {split}"
        )

    for image_path in image_dir.iterdir():
        if image_path.suffix.lower() not in [
            ".jpg", ".jpeg", ".png", ".bmp"
        ]:
            continue

        label_path = label_dir / (image_path.stem + ".txt")

        # Sao chep anh sang dataset moi
        shutil.copy2(image_path, new_image_dir / image_path.name)

        new_lines = []

        if label_path.exists():
            with open(label_path, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split()

                    if len(parts) != 5:
                        continue

                    old_id = int(parts[0])

                    # Chi giu 4 lop can thiet
                    if old_id in class_mapping:
                        parts[0] = str(class_mapping[old_id])
                        new_lines.append(" ".join(parts))

        new_label_path = new_label_dir / (image_path.stem + ".txt")

        with open(new_label_path, "w", encoding="utf-8") as file:
            file.write("\n".join(new_lines))

    print(f"Da xu ly xong: {split}")

print("\nHOAN THANH LOC DATASET!")
print("Dataset moi:", DEST)
