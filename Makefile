run:
	python3 examples.py

install: glove.840B.300d.txt SBW-vectors-300-min5.txt
	python3 -m pip install numpy scipy pandas tqdm

glove.840B.300d.txt:
	# Download from Stanford NLP GloVe page (Pennington et al.)
	wget https://nlp.stanford.edu/data/glove.840B.300d.zip
	unzip glove.840B.300d.zip && rm glove.840B.300d.zip
	mv glove.840B.300d.txt model/glove.840B.300d.txt

SBW-vectors-300-min5.txt:
	wget https://cs.famaf.unc.edu.ar/~ccardellino/SBWCE/SBW-vectors-300-min5.txt.bz2
	bzip2 -d SBW-vectors-300-min5.txt.bz2
	mv SBW-vectors-300-min5.txt model/SBW-vectors-300-min5.txt
	

.PHONY: run
.PHONY: install