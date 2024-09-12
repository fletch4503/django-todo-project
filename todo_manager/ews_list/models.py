from django.db import models
import logging

from todo_manager.common import conf_logging

log = logging.getLogger(__name__)

from todo_manager.settings import exch_username, exch_userkey, exch_usersmtpaddr, exch_authtype, exch_serverurl, \
    inb_fold, inb_fold_sales, inb_fold_supp, inb_fold_other

"""
Из файла настроек для Exchange-сервера берем
exch_username - это username для обращения к серверу
exch_userkey - пароль пользователя
exch_serverurl - адрес exchange-сервера
exch_usersmtpaddr - адрес электронной почты пользователя (пресейла)
exch_authtype - тип аутентификации на exchange-сервере 
inb_fold - название папки, в которую будут складываться входящие сообщения из компании
inb_fold_sales - название папки, в которую будут складываться входящие сообщения от менеджеров
inb_fold_supp - название папки, в которую будут складываться входящие сообщения от поставщиков
inb_fold_other - название папки, в которую будут складываться неидентифицированные входящие сообщения
"""

from exchangelib import (
    Account,
    Credentials,
    Build,
    Configuration,
    FaultTolerance,
    Version,
    # Message,
    # Mailbox,
    # Folder,
    # HTMLBody,
    # FileAttachment,
    # ItemAttachment,
    # EWSDateTime,
    # EWSTimeZone,
    # EWSDate,
)


# Класс для работы с Exchange-сервером
class pwp_exch_model:
    # def __str__(self):  # Информируем о параметрах
    # return f"{self.__class__.__name__}"
    # # return f"{self.__class__.__name__}(id={id(self)})"

    # 0 - Total, 1 - Unread, 2 - Suppl, 3 - mtst, 4 - other, 5 - TCB
    msg_cnt_list = [0, 0, 0, 0, 0, 0]  # Обнуляем список счетчиков полученных сообщений в папке inbox
    current_message = None  # Текущее обрабатываемое сообщение

    def __init__(self):  # Подключаемся к Exchange-серверу и проверяем подключение
        log.info("pwp_exch_model --> exch_username: %s",exch_username)
        log.info("pwp_exch_model --> exch_userkey: %s",exch_userkey)
        try:
            self.credents_project = Credentials(username=exch_username, password=exch_userkey)
            log.info("pwp_exch_model --> Запустили подключение Credentials")
        except AttributeError:
            log.warning("Потерялся файл с конфигурацией в директории проекта")
        self.version = Version(build=Build(15, 0, 1497, 4012))
        # Обрабатываем ошибку в параметрах Exchange-сервера
        try:
            self.conf_exchange = Configuration(
                server=exch_serverurl, retry_policy=FaultTolerance(max_wait=3600), credentials=self.credents_project,
                version=self.version, auth_type=exch_authtype, max_connections=10)
        except NameError:
            log.info("Не заданы параметры Exchange-сервера")
            exit()
        # Подключаемся к Exchange-аккаунту на основе данных из конфигурационного файла
        self.my_acc_exch = Account(primary_smtp_address=exch_usersmtpaddr, config=self.conf_exchange,
                                   credentials=self.credents_project, autodiscover=False)
        # Определяемся с Тайм-зонами
        # timezones = list(self.my_acc_exch.protocol.get_timezones(return_full_timezone_data=True))
        # print('pwp_exch_model -> __init__() -> Список timezones: ', timezones)
        # Инициируем папки для сортировки входящих сообщений
        # print("pwp_exch_model --> Подключились к аккаунту:", self.my_acc_exch)
        # print("pwp_exch_model --> exch_serverurl:", exch_serverurl)
        # print("pwp_exch_model --> self.credents_project:", self.credents_project)
        # print("pwp_exch_model --> exch_authtype:", exch_authtype)
        self.get_fold_supp = ''
        self.f_in = self.my_acc_exch.inbox // inb_fold
        self.f_in_sales = self.my_acc_exch.inbox // inb_fold_sales
        self.f_in_supp = self.my_acc_exch.inbox // inb_fold_supp
        self.f_in_other = self.my_acc_exch.inbox // inb_fold_other
        self.f_in_requests = self.my_acc_exch.inbox // 'ЗАПРОСЫ'
        self.f_in_projects = self.my_acc_exch.inbox // 'ПРОЕКТЫ'
        # self.f_supp_folder = None  # Начальный шаблон для добавления
        # self.f_supp_folder = self.my_acc_exch.inbox / 'DISTI'  # Начальный шаблон для добавления
        # self.f_vendor_folder = self.my_acc_exch.inbox / 'Vendors'  # Начальный шаблон для добавления
        log.warning("pwp_exch_model --> self.f_in: %s", inb_fold)
        log.warning("pwp_exch_model --> self.f_in_sales: %s", inb_fold_sales)
        log.warning("pwp_exch_model --> self.f_in_supp: %s", inb_fold_supp)
        log.warning("pwp_exch_model --> self.f_in_other: %s", inb_fold_other)
        log.warning("pwp_exch_model --> self.f_in_requests: %s", self.my_acc_exch.inbox / 'ЗАПРОСЫ')
        log.warning("pwp_exch_model --> self.f_in_projects: %s", self.my_acc_exch.inbox / 'ПРОЕКТЫ')

        # Отображаем количество сообщений в папке Входящие
        self.count_inbox_msg()
        # print("pwp_exch_model --> Определяем количество сообщений:")

    """
    Отправка сообщений адресату
    """

    # def msg_send(self, m_body):  # Передаем только тело сообщения для отправки
    #     item = self.current_message
    #     acc = self.my_acc_exch
    #     # recipients: list[Any]
    #     recipients = [item.sender.email_address]
    #     print(f'pwp_exch_model -> msg_send -> item.subject: {item.subject}')
    #     print(f'pwp_exch_model -> msg_send -> recipients: {recipients}')
    #     print(f'pwp_exch_model -> msg_send -> item.cc_recipients: {item.cc_recipients}')
    #     m = Message(account=acc, folder=acc.sent, subject=item.subject, body=m_body,
    #                 to_recipients=recipients, cc_recipients=item.cc_recipients)
    #     m.send_and_save()

    def count_inbox_msg(self):
        # 0 - Total, 1 - Unread, 2 - Suppl, 3 - mtst, 4 - other, 5 - TCB
        print("pwp_exch_model --> count_inbox_msg --> Обновляем папку Inbox")
        self.my_acc_exch.inbox.refresh()
        print("pwp_exch_model --> count_inbox_msg --> Считаем сообщения")
        self.msg_cnt_list[0] = self.my_acc_exch.inbox.total_count  # Всего сообщений в папке Входящие
        self.msg_cnt_list[1] = self.my_acc_exch.inbox.unread_count  # Непрочитанных сообщений в папке Входящие
        all_items = self.my_acc_exch.inbox // inb_fold_supp  # Всего сообщений в папке Поставщики
        self.msg_cnt_list[2] = all_items.total_count
        all_items = self.my_acc_exch.inbox // inb_fold_sales  # Всего сообщений в папке МТСТ
        self.msg_cnt_list[3] = all_items.total_count
        all_items = self.my_acc_exch.inbox // inb_fold_other  # Всего сообщений в папке Другие
        self.msg_cnt_list[4] = all_items.total_count
        all_items = self.my_acc_exch.inbox // inb_fold  # Всего сообщений в папке Inbox
        self.msg_cnt_list[5] = all_items.total_count

        self.my_acc_exch.inbox.refresh()

    # @staticmethod
    # def create_attachement_list(item, files_attach):
    #     # Сначала вытаскиваем вложения из письма
    #     for attachment in item.attachments:
    #         if isinstance(attachment, FileAttachment):
    #             local_path = os.path.join(psettings.tmp_path, attachment.name)
    #             # print('create_attachement_list -> local_path: ', local_path)
    #             # local_path = os.path.join(tmp_path, attachment.name)
    #             # Добавили название файла в список combobox_attach
    #             files_attach.append(attachment.name)
    #             try:
    #                 with open(local_path, 'wb') as f:
    #                     f.write(attachment.content)
    #             except:
    #                 print(f'Файл {f} занят другим процессом!')
    #                 pass
    #             # print('create_attachement_list -> Saved attachment to', local_path)
    #         elif isinstance(attachment, ItemAttachment):
    #             if isinstance(attachment.item, Message):
    #                 try:
    #                     print('create_attachement_list -> Сообщение:', attachment.item.subject, attachment.item.body)
    #                 except:
    #                     pass
    #     return files_attach
    #
    # @staticmethod
    # def clear_tmp_dir():
    #     # Проверяем наличие файлов в папке TMP и после этого удаляем
    #     # Добавляем файлы шаблонов в выпадающий список
    #     if platform.system() == 'Darwin':
    #         files = glob.glob(psettings.tmp_path + '/*')
    #     else:
    #         files = glob.glob(psettings.tmp_path + '/*')
    #     for f in files:
    #         try:
    #             os.remove(f)
    #         except:
    #             print('clear_tmp_dir -> файл - {f} открыт в другом приложении!')
    #
    # @staticmethod
    # def msg_move2folder(msg2move, folder, mark_unread):  # Перемещаем сообщение msg2move в папку folder
    #     if mark_unread == 0:
    #         msg2move.is_read = True
    #     else:
    #         msg2move.is_read = False
    #     try:  # Запускаем исключение для Meeting requests, которые не перекладываются в папки
    #         msg2move.move(folder)
    #         msg2move.save()
    #     except:
    #         pass  # Пока так - нужен анализ типа сообщения во входящих


class ewsitem(models.Model):
    class Meta:
        ordering = ("id",)  # со знаком '-' - обратная сортировка
        verbose_name = "EWS Item"

    # class Meta:
    #     project_id = ("id", )  # со знаком '-' - обратная сортировка
    #     project_req_date = "Project Date"
    conf_logging(level=logging.DEBUG)
    ews_exch = pwp_exch_model()
    log.info("Количество входящих сообщений %r", ews_exch.msg_cnt_list)
    total_count = 0
    for i in range(0, len(ews_exch.msg_cnt_list)):
        total_count = total_count + ews_exch.msg_cnt_list[i]
    if total_count == 0:
        log.warning("ews_list - У вас нет входящих сообщений!!")
    email_title = models.CharField(max_length=250)  # Сюда вставляем заголовки писем с типом из exchangelib
    sender = models.EmailField(max_length=254)  # адрес отправителя
    # sender = models.CharField(max_length=250)  # адрес отправителя
    done = models.BooleanField(default=False)
    log.warning("Got some data. email_title: %s, sender: %s, done: %s", email_title, sender, done)

    def __str__(self):
        return self.email_title
