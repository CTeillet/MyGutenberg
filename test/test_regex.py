from unittest import TestCase

from books.models import Words
from research_RegEx.regex import generate_dfa
import numpy as np
import time


# Create your tests here.


class RegExTest(TestCase):
    def setUp(self) -> None:

        self.words = Words.objects.values_list("word")
        self.list_word = np.array(
            ["baba", "father", "united", "state", "cia", "pierre", "java", "play", "code", "note", "music",
             "given", "file", "number", "are", "several", "duplicate", "here", "updates", "over", "years",
             "all", "original", "included", "old", "subdirectory", "may", "accessed", "raz", "bo", "brin"])

    def test_regex(self):
        list_res = Words.objects.filter(word__contains='united').values_list("word")
        res = set()
        for i in list_res:
            res.add(i[0])
        list_res = Words.objects.filter(word__contains='state').values_list("word")
        for i in list_res:
                res.add(i[0])

        rg_res = set()
        dfa = generate_dfa("united|state")
        for word in self.words:
            if dfa.apply(word[0]):
                rg_res.add(word[0])

        self.assertEqual(res, rg_res)


    def test_regex_altern(self):
        n = len(self.list_word)
        time_sum_regex = 0
        time_sum_sql = 0
        nb_appel = 0
        for i in range(n):
            for j in range(i + 1, n):
                word1 = self.list_word[i]
                word2 = self.list_word[j]
                print("test: ", word1, "|", word2)
                # search in DB
                start = time.time()
                list_res = Words.objects.filter(word__contains=word1).values_list("word")
                res = set()
                for k in list_res:
                    res.add(k[0])
                list_res = Words.objects.filter(word__contains=word2).values_list("word")
                for k in list_res:
                    res.add(k[0])
                end = time.time()
                t1 = end - start

                # search with ReGex
                expression = word1 + "|" + word2
                rg_res = set()
                start = time.time()
                dfa = generate_dfa(expression)
                for word in self.words:
                    if dfa.apply(word[0]):
                        rg_res.add(word[0])
                end = time.time()
                nb_appel += 1
                t2 = end - start
                print("temps sql: ", t1, " temps regex: ", t2)
                time_sum_sql += t1
                time_sum_regex += t2
                self.assertEqual(rg_res, res)
        print("En moyenne on obtient un temps de ", time_sum_regex / nb_appel, " avec regex pour une bd de taille ", len(self.words),
              "\nContre un temps moyen de : ", time_sum_sql/nb_appel, " avec sql lite.")
