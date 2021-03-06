'''
Popup
=====

.. versionadded:: 1.0.7

.. image:: images/popup.jpg
    :align: right

The :class:`Popup` widget is used to create modal popups. By default, the popup
will cover the whole "parent" window. When you are creating a popup, you must at
a minimum set a :data:`Popup.title` and a :data:`Popup.content` widget.

Remember that the default size of a Widget is size_hint=(1, 1). If you don't
want your popup to be fullscreen, either use lower than 1 size hints (for
instance size_hint=(.8, .8)) or deactivate the size_hint and use fixed size
attributes.


.. versionchanged:: 1.4.0
    The :class:`Popup` class now inherits from
    :class:`~kivy.uix.modalview.ModalView`.  The :class:`Popup` offers a default
    layout with a title and a separation bar.

Examples
--------

Example of a simple 400x400 Hello world popup::

    popup = Popup(title='Test popup',
        content=Label(text='Hello world'),
        size_hint=(None, None), size=(400, 400))

By default, any click outside the popup will dismiss it. If you don't
want that, you can set :data:`Popup.auto_dismiss` to False::

    popup = Popup(title='Test popup', content=Label(text='Hello world'),
                  auto_dismiss=False)
    popup.open()

To manually dismiss/close the popup, use :meth:`Popup.dismiss`::

    popup.dismiss()

The :meth:`Popup.open` and :meth:`Popup.dismiss` are bindable. That means you
can directly bind the function to an action, e.g., to a button's on_press::

    # create content and assign to the popup
    content = Button(text='Close me!')
    popup = Popup(content=content, auto_dismiss=False)

    # bind the on_press event of the button to the dismiss function
    content.bind(on_press=popup.dismiss)

    # open the popup
    popup.open()


Popup Events
------------

There are two events available: `on_open` when the popup is opening, and
`on_dismiss` when it is closed. For `on_dismiss`, you can prevent the
popup from closing by explictly returning True from your callback::

    def my_callback(instance):
        print('Popup', instance, 'is being dismissed, but is prevented!')
        return True
    popup = Popup(content=Label(text='Hello world'))
    popup.bind(on_dismiss=my_callback)
    popup.open()

'''

__all__ = ('Popup', 'PopupException')

from kivy.uix.modalview import ModalView
from kivy.properties import (StringProperty, ObjectProperty,
    NumericProperty, ListProperty)


class PopupException(Exception):
    '''Popup exception, fired when multiple content are added to the popup.

    .. versionadded:: 1.4.0
    '''


class Popup(ModalView):
    '''Popup class. See module documentation for more information.

    :Events:
        `on_open`:
            Fired when the Popup is opened
        `on_dismiss`:
            Fired when the Popup is closed. If the callback returns True, the
            dismiss will be canceled.
    '''

    title = StringProperty('No title')
    '''String that represents the title of the popup.

    :data:`title` is a :class:`~kivy.properties.StringProperty`, default to 'No
    title'.
    '''

    title_size = NumericProperty('14sp')
    '''Represents the font size of the popup title.

    .. versionadded:: 1.6.0

    :data:`title_size` is a :class:`~kivy.properties.NumericProperty`, default
    to '14sp'.
    '''

    content = ObjectProperty(None)
    '''Content of the popup that is displayed just under the title.

    :data:`content` is a :class:`~kivy.properties.ObjectProperty`, default to
    None.
    '''

    title_color = ListProperty([1, 1, 1, 1])
    '''Color used by the Title

    .. versionadded:: 1.8.0

    :data:`title_color` is a :class:`~kivy.properties.ListProperty`,
    default to [1, 1, 1, 1]
    '''

    separator_color = ListProperty([47 / 255., 167 / 255., 212 / 255., 1.])
    '''Color used by the separator between title and content.

    .. versionadded:: 1.1.0

    :data:`separator_color` is a :class:`~kivy.properties.ListProperty`,
    default to [47 / 255., 167 / 255., 212 / 255., 1.]
    '''

    separator_height = NumericProperty('2dp')
    '''Height of the separator.

    .. versionadded:: 1.1.0

    :data:`separator_height` is a :class:`~kivy.properties.NumericProperty`,
    default to 2dp.
    '''

    # Internals properties used for graphical representation.

    _container = ObjectProperty(None)

    def add_widget(self, widget):
        if self._container:
            if self.content:
                raise PopupException(
                        'Popup can have only one widget as content')
            self.content = widget
        else:
            super(Popup, self).add_widget(widget)

    def on_content(self, instance, value):
        if not hasattr(value, 'popup'):
            value.create_property('popup')
        value.popup = self
        if self._container:
            self._container.clear_widgets()
            self._container.add_widget(value)

    def on__container(self, instance, value):
        if value is None or self.content is None:
            return
        self._container.clear_widgets()
        self._container.add_widget(self.content)

    def on_touch_down(self, touch):
        if self.disabled and self.collide_point(*touch.pos):
            return True
        return super(Popup, self).on_touch_down(touch)


if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.gridlayout import GridLayout
    from kivy.core.window import Window

    # add popup
    content = GridLayout(cols=1)
    content_cancel = Button(text='Cancel', size_hint_y=None, height=40)
    content.add_widget(Label(text='This is a hello world'))
    content.add_widget(content_cancel)
    popup = Popup(title='Test popup',
                  size_hint=(None, None), size=(256, 256),
                  content=content, disabled=True)
    content_cancel.bind(on_release=popup.dismiss)

    layout = GridLayout(cols=3)
    for x in range(9):
        btn = Button(text=str(x))
        btn.bind(on_release=popup.open)
        layout.add_widget(btn)

    Window.add_widget(layout)

    popup.open()

    runTouchApp()
