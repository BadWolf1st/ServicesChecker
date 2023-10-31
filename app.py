import requests
import socket
import configparser
import os


class conf:
    def __init__(self, path):
        self._services_path = path
        self.__init_services__()

    def __init_services__(self):
        self._config = configparser.ConfigParser()
        if not os.path.exists(self._services_path + '/services.ini'):
            self._save_services()
        self._config.read(self._services_path + '/services.ini')

    def _save_services(self):
        with open(self._services_path + "/services.ini", "w") as config_file:
            self._config.write(config_file)

    def save_service(self, host: str, type_host: str, feedback: int):
        self._config.add_section(host)
        self._config.set(host, 'host', host)
        self._config.set(host, 'type', type_host)
        self._config.set(host, 'feedback', str(feedback))
        self._save_services()

    def remove_service(self, host: str):
        self._config.remove_section(host)
        self._save_services()

    def get_full_services_information(self) -> list:
        return [item(source=host, typeOfSource=self._config.get(section=host, option='type'),
                     rightAnswer=int(self._config.get(section=host, option='feedback'))) for host in
                self._config.sections()]


class item:
    def __init__(self, source: str, typeOfSource: str, rightAnswer: int):
        self.source = source
        self.type_host = typeOfSource
        self.answer = rightAnswer


class aitem(item):
    def __init__(self, source: str, typeOfSource: str, rightAnswer, newAnswer):
        super().__init__(source, typeOfSource, rightAnswer)
        self.source = source
        self.type_host = typeOfSource
        self.answer = rightAnswer
        self.newAnswer = newAnswer


class app:

    def __init__(self):
        self.showErrors = None
        self._services = conf('./')
        self.debug = False
        self._workList = self._services.get_full_services_information()

    def set(self, DEBUG: bool, ERRORS: bool):
        self.debug = DEBUG
        self.showErrors = ERRORS

    def __convertStr__(s):
        """Convert string to either int or float."""
        try:
            ret = int(s)
        except ValueError:
            # Try float.
            ret = float(s)
        return ret

    def add(self, host: str, type_host: str, feedback: int):
        self._services.save_service(host, type_host, feedback)

    def remove(self, host_num):
        host = self._workList[host_num].source
        self._workList.pop(host_num)
        self._services.remove_service(host)

    def get_list(self):
        return self._workList

    def check(self, num_host: int):
        item_host = self._workList[num_host]
        return item_host.source, True if (item_host.type_host == 'site' and self.checkURL(
            item_host.source) == item_host.answer) or (item_host.type_host != 'site' and self.checkServer(
            item_host.source) == item_host.answer) else False

    def checkServer(self, source: str) -> int:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            newSource = source.split(':', 1)
            if self.debug:
                print(newSource[0], newSource[1])
            # port like INT!!!
            s.connect((newSource[0], self.__convertStr__()))
            s.shutdown(socket.SHUT_RDWR)
            if self.debug:
                print(1)
            s.close()
            return 1
        except:
            if self.debug:
                print(0)
            s.close()
            return 0

    def checkURL(self, url: str) -> int:
        try:
            link = "https://" + url
            r = requests.head(link)
            if self.debug:
                print(url, ":", r.status_code)
            return r.status_code
        except requests.ConnectionError:
            return 0

    def works(self) -> list:
        answers = []
        for i in self._workList:
            answers.append(aitem(i.source, i.type_host, i.answer, self.checkURL(
                i.source) if i.type_host == 'site' else self.checkServer(i.source)))
        return answers

    def notValid(self, somelist: list) -> list:
        answer = []
        for i in somelist:
            if self.debug:
                print(i.answer, i.newAnswer)
            if i.answer != i.newAnswer:
                answer.append(i)
        return answer

    def run(self):
        if not self._workList:
            return
        done = self.works()
        wrong = self.notValid(done)
        if wrong:
            print("Have", len(wrong), "problems!")
            if self.showErrors:
                print('Problems:')
                for i in wrong:
                    print(i.source, ':', i.newAnswer, 'expected', i.answer)
        else:
            print("No problems")
