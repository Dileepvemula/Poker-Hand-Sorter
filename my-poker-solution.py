import fileinput


def check_increasing(numbers):
    """
    Checks if list numbers is strictly increasing or not and returns type of flush or straight
    :param numbers: <list>
        integers in range 2 to 14 (inclusive)
    :return: str
        'not_strict_increasing' if numbers are not strictly increasing by 1, can be stored in any order
        'royal' if list constitutes [10,11,12,13,14] in any order
        'straight' if list elements are strictly increasing by 1, stored in any order
    """
    numbers.sort()
    for i in range(1, 5):
        if numbers[i] != numbers[0] + i:
            return 'not_strict_increasing'
    if numbers[0] == 10:
        return 'royal'
    else:
        return 'straight'


def count_each_number(numbers):
    """
    Calculates occurrences of each element[2 to 14] and returns occurrences of non zero cards
    :param numbers: <list>
        integers in range 2 to 14 (inclusive)
    :return: ret <list>
        number of non zero occurrences of all elements
    """
    ret = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for item in numbers:
        ret[item - 2] += 1
    while 0 in ret:
        ret.remove(0)
    return ret


def create_num_suite(cards):
    """
    Each card in cards list is changed to separate numbers and suites list.
    :param cards: <list>
        cards of each player with number and suite
    :return: number, suite : <list> <list>
        numbers, suite separated from each cards element
    """
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
    """
    calculates and returns rank of cards list
    :param cards: <list>
        cards of each player with number and suite
    :return: int
        rank of each cards list
    """
    number, suite = create_num_suite(cards)
    suite_set = set(suite)
    # checking if all cards are of Same Suite
    if len(suite_set) == 1:
        # Checking Royal Flush
        if check_increasing(number) == 'royal':
            return 10
        # checking Straight Flush
        elif check_increasing(number) == 'straight':
            return 9
        # Flush
        else:
            return 6
    # checking if cards not of same suite and strictly increasing (Straight)
    elif len(suite_set) > 1 and check_increasing(number) == 'straight':
        return 5
    else:
        # Grouping cards by numbers
        number_list = count_each_number(number)
        # Checking if grouped cards are of 4-1 Group (Four of a kind)
        if max(number_list) == 4:
            return 8
        # Checking if grouped cards are of 3 Group (3-2 or 3-1-1)
        elif max(number_list) == 3:
            # Checking 3-2 Group (Full House)
            if len(number_list) == 2:
                return 7
            # Checking 3-1-1 Group (Three of a kind)
            else:
                return 4
        # Checking if grouped cards are of 2 Group (2-2-1 or 2-1-1-1)
        elif max(number_list) == 2:
            # Checking 2-2-1 Group (Two pairs)
            if len(number_list) == 3:
                return 3
            #Checking 2-1-1-1 Group (Pair)
            else:
                return 2
        # Checking 5 distinct numbers in cards (High Card)
        elif max(number_list) == 1:
            return 1


def get_pair(number):
    """
    Returns element if it exists twice in number list
    :param number: <list>
        number list from cards of player with at least 1 element repeating
    :return: int
        number which exist twice in the list
    """
    for j in range(len(number) - 1):
        for i in range(j + 1, len(number)):
            if number[j] == number[i]:
                return number[j]


def get_2_pair(number):
    """
    Calculates 2 pairs present in the list and returns max and min of the 2 pairs and remaining element
    :param number: <list>
        number list from cards of player with at least 2 elements repeating
    :return: int, int, int
        max, min of pair elements and the remaining element of number list
    """
    # get first pair element
    pair1 = get_pair(number)
    #remove all occurrences of pair element from list
    number = list(filter(lambda item: item != pair1, number))
    # get second pair element
    pair2 = get_pair(number)
    return max(pair1, pair2), min(pair1, pair2), number


# only used for cases like 22233 or 22234 (with 1 triplet)
def get_triplet(number):
    """
    Finds element that is occurs 3 times in number list and returns it along with a pair element if exists
    :param number: <list>
        number list from cards of player with at least 1 triplet(either 3-2 or 3-1-1 groups)
    :return: int, int
        triplet number, pair number if pair exists (3-2)
        triplet number, 0 if pair does not exist (3-1-1)
    """
    ret = get_pair(number)
    number.remove(ret)
    number.remove(ret)
    if ret in number:
        return ret, 0
    else:
        return number[0], ret


def compute_high_pair_2_pair(number1, number2):
    """
    Compares high pairs of pairs, quadruple and returns high player number
    :param number1: <list>
        number list from cards of player1 with at least 2 pairs(2-2-1 or 4-1)
    :param number2: <list>
        number list from cards of player2 with at least 2 pairs(2-2-1 or 4-1)\
    :return: int
        returns player number whose pair of cards or quadruple is higher . If they are same, comparison moves to next element
    """
    pair1 = get_pair(number1)
    pair2 = get_pair(number2)
    if pair1 > pair2:
        return 1
    elif pair2 > pair1:
        return 2
    else:
        # Removes all occurrences of pair1, pair2
        number1 = list(filter(lambda item: item != pair1, number1))
        number2 = list(filter(lambda item: item != pair2, number2))
        return high_card(number1, number2)


def high_pair(cards1, cards2, eq_rank):
    """
    calculates the player with high pair of cards, if a pair is equal, calculates the next high pair.
    Also calculates the player with high triplet or quadruple.
    :param cards1: <list>
        Cards of player1 with number and suite
    :param cards2: <list>
        Cards of player2 with number and suite
    :param eq_rank: int
        rank of each player's cards (same in this case)
    :return: int
        returns player with high pair/ triplet/ quadruple
        0 if all cards' numbers are same for players (Exceptional case) and if both cards are royal flush
    """
    number1, suite1 = create_num_suite(cards1)
    number2, suite2 = create_num_suite(cards2)
    # if both cards are of rank 2 (pair)
    if eq_rank == 2:
        return compute_high_pair_2_pair(number1, number2)
    elif eq_rank == 3:
        # if both cards are of rank 3 (2 pairs)
        pair1_1, pair1_2, number1 = get_2_pair(number1)
        pair2_1, pair2_2, number2 = get_2_pair(number2)
        # comparing 1st pair
        if pair1_1 > pair2_1:
            return 1
        elif pair2_1 > pair1_1:
            return 2
        # comparing 2nd pair
        elif pair1_2 > pair2_2:
            return 1
        elif pair2_2 > pair1_2:
            return 2
        # comparing last element
        else:
            number1 = list(filter(lambda item: item != pair1_2, number1))
            number2 = list(filter(lambda item: item != pair2_2, number1))
            return high_card(number1, number2)
    # if both cards are of rank 4 (3 of a kind)
    elif eq_rank == 4:
        triplet1, tmp1 = get_triplet(number1)
        triplet2, tmp2 = get_triplet(number2)
        if triplet1 > triplet2:
            return 1
        elif triplet2 > triplet1:
            return 2
        # computing high card after removing triplet
        else:
            number1 = list(filter(lambda item: item != triplet1, number1))
            number2 = list(filter(lambda item: item != triplet2, number2))
            return high_card(number1, number2)
    # if both cards are of rank 7 (Full House 3-2)
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
    # if both cards are of rank 8 (4 of a kind 4-1)
    elif eq_rank == 8:
        return compute_high_pair_2_pair(number1, number2)
    # if all cards are of same number, no player is winner
    return 0


def high_card(number1, number2):
    """
    calculates high card in both lists. If same, moves to next max card comparison. Returns high player number
    :param number1: <list>
        list of player1's unique card numbers (no groups)
    :param number2: <list>
        list of player2's unique card numbers (no groups)
    :return: int
        player number who has high card (if number not null)
        0 if number list is empty (no cards present)
    """
    # checking number1, number2 are not null
    if number1 and number2:
        max1 = max(number1)
        max2 = max(number2)
        if max1 > max2:
            return 1
        elif max1 < max2:
            return 2
        # if max card in both lists equal, compare next max card
        else:
            number1.remove(max1)
            number2.remove(max1)
            # if max card is equal, compare next max card
            return high_card(number1, number2)
    else:
        # if lists empty, no player is winner, so return 0
        return 0


def decide_winner(cards1, cards2):
    """
    compares rank of both cards list and returns max rank player. If rank is equal, compares
    high pair or card and returns high player number. If both ranks are 10(royal flush),
    no player is winner
    :param cards1: <list>
        Cards of player1 with number and suite
    :param cards2: <list>
        Cards of player2 with number and suite
    :return: int
        0: if both rank == 10 (royal flush)
        winner player number based on rank and/or high card/ high rank
    """
    rank1 = rank(cards1)
    rank2 = rank(cards2)
    if rank1 > rank2:
        return 1
    elif rank2 > rank1:
        return 2
    # if a pair/ 2 pairs/ triplet/ quadruple does not exist
    elif rank1 in [1, 5, 6, 9]:
        number1, suite1 = create_num_suite(cards1)
        number2, suite2 = create_num_suite(cards2)
        return high_card(number1, number2)
    # if a pair/ 2 pairs/ triplet/ quadruple exists
    elif rank1 in [2, 3, 4, 7, 8]:
        return high_pair(cards1, cards2, rank1)
    # ranks equal to 10 (royal flush)
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
