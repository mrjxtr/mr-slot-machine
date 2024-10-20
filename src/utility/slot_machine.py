"""Implements a slot machine game with various functionalities."""

import random
import time

from utility.config import (
    COLS,
    MAX_BET,
    MAX_LINES,
    MIN_BET,
    ROWS,
    symbol_count,
    symbol_value,
)


class SlotMachine:
    """Represents a slot machine with game logic and user interactions."""

    def __init__(self) -> None:
        """Initialize the slot machine with zero balance."""
        self.balance = 0

    def check_winnings(self, columns, lines, bet, values):
        """Calculate winnings and winning lines."""
        winnings = 0
        winning_lines = []
        for line in range(lines):
            symbol = columns[0][line]
            for column in columns:
                symbol_to_check = column[line]
                if symbol != symbol_to_check:
                    break
            else:
                winnings += values[symbol] * bet
                winning_lines.append(line + 1)

        return winnings, winning_lines

    def get_slot_machine_spin(self, rows, cols, symbols):
        """Generate a random spin result for the slot machine."""
        all_symbols = []
        for symbol, count in symbols.items():
            all_symbols.extend([symbol] * count)

        columns = []
        for _ in range(cols):
            column = []
            current_symbols = all_symbols[:]
            for _ in range(rows):
                value = random.choice(current_symbols)
                current_symbols.remove(value)
                column.append(value)
            columns.append(column)

        return columns

    def print_slot_machine(self, columns):
        """Display the slot machine result with a delay between rows."""
        for row in range(len(columns[0])):
            for i, column in enumerate(columns):
                if i != len(columns) - 1:
                    print(column[row], end=" | ")
                else:
                    print(column[row])
                    time.sleep(1)

    def deposit(self):
        """Handle user deposit input and update balance."""
        while True:
            amount = input("How much would you like to deposit? $")
            if amount.isdigit():
                amount = int(amount)
                if amount > 0:
                    self.balance = amount
                    return self.balance
                else:
                    print()
                    print("Amount must be greater than 0.")
                    print()
            else:
                print()
                print("Please enter a number.")
                print()

    def get_number_of_lines(self):
        """Get user input for number of lines to bet on."""
        while True:
            print()
            lines = input(
                "Which lines do you want to bet on? (1-" + str(MAX_LINES) + ")? "
            )
            if lines.isdigit():
                lines = int(lines)
                if 1 <= lines <= MAX_LINES:
                    return lines
                else:
                    print()
                    print("Enter a valid number of lines.")
                    print()
            else:
                print()
                print("Please enter a number.")
                print()

    def get_bet(self):
        """Get user input for bet amount per line."""
        while True:
            amount = input("How much would you like to bet ($1-$100)? $")
            if amount.isdigit():
                amount = int(amount)
                if MIN_BET <= amount <= MAX_BET:
                    break
                else:
                    print()
                    print(f"Amount must be between ${MIN_BET} - ${MAX_BET}.")
            else:
                print()
                print("Please enter a number.")
                print()

        return amount

    def spin(self, balance):
        """Execute a complete spin cycle, including betting and result calculation."""
        print("=========================================================")
        print()
        lines = self.get_number_of_lines()
        while True:
            bet = self.get_bet()
            total_bet = bet * lines

            if total_bet > balance:
                print()
                print("You do not have enough to bet that amount")
                print(f"your current balance is: ${balance}")
                print()
            else:
                break

        print()
        print(f"You are betting ${bet} on {lines} line(s).")
        print(f"Total bet is equal to: ${total_bet}")
        print()
        time.sleep(3)
        print("Spinning...")
        print()
        time.sleep(2)

        slots = self.get_slot_machine_spin(ROWS, COLS, symbol_count)
        self.print_slot_machine(slots)
        winnings, winning_lines = self.check_winnings(slots, lines, bet, symbol_value)
        time.sleep(1)
        print()
        print(f"You won ${winnings}.")
        print("You won on lines:", *winning_lines)
        time.sleep(1)
        return winnings - total_bet
