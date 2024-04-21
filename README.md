# Divergent Association Task code (revised)

The DAT measures creativity in under 4 minutes. It involves thinking of 10
unrelated words. Creative people choose words with greater semantic distances
between them.

## Installation

First, make sure you have python installed

Then, there are two ways to set up:

First way: `$ make install` 

Second way: Run the following commands

```
# install python packages
$ python3 -m pip install numpy scipy pandas tqdm

# install English glove model
$ wget https://nlp.stanford.edu/data/glove.840B.300d.zip
$ unzip glove.840B.300d.zip && rm glove.840B.300d.zip
$ mv glove.840B.300d.txt model/glove.840B.300d.txt

# install English glove model
$ wget https://cs.famaf.unc.edu.ar/~ccardellino/SBWCE/SBW-vectors-300-min5.txt.bz2
$ bzip2 -d SBW-vectors-300-min5.txt.bz2
$ mv SBW-vectors-300-min5.txt model/SBW-vectors-300-min5.txt
```

## Run the program

`python3 -m examples.py`











## Credits


Adapted from [Jay Olson](https://www.jayolson.org) at Harvard University. 
[Naming unrelated words predicts creativity](https://www.pnas.org/content/118/25/e2022340118)


## Online version

Try the task and see your score at
[datcreativity.com](https://www.datcreativity.com).

The dictionary (words.txt) is based on [Hunspell](https://hunspell.github.io)
by László Németh.


## License

MIT
