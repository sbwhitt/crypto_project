Usage:
    Within downloaded project folder
    Run init.sh to set up executable
    Call main executable from command line:
        ./dist/main
    Optional: Provide cipher text file on command line:
        ./dist/main cipher.txt

Commands:
    help    Displays help info
    m       Display current matrix
    t       Display current matrix plaintext
    n       Change to next permutation of key and display new matrix
    k       Changes current key size
    kf      Changes current key to inputted key (comma separated list)
    b       Brute force attack for single key size or key size range (comma separated range)
    h       Hill Climb attack for single key size or key size range (comma separated range)
    q       Quit program

Settings:
    settings.py contains parameters for Hill Climb attack.
    HC_SINGLE_RESULT_AMNT: Number of promising candidates a single key Hill Climb attack will return
        Default value is 25
    HC_RANGE_RESULT_AMNT: Number of promising candidates a key range Hill Climb attack will return
        Default value is 10
    HC_SINGLE_WAIT_AMNT: Number of candidates that will be tried between promising candidates before resetting search
        for a single key Hill Climb attack
        Default value is 1000
    HC_RANGE_WAIT_AMNT: Number of candidates that will be tried between promising candidates before resetting search
        for a key range Hill Climb attack
        Default value is 1000

Classes:
    main.py:
        Main driver file. Accepts user input and organizes attack outputs.
    matrix.py:
        Represents the columnar transposition matrix.
    candidate.py:
        Represents a matrix for a specific key. Holds the candidate weight and words found in candidate plaintext.
    attacks.py:
        Holds the cipher attack code. Also holds dictionaries of words used for lookup.
        Brute force attack cycles through all keys for a given key size and returns the highest weighted candidate.
        Hill climb attack starts with randomized key for given key size and gradually shifts it until higher weighted candidate is
            found. If the loop fails to find a better candidate after the specified amount of wait trials, it appends the current
            candidate to its return array and starts over with a new randomized key.

Misc Technical Details:
    Candidate weights are calculated by averaging the length of all words found within the candidate plaintext. If a frequent
        word file is provided, these words are weighted more.
    Candidate words found by splitting candidate plaintext into ngrams and searching them against an nltk corpus. The default ngram
        values are 3 to 10 inclusive. All words that are discovered are lemmatized and treated as unique.
    Hill climb entropy is a measure of how much a current candidate key is altered each iteration. Entropy increases based on how far
        the current candidates weight is from the highest weighted candidate so far.
    Project was built using pyinstaller: https://www.pyinstaller.org/
