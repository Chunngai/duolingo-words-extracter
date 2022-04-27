# duolingo-words-extracter
This repo contains code that extracts new words from each lesson in Duolingo.

## Intro
When we are learning a language in the [Duolingo website](https://www.duolingo.cn/), 
we can access the [word list](https://www.duolingo.cn/words) (MORE → Words on the navi bar) 
that contains all words we've learned. 
However, words of each lesson are mixed together, 
and it's hard to figure out which lesson each word belongs to.  
&ensp;&ensp;This repo is for extracting new words of a specific lesson in Duolingo.
It's partially automatic and manual efforts are still needed.

## New Words Extraction
The primary aim of the repo is to extract the words of a newly learnt lesson.
The logic is that when a new lesson is learnt, the length of the word list
in Duolingo will increase.  
&ensp;&ensp;Note that some words will not appear in the Duolingo word list in level 1 
of a certain lesson, but will appear in higher levels. Those words can be discovered using
the method of **Extracting Words of Previously Learnt Lessons** described below.

### Step 1. Preparing for a .xlsx Log File

### Step 2. New Words Extraction

## Extracting Words of Previously Learnt Lessons
You may have learnt some lessons on Duolingo before using this repo and do not know
the words belonging to each lesson previously learnt. But it's ok. 
This repo also suggests extracting words of previously learnt lessons.
The logic is that when a learnt lesson is reviewed, the length of the word list in Duolingo
will not change, but some words will become "Just now" in the "Last practice" column of the
Duolingo word list. And those words contain the words belonging to that reviewed lesson.  
&ensp;&ensp;Note that 
this function requires you to review all the previously learnt lessons, starting from the 
FIRST lesson. And also note that the extraction should be done 
right after a certain previously learnt lesson is reviewed (practiced).

## Spanish Words of Each Lesson in Duolingo
This repo also provides the words of each lesson in the Duolingo Spanish course (`duolingo_espanol.xlsx`). 
It's still on progress.