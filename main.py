__version__ = "1.0.0"

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.utils import get_color_from_hex


class CalculatorApp(App):
    def build(self):
        self.title = "PyCalc"
        self.expression = ""
        self.just_evaluated = False

        # Desktop preview size; Android uses the device's screen size.
        Window.clearcolor = get_color_from_hex("#10131A")
        Window.size = (360, 640)

        root = BoxLayout(
            orientation="vertical",
            padding=14,
            spacing=12,
        )

        heading = Label(
            text="[b]PyCalc[/b]",
            markup=True,
            font_size="22sp",
            color=get_color_from_hex("#AAB4C8"),
            size_hint_y=0.10,
            halign="left",
            valign="middle",
        )
        heading.bind(size=lambda widget, size: setattr(widget, "text_size", size))
        root.add_widget(heading)

        self.display = Label(
            text="0",
            font_size="42sp",
            color=get_color_from_hex("#FFFFFF"),
            size_hint_y=0.22,
            halign="right",
            valign="middle",
            shorten=True,
            text_size=(Window.width - 30, None),
        )
        self.display.bind(size=lambda widget, size: setattr(widget, "text_size", size))
        root.add_widget(self.display)

        keys = [
            ["AC", "DEL", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["±", "0", ".", "="],
        ]
        grid = GridLayout(cols=4, spacing=8, size_hint_y=0.68)

        for row in keys:
            for key in row:
                button = Button(
                    text=key,
                    font_size="24sp",
                    background_normal="",
                    background_color=self.button_color(key),
                    color=get_color_from_hex("#FFFFFF"),
                )
                button.bind(on_release=lambda instance, value=key: self.on_key(value))
                grid.add_widget(button)

        root.add_widget(grid)
        return root

    def button_color(self, key):
        if key == "=":
            return get_color_from_hex("#5B8CFF")
        if key in {"AC", "DEL", "%", "±"}:
            return get_color_from_hex("#343B4A")
        if key in {"÷", "×", "−", "+"}:
            return get_color_from_hex("#253B5C")
        return get_color_from_hex("#1B202B")

    def on_key(self, key):
        if key == "AC":
            self.expression = ""
            self.just_evaluated = False
            self.update_display()
            return

        if key == "DEL":
            self.expression = self.expression[:-1]
            self.just_evaluated = False
            self.update_display()
            return

        if key == "=":
            self.calculate()
            return

        if key == "±":
            if self.expression.startswith("-"):
                self.expression = self.expression[1:]
            elif self.expression:
                self.expression = "-" + self.expression
            self.just_evaluated = False
            self.update_display()
            return

        if key == "%":
            # Convert the current trailing number into a percentage.
            try:
                import re
                match = re.search(r"(\d+(?:\.\d*)?|\.\d+)$", self.expression)
                if match:
                    number = float(match.group(0)) / 100
                    self.expression = self.expression[:match.start()] + str(number)
            except (ValueError, OverflowError):
                pass
            self.just_evaluated = False
            self.update_display()
            return

        if self.just_evaluated and key not in {"÷", "×", "−", "+"}:
            self.expression = ""

        self.just_evaluated = False
        translated = {"÷": "/", "×": "*", "−": "-"}.get(key, key)

        if translated in {"+", "-", "*", "/"}:
            if not self.expression and translated != "-":
                return
            if self.expression and self.expression[-1] in "+-*/":
                self.expression = self.expression[:-1]
        self.expression += translated
        self.update_display()

    def update_display(self):
        shown = self.expression.replace("/", " ÷ ").replace("*", " × ").replace("-", " − ").replace("+", " + ")
        self.display.text = shown or "0"

    def calculate(self):
        if not self.expression:
            return
        # Only arithmetic characters are allowed; no eval of arbitrary input.
        allowed = set("0123456789.+-*/() ")
        if any(character not in allowed for character in self.expression):
            self.display.text = "Invalid input"
            return
        try:
            result = eval(self.expression, {"__builtins__": {}}, {})
            if isinstance(result, float) and not (float("-inf") < result < float("inf")):
                raise ValueError("Non-finite result")
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.expression = str(result)
            self.display.text = str(result)
            self.just_evaluated = True
        except ZeroDivisionError:
            self.display.text = "Cannot divide by zero"
            self.expression = ""
            self.just_evaluated = False
        except (SyntaxError, ValueError, TypeError, OverflowError):
            self.display.text = "Error"
            self.expression = ""
            self.just_evaluated = False


if __name__ == "__main__":
    CalculatorApp().run()
