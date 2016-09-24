from pprint import pprint

from climvc.clicontroller import CLIController

from decisionmaker import Choice, ChoiceList


class Controller(CLIController):
    def b(self):
        """Command. Select the best item from a list."""
        print(self.model.lists[self.input("list")].best())
    
    def nb(self):
        """Comand. Get the best item in a list, excluding the last returned best item."""
        print(self.model.lists[self.input("list")].next_best())
    
    def i(self, exclude=False):
        """Comand. Include items for consideration"""
        operation = 'exclude' if exclude else 'include'
        list_name = self.input("list name")
        inclusions = self.input(operation + " what? (optional)").split(", ")
        if not inclusions or not inclusions[0]:
            inclusions = self.model.lists[list_name].excluded()
        for choice_name in inclusions:
            if len(inclusions) > 1:
                answer = self.input(operation + " " + str(choice_name) + "? (y/n)")
            else:
                answer = 'y'
    
            if answer == 'y':
                choice = next(i for i in self.model.lists[list_name] if i.text == choice_name)
                if operation == 'include':
                    self.model.lists[list_name].include(choice)
                else:
                    self.model.lists[list_name].exclude(choice)
    
    
    def x(self):
        """Command. Exclude items from consideration."""
        self.i(exclude=True)
    
    def n(self):
        """Command. Add something."""
        type_ = self.input("list or choices?")
        list_ = self.input("list name")
        if type_ == "list":
            self.model.lists[list_] = ChoiceList()
            scale_values = self.input('scale values (optional)').split(', ')
            if scale_values:
                self.model.lists[list_].scale.values = scale_values
        for choice_text in self.input("choices").split(", "):
            self.model.lists[list_].add(Choice(choice_text, self.model.lists[list_].scale))
    
    def s(self):
        """Command. Sort a list."""
        print(*sorted(self.model.lists[self.input('list name')]), sep="\n")
    
    def d(self):
        """Command. Delete something."""
        type_ = self.input("list or choices?")
        if type_ == "list":
            del self.model.lists[self.input("name")]
        elif type_ == "choices":
            choices = self.input("choices").split(", ")
            list_name = self.input("list")
            for i in choices:
                self.model.lists[list_name].discard(i)
        else:
            raise RuntimeError("Unknown option.")
    
    def p(self):
        """Command. Show useful info"""
        for list_ in self.model.lists:
            pprint(vars(list_))
    
    def blargh(self):
        """Command. For debug purposes only. Do not run!"""
        print(', '.join(str(i) for i in self.model.lists['activities']))
    
    def ss(self):
        """Command. Set the rating scale for a list"""
        self.model.lists[self.input('list name')].scale.values = self.input('scale values').split(', ')
    
    def rn(self):
        """Command. rename a choice."""
        list_name = self.input('list name')
        choice_name = self.input('choice name')
        replacement_text = self.input('replacement text')
        for i in self.model.lists[list_name]:
            if i.text == choice_name:
                i.text = replacement_text
