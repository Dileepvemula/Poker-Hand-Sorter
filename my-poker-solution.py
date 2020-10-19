import fileinput


def check_increasing(numbers):
    '''

    :param numbers:
    :return:
    '''
    numbers.sort()
    for i in range(1, 5):
        if numbers[i] != numbers[0] + i:
            return 'not_strict_increasing'
    if numbers[0] == 10:
        return 'royal'
    else:
        return 'straight'


def convert_numbers_to_list(numbers):
    '''

    :param numbers:
    :return:
    '''
    ret = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for item in numbers:
        ret[item - 2] += 1
    while 0 in ret:
        ret.remove(0)
    return ret


def create_num_suite(cards):
    '''

    :param cards:
    :return:
    '''
    number = []
    suite = []
    for card in cards:
        if card[0] == 'T':
            number.append(10)
        elif card[0] == 'J':
            number.append(11)
        elif card[0] == 'Q':
            number.append(12)
        elif card[0] == 'K':
            number.append(13)
        elif card[0] == 'A':
            number.append(14)
        else:
            number.append(int(card[0]))
        suite.append(card[1])
    return number, suite


def rank(cards):
    '''

    :param cards:
    :return:
    '''
    number, suite = create_num_suite(cards)
    suite_set = set(suite)
    # Same Suite
    if len(suite_set) == 1:
        # Royal Flush
        if check_increasing(number) == 'royal':
            return 10
        # Straight Flush
        elif check_increasing(number) == 'straight':
            return 9
        # Flush
        else:
            return 6
    # Straight
    elif len(suite_set) > 1 and check_increasing(number) == 'straight':
        return 5
    else:
        number_list = convert_numbers_to_list(number)
        if max(number_list) == 4:
            return 8
        elif max(number_list) == 3:
            if len(number_list) == 2:
                return 7
            else:
                return 4
        elif max(number_list) == 2:
            if len(number_list) == 3:
                return 3
            else:
                return 2
        elif max(number_list) == 1:
            return 1


def get_pair(number):
    '''

    :param number:
    :return:
    '''
    for j in range(len(number) - 1):
        for i in range(j + 1, len(number)):
            if number[j] == number[i]:
                return number[j]


def get_2_pair(number):
    '''

    :param number:
    :return:
    '''
    pair1 = get_pair(number)
    number = list(filter(lambda item: item != pair1, number))
    pair2 = get_pair(number)
    return max(pair1, pair2), min(pair1, pair2), number


# only used for cases like 22233 or 22234 (with 1 triplet)
def get_triplet(number):
    '''

    :param number:
    :return:
    '''
    ret = get_pair(number)
    number.remove(ret)
    number.remove(ret)
    if ret in number:
        return ret, 0
    else:
        return number[0], ret


def high_pair(cards1, cards2, eq_rank):
    '''

    :param cards1:
    :param cards2:
    :param eq_rank:
    :return:
    '''
    # 8,7,4,3,2
    number1, suite1 = create_num_suite(cards1)
    number2, suite2 = create_num_suite(cards2)
    if eq_rank == 2:
        pair1 = get_pair(number1)
        pair2 = get_pair(number2)
        if pair1 > pair2:
            return 1
        elif pair2 > pair1:
            return 2
        else:
            number1 = list(filter(lambda item: item != pair1, number1))
            number2 = list(filter(lambda item: item != pair2, number2))
            return high_card(number1, number2, 2)
    elif eq_rank == 3:
        pair1_1, pair1_2, number1 = get_2_pair(number1)
        pair2_1, pair2_2, number2 = get_2_pair(number2)
        if pair1_1 > pair2_1:
            return 1
        elif pair2_1 > pair1_1:
            return 2
        elif pair1_2 > pair2_2:
            return 1
        elif pair2_2 > pair1_2:
            return 2
        else:
            number1 = list(filter(lambda item: item != pair1_2, number1))
            number2 = list(filter(lambda item: item != pair2_2, number1))
            return high_card(number1, number2, eq_rank)
    elif eq_rank == 4:
        triplet1, tmp1 = get_triplet(number1)
        triplet2, tmp2 = get_triplet(number2)
        if triplet1 > triplet2:
            return 1
        elif triplet2 > triplet1:
            return 2
        else:
            number1 = list(filter(lambda item: item != triplet1, number1))
            number2 = list(filter(lambda item: item != triplet2, number2))
            return high_card(number1, number2, eq_rank)
    elif eq_rank == 7:
        triplet1, pair1 = get_triplet(number1)
        triplet2, pair2 = get_triplet(number2)
        if triplet1 > triplet2:
            return 1
        elif triplet2 > triplet1:
            return 2
        elif pair1 > pair2:
            return 1
        else:
            return 2
    elif eq_rank == 8:
        pair1 = get_pair(number1)
        pair2 = get_pair(number2)
        if pair1 > pair2:
            return 1
        elif pair2 > pair1:
            return 2
        else:
            number1 = list(filter(lambda item: item != pair1, number1))
            number2 = list(filter(lambda item: item != pair2, number2))
            return high_card(number1, number2, 8)

    return 0


def high_card(number1, number2, eq_rank):
    '''

    :param number1:
    :param number2:
    :param eq_rank:
    :return:
    '''
    # 9,6,5,1
    if number1 and number2:
        max1 = max(number1)
        max2 = max(number2)
        if max1 > max2:
            return 1
        elif max1 < max2:
            return 2
        else:
            number1.remove(max1)
            number2.remove(max1)
            return high_card(number1, number2, eq_rank)
    else:
        return 0


def decide_winner(cards1, cards2):
    '''

    :param cards1:
    :param cards2:
    :return:
    '''
    rank1 = rank(cards1)
    rank2 = rank(cards2)
    if rank1 > rank2:
        return 1
    elif rank2 > rank1:
        return 2
    elif rank1 in [1, 5, 6, 9]:
        number1, suite1 = create_num_suite(cards1)
        number2, suite2 = create_num_suite(cards2)
        return high_card(number1, number2, rank1)
    elif rank1 in [2, 3, 4, 7, 8]:
        return high_pair(cards1, cards2, rank1)
    else:
        return 0


if __name__ == '__main__':
    count1 = 0
    count2 = 0
    for line in fileinput.input():
        line = line.split()
        player1_cards = line[:5]
        player2_cards = line[5:]
        winner = decide_winner(player1_cards, player2_cards)
        if winner == 1:
            count1 += 1
        elif winner == 2:
            count2 += 1
    print("Player 1:", count1)
    print("Player 2:", count2)
