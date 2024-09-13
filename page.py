"""Classes to store page information"""


class Unit:
    """
    A general case of a unit

    A unit is one element that can be activated. I.e you can move to a new page, or trigger an action etc.

    Unit can have other units as children. Unit's children define which units can be transitioned to from itself.
    """
    children: list['Unit']
    title: str
    id: int = 0
    parent_id: int = -1

    def __init__(self, title="", children: list['Unit'] = ()):
        self.title = title
        self.id = Unit.id
        Unit.id += 1
        self.children = []
        for child in children:
            self.add_child(child)

    def add_child(self, element: 'Unit'):
        self.children.append(element)
        element.parent_id = self.id

    def remove_child(self, element: 'Unit'):
        self.children.remove(element)
        element.parent_id = -1

    def flatten(self) -> list['Unit']:
        flat = [self]
        for child in self.children:
            flat.extend(child.flatten())
        return flat

    def __str__(self):
        s = f"[{self.title} ({self.id})"
        for i in self.children:
            s += f" {i}"
        s += "]"
        return s


class Page(Unit):
    """
    A subclass of Unit representing a page

    Unlike generic unit, a page has a content that it can display.

    Content is a string that will be sent to the user in the body of the message
    """
    content: str

    def __init__(self, title="Page", content="", children: list['Unit'] = ()):
        super().__init__(title, children)
        self.content = content


class Button(Unit):
    """
    A subclass of Unit representing a custom action

    Unlike generic unit, a button can trigger a callback function.
    Callback function is an async function that takes ``aiogram.CallbackQuery`` as an argument.

    It can then perform any operation it deems necessary. For example: send user a message.

    Callbacks should be defined in callbacks.py.

    To link a button to a callback the name of the callback
    function should be added to the body of the ``<button>`` element
    """
    callback: callable

    def __init__(self, title="Action", callback=None):
        super().__init__(title)
        self.callback = callback
