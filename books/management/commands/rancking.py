from books.models import JaccardDistance

nb_books = 103


def crank(node):
    distances = list(JaccardDistance.objects.filter(idBook1=node).values_list('distance')) + list(JaccardDistance.objects.filter(idBook2=node).values_list('distance'))
    s = 0
    for i in distances:
        print(i)
        s += i[0]
    return (nb_books - 1) / s

print(crank(1))

