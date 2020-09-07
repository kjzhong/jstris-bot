# Tetris Bot

This is a python implementation of a tetris bot.

The goal of this code is to automatically play jstris with a simple AI.

*NOTE* this code is very brittle. A configuration script is in the roadmap to enable to code to work on other machines. As is, it is likely to only work on my computer setup.

## Approach
1. Read piece from jstris to game
2. Adjust jstris piece to match game piece (They are generated slightly differently)
3. Intercept strategy from AI and input into jstris
4. Repeat 1-3

## Roadmap
* Create configuration script
* Redevelop AI

## Disclosure
This code builds heavily from the work done by LoveDaisy (https://github.com/LoveDaisy/tetris_game)