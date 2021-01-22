This is test task implementation for:
```
Спасибо, что уделили сегодня время на интервью. Как и было договорено, высылаю тестовое задание, по которому мы друг друга поймем гораздо легче, чем в беседе.


Реализовать доступное по сети in-memory key-value хранилище (сервер).

In-memory означает, что все данные (пары ключ-значение) должны храниться в памяти и при перезапуске хранилища исчезать.

Требования:

- нельзя использовать готовые решения (redis, memcached и тому подобные)

- хранилище должно позволять установить значение ключу, прочитать значение ключа, удалить значение ключа, а также получать список всех ключей, у которых есть значения.

Желательно:

- хранилище должно поддерживать несколько одновременных соединений.

- возможность послать несколько команд в одном соединении (например, без переподключения запросить список всех ключей и значение каждого)

К серверу так же реализовать клиента, позволяющего посылать все команды к хранилищу (установить/прочитать/удалить ключ, получить список всех ключей).

Если сервер реализует посылку нескольких команд в одном соединении, то и клиент должен это поддерживать.


Прошу подтвердить получение письма ответным сообщением с датой, к которой Вы предоставите решение.
```

GRPC decided to use a server with 4 workers. RPC selected due to performance and simple implementation. 
Supported commands(For API checkout *client.py*):
 - ChainStart/ChainEnd    : Starting chain command, this command allows us to send multiple commands in single request
 - Set                    : Set value on Server
 - Get                    : Get value from Server
 - GetAll                 : Get all keys with values from Server
 - Delete                 : Delete key from Server
 - Chain[CLI Unsupported] : Server Chain call, for Chain call use ChainStart

Client has a CLI interface.


Usage:
    0) Run ``` $ python -m grpc_tools.protoc --experimental_allow_proto3_optional -I. --python_out=. --grpc_python_out=. scheme.proto ``` to generate scheme
    1) Run server using ``` $ python server.py ```
    2) Run client in another window using ``` $ python client.py ```