# Conway's Game of RGB
Conway's Game of Life Played out on Razer LED Keyboards
![Demonstration](https://github.com/chandlerkincaid/Conways_Game_of_RGB/blob/master/conway.gif)

When I purchased my Razer brand laptop I had little initial interest in the vibrant LED lightup keyboard it came standard with. I mostly wanted a machined aluminum case for a decent price, but after having it for a few months I decided It would be a shame to just leave all those ridiculous colors permanetly turned off. Being a fan of classical AI my mind wandered to [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life). Conway's is an example of cellular automata in which simple rules can give rise to complex "lifelike" patterns. The rules are as follows:

1. Any live cell with fewer than two live neighbors dies, as if by underpopulation.
2. Any live cell with two or three live neighbors lives on to the next generation.
3. Any live cell with more than three live neighbors dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.

My version is adapted to seed the keyboard with a random series of colors. When a new cell comes alive from the forth rule it takes on a random color from its neightbors. This results in a behavior where automata colors "fight" to become the dominant color on the keyboard.

The code relies on a fantastic library [openrazer](https://github.com/openrazer/openrazer) and is adapted from one of their examples.
