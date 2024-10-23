import os

import pytest

from app.core.configs import settings, BASE_DIR


@pytest.fixture
def test_storage_path():
    original_storage_path = settings.storage_full_path
    test_storage = BASE_DIR.joinpath("media/test_attachments")
    os.makedirs(test_storage, exist_ok=True)
    settings.MEDIA_PATH = test_storage
    yield test_storage

    settings.MEDIA_PATH = original_storage_path
    if test_storage.exists():
        for file in test_storage.iterdir():
            file.unlink()
        test_storage.rmdir()
