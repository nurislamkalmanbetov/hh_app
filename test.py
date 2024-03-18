from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.utils import platform
import webbrowser

class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 1
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Белый фон
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Заголовок
        title = Label(text="Заголовок", font_size='30sp', color=(0, 0, 0, 1), size_hint_y=None, height=100)
        self.add_widget(title)

        # Кнопки
        btn_js = Button(text="Перейти на YouTube (JavaScript)", size_hint_y=None, height=100)
        btn_js.bind(on_press=self.open_youtube_js)
        self.add_widget(btn_js)

        btn_kids = Button(text="Перейти на YouTube (дети)", size_hint_y=None, height=100)
        btn_kids.bind(on_press=self.open_youtube_kids)
        self.add_widget(btn_kids)

        # Маленький текст
        small_text = Label(text="Маленький текст", font_size='12sp', color=(0, 0, 0, 1))
        self.add_widget(small_text)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def open_youtube_js(self, instance):
        if platform == 'android':
            webbrowser.open("https://www.youtube.com", autoraise=True)
        else:
            print("Открытие браузера не поддерживается на данной платформе.")

    def open_youtube_kids(self, instance):
        if platform == 'android':
            webbrowser.open("https://www.youtube.com/kids", autoraise=True)
        else:
            print("Открытие браузера не поддерживается на данной платформе.")

class MyApp(App):
    def build(self):
        return MyGrid()

if __name__ == "__main__":
    MyApp().run()
