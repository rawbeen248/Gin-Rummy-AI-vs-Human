# Gin-Rummy-AI-vs-Human

Gin-Rummy-AI-vs-Human is a fully-featured implementation of the classic card game, Gin Rummy, presented in an interactive console environment.It integrates every essential element of the original game while introducing a strategically competant AI bot as an opponent. 

### Installation
___
1. Clone the repository to your local machine. <br />
```
git clone https://github.com/rawbeen248/Gin-Rummy-AI-vs-Human
```
2. Navigate to the cloned repository. <br />
```
cd Gin-Rummy-AI-vs-Human
```
3. Ensure you have Python installed and run the game. <br />
```
python main.py
```
### Usage 
___
The game, carried out in the console, adheres to the standard rules of Gin Rummy. Each game round commences by dealing 10 cards to both the player and the AI bot. Subsequently, players alternate turns, during which they can opt to draw from either the deck or the discard pile, and must discard one card from their hand.

Each round concludes when a player either knocks or declares gin. The match continues over multiple rounds until either the player or the bot accumulates a score of 100 or above.

### Unique Features
___
* Player Assist: <br />
The program assists players in identifying the best possible melds from their hand, easing the gameplay experience while simultaneously aiding them in understanding melding strategies.

* Scoring System: <br />
The game implements a sophisticated scoring system that strictly adheres to the traditional rules of Gin Rummy. Points are calculated and accumulated over each round, extending the game over multiple rounds until a player surpasses the 100-point threshold.

### AI Bot Logic
___
The AI bot, acting as the opponent, demonstrates a tactical approach by:

1. FInding the optimal melds possible.
2. Analyzing its hand for potential melds and deadwood.
3. Strategically drawing from the discard pile when it is deemed advantageous.
4. Endeavoring to minimize its deadwood count, and knocking when this count is 10 or less and declaring gin when it is 0.
