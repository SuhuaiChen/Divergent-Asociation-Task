# Divergent Thinking Experiment  

Divergent thinking is a key component of creativity, allowing individuals to generate multiple solutions to a problem. This experiment involves two tasks designed to assess divergent thinking: **Forward Flow** and **Alternative Use**.  

---

## Experiment Procedure  

### 🔹 Task 1: Forward Flow  
**Objective:**  
To measure how fluidly participants generate a continuous stream of related ideas.  

**Procedure:**  
1. **Stimulus Presentation:** Participants are given a starting word (e.g., "ocean").  
2. **Idea Generation:** They must generate a sequence of words related to the previous word they mentioned (e.g., "ocean → waves → beach → vacation").  
3. **Time Constraint:** They are given a fixed time (e.g., **60 seconds**) to produce as many words as possible.  
4. **Recording & Scoring:**  
   - The number of words generated is recorded.  
   - The semantic distance between consecutive words may be analyzed to assess creativity.  

**Example Response:**  
**Stimulus Word:** *Tree*  
**Generated Words:** "Tree → Forest → Animals → Ecosystem → Climate → Change"  

---

### 🔹 Task 2: Alternative Use  
**Objective:**  
To assess flexibility in thinking by identifying multiple, unconventional uses for a common object.  

**Procedure:**  
1. **Stimulus Presentation:** Participants are given an everyday object (e.g., a brick, paperclip, spoon).  
2. **Idea Generation:** They must list as many alternative uses as possible within a fixed time (e.g., **90 seconds**).  
3. **Encouragement of Creativity:** There are no right or wrong answers—unusual and novel responses are encouraged.  
4. **Recording & Scoring:**  
   - **Fluency:** Total number of alternative uses generated.  
   - **Flexibility:** The variety of categories covered in responses.  
   - **Originality:** How unique the ideas are compared to others.  

**Example Responses for a "Brick":**  
- **Paperweight**  
- **Doorstop**  
- **Self-defense tool**  
- **DIY flower pot**  
- **Art sculpture base**  

---

## ⚙️ Installation  

Before conducting the experiment, ensure **Python** is installed on your system. If not, download it from [Python.org](https://www.python.org/).  

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

## Extended Work (updated Feb 18, 2025)
I have developed more sophisticated models for the Alternative Uses Task.
- [Bilingual AUT](https://colab.research.google.com/drive/1e38KxvIXqv11Q61bZnclyPRlnMyKlMOJ)
- [Bilingual AUT LLM](https://colab.research.google.com/drive/11UgMBS4zX4lY2ta-b6ORsVCAaKVp04Is#scrollTo=dGkrnFlLbcyC)
- [AUT Analysis](https://colab.research.google.com/drive/1ECgmLWCzGiiVphUU3rOQmCxqDQxFRda3#scrollTo=LhjPnAbqRPkw)

## Credits
Adapted from [Jay Olson](https://www.jayolson.org) at Harvard University. 
[Naming unrelated words predicts creativity](https://www.pnas.org/content/118/25/e2022340118)

The dictionary (words.txt) is based on [Hunspell](https://hunspell.github.io)
by László Németh.

## License
MIT