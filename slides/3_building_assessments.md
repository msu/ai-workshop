---
defaults:
  layout: two-cols
mdc: true
fonts:
  mono: Cascadia Mono
  sans: Atkinson Hyperlegible
layout: cover
---

# Building Assessments
## Quizzes, keys, and study guides from your notes

---

## Assessment in the AI Era

* Take-home work is no longer a reliable signal
* In-person, written-response quizzes move the signal back in the room
* One handwritten page of notes, no devices

::right::

```
  every ~3 weeks:
    in-person quiz
    written responses
    1 page handwritten notes
    no laptops, no phones
```

---

## The Quiz Pipeline

* One prompt produces the quiz, the answer key, and the study guide
* Each lands as markdown, then a print-ready PDF
* Format rules live in CLAUDE.md

::right::

```
  meta/quizzes/spring-2026/quiz3/
    3_memory_quiz.md
    3_memory_quiz.pdf
    3_memory_answer_key.md
    3_memory_answer_key.pdf
    3_memory_study_guide.md
    3_memory_study_guide.pdf
```

---

## From Notes to Quiz

* The agent builds questions from the lecture notes you taught
* Questions track the material, so prep is the study guide
* You edit wording and difficulty before it prints

::right::

```
  > generate quiz 3 from the
    memory and pointers lectures,
    5 questions, follow the quiz
    rules in CLAUDE.md
```

---

## Answer Keys and Rubrics

* The key carries a grading rubric for the TA
* Points are fixed; partial-credit guidance is spelled out
* Grading stays consistent across graders

::right::

```markdown
### Q3: Stack vs Heap

Stack: automatic, LIFO, freed on
return. Heap: manual, malloc/free.

*Grading: 10 full. 7 if lifetime
is vague. 5 for any real effort.*
```

---

## Study Guides

* A short list of topics, no answers given away
* Students get it ahead of the quiz
* Same source notes, different view

::right::

```markdown
# Quiz 3 Study Guide

* Stack frames and lifetime
* Heap allocation with malloc
* Pointer arithmetic
* Dangling pointers
```

---

## Print-Ready PDFs

* `\newpage` after each question leaves room to write
* pandoc turns the markdown into a printable PDF
* No styling fuss -- the questions are the point

::right::

```bash
  pandoc 3_memory_quiz.md \
    -o 3_memory_quiz.pdf
```

---

## The Lecture Review Loop

* After lecture, download the recording transcript
* `/review-lecture` compares the transcript to the slides
* Output: timing, coverage gaps, and proposed slide fixes

::right::

```
  deliver  -> transcript
  transcript + slides
           -> /review-lecture
           -> gaps + fixes
           -> revise slides
```

---

## Generating Assignments

* Draft assignment specs and starter code from a description
* The agent can build a sample system you stub out for students
* You own the spec; it handles the boilerplate

::right::

```
  > write an assignment spec for
    a malloc implementation, plus
    a test skeleton students fill
    in
```

---

## DEMO: Notes to Quiz

<!-- Demo: generate a quiz + answer key from a lecture's notes, show the rubric -->

* Generate a quiz and answer key from one lecture's notes
* Show the rubric the TA will grade against
* Render the PDF and show the per-question page breaks

---
layout: default
---

## Summary

* Take-home work is a weak signal; in-person written quizzes are stronger
* One prompt yields the quiz, the answer key, and the study guide
* Questions are built from the notes you actually taught
* Answer keys carry a rubric so grading stays consistent
* Study guides hint at topics without giving away answers
* `\newpage` and pandoc produce print-ready quizzes
* `/review-lecture` checks the recording against your slides
* The agent can draft assignment specs and starter code

---
layout: end
---

# Building Assessments

## Quizzes, keys, and study guides from your notes
