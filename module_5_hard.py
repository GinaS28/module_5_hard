import hashlib
import time


class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname # имя пользователя
        self.password = self.hash_password(password) # пароль в хэшированном виде
        self.age = age # возраст

    def hash_password(self, password):
        return hashlib.md5(password.encode()).hexdigest() # хеширование пароля

class Video:
    def __init__(self, title, duration, adult_mode = False):
        self.title = title # заголовок
        self.duration = duration # продолжительность в секундах
        self.time_now = 0  # Текущее время просмотра видео
        self.adult_mode = adult_mode # Ограничение по возрасту, bool (False по умолчанию)

class UrTube:
    def __init__(self):
        self.users = []  # Список пользователей
        self.videos = []  # Список видео
        self.current_user = None  # Текущий пользователь

    def log_in(self, nickname, password):  # Проверка на наличие пользователя с указанным логином и паролем
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        for user in self.users:
            if user.nickname == nickname and user.password == hashed_password:
                self.current_user = user # Если такой пользователь существует, то current_user меняется на найденного
                print('Вход выполнен успешно.')
                return True
        print('Неверный логин или пароль.')
        return False

    def register(self, nickname, password, age):
        for user in self.users:                #Регистрируем нового пользователя и автоматически выполняет вход
            if user.nickname == nickname:
                print(f'Пользователь {nickname} уже существует')
                return
        new_user = User(nickname, password, age)
        self.users.append(new_user)
        self.current_user = new_user

    def log_out(self):
        self.current_user = None # сброс текущего пользователя

    def add(self, *videos):
        for video in videos: # Добавляем новые видео в список, если видео с таким названием ещё нет
            if video not in self.videos:
                self.videos.append(video)

    def get_videos(self, search_term):
        search_term_lower = search_term.lower()
        return [video.title for video in self.videos if search_term_lower in video.title.lower()]

    def watch_video(self, title):
        if not self.current_user:
            print('Войдите в аккаунт, чтобы смотреть видео')
            return

        for video in self.videos:
            if video.title == title:
                if video.adult_mode and self.current_user.age < 18:
                    print("Вам нет 18 лет, пожалуйста покиньте страницу")
                    return

                while video.time_now < video.duration:
                    print(f"{video.time_now} сек.")
                    time.sleep(1)
                    video.time_now += 1

                print("Конец видео")
                video.time_now = 0  # текущее время просмотра видео сбрасывается
                return

        print("Видео не найдено.")

ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)
ur.add(v1, v2)


# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')

