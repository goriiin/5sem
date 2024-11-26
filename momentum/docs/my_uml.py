import os
import subprocess

# Укажите путь к сохранению диаграмм и путь к plantuml.jar
uml_path = os.path.join(os.getcwd(), 'docs/diagrams')
os.makedirs(uml_path, exist_ok=True)
plantuml_jar_path = './docs/plantuml-1.2024.7.jar'  # Укажите здесь путь к plantuml.jar


#
# Функция для записи PlantUML диаграмм в файл
def create_uml_file(file_name, uml_code):
    file_path = os.path.join(uml_path, file_name)
    with open(file_path, 'w') as f:
        f.write(uml_code)
    return file_path


# Функция для генерации диаграммы через локальный PlantUML
def generate_diagram(file_path):
    try:
        print(f"Запуск PlantUML для файла: {file_path}")
        subprocess.run(["java", "-jar", plantuml_jar_path, file_path], check=True)
        print(f"Диаграмма успешно сгенерирована: {file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при генерации диаграммы {file_path}: {e}")
    except FileNotFoundError:
        print("Не удалось найти Java. Убедитесь, что Java установлена и доступна.")



# # 5.3.2 Концептуальная модель предметной области (Conceptual Model Diagram)
# conceptual_model_code = """
# @startuml
# class Пользователь {
#     +имя_пользователя: String
#     +электронная_почта: String
# }
#
# class Профиль {
#     +аватар: String
#     +количество_ответов: int
#     +время_обновления: DateTime
#     +количество_подписчиков: int
# }
#
# class Тег {
#     +название_тега: String
#     +использований: int
# }
#
# class Пост {
#     +содержимое: String
#     +время_создания: DateTime
#     +количество_лайков: int
#     +количество_ответов: int
#     +режим_доступа: String
# }
#
# class Ответ {
#     +текст_ответа: Text
#     +время_создания: DateTime
#     +количество_лайков: int
# }
#
# class ЛайкПоста {
#     +оценка: int
# }
#
# class ЛайкОтвета {
#     +оценка: int
# }
#
# class Подписка {
#     +время_создания: DateTime
# }
#
# class ФайлПоста {
#     +файл: File
# }
#
# Пользователь "1" -- "1" Профиль
# Профиль "1" -- "*" Пост
# Профиль "1" -- "*" Ответ
# Профиль "1" -- "*" Профиль : подписчики
# Пост "1" -- "*" Ответ
# Пост "1" -- "*" ЛайкПоста
# Ответ "1" -- "*" ЛайкОтвета
# Пост "1" -- "*" Тег
# Пост "1" -- "*" ФайлПоста
# Профиль "1" -- "*" Подписка : подписчик
# Профиль "1" -- "*" Подписка : подписан
# @enduml
# """
# conceptual_model_path = create_uml_file("conceptual_model.puml", conceptual_model_code)
# generate_diagram(conceptual_model_path)
#
# # 5.3.3 Диаграмма классов предметной области (Class Diagram)
# class_diagram_code = """
# @startuml
# class Tag {
#     + tag_name: CharField
#     + used_times: PositiveIntegerField
#     + __str__(): str
#     + objects: TagManager
# }
#
# class Profile {
#     + updated_time: DateTimeField
#     + avatar_path: ImageField
#     + answers_count: PositiveIntegerField
#     + user: OneToOneField(User)
#     + recalculate_answers_count(): None
#     + __str__(): str
#     + __int__(): int
#     + objects: ProfileManager
# }
#
# class Post {
#     + content: TextField
#     + author: ForeignKey(Profile)
#     + created_time: DateTimeField
#     + likes_count: IntegerField
#     + answers_count: IntegerField
#     + tags: ManyToManyField(Tag)
#     + access_mode: CharField
#     + save(*args, **kwargs): None
#     + recalculate_likes(): None
#     + recalculate_answers_count(): None
#     + __int__(): int
#     + objects: PostManager
# }
#
# class PostLike {
#     + user_id: ForeignKey(Profile)
#     + question_id: ForeignKey(Post)
#     + vote: IntegerField
#     + objects: PostLikeManager
# }
#
# class Answer {
#     + answer: TextField
#     + created_time: DateTimeField
#     + author: ForeignKey(Profile)
#     + likes_count: IntegerField
#     + question: ForeignKey(Post)
#     + save(*args, **kwargs): None
#     + recalculate_likes(): None
#     + __str__(): str
#     + __int__(): int
#     + objects: AnswerManager
# }
#
# class AnswerLike {
#     + answer: ForeignKey(Answer)
#     + vote: IntegerField
#     + user_id: ForeignKey(Profile)
#     + objects: AnswerLikeManager
# }
#
# class PostFile {
#     + post: ForeignKey(Post)
#     + file: FileField
#     + __str__(): str
# }
#
# class Subscription {
#     + follower: ForeignKey(Profile)
#     + followed: ForeignKey(Profile)
#     + created_at: DateTimeField
# }
#
# User --> Profile : "1 : 1"
# Profile --> Subscription : "1 *"
# Profile --> Post : "1 *"
# Post --> PostFile : "1 *"
# Post --> PostLike : "1 *"
# Post --> Answer : "1 *"
# Answer --> AnswerLike : "1 *"
# Profile --> Answer : "1 *"
# Profile --> PostLike : "1 *"
# Profile --> AnswerLike : "1 *"
# Post --> Tag : "ManyToMany"
# @enduml
# """
# class_diagram_path = create_uml_file("class_diagram.puml", class_diagram_code)
# generate_diagram(class_diagram_path)
#
# # 5.3.4 Диаграмма последовательности (Sequence Diagram)
# sequence_diagram_code = """
# @startuml
# skinparam DefaultFontSize 25
# skinparam ParticipantFontSize 16
# skinparam ActorFontSize 25
# skinparam ParticipantPadding 20
# skinparam BoxPadding 25
#
# actor User
# participant "Клиент" as Browser
# participant "Сервер" as Backend
# participant "База Данных" as Database
#
# User -> Browser: Запрос "Подписаться"
# Browser -> Backend: Отправка запроса на подписку
# Backend -> Database: Проверить, вошел ли пользователь
# Database --> Backend: Ответ (Пользователь не аутентифицирован)
#
# alt Пользователь не аутентифицирован
#     Backend -> Browser: Перенаправление на страницу входа
#     Browser -> Backend: Отправка учетных данных
#     Backend -> Database: Проверка учетных данных
#     Database --> Backend: Учетные данные верны
#     Backend -> Browser: Перенаправление обратно в профиль
# end
#
# Browser -> Backend: Повторный запрос "Подписаться"
# Backend -> Database: Проверить наличие подписки
# Database --> Backend: Подписка отсутствует
# Backend -> Database: Создание подписки
# Database --> Backend: Подписка создана
# Backend -> Browser: Уведомление об успешной подписке
# Browser -> User: Вы подписались на пользователя
# @enduml
# """
# sequence_diagram_path = create_uml_file("sequence_diagram.puml", sequence_diagram_code)
# generate_diagram(sequence_diagram_path)
#
# # 5.3.5 Диаграмма компонентов (Component Diagram)
# component_diagram_code = """
# @startuml
# package "Формы" {
#     component ФормаВхода
#     component ФормаРегистрации
#     component ФормаВопроса
# }
#
# package "Модели" {
#     component Пользователь
#     component Профиль
#     component Пост
#     component Ответ
#     component Тег
# }
#
# ФормаВхода --> Пользователь : Проверка входа
# ФормаРегистрации --> Пользователь : Создание учетной записи
# ФормаВопроса --> Пост : Создание поста
# ФормаВопроса --> Тег : Добавление тегов к посту
# @enduml
# """
# component_diagram_path = create_uml_file("component_diagram.puml", component_diagram_code)
# generate_diagram(component_diagram_path)

# 5.3.6 Схема алгоритма модуля (Activity Diagram)
project_layout = """
@startuml
skinparam componentStyle rectangle

package "Project Momentum" {
    folder "Web Server" as WebServer
    folder "Django Application" as DjangoApp {
        folder "back" as BackApp {
            file "models.py"
            file "views.py"
            file "forms.py"
            file "urls.py"
            file "admin.py"
            folder "management" as Management {
                folder "commands" as Commands {
                    file "fill_db.py"
                    file "__init__.py"
                }
                file "__init__.py"
            }
            folder "migrations" as Migrations {
                file "0001_initial.py"
                file "0002_remove_answer_correct.py"
                file "0003_remove_post_title.py"
                file "0004_postfile.py"
                file "0005_alter_postfile_file.py"
                file "0006_subscription.py"
                file "0007_post_access_mode.py"
                file "__init__.py"
            }
            folder "templatetags" as TemplateTags {
                file "custom_filters.py"
                file "__init__.py"
            }
        }
        folder "momentum" as CoreApp {
            file "settings.py"
            file "urls.py"
            file "wsgi.py"
            file "asgi.py"
            file "__init__.py"
        }
        folder "templates" as Templates {
            file "index.html"
            file "profile.html"
            file "question.html"
            file "base.html"
        }
        folder "static" as StaticFiles {
            folder "css"
            folder "js"
            folder "img"
        }
    }
    folder "Database (PostgreSQL)" as Database
    folder "Config Files" as Config {
        file "Dockerfile"
        file "docker-compose.yml"
        file ".env"
    }
}

WebServer --> DjangoApp
DjangoApp --> BackApp
BackApp --> Management
BackApp --> Migrations
BackApp --> TemplateTags
DjangoApp --> CoreApp
DjangoApp --> Templates
DjangoApp --> StaticFiles
DjangoApp --> Database
DjangoApp --> Config
@enduml
"""
activity_diagram_path = create_uml_file("project_layout.puml", project_layout)
generate_diagram(activity_diagram_path)
