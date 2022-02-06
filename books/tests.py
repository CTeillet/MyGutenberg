from django.test import TestCase
from books.models import Words
from research_RegEx.regex import generate_dfa


# Create your tests here.


class RegExTest(TestCase):
    def setUp(self) -> None:
        list_res = Words.objects.filter(word__contains='united').values_list("id")
        self.res = set()

        for i in list_res:
            self.res.add(i[0])

        list_res = Words.objects.filter(word__contains='state').values_list("id")
        for i in list_res:
            self.res.add[i[0]]

    def test_regex(self):
        l = Words.objects.values_list("id", "word")
        rg_res = set()
        dfa = generate_dfa()
        for (id, word) in l:
            if dfa.apply(word):
                rg_res.add(id)
        self.assertEqual(rg_res, self.res)
