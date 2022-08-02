from pathlib import Path
from typing import Union


def path_prepare(path: Union[Path, str]) -> Path:
    return Path(path) if isinstance(path, str) else path
