from colorama import Fore, Style


class Message:
    """ Message Controller to handle colored message in terminal to ease the job of debugging """

    @staticmethod
    def info(message: str) -> None:
        """ Prints Blue Message """
        print(Fore.BLUE + message)
        print(Style.RESET_ALL)

    @staticmethod
    def success(message: str) -> None:
        """ Prints Green Message """
        print(Fore.LIGHTGREEN_EX + message)
        print(Style.RESET_ALL)

    @staticmethod
    def error(message: str) -> None:
        """ Prints Red Message """
        print(Fore.RED + message)
        print(Style.RESET_ALL)
