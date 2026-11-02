
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent
DATASET = ROOT / "dataset_4class"

classes = {
    0: "Helmet",
    1: "No Helmet",
    2: "Mask",
    3: "No Mask"
}

for split in ["train", "valid", "test"]:
    image_dir = DATASET / split / "images"
    label_dir = DATASET / split / "labels"

    if not image_dir.exists() or not label_dir.exists():
        print(f"LOI: Thieu thu muc trong {split}")
        continue

    images = [
        p for p in image_dir.iterdir()
        if p.suffix.lower() in [".jpg", ".jpeg", ".png", ".bmp"]
    ]

    counts = Counter()
    invalid = 0
    missing = 0

    for image_path in images:
        label_path = label_dir / (image_path.stem + ".txt")

        if not label_path.exists():
            missing += 1
            continue

        for line in label_path.read_text(encoding="utf-8").splitlines():
            parts = line.split()

            if len(parts) != 5:
                invalid += 1
                continue

            try:
                class_id = int(parts[0])
                if class_id not in classes:
                    invalid += 1
                else:
                    counts[class_id] += 1
            except ValueError:
                invalid += 1

    print(f"\n--- {split.upper()} ---")
    print("So anh:", len(images))
    print("So nhan:", sum(counts.values()))
    print("Thieu file nhan:", missing)
    print("Dong nhan loi:", invalid)

    for class_id, name in classes.items():
        print(f"{name}: {counts[class_id]}")

print("\nKIEM TRA HOAN TAT!")
