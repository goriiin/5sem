import os
import subprocess

# Укажите путь к сохранению диаграмм и путь к plantuml.jar
uml_path = os.path.join(os.getcwd(), 'uml_diagrams')
os.makedirs(uml_path, exist_ok=True)
plantuml_jar_path = './plantuml-1.2024.7.jar'  # Укажите здесь путь к plantuml.jar


# Функция для записи PlantUML диаграмм в файл
def create_uml_file(file_name, uml_code):
    file_path = os.path.join(uml_path, file_name)
    with open(file_path, 'w') as f:
        f.write(uml_code)
    return file_path


# Функция для генерации диаграммы через локальный PlantUML
def generate_diagram(file_path):
    try:
        subprocess.run(["java", "-jar", plantuml_jar_path, file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при генерации диаграммы {file_path}: {e}")


# 5.3.1 Диаграмма вариантов использования (Use Case Diagram)
use_case_diagram_code = """
@startuml
actor "Пользователь" as User
actor "Администратор" as Admin

User -> (Вход в систему)
User -> (Регистрация)
User -> (Просмотр поста)
User -> (Поставить лайк)
User -> (Ответить на вопрос)
User -> (Подписаться на пользователя)
User -> (Поиск контента)

Admin -> (Управление постами)
Admin -> (Удаление постов)
@enduml
"""
use_case_diagram_path = create_uml_file("use_case_diagram.puml", use_case_diagram_code)
generate_diagram(use_case_diagram_path)

# 5.3.2 Концептуальная модель предметной области (Conceptual Model Diagram)
conceptual_model_code = """
@startuml
class Пользователь {
    +username: String
    +email: String
}

class Профиль {
    +avatar_path: String
    +answers_count: int
    +followers_count: int
}

class Пост {
    +content: String
    +created_time: DateTime
    +likes_count: int
    +answers_count: int
}

class Ответ {
    +answer: Text
    +created_time: DateTime
    +likes_count: int
}

Пользователь "1" -- "1" Профиль
Профиль "1" -- "*" Пост
Профиль "1" -- "*" Ответ
Профиль "1" -- "*" Профиль : подписчики
Пост "1" -- "*" Ответ
@enduml
"""
conceptual_model_path = create_uml_file("conceptual_model.puml", conceptual_model_code)
generate_diagram(conceptual_model_path)

# 5.3.3 Диаграмма классов предметной области (Class Diagram)
class_diagram_code = """
@startuml
class Пользователь {
    +username: CharField
    +email: EmailField
}

class Профиль {
    +avatar_path: String
    +answers_count: Integer
    +followers_count: Integer
}

class Пост {
    +content: Text
    +created_time: DateTime
    +likes_count: Integer
    +answers_count: Integer
}

class Ответ {
    +answer: Text
    +created_time: DateTime
    +likes_count: Integer
}

Пользователь "1" -- "1" Профиль
Профиль "1" -- "*" Пост
Профиль "1" -- "*" Ответ
Пост "1" -- "*" Ответ
@enduml
"""
class_diagram_path = create_uml_file("class_diagram.puml", class_diagram_code)
generate_diagram(class_diagram_path)

# 5.3.4 Диаграмма последовательности (Sequence Diagram)
sequence_diagram_code = """
@startuml
actor Пользователь
Пользователь -> ФормаВхода : Вводит логин и пароль
ФормаВхода -> Пользователь : Проверка учетных данных
ФормаВхода -> БазаДанных : Запрос на получение пользователя
БазаДанных -> ФормаВхода : Возврат информации о пользователе
ФормаВхода -> Пользователь : Успешный вход

Пользователь -> ФормаВопроса : Создать пост
ФормаВопроса -> БазаДанных : Сохранение поста
БазаДанных -> ФормаВопроса : Подтверждение
ФормаВопроса -> Пользователь : Пост создан
@enduml
"""
sequence_diagram_path = create_uml_file("sequence_diagram.puml", sequence_diagram_code)
generate_diagram(sequence_diagram_path)

# 5.3.5 Диаграмма компонентов (Component Diagram)
component_diagram_code = """
@startuml
package "Формы" {
    component ФормаВхода
    component ФормаРегистрации
    component ФормаВопроса
}

package "Модели" {
    component Пользователь
    component Профиль
    component Пост
    component Ответ
    component Тег
}

ФормаВхода --> Пользователь : Проверка входа
ФормаРегистрации --> Пользователь : Создание учетной записи
ФормаВопроса --> Пост : Создание поста
ФормаВопроса --> Тег : Добавление тегов к посту
@enduml
"""
component_diagram_path = create_uml_file("component_diagram.puml", component_diagram_code)
generate_diagram(component_diagram_path)

# 5.3.6 Схема алгоритма модуля (Activity Diagram)
activity_diagram_code = """
@startuml
start
:Пользователь отправляет форму входа;
if (Учетные данные верны?) then (да)
    :Аутентификация пользователя;
    :Перенаправление на главную страницу;
else (нет)
    :Вывод сообщения об ошибке;
    :Остаётся на странице входа;
endif
stop
@enduml
"""
activity_diagram_path = create_uml_file("activity_diagram.puml", activity_diagram_code)
generate_diagram(activity_diagram_path)
