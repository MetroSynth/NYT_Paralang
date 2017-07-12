# NYT PARALANG #

## PREMISE ##
In trying to learn written Chinese, a great way to learn is by picking out useful vocabulary words in articles, books, etc.
This tool attempts to parse a block of Chinese language text and spit out a sequential list of the longest character combinations found.
The resultant output will be essentially a ready-made vocabulary list of all words found in the text, along with their pinyin pronunciation and definition

## USAGE ##
* Module simply takes a URL
* Outputs each sentence one by one, a list of all vocab words that sentence contains will be shown below


## TODO ##
* Ensure parser is picking out entire words and not just outputting definitions for each individual component character
* Add functionality so that once a definition is found it is not repeated again. The source text is shown, but without that definition
