class ConfirmationInput:

    def __init__(self, message):
        confirmation = input(f"{message} (y/n) ")
        if (confirmation != "y"):
            print("Command cancelled.")
            exit()
