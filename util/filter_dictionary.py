import sys


def main():
    input = sys.argv[1]

    with open(input) as input_file:
        for line in input_file.readlines():
            word = line.strip()

            if word[0].isupper():
                continue

            if len(word) == 5:
                print(word)


if __name__ == '__main__':
    main()
