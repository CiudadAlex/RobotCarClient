

class MatchUtils:

    @staticmethod
    def get_most_matching_text_item(text, list_text_items):

        max_similarity = -1
        most_similar_item = None

        for text_item in list_text_items:

            similarity = MatchUtils.get_similarity(text, text_item)

            # print(text + " >> " + text_item + " >> " + str(similarity))

            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_item = text_item

        return most_similar_item

    @staticmethod
    def get_similarity(text1, text2):
        list_words_1 = MatchUtils.get_list_words_longer_than_2(text1)
        list_words_2 = MatchUtils.get_list_words_longer_than_2(text2)

        similarity_1 = MatchUtils.calculate_one_way_similarity(list_words_1, list_words_2)
        similarity_2 = MatchUtils.calculate_one_way_similarity(list_words_2, list_words_1)
        return similarity_1 + similarity_2

    @staticmethod
    def calculate_one_way_similarity(list_words_1, list_words_2):

        similarity = 0

        for word_1 in list_words_1:
            if word_1 in list_words_2:
                similarity = similarity + 1

        return similarity

    @staticmethod
    def get_list_words_longer_than_2(text):
        list_words = text.split()
        return set(list(filter(MatchUtils.get_longer_than_2, list_words)))

    @staticmethod
    def get_longer_than_2(text):
        return len(text) > 2
