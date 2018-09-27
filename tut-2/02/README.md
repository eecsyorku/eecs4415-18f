# Example 2: Word Frequency (Tutorial 2)

A Python program (use Python 3) to find the top ten words in an input stream
by number of occurrences and to make a bar-chart plot and CSV output of them.
Reads `book.txt` as input (downloaded from [Dracula by Bram Stoker][1] on The
Project Gutenberg website).

Eliminate stopwords — the very common words in English — and words just one
character long as not being interesting. When tokenizing, split with `[\W+_]`
(This splits on whitespace and underscores `_`). We won't worry about
preserving words with apostrophes for now (e.g., “won't”). If we were to
extend our program to be more robust and useful later, we surely would improve
on our tokenizer, or find a good library for it. Use the file `stopwords.txt`
for stopwords. Our program can read in the file and make a `stopword` dictionary
to use to check against to eliminate the stopwords as we are parsing the input
stream.

Based on last year's [Project 1][2] by Professor [Parke Godfrey][3].

## Demonstrates

- Reading and parsing text files into words
- Multiple Python files
- Plotting bar graphs with matplotlib
- Writing to a CSV file

## Usage:

- Start Python Docker container with volume mounted
- Run `./start.sh` to install the python library dependencies
- Run `python src/main.py`
- Output graph and CSV should be found in the `outputs/` directory.

```
$ docker run -it –v $PWD:/usr/src/app –w /usr/src/app python bash
root:/usr/src/app# ls -la
root:/usr/src/app# ./start.sh
root:/usr/src/app# python src/main.py
root:/usr/src/app# ls -la outputs/
```

[1]: https://www.gutenberg.org/ebooks/345
[2]: https://www.eecs.yorku.ca/course_archive/2017-18/F/4415/project/zipf/
[3]: https://www.eecs.yorku.ca/~godfrey/
