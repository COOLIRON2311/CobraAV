from enum import Enum
from config import LANG


class L(Enum):
    Add = {'ru': 'Добавить', 'en': 'Add'}
    Remove = {'ru': 'Удалить', 'en': 'Remove'}
    Done = {'ru': 'Готово', 'en': 'Done'}
    Cancel = {'ru': 'Отмена', 'en': 'Cancel'}
    Minutes = {'ru': 'Минут', 'en': 'Minutes'}
    Hours = {'ru': 'Часов', 'en': 'Hours'}
    Days = {'ru': 'Дней', 'en': 'Days'}
    Weeks = {'ru': 'Недель', 'en': 'Weeks'}
    Months = {'ru': 'Месяцев', 'en': 'Month'}
    Bytes = {'ru': 'Б', 'en': 'B'}
    KBytes = {'ru': 'КБ', 'en': 'KB'}
    MBytes = {'ru': 'МБ', 'en': 'MB'}
    GBytes = {'ru': 'ГБ', 'en': 'GB'}
    TBytes = {'ru': 'ТБ', 'en': 'TB'}
    UpdatesFrame = {'ru': 'Обновление', 'en': 'Updates'}
    Upd_Label1 = {'ru': 'Проверять обновления антивирусных баз',
                  'en': 'Check for signature updates'}
    Upd_Label2 = {'ru': 'Частота проверки:   каждые',
                  'en': 'Update frequency: '}
    Upd_Button1 = {'ru': 'Источники антивирусных сигнатур',
                   'en': 'Update channels'}
    ScanFrame = {'ru': 'Сканирование', 'en': 'Scan'}
    Scn_Label1 = {'ru': 'Максимальный размер файла:', 'en': 'Max file size:'}
    Quar_Label = {'ru': 'При обнаружении угрозы', 'en': 'On threat detection'}
    Quar_RadButton1 = {'ru': 'Удаление', 'en': 'Delete'}
    Quar_RadButton2 = {'ru': 'Карантин', 'en': 'Quarantine'}
    Scn_Edit_Targets = {'ru': 'Цели сканирования', 'en': 'Scan targets'}
    Scn_Edit_Exceptions = {'ru': 'Исключения', 'en': 'Whitelist'}
    Quar_Button1 = {'ru': 'Расположение карантина',
                    'en': 'Quarantine location'}
    ReportFrame = {'ru': 'Отправка отчета', 'en': 'Email reports'}
    Rpt_Label1 = {'ru': 'Отправлять отчеты о сканировании',
                  'en': 'Send scan reports'}
    Rpt_Label2 = {'ru': 'Адрес отправки отчетов:', 'en': 'Send from:'}
    Rpt_Label3 = {'ru': 'Пароль:', 'en': 'Password:'}
    Rpt_Label4 = {'ru': 'Частота отправки', 'en': 'Send every'}
    Rpt_Button1 = {'ru': 'Получатели', 'en': 'Recipients'}

    def __str__(self) -> str:
        return self.value[LANG]
