import re
import json

"""
/**
 * Takes as a first argument a name of an executive and prints out which users 
 * work under him and what their departments, salaries and roles are.
 *
 * It collects data from several tables, correlates different user types by 
 * name and fills in the blanks if a user has missing information on a table.
 * Students don't get a salary even if they have other roles with values in 
 * their salary field. That is company policy and not negotiable.
 * 
 * Note:
 * This application is supposed to be a reporting type application. This means
 * that it doesn't concern itself with putting data into the database. It just 
 * reads it out and corrects inconsistencies (if needed) after the reads.
 *
 * Assignment:
 * 1. Read the codebase and understand.
 * 2. Things to think about:
 *    - Is this good code?
 *    - Is the output of the application suited for an executive tool?
 *    - How would you test this code?
 *    - Is the code intuitive?
 *    - Are there things that should be refactored to make the code more 
 *      understandable?
 *    - Are there things that should be refactored to make it easier to write
 *      unit tests focusing on only one part of the logic?
 *    - Are there error cases that must be dealt with?
 */
"""


class Application:
    class User:

        def __init__(self, name: str, birth: str, salary: float, role: str, department: str):
            self.name = name
            self.birth = birth
            self.salary = salary
            self.department = department
            self.role = role

        def __repr__(self):
            rep = f'User( name: {self.name},' \
                  f' birth: {str(self.birth)},' \
                  f' salary: {self.salary},' \
                  f' role: {self.role},' \
                  f' department: {self.department})'

            return rep

        def __eq__(self, other):
            return self.name == other.name and \
                   self.birth == other.birth and \
                   self.salary == other.salary and \
                   self.department == other.department and \
                   self.role == other.role

    users: [User] = []

    TYPE_ONE = "1"
    TYPE_TWO = "2"
    TYPE_TRE = "3"
    TYPE_FUR = "4"

    def run_logic(self, executive: str):

        f = open('../data/users.json')
        data = json.load(f)

        for item in data:
            print(item)
            self.users.append(
                Application.User(name=item["name"], department=item["department"], salary=item["salary"],
                                 birth=item["birth"], role=item["role"]))

        f.close()

        mgrs: [Application.User] = [x for x in self.users if x.role is self.TYPE_ONE and x.name == executive]

        for mngr in mgrs:

            testers: [Application.User] = [x for x in self.users if x.role is self.TYPE_TWO]
            devs: [Application.User] = [x for x in self.users if x.role is self.TYPE_TRE]
            students: [Application.User] = [x for x in self.users if x.role is self.TYPE_FUR]
            print("")
            print("")
            print("")

            print("Manager" + mngr.name + " " + str(mngr.salary) + " " + "(" + mngr.department + ") manages: ")

            persons: [Application.User] = []

            for p in testers:
                p.role = "Tester"
                persons.append(p)

            for p in devs:
                p.role = "Developer"
                existing = next((e for e in persons if e.name == p.name), None)
                if existing is None:
                    persons.append(p)
                else:
                    self.merge_User(p, existing)

            for p in students:
                p.role = "Student"
                existing = next((e for e in persons if e.name == p.name), None)

                if existing is None:
                    persons.append(p)
                else:
                    self.merge_User(p, existing)

                existing = next((e for e in persons if e.name == p.name), None)
                existing.salary = 0

            print("")
            print("")

            for p in persons:
                rx = re.compile(".*" + mngr.department + ".*")
                if re.match(rx, p.department):
                    print(p)

            print("")
            print("")
            print("")

    # Merges information from User one into user two
    def merge_User(self, one: User, two: User):

        print("LOG: Merging: " + one.__repr__() + " into: " + two.__repr__() + " ");

        two.name = one.name if one.name is None else one.name
        two.birth = one.birth if one.birth is None else one.birth
        two.salary = two.salary + one.salary
        two.role = two.role + " " + one.role

        if not (two.department == one.department):
            two.department = two.department + " " + one.department


if __name__ == '__main__':
    application = Application().run_logic("Adam")
