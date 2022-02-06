from books.models import JaccardDistance


def closeness_rank(node, nb_books):
    distances = list(JaccardDistance.objects.filter(idBook1=node).values_list('distance')) + \
                list(JaccardDistance.objects.filter(idBook2=node).values_list('distance'))
    s = 0
    for i in distances:
        # print(i)
        s += i[0]
    return (nb_books - 1) / s

# print(closeness_rank(1, 103))


def parcours_closeness():
    books = list(JaccardDistance.objects.all().values_list('idBook1', 'idBook2', 'distance'))
    sums = dict()

    for (i, j, d) in books:
        if i not in sums:
            sums[i] = d
        else:
            sums[i] += d
        if j not in sums:
            sums[j] = d
        else:
            sums[j] += d

    for i in sums:
        sums[i] = (len(sums) - 1) / sums[i]
    return sums

temp = parcours_closeness()
max = 0
max_id = 0
for i in temp:
    if temp[i] > max:
        max = temp[i]
        max_id = i

