import socket
from select import select

class ChatServer:
    def __init__(self, host='127.0.0.1', port=5001):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen()

        self.to_monitor = [self.server_socket]
        self.client_addresses = {}
        self.client_names = {}
        self.players_for_game = []  # Список игроков, которые хотят сыграть
        self.game_choices = {}  # Словарь для хранения выборов игроков
        self.active_players = set()  # Множество для отслеживания активных игроков

        print(f"Сервер запущен на {host}:{port}")

    def accept_connection(self):
        """Функция для принятия нового соединения и получения имени клиента."""
        print("Ожидание соединения...")
        client_socket, client_address = self.server_socket.accept()
        print(f"Подключен клиент: {client_address}")

        # Запрашиваем имя клиента
        client_socket.send("Введите ваше имя: ".encode('utf-8'))
        name = client_socket.recv(1024).decode('utf-8').strip()

        if name:
            self.client_names[client_socket] = name
        else:
            self.client_names[client_socket] = f"Гость{client_address[1]}"

        # Добавляем сокет клиента в список мониторинга
        self.to_monitor.append(client_socket)
        self.client_addresses[client_socket] = client_address

        # Добавляем клиента в список игроков для игры
        self.players_for_game.append(client_socket)
        self.active_players.add(client_socket)

        # Уведомляем всех клиентов о новом подключении
        self.broadcast_message(f"Новый клиент подключился: {self.client_names[client_socket]}\n".encode('utf-8'), None)

        # Печатаем имена всех подключенных клиентов
        print("Все подключенные клиенты:", ", ".join(self.client_names.values()))
        print(f"Общее количество игроков: {len(self.players_for_game)}")

        # Проверяем, если подключился "Ardager", то начинаем игру
        if "Ardager" in self.client_names.values():
            self.start_game()

    def start_game(self):
        """Начинаем игру, если в списке есть 'Ardager' и достаточно игроков."""
        if len(self.players_for_game) < 2:
            return  # Игра не может начаться, если игроков меньше 2

        # Сообщаем всем игрокам, что начинается игра
        self.broadcast_message("Игра начинается! Выберите: 1 (камень), 2 (ножницы), 3 (бумага).\n".encode('utf-8'), None)

        # Сохраняем выборы игроков
        self.game_choices = {}

        # Каждый игрок должен выбрать, прежде чем играть
        while len(self.game_choices) < len(self.active_players):
            ready_to_read, _, _ = select(list(self.active_players), [], [])
            for player in ready_to_read:
                choice = player.recv(1024).decode('utf-8').strip()
                if choice:
                    self.game_choices[player] = self.map_choice_to_move(choice)
                else:
                    self.game_choices[player] = None  # Если выбор пустой, ставим None

        # После того как все игроки сделали выбор, проводим игру
        self.process_game()

    def map_choice_to_move(self, choice):
        """Подставляем число в соответствующий выбор (1 - камень, 2 - ножницы, 3 - бумага)."""
        if choice == '1':
            return 'камень'
        elif choice == '2':
            return 'ножницы'
        elif choice == '3':
            return 'бумага'
        else:
            return None

    def process_game(self):
        """
        Обрабатываем выборы игроков и определяем победителей, проигравших и ничью.
        """
        if len(self.game_choices) < 2:
            return  # Игра не может быть завершена, если меньше 2 игроков сделали выбор

        results = {}
        # Записываем выбор каждого игрока в словарь
        for player, choice in self.game_choices.items():
            if choice is None:
                results[player] = "Неверный выбор. Выход из игры."
            else:
                results[player] = choice

        winners = []  # Список победителей
        losers = []  # Список проигравших
        all_choices = set(results.values())  # Множество всех выборов

        # Если все выбрали одно и то же (ничья)
        if len(all_choices) == 1 or all_choices == {'камень', 'ножницы', 'бумага'}:
            # Сообщаем игрокам, что это ничья
            self.broadcast_message(
                "Ничья! Все выбрали одинаково или присутствуют все три варианта. Повторите ваш выбор.\n".encode(
                    'utf-8'), None)
            self.game_choices.clear()  # Очищаем старые выборы

            # Повторный выбор для всех игроков
            while len(self.game_choices) < len(self.active_players):
                ready_to_read, _, _ = select(list(self.active_players), [], [])
                for player in ready_to_read:
                    choice = player.recv(1024).decode('utf-8').strip()
                    if choice:
                        self.game_choices[player] = self.map_choice_to_move(choice)
                    else:
                        self.game_choices[player] = None  # Если выбор пустой, ставим None

            # После того как все игроки сделали новый выбор, проводим игру снова
            self.process_game()
            return  # Прерываем текущую обработку игры, так как она будет продолжена

        # Сравниваем выборы игроков и определяем победителей и проигравших
        for player1, choice1 in results.items():
            if choice1 == "Неверный выбор. Выход из игры.":
                losers.append(player1)
            else:
                for player2, choice2 in results.items():
                    if player1 != player2:
                        if (choice1 == 'камень' and choice2 == 'ножницы') or \
                                (choice1 == 'ножницы' and choice2 == 'бумага') or \
                                (choice1 == 'бумага' and choice2 == 'камень'):
                            winners.append(player1)
                            losers.append(player2)

        # Убираем дубли из списка победителей (чтобы не было повторных победителей)
        winners = list(set(winners))

        # Если есть победители и проигравшие, то их нужно обработать
        for loser in losers:
            if loser in self.active_players:  # Проверяем, что игрок активен
                loser.send("Вы проиграли. Выход из игры.\n".encode('utf-8'))
                self.active_players.discard(loser)  # Убираем проигравших из активных игроков

        # Уведомляем победителей
        for winner in winners:
            winner.send("Вы победили!\n".encode('utf-8'))

        # Если остался только один победитель, игра заканчивается
        if len(winners) == 1:
            winner = winners[0]
            self.broadcast_message(
                f"Победитель: {self.client_names.get(winner, 'Неизвестный игрок')}!\n".encode('utf-8'), None)

        # Если победителей несколько, продолжаем игру с новым выбором только для них
        if len(winners) > 1:
            self.game_choices.clear()  # Очищаем старые выборы
            self.broadcast_message("Игра продолжается. Повторите ваш выбор, если вы победили!\n".encode('utf-8'), None)

            # Теперь выбор делают только победители
            self.game_choices = {}
            while len(self.game_choices) < len(winners):
                ready_to_read, _, _ = select(list(winners), [], [])  # Ожидаем, когда победители сделают новый выбор
                for player in ready_to_read:
                    choice = player.recv(1024).decode('utf-8').strip()
                    if choice:
                        self.game_choices[player] = self.map_choice_to_move(choice)
                    else:
                        self.game_choices[player] = None

            # После того как все победители сделали новый выбор, проводим игру снова
            self.process_game()

    def remove_client(self, client_socket):
        """Удаляем клиента из всех списков при отключении."""
        # Проверяем, существует ли сокет в списке перед удалением
        if client_socket in self.to_monitor:
            self.to_monitor.remove(client_socket)

        # Закрываем соединение с клиентом
        if client_socket.fileno() != -1:  # Проверка, что сокет еще не закрыт
            client_socket.close()

        # Удаляем клиента из словарей и множества, если он еще существует
        self.client_addresses.pop(client_socket, None)
        self.client_names.pop(client_socket, None)
        self.active_players.discard(client_socket)

        # Убедимся, что сокет еще есть в списке игроков перед удалением
        if client_socket in self.players_for_game:
            self.players_for_game.remove(client_socket)

        # Сообщаем всем клиентам, что этот клиент покинул чат
        self.broadcast_message(
            f"{self.client_names.get(client_socket, 'Неизвестный клиент')} покинул чат.\n".encode('utf-8'), None)

    def broadcast_message(self, message, sender_socket):
        """Функция для рассылки сообщений всем клиентам, кроме отправителя."""
        for sock in self.to_monitor:
            if sock is not self.server_socket and sock is not sender_socket:
                try:
                    sock.send(message)
                except BrokenPipeError:
                    self.remove_client(sock)

    def event_loop(self):
        """Главный цикл событий для мониторинга сокетов и обработки сообщений."""
        while True:
            ready_to_read, _, _ = select(self.to_monitor, [], [])
            for sock in ready_to_read:
                if sock is self.server_socket:
                    self.accept_connection()  # Обрабатываем новое подключение
                else:
                    self.handle_client_message(sock)  # Обрабатываем сообщение от клиента

    def handle_client_message(self, client_socket):
        """Обрабатываем сообщение от клиента."""
        try:
            request = client_socket.recv(1024)  # Читаем данные от клиента

            if request:
                sender_name = self.client_names.get(client_socket, 'Неизвестный клиент')
                message = f"{sender_name}: {request.decode('utf-8')}\n".encode('utf-8')
                print(f"Получено сообщение от {sender_name}: {request.decode('utf-8')}")
                self.broadcast_message(message, client_socket)
            else:
                # Если запрос пустой, клиент закрыл соединение
                self.remove_client(client_socket)
        except ConnectionResetError:
            # Обработка ошибки, если клиент неожиданно отключился
            self.remove_client(client_socket)


if __name__ == "__main__":
    # Создаем и запускаем сервер
    server = ChatServer()
    server.event_loop()
