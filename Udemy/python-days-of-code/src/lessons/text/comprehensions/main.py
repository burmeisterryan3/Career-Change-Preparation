import pandas as pd


def gen_phonetic(df):
    """Generate the phonetic representation of the user input."""
    user_word = input("Enter a word: ").upper()

    try:
        phonetic_pronunciation = [phonetic_map[letter] for letter in user_word]
    except KeyError:
        print("Sorry, only letters in the alphabet please.")
        gen_phonetic(df)
    else:
        print(phonetic_pronunciation)


if __name__ == "__main__":
    df = pd.read_csv(
        "./days_of_code/lessons/text/comprehensions/nato_phonetic_alphabet.csv"
    )

    phonetic_map = {row["letter"]: row["code"] for (_, row) in df.iterrows()}
    gen_phonetic(df)
