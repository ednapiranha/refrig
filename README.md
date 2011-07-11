# Refrig (refridge)

A basic tumblelog/bookmarking application built in Django and MongoDB


## Installation

Change into the project directory and install the required libraries:

>> cd refrig
>> pip install -r requirements.txt

*Note: nltk will not install properly in virtualenv. I got around this by download the tar file and running pip in nltk's directory where setup.py is located.

Download the nltk resources:

>> python
>> import nltk
>> nltk.downlad()