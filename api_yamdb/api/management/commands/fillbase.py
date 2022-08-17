import contextlib
import csv
import os
from typing import Dict, List

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

PATH: str = os.path.join('static', 'data')
FILE_EXT: str = '.csv'
APPS_MODELS: dict = {model.__name__.lower(): model
                     for model in apps.get_models(include_auto_created=True)}
MESSAGE_TYPE_ERROR: str = ('Назование столбца таблицы {} '
                           'отличается. Используйте {}.')
MESSAGE_VALUE_ERROR: str = ('В папке {} есть файлы - {}, '
                            'для которых нет таблиц. '
                            'Используйте имена - {}.')
MESSAGE_EXCEPTION: str = ('В таблице {} есть некорректные данные. '
                          'Проверьте csv.')
MESSAGE_COMMAND_ERROR: str = ('В папке {} нет файлов для импорта.')
MESSAGE_SUCCESS: str = ('Данные файла {}.csv успешно занесены в базу. '
                        'Заполнено {} строк.')


def change_key_name(key):
    """Подменить значение ключа для user."""
    name = ['author', 'user']
    try:
        name.remove(key)
    except ValueError:
        return key
    return name[0]


class Command(BaseCommand):
    help = ('Команда для импорта .csv в базу данных. ')

    def handle(self, *args, **options):
        """Перебрать все файлы в цикле, пока не будут установлены все,
        в необходимом порядке, для создания related связей.
        Raises:
            Exception: Выйти из цикла, если есть данные,
            которые не могут быть установлены по причине
            полного отсутствия ссылки в related таблицах.
            (Ошибка при заполнении csv оператором)
        """
        files_names = self.files_is_exists_and_file_name_is_done()

        start_round_flag = True
        while start_round_flag:
            unrecorded_files = []
            for file_name in files_names:
                file = File(file_name)
                unrecorded_files: dict = (
                    file.open_read_save_file(unrecorded_files)
                )
            if len(unrecorded_files):
                if files_names == unrecorded_files:
                    raise Exception(MESSAGE_EXCEPTION.format(file))
                files_names = unrecorded_files
                start_round_flag = True
            else:
                start_round_flag = False

    def files_is_exists_and_file_name_is_done(self) -> list:
        """Проверяем наличие файлов и корректности их имен.
        Raises:
            CommandError: В папке нет файлов.
            ValueError: Названия некорректны.
        Returns:
            list: Список названий файлов .csv
        """
        files_names: list = [_.replace(FILE_EXT, '') for _ in os.listdir(PATH)
                             if _.endswith(FILE_EXT)]
        if not len(files_names):
            raise CommandError(MESSAGE_COMMAND_ERROR.format(PATH))

        files_name_error = set(files_names).difference(set(APPS_MODELS))
        if len(files_name_error):
            raise ValueError(
                MESSAGE_VALUE_ERROR.format(PATH, files_name_error,
                                           list(APPS_MODELS))
            )
        return files_names


class File():
    """Файл csv для записи в таблицу."""

    def __init__(self, file_name) -> None:
        self.file_name = file_name

    @property
    def get_file_path(self) -> str:
        """Получить путь до файла.
        """
        return os.path.join(PATH, self.file_name + FILE_EXT)

    @property
    def get_table(self) -> object:
        """Получить объект модели таблицы по имени файла.
        """
        return APPS_MODELS[self.file_name]

    @property
    def get_table_all_fields(self) -> List[str]:
        """Получить все поля таблицы. Информационно.
        """
        table_model = self.get_table
        return [f.name for f in table_model._meta.fields]

    @property
    def get_table_related_fields(self) -> List[str]:
        """Получить список полей таблицы с полем типа ForeigenKey.
        """
        table_model = self.get_table
        return [f.name for f in table_model._meta.fields
                if f.__class__.__name__ == 'ForeignKey']

    def open_read_save_file(self, unrecorded_files) -> List[str]:
        """Открыть файл и записать его в таблицу
        Args:
            unrecorded_files (list): Пустой список
        Returns:
            List[str]: Список файлов, которые не были записаны в таблицы.
        """
        with open(self.get_file_path, 'r', encoding="utf-8") as csvfile:
            rows = csv.reader(csvfile, delimiter=',')
            field_name = next(rows)
            data = self.save_by_rows(rows, field_name)
            check_recorded_row = data['check']
            if False not in check_recorded_row:
                print(MESSAGE_SUCCESS.format(self.file_name, data['row_done']))
            else:
                unrecorded_files.append(self.file_name)
        return unrecorded_files

    def save_by_rows(self, rows, field_name) -> dict:
        """Построчная запись в таблицу.
        Raises:
            TypeError: В csv есть столбец,
            название которого не совпадает с табличными столбцами.
        Returns:
            List[bool]: Контрольный список - удачно ли прошла запись строки.
        """
        check_recorded_row = []
        count = 0
        for row in rows:
            record_flag = True
            values_for_save: Dict[str, str] = dict(zip(field_name, row))
            if len(self.get_table_related_fields):
                values_for_save = (
                    self.save_by_rows_related_from_another_table(
                        values_for_save
                    ))
            try:
                data = self.get_table(**values_for_save)
            except ValueError:
                pass
            except TypeError as e:
                raise TypeError(MESSAGE_TYPE_ERROR.format(
                    self.file_name,
                    self.get_table_all_fields
                )) from e
            try:
                data.save()
                count += 1
            except Exception:
                record_flag = False
            check_recorded_row.append(record_flag)
            data = {
                'check': check_recorded_row,
                'row_done': count
            }
        return data

    def save_by_rows_related_from_another_table(self,
                                                values_for_save
                                                ) -> Dict[str, object]:
        """Построчная запись в таблицу для таблиц с related_field
        Args:
            values_for_save (_type_): Данные,
            которые не имеют ссылочных объектов.
        Returns:
            Dict[str, object]: Измененные данные,
            в которых вместо строки объект.
        """
        for key, value in values_for_save.items():
            if key in self.get_table_related_fields:
                key = change_key_name(key)
                table_related = APPS_MODELS[key]
                with contextlib.suppress(table_related.DoesNotExist):
                    value = table_related.objects.get(id=value)
                key = change_key_name(key)
            values_for_save[key] = value
        return values_for_save

    def __str__(self) -> str:
        return self.file_name
