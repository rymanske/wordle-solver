import sys

GRAY = u"\u001b[1;37;100m {} \u001b[0m"
GREEN = u"\u001b[1;37;42m {} \u001b[0m"
YELLOW = u"\u001b[1;37;43m {} \u001b[0m"

MAX_GUESSES = 10


def main():
    words_file = sys.argv[1]
    target = sys.argv[2]

    if len(target) != 5:
        print('Word must be five letters long!')
        exit(1)

    words_list_unsorted = []

    with open(words_file) as f:
        for line in f:
            words_list_unsorted.append(line.strip())

    word_list = rank_words(words_list_unsorted)

    if target not in word_list:
        print('Word not found in dictionary!')
        return

    match = {}
    move = set()
    bad = {}

    guess = word_list[0]

    guesses = set()

    # Start guessing
    for guess_num in range(1, MAX_GUESSES + 1):
        for g, t, i in zip(guess, target, range(5)):
            if g == t:
                match[i] = g
                if g in move:
                    move.remove(g)
            elif g in target:
                move.add(g)
                if g in bad:
                    bad[g].add(i)
                else:
                    bad[g] = {i}
            else:
                # this letter is bad at all positions
                bad[g] = set(range(5))

        # keep track of guesses
        guesses.add(guess)

        # construct print output
        guess_print = ''

        for g, t in zip(guess, target):
            if g == t:
                guess_print += GREEN.format(g.upper())
            elif g in target:
                guess_print += YELLOW.format(g.upper())
            else:
                guess_print += GRAY.format(g.upper())

        print(guess_print)

        # debug
        # print('\tmatch:', match)
        # print('\tmove:', move)
        # print('\tbad:', bad)

        if guess == target:
            print('Found solution in', guess_num, 'guesses')
            return

        # Rerank words
        word_list = rank_words(word_list, match, move, bad)

        # choose next word
        for word in word_list:
            # don't guess the same word again
            if word in guesses:
                continue
            else:
                guess = word
                break
    else:
        print('No solution found!')


def rank_words(word_list, match={}, move=set(), bad={}):
    # filter words
    filtered_word_list = []

    for word in word_list:
        for c, i in zip(word, range(5)):
            if c in bad:
                if i in bad[c]:
                    break
        else:
            filtered_word_list.append(word)

    letter_rank = rank_letters(filtered_word_list, match, move, bad)

    # rank words
    word_rank = {}

    for word in filtered_word_list:
        score = 0

        seen_letters = set()
        for c, i in zip(word, range(5)):
            letter_scale = 1

            if c in seen_letters:
                letter_scale = 0
            else:
                seen_letters.add(c)

            score += (letter_rank[(c, i)] * letter_scale)

        word_scale = 1

        # if (len(match) + len(move)) < 4:
        #     if len(match.keys() & set(word)) > 0:
        #         word_scale = 0.25
        #     elif len(move & set(word)) > 0:
        #         word_scale = 0.5

        word_rank[word] = (score * word_scale)

    return [w[0] for w in sorted(word_rank.items(), key=lambda item: item[1], reverse=True)]


def rank_letters(word_list, match={}, move=set(), bad={}):
    # count leters
    letter_counts = {}

    for word in word_list:
        for c in word:
            if c not in letter_counts:
                letter_counts[c] = 1
            elif c in bad:
                letter_counts[c] = 0
            else:
                letter_counts[c] += 1

    # rank words
    letter_rank = {}

    for c, score in sorted(letter_counts.items(), key=lambda item: item[1], reverse=True):
        for i in range(5):
            scale_factor = 1
            if (i in match) and (match[i] == c):
                if len(match) + len(move) < 4:
                    scale_factor = 0
                else:
                    scale_factor = len(match) / 2
            elif c in match.values():
                scale_factor = 0
            elif c in move:
                scale_factor = 0.25

            letter_rank[(c, i)] = (score * scale_factor)
    return letter_rank


if __name__ == '__main__':
    main()
