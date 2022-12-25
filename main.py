def error_handler(func):
    def wrapper(*args):
        try:
            return func(*args)
        except IndexError:
            return "You didn't provide contact name or phone number"
        except ValueError:
            return "Phone number must include digits only"
        except KeyError:
            return "Username is not in contact list"

    return wrapper


CONTACTS = {}

HELP_INSTRUCTIONS = """This contact bot save your contacts 
    Global commands:
      'add' - add new contact. Input user name and phone
    Example: add User_name 095-xxx-xx-xx
      'change' - change users old phone to new phone. Input user name, old phone and new phone
    Example: change User_name 095-xxx-xx-xx 050-xxx-xx-xx
      'phone' - show contacts of input user. Input user name
    Example: phone User_name
      'show all' - show all contacts
    Example: show all
      'exit/'.'/'bye'/'close' - exit bot
    Example: exit"""


def sanitize_number(number):
    """Return phone number that only include digits"""
    return number.strip().replace("-", "").replace("(", "").replace(")", "").replace("+", "")


@error_handler
def add(*args):
    """Adds new contact, requires name and phone"""
    name = args[0]
    phone = sanitize_number(args[1])

    if name in CONTACTS:
        user_input = input(
            "Contact with this name already exist, do you want to rewrite it or create new record? '1'/'2'\n")
        if user_input == "2":
            name += "(1)"

    if not phone.isnumeric():
        raise ValueError
    CONTACTS[name] = phone
    return f'You just added contact "{name}" with phone "{phone}" to your list of contacts'


@error_handler
def hello(*args):
    """Greets user"""
    return "How can I help you?"


@error_handler
def show_all(*args):
    """Show a list of all contacts that were added before"""
    if not CONTACTS:
        return "Your contact list is empty"
    text = "Your list of contacts:\n"
    for name, number in CONTACTS.items():
        phones = ""
        for n in number:
            phones += n + " "
        text += ''.join("Username: " + name + " Number: " + number + "\n")
    return text


@error_handler
def change(*args):
    """Replace phone number for an existing contact"""
    name = args[0]
    phone = sanitize_number(args[1])

    if not phone.isnumeric():
        raise ValueError

    del CONTACTS[name]
    CONTACTS[name] = phone
    return f"You just changed number for contact '{name}'. New number is '{phone}'"


@error_handler
def phone(*args):
    """Shows a phone number for a chosen contact"""
    name = args[0]
    return f"For this contact: '{name}' number is '{CONTACTS[name]}'"


@error_handler
def helper(*args):
    return HELP_INSTRUCTIONS


COMMANDS = {
    add: "add",
    hello: "hello",
    show_all: "show all",
    change: "change",
    phone: "phone",
    helper: "help"
}


def command_parser(user_input):
    for command, key_word in COMMANDS.items():
        if user_input.startswith(key_word):
            return command, user_input.replace(key_word, "").strip().split(" ")
    return None, None


def main():
    print("Here's a list of available commands: 'Hello', 'Add', 'Change', 'Phone', 'Show all', 'Help', 'Exit'")
    while True:
        user_input = input(">>>")
        end_words = [".", "close", "bye", "exit"]

        if user_input.lower() in end_words:
            print("Goodbye and good luck")
            break

        command, data = command_parser(user_input.lower())

        if not command:
            print("Sorry, unknown command")
        else:
            print(command(*data))


if __name__ == '__main__':
    main()
