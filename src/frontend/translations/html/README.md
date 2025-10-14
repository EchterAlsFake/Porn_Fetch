# Why?
QTextBrowser uses html to style the texts e.g., bolder test, different font sizes and 
colors. The problem is, that when I make these text translateable, QLinguist and Crowdin 
pick the HTML source code and think that you as the translator need to translate this
too which is of course not the case. The solution is to embed this as HTML, because
crowdin can automatically strip that out when the files are uploaded as .html. 

