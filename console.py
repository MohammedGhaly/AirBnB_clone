#!/usr/bin/python3
'''entry point to the console'''
import cmd
from models.base_model import BaseModel
from models import storage
import re


class HBNBCommand(cmd.Cmd):
    '''a class to configure the console options and supported commands'''
    prompt = '(hbnb) '

    def do_update(self, arg):
        ' Updates an instance based on the class name and id'
        if arg == "" or arg is None:
            print("** class name missing **")
            return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'

        match = re.search(rex, arg)
        class_name = match.group(1)
        obj_id = match.group(2)
        attr_name = match.group(3)
        attr_value = match.group(4)

        if match is None:
            print('** class name missing **')
        elif class_name not in storage.classes():
            print("** class doesn't exist **")
        elif obj_id is None:
            print("** instance id missing **")
        else:
            key = f'{class_name}.{obj_id}'
            if key not in storage.all().keys():
                print("** no instance found **")
            elif attr_name is None:
                print("** attribute name missing **")
            elif attr_value is None:
                print("** value missing **")
            else:
                casting = None
                if re.search('^".*"$', attr_value) is None:
                    if '.' in attr_value:
                        casting = float
                    else:
                        casting = int
                else:
                    attr_value = attr_value.replace('"', '')
                attrs = storage.attributes()[class_name]
                if attr_name in attrs:
                    attr_value = attrs[attr_name](attr_value)
                elif casting:
                    try:
                        attr_value = casting(attr_value)
                    except ValueError:
                        pass
                setattr(storage.all()[key], attr_name, attr_value)
                storage.all()[key].save()

    def do_all(self, arg):
        'prints string representation of instances based on or not class'
        line = arg.split()
        if len(line) == 0:
            objs_list = [str(obj) for obj in storage.all().values()]
            print(objs_list)
        else:
            if line[0] in storage.classes().keys():
                objs_list = [str(obj) for obj in storage.all().values()
                             if type(obj).__name__ == line[0]]
                print(objs_list)
            else:
                print("** class doesn't exist **")

    def do_create(self, class_name):
        '''
        Creates a new instance
        saves it to data file
        prints its (id)
        '''
        if class_name == "":
            print("** class name missing **")
            return
        res = storage.classes().get(class_name, False)
        if res:
            obj = res()
            obj.save()
            print(obj.id)
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        'deletes an instance by id based on class type.'
        line = arg.split()
        if len(line) == 0:
            print("** class name missing **")
        elif len(line) == 1:
            if line[0] in storage.classes().keys():
                print("** instance id missing **")
            else:
                print("** class doesn't exist **")
        else:
            if line[0] in storage.classes().keys():
                key = f'{line[0]}.{line[1]}'
                if key in storage.all().keys():
                    del storage.all()[key]
                    storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** class doesn't exist **")

    def do_show(self, arg):
        'prints the string representation of an instance based on class name'
        line = arg.split()
        if len(line) == 0:
            print("** class name missing **")
        elif len(line) == 1:
            if line[0] in storage.classes().keys():
                print("** instance id missing **")
            else:
                print("** class doesn't exist **")
        else:
            if line[0] in storage.classes().keys():
                obj = storage.all().get(f'{line[0]}.{line[1]}', False)
                if obj:
                    print(obj)
                else:
                    print("** no instance found **")
            else:
                print("** class doesn't exist **")

    def do_EOF(self, line):
        'returns True and exits the command interpreter'
        print()
        return True

    def do_quit(self, line):
        'returns True and exits the command interpreter'
        return True

    def emptyline(self) -> bool:
        'does nothing on empty line'
        return


if __name__ == '__main__':
    HBNBCommand().cmdloop()
