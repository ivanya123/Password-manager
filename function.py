import json


class Password:

    def __init__(self, login: str, company: str, password: str):
        self.login = login
        self.password = password
        self.company = company

    def __str__(self):
        return f'{self.company};{self.login}:\n{self.password}'

    def to_dict(self):
        return {f'{self.company};{self.login}': self.password}


class ListPassword:
    def __init__(self, name: str):
        self.name: str = name
        self.list_pass: list[Password] = []

    def add(self, *password: Password):
        self.list_pass.extend(password)

    def __str__(self):
        string = ''
        n = 0
        for password in self.list_pass:
            n += 1
            string += f'{n}: {password.login}_{password.company}__{password.password}\n'
        return string

    def to_json(self):
        with open(f'{self.name}.json', 'w') as file:
            dict_passwords = {f'{item.company};{item.login}': item.password for item in
                              self.list_pass}

            json.dump(dict_passwords, file)

    def from_json(self):
        with open(f'{self.name}.json', 'r') as file:
            dict_passwords: dict[str, str] = json.load(file)

        for key, item in dict_passwords.items():
            company_login = key.split(';')
            company = company_login[0]
            login = company_login[1]
            password = item
            new_pass = Password(login, company, password)
            self.list_pass.append(new_pass)

    def delete_pass(self, login_company):
        for i in range(len(self.list_pass)):
            if login_company == f'{self.list_pass[i].company};{self.list_pass[i].login}':
                self.list_pass.pop(i)
                self.to_json()
                break

