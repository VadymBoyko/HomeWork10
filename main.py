from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def get_info(self):
        phones_info = ''

        for phone in self.phones:
            phones_info += f'{phone.value}, '

        return f'{self.name.value} : {phones_info[:-2]}'

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        for record_phone in self.phones:
            if record_phone.value == phone:
                self.phones.remove(record_phone)
                return True
        return False

    def change_phones(self, phones):
        for phone in phones:
            if not self.delete_phone(phone):
                self.add_phone(phone)


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def get_all_record(self):
        return self.data

    def has_record(self, name):
        return bool(self.data.get(name))

    def get_record(self, name):
        return self.data.get(name)

    def remove_record(self, name):
        del self.data[name]

    def search(self, value):
        if self.has_record(value):
            return self.get_record(value)

        for record in self.get_all_record().values():
            for phone in record.phones:
                if phone.value == value:
                    return record

        raise ValueError(f"Contact with this value ""{value}"" does not exist.")

contacts = AddressBook()

def input_error(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except KeyError:
            return 'Wrong name'
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return 'Enter: name and number'
        except TypeError:
            return 'Wrong command'
    return wrapper


@input_error
def hello_func():
    return 'How can I help you?'


@input_error
def exit_func():
    return 'Good bye!'


@input_error
def add_func(data):
    name, phone = pars_params(data)
    if name in contacts:
        raise ValueError(f'Contact {name} exist. ''name'' should be unique')
    contacts[name] = phone
    return f'New contact: {name} {phone} was added'


@input_error
def change_func(data):
    name, phone = pars_params(data)
    if name in contacts:
        contacts[name] = phone
        return f'You changed number to {phone} for {name}'
    return f'Contact {name} was not found'


@input_error
def search_func(name):
    if name not in contacts:
        raise ValueError(f'Contact {name} does not exist')
    return contacts.get(name)


@input_error
def show_all_func():
    contacts_result = ''
    for key, value in contacts.items():
        contacts_result += f'{key} : {value} \n'
    return contacts_result


commands = {
    'hello': hello_func,
    'add': add_func,
    'change': change_func,
    'show all': show_all_func,
    'phone': search_func,
    'exit': exit_func,
    'close': exit_func,
    'good bye': exit_func
}


def process_input_data(user_input):
    new_input = user_input
    data = ''
    for key in commands:
        if user_input.strip().lower().startswith(key):
            new_input = key
            data = user_input[len(new_input):]
            break
    if data:
        return process_func(new_input)(data)
    return process_func(new_input)()


def process_func(command_name):
    return commands.get(command_name, unknown_func)


def pars_params(data):
    name, phone = data.strip().split(" ")
    if name.isnumeric():
        raise ValueError(f'Name {name} should contains letters')
    if not phone.isnumeric():
        raise ValueError(f'Phone {phone} can contain numbers only')
    return name, phone


def unknown_func():
    return 'Unknown command name'



def main():
    while True:
        user_input = input('Enter command: ')
        result = process_input_data(user_input)
        print(result)
        if result == 'Good bye!':
            break


if __name__ == '__main__':
    main()
