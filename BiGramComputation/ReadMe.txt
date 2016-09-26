main.py :  Version 1.0 09/25/2016

General Usage Notes
-------------------

-The program supports Python 2.7

Program Description
-------------------
An automatic speech recognition system has provided two written sentences as possible interpretations to a speech input. 
S1: The president has relinquished his control of the company's board. 
S2: The chief executive officer said the last year revenue was good. 
Using the bigram language model trained on Corpus A, this program is used to compute the BiGram probability of each of the two sentences under the three following scenarios: 
i. Use the bigram model without smoothing.
ii. Use the bigram model with add-one smoothing 
iii. Use the bigram model with Good-Turing discounting


To run the program 
-------------------

In the terminal, enter the following commands:

pip install pandas
python main.py

Observation:
------------

After running the program, 
the total probability of the statement one s1 with add-one smoothing model gives a higher probability when compared to s2. Hence, we can say that s1 is more probable than s2.