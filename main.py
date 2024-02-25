import os
import sys
import uvicorn
root_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
src_path = os.path.abspath(os.path.join(root_path, "src"))
# libs_path = os.path.abspath(os.path.join(src_path, "libs"))

if src_path not in sys.path:
    sys.path.append(src_path)


if __name__ == "__main__":
    from src.shared_kernel.adapter.app import create_app
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=600)
