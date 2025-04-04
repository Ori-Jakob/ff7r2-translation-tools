"""
This is a custom CLI gui that allows you to select from a list of options with keyboard controls

Author: Ori Jakob
"""

from pynput.keyboard import Key, Listener
import os

# Only import msvcrt on Windows
if os.name == 'nt':
    import msvcrt
else:
    import termios

class Colors:
    """
        A class to hold the colors for the CLI
    """
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[0m'

class cli_gui:
    """
        A class to render a CLI GUI
    """

    def __init__(self, items=[]):
        """
            Initializes the class
            :items list: a list of items to display
        """
        self.items = list()
        self.position = 0
        self.message = str()
        self.__offset = 4
        self.terminal_size = self.__update_terminal()
        
    def move(self, direction, absolute=False):
        """
            Moves the cursor in the GUI
            :direction int: the direction to move the cursor
            :absolute bool: whether to move the cursor absolutely or relatively
        """
        if absolute:
            self.position = direction
        else:
            temp = self.position + direction
            n = len(self.items) - 1

            if temp > n:
                self.position = 0
            elif temp < 0:
                self.position = n
            else:
                self.position = temp

        self.display()
    
    def display(self, isArticle=False):
        """
            Displays the GUI
            :isArticle bool: whether the items are articles or not
        """
        os.system("cls")
        self.__instructions()

        temp = self.position // self.terminal_size
        self.__color(f"{self.message} ({temp + 1}/{(len(self.items) // self.terminal_size) + 1})", Colors.GREEN)
        
        num = self.terminal_size * temp
        display_items = self.items[num:num + self.terminal_size] if len(self.items) > self.terminal_size else self.items

        for i, article in enumerate(display_items):
            if isArticle: item = article["title"]
            else: item = article

            self.__color(f"{(num + i + 1) if item != 'Exit' else ' '}", Colors.RED, end="")
            if num + i == self.position:
                self.__color(f" {item}", Colors.BLUE)
            else:
                self.__color(f" {item}")

        print(Colors.WHITE, end="")

    def start(self, new_items, message, reset=True):
        """
            Starts the GUI
            :new_items list: a list of items to display
            :message string: the message to display
        """
        self.__update(new_items, message, reset)
        self.display()
        with Listener(on_press=self.__listen) as listener:
            listener.join()

        # Flush input buffer on exit
        self.__flush_input()
        return self.position
    
    def reset(self):
        self.position = 0

    def __listen(self, key):
        """
            Listens for the key press and acts accordingly to the key
            :key Key: the key that was pressed
        """
        if os.get_terminal_size().lines != self.terminal_size:
            self.terminal_size = self.__update_terminal()

        match key:
            case Key.up:
                self.move(-1)
                return True  # Keep listener alive
            case Key.down:
                self.move(1)
                return True  # Keep listener alive
            case Key.right:
                self.move(self.terminal_size)
                return True  # Keep listener alive
            case Key.left:
                self.move(-self.terminal_size)
                return True  # Keep listener alive
            case Key.page_up:
                self.move(0, absolute=True)
                return True  # Keep listener alive
            case Key.page_down:
                self.move(len(self.items) - 1, absolute=True)
                return True  # Keep listener alive
            case Key.enter:
                os.system("cls")
                return False  # Stop listener on Enter
        return True  # Default: keep listener running for unhandled keys

    def __update(self, items, message, reset=True):
        """
            Updates the items and message
            :items list: a list of items to display
            :message string: the message to display
        """
        self.message = message
        self.items = items
        if reset or self.position >= len(items):
            self.position = 0

    def __color(self, text, color=Colors.WHITE, end="\n"):
        """
            Prints the text in the specified color
            :text string: the text to print
            :color string: the color to print the text in
            :end string: the end character to print
        """
        print(color + text, end=end)

    def __update_terminal(self):
        """
            Updates the terminal size
            :return int: the terminal size
        """
        return os.get_terminal_size().lines - self.__offset
    
    def __instructions(self):
        """
            Displays the instructions to the user
        """
        self.__color("[↑|↓]=UP/DOWN, [←|→]=NEXT/PREV PAGE, [PGUP|PGDOWN]=FIRST/LAST ITEM, [ENTER]=SELECT", Colors.YELLOW)

    def __flush_input(self):
        """
            Flushes the input buffer (Windows-specific)
        """
        if os.name == 'nt':  # Windows only
            while msvcrt.kbhit():
                msvcrt.getch()
        else:  # Unix-like (Linux, macOS)
            try:
                termios.tcflush(sys.stdin, termios.TCIFLUSH)
            except termios.error:
                pass

render = cli_gui()