import wikipediaapi


class Wikipedia:

    def __init__(self):
        self.wiki = wikipediaapi.Wikipedia('Leviathan (saizen@leviathan.com)', 'en')

    def retrieve_full(self, title):

        page_py = self.page(title)
        return page_py.text

    def retrieve_first_part(self, title):
        full_article = self.retrieve_full(title)
        return self.trunk_first_part(full_article)

    @staticmethod
    def trunk_first_part(text):
        end = text.find('\r\n\r\n')
        if end != -1:
            return text[:end]
        else:
            return text
