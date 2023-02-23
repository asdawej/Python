import cmd
import pickle


class Note(cmd.Cmd):
    intro = '''
        A notebook used on the desktop in a cmd interface.
    ==========================================================
    '''
    prompt = '<note>'
    fnote = open('note.dat', 'rb')
    note: list[list[str, list[str]]] = pickle.load(fnote)
    fnote.close()

    def do_show(self, arg):
        for i, x in enumerate(Note.note):
            print('Title:', i, x[0])
            print('Text:')
            for s in x[1]:
                print(s)
            print()

    def do_write(self, arg):
        temp_title = input('New note title:')
        temp_text: list[str] = []
        print('New note text(end with END):')
        while (s := input()) != 'END':
            temp_text.append(s)
        Note.note.append([temp_title, temp_text])
        Note.fnote = open('note.dat', 'wb')
        pickle.dump(Note.note, Note.fnote)
        Note.fnote.close()

    def do_delete(self, arg):
        arg = int(arg)
        Note.note.pop(arg)
        Note.fnote = open('note.dat', 'wb')
        pickle.dump(Note.note, Note.fnote)
        Note.fnote.close()

    def do_exit(self, arg):
        exit(0)


Note().cmdloop()
