---
defaults:
  layout: two-cols
mdc: true
fonts:
  mono: Cascadia Mono
  sans: Atkinson Hyperlegible
layout: cover
---

# Command-Line Agents

---

## What's a Coding Agent?

* Coding agents are local programs that read your files
* Can run commands directly
* Can make edits in place

::right::

```bash
> fix the typo on slide 4

  Read   20_compilers.md
  Edit   20_compilers.md
   -  * a compilier turns source
   +  * a compiler turns source

  Done. One line changed.
```

---

## What's a Coding Agent?

* Coding agents work in a loop, not a single reply
* Working with a coding agent is typically conversation-like
* Rewards good writing skills!

::right::

```bash
> add a slide on linkers after slide 6

  Read   20_compilers.md
  Edit   20_compilers.md (+14)

> too long, cut it to three bullets

  Edit   20_compilers.md (-6)

> good, now add a code example

  Edit   20_compilers.md (+8)
```

---

## Online Chat vs Terminal

* Many people are used to using AI agents online, via Chat
* Chat sees only what you paste in
* Chat hands back text

::right::

```
  Chat window          Coding agent
  -----------          ------------
  paste a file    ->   reads any file
  copy reply back ->   edits in place
  no memory       ->   project rules
  no commands     ->   runs the build
```

---

## Online vs Terminal

* Command line agents see the whole repo
* Command line agents hand back a diff you can review
* Command line agents run commands locally -- powerful and dangerous

::right::

```
  > what does this project do?

  read  CLAUDE.md
  read  meta/lectures/ (36 files)
  bash  git log --oneline -5

  "A systems course built around
   two teaching CPUs..."
```

---

## Claude Code

* In today's presentation I am going to use Claude Code
* There are many command line agents, I am used to Claude
* The same concepts should work with any command line agent

::right::

```bash
  $ claude

  * Welcome to Claude Code

    cwd: ~/csci-366-template
    model: claude-opus-4-8

  > _
```

---

## Installing

* Install once with `npm`, then run `claude` in any project
* Sign in with your Anthropic account on first launch
* Verify the exact command at the current Claude Code docs

::right::

```bash
  npm install -g @anthropic-ai/claude-code

  cd your-project
  claude
```

---

## CLAUDE.md

* A markdown file the agent reads on every run
* Holds project rules: style, conventions, what not to touch
* Encode your taste once, reuse it on every task

::right::

```markdown
# Lectures

* Use a two-cols layout
* Titles short, no "Best Practices"
* Max three bullets per slide
* Italics for emphasis, not bold
* Asterisk bullets, no numbered lists
```

<!-- this is a real excerpt from the course CLAUDE.md -->

---

## Permissions

* The agent asks before it edits or runs commands
* You allowlist the safe, repetitive calls
* Nothing lands without your say-so

::right::

```
  Edit  meta/lectures/37_ai.md   [y/n]
  Bash  just gen-pdfs            [y/n]
  Bash  rm -rf meta/             [n]
```

---

## Permission Modes

* _Default_ -- ask before each edit and command
* _Accept edits_ -- apply edits automatically, still ask for commands
* _Plan_ is read-only; _bypass_ skips every prompt -- use with care

::right::

```
  shift+tab cycles the mode:

  default       ask every time
  accept edits  auto-apply edits
  plan          read-only, no edits
  bypass        no prompts (risky)
```

---

## Selecting a Model

* Bigger models reason better; smaller ones are faster and cheaper
* Switch any time with `/model`
* Match the model to the task -- drafting vs a quick rename

::right::

```
  > /model

    opus 4.8    most capable
    sonnet 4.6  balanced
    haiku 4.5   fast, cheap
```

---

## Context

* Context is everything the agent currently sees
* Your prompts, the files it read, and command output all go in
* It is a fixed window -- it fills as the session runs

::right::

```
  in the context window:

  CLAUDE.md (always)
  files you @-mention
  command output
  the whole conversation
```

---

## Managing Context

* A full window is slower and less accurate
* `/clear` resets to a blank slate -- use it between unrelated tasks
* `/compact` summarizes the session so far, freeing room to keep going

::right::

```
  > /clear
    fresh start, nothing carried

  > /compact
    summarize, keep the gist,
    drop the raw history
```

---

## Skills

* A skill is a markdown file: a reusable prompt plus steps
* Lives in `.claude/commands/`, per user or per project
* Invoke it with a slash; `$ARGUMENTS` passes input

::right::

```
  ~/.claude/commands/
    review-lecture.md
    pick-session.md

  .claude/commands/   (per project)
```

---

## Skill Example: /review-lecture

* `/review-lecture <url>` grades a recording against its slides
* Pulls the transcript, matches it to the lecture, writes a review
* Output: timing, coverage gaps, and proposed slide fixes

::right::

```markdown
# Review Lecture

## Steps
1. Fetch the transcript
2. Match it to the slide deck
3. Read both files
4. Write the review:
   timing, gaps, fixes
```

---

## IntelliJ Integration

* Claude Code runs inside the IDE, not just a separate terminal
* Edits land where you expect: the editor, diffs, the gutter
* Similar plugins exist for VS Code and many other editors

::right::

```
  IntelliJ + Claude Code plugin

  * chat panel beside your code
  * agent edits show as diffs
  * selection becomes context
```

---

## Using AI Effectively

* Code is cheap to generate - understanding is expensive
* Work in small steps, not giant changelists no one can read

::right::

```
  generate -> read -> accept
  generate -> read -> reject
  generate -> read -> revise

  never:
  generate -> commit -> hope
```

---

## Review Diffs!

* The agent is fast and confident, including when it is wrong
* A diff is the unit of trust -- read it before you accept
* `git` is the safety net: nothing is permanent until you commit

::right::

```diff
  ## C's Design Principles

- * Trust the programmer
+ * _Trust the programmer_ -- low-level access
  * One-to-one with assembly where possible
+ * No runtime safety net
```

---

## DEMO: Explain Project

<!-- Demo: open the 366 repo, ask the agent to explain the project from CLAUDE.md -->

* Open the course repo and ask the agent what the project is
* It reads CLAUDE.md and the tree, then answers
* Shows the loop, the file access, and the project rules in one shot

---
layout: default
---

## Summary

* A coding agent reads files, runs commands, and edits in a loop
* The terminal beats chat: full repo context and reviewable diffs
* CLAUDE.md encodes your rules so output matches your style
* Permissions keep you in control of edits and commands
* Skills wrap multi-step workflows behind a slash command
* Code is cheap; understanding is the bottleneck
* Work incrementally and read every diff before accepting
* git is the undo button -- nothing lands until you commit

---
layout: end
---

# Command-Line Agents

## Moving past the chat window
