from colorama import Fore, Style
import sys


class Message:
    """ Message Controller to handle
        colored message in terminal to ease
        the job of debugging.
    """
    @staticmethod
    def info(message: str) -> None:
        """ Prints Blue Message """
        print(Fore.BLUE + message)
        print(Style.RESET_ALL, end='')

    @staticmethod
    def success(message: str) -> None:
        """ Prints Green Message """
        print(Fore.LIGHTGREEN_EX + message)
        print(Style.RESET_ALL, end='')

    @staticmethod
    def error(message: str) -> None:
        """ Prints Red Message """
        print(Fore.RED + message)
        print(Style.RESET_ALL, end='')

    @staticmethod
    def progress(value, end_value, bar_length=20) -> None:
        """ Prints progress bar """
        percent = float(value) / end_value
        arrow = '-' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))
        sys.stdout.write(f"\rPercent: [{arrow + spaces}] {int(round(percent * 100))}%")
        sys.stdout.flush()
