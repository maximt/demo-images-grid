from pathlib import Path


ALLOW_IMAGE_EXT = ['*.png', '*.jpg', '*.jpeg', '*.gif']


def get_dir_files(dir_path: str, ext: str) -> list[str]:
    path = Path(dir_path)
    files = [str(file) for file in path.rglob(ext, case_sensitive=False) if file.is_file()]
    return files


def get_all_files(dirs: list[str]) -> list[str]:
    all_files = []
    for dir_path in dirs:
        for ext in ALLOW_IMAGE_EXT:
            files = get_dir_files(dir_path, ext)
            all_files.extend(files)
    return all_files


def run():
    dirs = [
        '../data/1388_6_Наклейки 3-D_2',
        '../data/1388_2_Наклейки 3-D_1',
        '../data/1388_12_Наклейки 3-D_3',
        '../data/1369_12_Наклейки 3-D_3',
    ]

    files = get_all_files(dirs)
    print(len(files))
    print(files)



if __name__ == "__main__":
    run()
