# Stastitical Mimicry
Reads a large body of text, learns patterns of speech, and attempts to produce new text that sounds similar to the speech that it learned. Results are often comical. Check out and run `example_application.py` to see what it's all about!

## How it Works
The mimicry works by
1. Breaking a large body of text up into all the groups of `n` words found in it. For `n=3`...

  `"This is a decently long sentence. This is a shorter one."`

  Becomes

  ```python
[
['This',     'is',       'a'],
['is',       'a',        'decently'],
['a',        'decently', 'long'],
['decently', 'long',     'sentence'],
['long',     'sentence', '.'],
['sentence', '.',        'This'],
['.',        'This',     'is']
['This',     'is',       'a'],
['is',       'a',        'shorter'],
['a',        'shorter',  'one'],
['shorter',  'one',      '.']
]
  ```
  (Notice we treat punctuation as it's own word. Helps to pull even more information out of the text body)

2. Counting how frequently each group of words occurs. In the above Example, `This is a` seems to appear twice, while all other three word groups occur once.
  ```python
  {
  'This is a'      : 2, #This group occurs two times
  'is a decently'  : 1, #All other groups occur once
  'a decently long': 1,
          '...'          #I'm too lazy to type all that again (:
  'shorter one .'  : 1
   }
  ```
3. Picking a random starting group as a starting seed, and "building" a sentence off of it. We "build" Let's say we use `This is a` as our starting group. We would then build sentences by:
  1. Looking at the last half of that seed group, in our case the last half is `is a`
  2. Picking another group that starts with `is a`, and tacking that on to the end...We pick this next group "randomly," but we try to follow the distribution we calculated in step two. Since we have two options `is a decent` and `is a shorter`, and both occur the same number of times, (once), there's a 50% chance that our generator will tack on either option. Let's just SUPPOSE `is a decent` occurs 3 times, and `is a shorter` occurred once. THEN, there'd be a 75% chance that `is a decent` will be tacked on, and a 25% chance that `is a shorter` will be tacked on.
  3. Repeating steps 1 (for our most recent group, at the end of the sentence!) and 2, until we've tacked on multiple sentences worth of groups, and generated "new" speech!

## Useful Endpoints

* `mimic(file_name, sentences_to_produce, group_length=5)`  - returns a single string of sentences.
  * `file_name` is the name of the text file that contains a substantial amount of text. The program will attempt to mimic its patterns of speech.
  * `sentences_to_produce` is how many 'sentences' long the output will be. Guessing what is, and isn't a sentence is more of an art than a science...so take results with a grain of salt!
  * `group_length` determines how 'coherent' the output sounds. The longer the group length, the better sounding the output...however...as group length gets longer, thing's start to sound unoriginal real quick, if the text file the program is learning from doesn't contain enough information!
