# ArtAPI-FastAPI-DDD
ArtAPI refactoring with Hexagonal Architcture for DDD.

- ArtCore-FastAPI is a FastAPI server that handles the service.
- It utilizes PostgreSQL and MongoDB for data storage
- It communicates with the Go core server through gRPC.

<br>


## Tree

```
.
├── Dockerfile
├── README.md
├── entrypoint.sh
├── main.py
├── proto
│   └── stream.proto
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── account
│   │   ├── __init__.py
│   │   ├── adapter
│   │   │   ├── __init__.py
│   │   │   ├── database.py
│   │   │   └── rest
│   │   │       ├── __init__.py
│   │   │       ├── api.py
│   │   │       ├── request.py
│   │   │       └── response.py
│   │   ├── application
│   │   │   ├── __init__.py
│   │   │   └── command.py
│   │   ├── domain
│   │   │   ├── __init__.py
│   │   │   ├── entity.py
│   │   │   ├── errorcode.py
│   │   │   ├── exception.py
│   │   │   ├── service
│   │   │   │   ├── log_in.py
│   │   │   │   └── sign_up.py
│   │   │   └── util
│   │   │       └── cipher.py
│   │   └── infra
│   │       ├── __init__.py
│   │       ├── container.py
│   │       └── database
│   │           ├── __init__.py
│   │           ├── model.py
│   │           └── repository.py
│   ├── admin
│   │   ├── __init__.py
│   │   ├── adapter
│   │   │   ├── __init__.py
│   │   │   ├── database
│   │   │   │   └── database_abs.py
│   │   │   └── rest
│   │   │       ├── __init__.py
│   │   │       ├── api.py
│   │   │       └── response.py
│   │   ├── application
│   │   │   └── command.py
│   │   ├── domain
│   │   │   ├── __init__.py
│   │   │   ├── entity.py
│   │   │   ├── errorcode.py
│   │   │   ├── exception.py
│   │   │   ├── service
│   │   │   │   ├── __init__.py
│   │   │   │   └── generated_content.py
│   │   │   └── util.py
│   │   └── infra
│   │       ├── __init__.py
│   │       ├── container.py
│   │       └── database
│   │           ├── __init__.py
│   │           └── repository.py
│   ├── shared_kernel
│   │   ├── __init__.py
│   │   ├── adapter
│   │   │   ├── __init__.py
│   │   │   ├── app.py
│   │   │   └── database_abs.py
│   │   ├── domain
│   │   │   ├── __init__.py
│   │   │   ├── error_code.py
│   │   │   ├── exception.py
│   │   │   └── jwt.py
│   │   └── infra
│   │       ├── __init__.py
│   │       ├── container.py
│   │       ├── database
│   │       │   ├── __init__.py
│   │       │   ├── connection.py
│   │       │   └── model.py
│   │       ├── elasticsearch.py
│   │       └── fastapi
│   │           ├── __init__.py
│   │           ├── auth.py
│   │           ├── config.py
│   │           ├── error_handler.py
│   │           ├── logger.py
│   │           └── util.py
│   └── user
│       ├── __init__.py
│       ├── adapter
│       │   ├── __init__.py
│       │   ├── database
│       │   │   └── database_itf.py
│       │   ├── grpc
│       │   │   ├── __init__.py
│       │   │   ├── stream_pb2.py
│       │   │   └── stream_pb2_grpc.py
│       │   └── rest
│       │       ├── __init__.py
│       │       ├── api.py
│       │       ├── request.py
│       │       └── response.py
│       ├── application
│       │   ├── __init__.py
│       │   ├── command.py
│       │   └── demo.py
│       ├── domain
│       │   ├── __init__.py
│       │   ├── demo
│       │   │   ├── loading.gif
│       │   │   ├── main.mp3
│       │   │   └── origin_img.jpg
│       │   ├── entity.py
│       │   ├── errorcode.py
│       │   ├── exception.py
│       │   ├── service
│       │   │   ├── __init__.py
│       │   │   └── insert_image.py
│       │   └── util
│       │       └── local_file.py
│       └── infra
│           ├── __init__.py
│           ├── container.py
│           ├── database
│           │   ├── __init__.py
│           │   ├── model.py
│           │   └── repository.py
│           └── torch
│               ├── __init__.py
│               ├── image_dict.json
│               ├── model_save.py
│               └── resnet50_model.pth
└── tests
    ├── __init__.py
    ├── account
    │   ├── __init__.py
    │   ├── test_adapter_rest_api.py
    │   ├── test_application_command.py
    │   ├── test_repository.py
    │   ├── test_service_log_in.py
    │   └── test_service_sign_up.py
    ├── admin
    │   ├── __init__.py
    │   ├── test_adapter_rest_api.py
    │   ├── test_application_command.py
    │   ├── test_database_repository.py
    │   ├── test_img
    │   │   ├── main.mp3
    │   │   └── origin_img.jpg
    │   └── test_service_generated_content.py
    └── user
        ├── __init__.py
        ├── test_adapter_rest_api.py
        ├── test_application_common.py
        ├── test_application_demo.py
        ├── test_database_repository.py
        ├── test_img
        │   ├── hello.jpg
        │   ├── main.mp3
        │   ├── test.jpg
        │   └── wrong.jpg
        ├── test_service_generated_content.py
        └── test_service_insert_image.py
```

<br>

## Service monitoring

![image](https://github.com/FLYAI4/ArtAPI-FastAPI-DDD/assets/91866763/f6139465-3b27-4811-b7dd-deea2a90dfce)




<br>

## Getting Started

To run the service, follow the instructions below:

1. Clone the repository:

```sh
git clone https://github.com/robert-min/ArtCore-FastAPI-DDD.git
```

2. Navigate to the project directory:

```sh
cd ArtCore-FastAPI-DDD
```

3. Install the dependencies:

```sh
pip install -r requirements.txt
```

4. Run the server:
- add src/shared_kernel/infra/fastapi/.env

```sh
python main.py
```

<br>


## Contributing

Contributions are welcome! If you would like to contribute to ArtCore-Go, please follow these steps:

1. Fork the repository.

2. Create a new branch:

```sh
git checkout -b my-feature
```


3. Make your changes and commit them:

```sh
git commit -m "Add my feature"
```

4. Push to your forked repository:

```sh
git push origin my-feature
```

5. Open a pull request. 

<br>

