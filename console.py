#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        return True

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        return True

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        return False

    def do_create(self, args):
        """ Create an object of any class"""
        if not args:
            print("** class name missing **")
            return
        arg_list = args.split(" ")
        if arg_list[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(arg_list) == 1:
            new_obj = HBNBCommand.classes[arg_list[0]]()
        else:
            kwargs = {}
            for i in range(1, len(arg_list)):
                try:
                    key, val = tuple(arg_list[i].split("="))
                except ValueError:
                    print("**Usage: create <Class name> <key name=value>")
                    return False
                if val.startswith('"'):
                    val = val.strip('"').replace('_', " ")
                else:
                    try:
                        val = eval(val)
                    except (SyntaxError, NameError):
                        pass
                kwargs[key] = val
            new_obj = eval(arg_list[0])(**kwargs)
        print(new_obj.id)
        new_obj.save()

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def do_all(self, line):
        """
           Prints all string representation of all
        instances based or not on the class name.
        Ex: $ all BaseModel or $ all
        """
        inst_list = []
        if line:
            args = line.split(" ")
            if args[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return False
            else:
                all_inst = storage.all(eval(args[0]))
                for val in all_inst.values():
                    inst_list.append(val.__str__())
                print(inst_list)
        else:
            all_inst = storage.all()
            for val in all_inst.keys():
                inst_list.append(val.__str__())
            print(inst_list)

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        if not line:
            print("** class name missing **")
        else:
            cmd_list = shlex.split(line)
            if cmd_list[0] not in self.class_list:
                print("** class doesn't exist **")
                return False
            if len(cmd_list) == 1:
                print("** instance id missing **")
                return False
            elif len(cmd_list) == 2:
                print("** attribute name missing **")
                return False
            elif len(cmd_list) == 3:
                print("** value missing **")
                return False
            else:
                not_to_be_updated = ["id", "created_at", "updated_at"]
            if cmd_list[2] not in not_to_be_updated:
                try:
                    all_objs = storage.all()
                    obj_id = "{}.{}".format(cmd_list[0], cmd_list[1])
                    obj = all_objs[obj_id]
                    attr = cmd_list[2]
                    value = cmd_list[3]
                    setattr(obj, attr, value)
                    storage.save()
                except KeyError:
                    print("** no instance found **")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
