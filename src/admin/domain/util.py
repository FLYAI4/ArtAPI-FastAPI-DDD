import os
import shutil


def create_folder_if_not_exists(folder_path: str) -> str:
    """Create folder if not exists."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return "Success create folder."
    return "Already exist folder."


def find_storage_path():
    domain_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
    admin_path = os.path.abspath(os.path.join(domain_path, os.path.pardir))
    src_path = os.path.abspath(os.path.join(admin_path, os.path.pardir))
    root_path = os.path.abspath(os.path.join(src_path, os.path.pardir))
    storage_path = os.path.abspath(os.path.join(root_path, 'storage'))
    create_folder_if_not_exists(storage_path)
    return storage_path


async def delete_folder(folder_path: str):
    """Delete folder if exists"""
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
        except Exception:
            return "Fail to delete folder."
    return "Success to delete folder."
