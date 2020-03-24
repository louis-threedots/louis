from app import App
import random
from characters import alphabet_dict, digit_dict

class Memory(App):

    def on_start(self):
        num_cells = len(self.cells)
        if num_cells < 4 and num_cells % 2 != 0:
            self.audio.speak("""
                This game is meant to be played with an even number of modules, at least 4.
                Right now there are """ + str(num_cells) + """ modules connected.
            """)
            self.on_quit()

        self.app_instruction("""
            This is the braille version of the traditional Memory card game.
            You can play it with one or two players. The Memory cards are the cells,
            each corresponding to a braille alphabet character.
            The whole set of cards consists of random, distinct pairs of characters.
            The app first mixes up the cards and assigns them to all the cells.
            Then, turn over any two cards by pressing the button on a cell.
            That cell will go from a blank output to rendering the associated character.
            If the two cards match, you score a point and get another turn.
            If they don't match, you and your opponent get time to inspect them and can move on to the next turn by saying 'next'.
            The output will then return to blank again, so remember what was on each card and where it was.
            The game is over when all the cards have been matched.

            In solo mode, the number of turns is recorded, so that you
            can attempt to find all pairs in as little turns as possible.
            When playing together, the app will keep track of the score.
        """)
        self.play_memory()

    def play_memory(self):
        self.audio.speak("Are you playing memory with one or two players?")
        reply = self.await_response(["one", "two"])

        self.field = self.initialise_field()
        self.num_turns = 0
        self.score = [0, 0, 0]
        self.flipped_cells = []

        if reply == 'one':
            player = 0
            self.audio.speak("Try to find all pairs with as little turns as possible!")
        elif reply == 'two':
            player = 1

        self.next_turn(player)

    def have_turn(self, player=0):
        self.num_turns += 1
        if player != 0:
            self.audio.speak("It is now player " + digit_dict[str(player)]['pronunciation'] + "'s turn.")
        cell_idx1 = self.wait_for_flip()
        cell_idx2 = self.wait_for_flip()
        return cell_idx1, cell_idx2

    def check_for_match(self, cell_idx1, cell_idx2, player):
        char1 = self.field[cell_idx1 - 1]
        char2 = self.field[cell_idx2 - 1]
        if char1 == char2:
            self.audio.speak("You have found a match! This is the letter " + alphabet_dict[char1]['pronunciation'] + ".")
            self.score[player] += 1
            self.flipped_cells.append(cell_idx1)
            self.flipped_cells.append(cell_idx2)
            return True
        else:
            return False

    def next_turn(self, player):
        self.print_cells_to_terminal()
        cell_idx1, cell_idx2 = self.have_turn()
        is_match = self.check_for_match(cell_idx1, cell_idx2, player)
        self.check_game_done(player)
        self.await_response(["next"])

        next_player = player

        if not is_match:
            self.cells[cell_idx1 - 1].reset(to='space') # flip back to face-down
            self.cells[cell_idx2 - 1].reset(to='space') # flip back to face-down
            if player == 1:
                next_player = 2
            elif player == 2:
                next_player = 1

        self.next_turn(next_player)

    def check_game_done(self, player):
        if sum(self.score) == int(len(self.field) / 2):
            if player == 0:
                self.audio.speak("You have found all pairs in " + str(self.num_turns) + " turns.")
            else:
                self.audio.speak("""
                    All pairs have been found. Player 1 has a score of """ + str(self.score[1]) + """
                    and player 2 has a score of """ + str(self.score[2]) + """.
                """)
                if self.score[2] > self.score[1]:
                    self.audio.speak("Player 2 has won!")
                elif self.score[1] > self.score[2]:
                    self.audio.speak("Player 1 has won!")
                else:
                    self.audio.speak("It's a draw!")

            self.audio.speak("Do you want to play another game?")
            reply = self.await_response(["yes","no"])
            if reply == 'yes':
                self.reset_cells(to='space')
                self.play_memory()

            self.on_quit()

    def wait_for_flip(self):
        cell_idx = self.get_pressed_button()
        if cell_idx in self.flipped_cells:
            self.audio.speak("You've already found this pair.")
            return self.wait_for_flip()
        c = self.field[cell_idx - 1]
        self.cells[cell_idx - 1].print_character(c)
        self.audio.speak("This is cell " + str(cell_idx))
        self.print_cells_to_terminal()
        return cell_idx

    def initialise_field(self):
        chars = random.sample(list(alphabet_dict), int(len(self.cells) / 2))
        chars = chars + chars
        chars_shuffled = random.sample(chars, len(chars))
        return chars_shuffled
