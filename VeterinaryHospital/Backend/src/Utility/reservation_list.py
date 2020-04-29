reservation_list = []


def get_list():
    return reservation_list


def update_list(l):
    global reservation_list
    l = map(eval, l)
    reservation_list = list(l)
    return reservation_list
