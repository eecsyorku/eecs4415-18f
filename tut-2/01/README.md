# Example 1: Basic Python and CSVs (Tutorial 2)

## Demonstrates

- Running Python scripts in Docker
- Reading and parsing STDIN into words
- Reading and writing CSV files
- Printing output to the terminal

## Usage

- Start Python Docker container with volume mounted
- Run each of the python scripts in the directory to observe the output

```
$ docker run -it –v $PWD:/usr/src/app –w /usr/src/app python bash
root:/usr/src/app# ls -la
root:/usr/src/app# python readstdin.py < inputs/input.txt
root:/usr/src/app# python readstdin.py < inputs/input.csv
root:/usr/src/app# python readtxt.py
root:/usr/src/app# python readcsv.py
```
