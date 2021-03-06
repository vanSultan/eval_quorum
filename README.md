## Оценка согласованности разметки

Данное приложение предназначено для оценки согласованности разметки.

---

### Функциональные возможности

В данном релизе предоставляется возможность:
* оценить конкретного волонтера; ![volunteer.jpg](img/volunteer.jpg)
* оценить конкретный абзац; ![section.jpg](img/section.jpg)
* оценить срез спанов. ![frame.jpg](img/frame.jpg)

---

### Интерфейс: ![interface.jpg](img/interface.jpg)

Предусмотрена возможность выбора периода оценки - 
для этого рассматривается поле уникального идентификатора записи спан-волонтер (столбец *idVolSpan*).

---

Оставлен вопрос для дальнейшего рассмотрения: что делать с пользователями-модераторами, 
так как их мнение является эталлонным?

Предложены несколько вариантов решения:
1. Выделить пользователей-модераторов в отедльную таблицу или файл и игнорировать их при оценке.
2. Игнорировать мнение 5-го волонтера в абзаце (плохое решение).
3. Учитывать мнение пользователей-модераторов. (Не совсем правильно, так как их мнение априори верное).

---

### Режимы работы:
* Взаимодействие с базой данных:
    - Реализована возможность получать информацию из базы данных *PostgresSql*.
    - Схема: ![scheme.jpg](img/scheme.jpg)
    - Пример запуска: *python3 [src/eval_quorum.py](src/eval_quorum.py) -c 
    postgresql://eval_quorum:eval_quorum@192.168.10.36/inter_annotation_db*
* Дамп данных в формате *.csv*:
    - В основе анализа лежит демонстрационный набор данных.
    - Заголовок данного файла: *par_id,user_id,entity_id,tag_name,start_token,length*.
    - Для обработки данного формата используется модуль *pandas*.
    - Пример запуска: *python3 [src/eval_quorum.py](src/eval_quorum.py) -f spans.csv*.
    
---

### Дальнейшее развитие

Предполагается использование боевой базы данных, что подразумевает изменения в некоторых классах модели.

Планируемые доработки:
1. При использовании боевого источника данных необходимо скорректировать классы модели.
2. Чтобы избежать постоянных изменений предлагается ввести в схему дополнительное поле, 
в котором будет храниться оценка той или иной сущности (например волонетра или абзаца) 
и при добавлении новых записей *волонтер-спан* обновлять данное значение.
3. Введение дополнительных метрик, таких как: рейтинг волонтеров, ... (надо вспомнить)
    > Данные метрики позволят мотивировать волонтеров, которые участвуют в разметке корпуса.
4. Продумать обработку записей модераторов: либо не учитывать абзацы размеченные ими или не вовсе не учитывать их мнение.
5. При необходимости переделать данный инструмент в веб-приложение.
