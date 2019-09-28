import json

class I18nException(Exception):
    pass

class I18n:
    def __init__(self, file):
        self.file = json.load(open(file, encoding='UTF-8'))

    def get_message(self, phase):
        path = phase.split('.')
        try:
            message = self.file[path[0]]
            return message[path[1]]
        except Exception as e:
            raise I18nException('Message or language not found')


    def get_languages(self):
        list_ = []
        for i in self.file:
            list_.append(i)

        return list_



if __name__ == "__main__":
    lang = I18n('langs/en.json')
    res = lang.get_message('en', 'Hello')
    print(res)