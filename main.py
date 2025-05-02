from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner


# Function for Camel Zakat Calculation
def zakat_camel(camels):
    if 121 < camels < 130:
        camels = 121
    elif camels >= 130:
        camels = (camels // 10) * 10  # Round down to nearest ten

    if camels < 5:
        return "0 Zakat Due"
    elif camels < 10:
        return "1 sheep"
    elif camels < 15:
        return "2 sheep"
    elif camels < 20:
        return "3 sheep"
    elif camels < 25:
        return "4 sheep"
    elif camels < 36:
        return "1 Bint Makhad (1-year-old camel)"
    elif camels < 46:
        return "1 Bint Labun (2-year-old camel)"
    elif camels < 61:
        return "1 Hiqqah (3-year-old camel)"
    elif camels < 76:
        return "1 Jadh’ah (4-year-old camel)"
    elif camels < 91:
        return "2 Bint Labun (2-year-old camel)"
    elif camels < 121:
        return "2 Hiqqah (3-year-old camel)"
    elif camels == 121:
        return "3 Bint Labun (2-year-old camel)"
    else:
        combinations = []
        for hiqqah in range(camels // 50 + 1):
            for bint_labun in range(camels // 40 + 1):
                if (hiqqah * 50 + bint_labun * 40) == camels:
                    combinations.append(f"{hiqqah} Hiqqah (3-year-old camel), {bint_labun} Bint Labun (2-year-old camel)")
        if combinations:
            return "\n".join(combinations)
        else:
            return f"No exact 40/50 combination for {camels} camels (consult scholar)"


# Function for Cow Zakat Calculation
def zakat_cow(cows):
    if cows > 70:
        cows = (cows // 10) * 10  # Round down to nearest 10

    if cows < 30:
        return "0 Zakat Due"
    elif cows < 40:
        return "1 Tabi’ (1-year-old calf)"
    elif cows < 60:
        return "1 Musina (2-year-old cow)"
    elif cows < 70:
        return "2 Tabi’ (1-year-old calf)"
    else:
        combinations = []
        for musina in range(cows // 40 + 1):
            remaining = cows - (musina * 40)
            if remaining % 30 == 0:
                tabi = remaining // 30
                combinations.append(f"{musina} Musina(s), {tabi} Tabi’(s)")
        if combinations:
            return "\n".join(combinations)
        else:
            return f"No exact 30/40 combination for {cows} cows (consult scholar)"


# Function for Sheep Zakat Calculation
def zakat_sheep(sheep):
    if sheep < 40:
        return "0 Zakat"
    elif sheep <= 120:
        return "1 sheep"
    elif sheep <= 200:
        return "2 sheep"
    else:
        return f"{sheep // 100} sheep"


# Function for Agricultural Product Zakat Calculation
def zakat_agricultural(agri_qty, irrigation_type):
    nisab = 611  # Nisab for agricultural products (5 wasaq = 611 kg)
    if agri_qty < nisab:
        return "No Zakat Due"
    if irrigation_type == 'effort':
        zakat_rate = 1 / 20
    elif irrigation_type == 'rain':
        zakat_rate = 1 / 10
    else:
        zakat_rate = 3 / 40  # Combination of effort and rain

    zakat_due = agri_qty * zakat_rate
    return f"Zakat Due: {zakat_due} kg"


# Function for Gold Zakat Calculation
def zakat_gold(gold_qty):
    nisab_gold = 85  # Nisab for gold (in grams)
    if gold_qty < nisab_gold:
        return "No Zakat Due"
    return f"Zakat Due: {gold_qty * 0.025} grams"


# Function for Silver Zakat Calculation
def zakat_silver(silver_qty):
    nisab_silver = 595  # Nisab for silver (in grams)
    if silver_qty < nisab_silver:
        return "No Zakat Due"
    return f"Zakat Due: {silver_qty * 0.025} grams"


# Function for Cash Zakat Calculation
def zakat_cash(cash_qty):
    nisab_cash = 3000  # Approximate cash Nisab in value (depends on currency)
    if cash_qty < nisab_cash:
        return "No Zakat Due"
    return f"Zakat Due: {cash_qty * 0.025} units"


# Kivy App UI
class ZakatCalculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.input = TextInput(hint_text='Enter number of camels, cows, sheep, gold, silver, cash, or agricultural qty', multiline=False)
        self.result = Label(text='Zakat will appear here')

        # Spinner for irrigation type selection
        self.irrigation_spinner = Spinner(
            text='Select Irrigation Type',
            values=('effort', 'rain', 'both'),
            size_hint=(None, None),
            size=(200, 44)
        )

        self.add_widget(self.input)
        self.add_widget(self.irrigation_spinner)

        # Buttons for different types of Zakat
        self.camel_button = Button(text='Calculate Zakat for Camels')
        self.camel_button.bind(on_press=self.calculate_camel)

        self.cow_button = Button(text='Calculate Zakat for Cows')
        self.cow_button.bind(on_press=self.calculate_cow)

        self.sheep_button = Button(text='Calculate Zakat for Sheep')
        self.sheep_button.bind(on_press=self.calculate_sheep)

        self.agri_button = Button(text='Calculate Zakat for Agricultural Products')
        self.agri_button.bind(on_press=self.calculate_agricultural)

        self.gold_button = Button(text='Calculate Zakat for Gold')
        self.gold_button.bind(on_press=self.calculate_gold)

        self.silver_button = Button(text='Calculate Zakat for Silver')
        self.silver_button.bind(on_press=self.calculate_silver)

        self.cash_button = Button(text='Calculate Zakat for Cash')
        self.cash_button.bind(on_press=self.calculate_cash)

        self.add_widget(self.camel_button)
        self.add_widget(self.cow_button)
        self.add_widget(self.sheep_button)
        self.add_widget(self.agri_button)
        self.add_widget(self.gold_button)
        self.add_widget(self.silver_button)
        self.add_widget(self.cash_button)
        self.add_widget(self.result)

    def calculate_camel(self, instance):
        try:
            num = int(self.input.text)
            result = zakat_camel(num)
            self.result.text = result
        except:
            self.result.text = "Invalid input"

    def calculate_cow(self, instance):
        try:
            num = int(self.input.text)
            result = zakat_cow(num)
            self.result.text = result
        except:
            self.result.text = "Invalid input"

    def calculate_sheep(self, instance):
        try:
            num = int(self.input.text)
            result = zakat_sheep(num)
            self.result.text = result
        except:
            self.result.text = "Invalid input"

    def calculate_agricultural(self, instance):
        try:
            qty = int(self.input.text)
            irrigation_type = self.irrigation_spinner.text.lower()
            result = zakat_agricultural(qty, irrigation_type)
            self.result.text = result
        except:
            self.result.text = "Invalid input"

    def calculate_gold(self, instance):
        try:
            qty = float(self.input.text)
            result = zakat_gold(qty)
            self.result.text = result
        except:
            self.result.text = "Invalid input"

    def calculate_silver(self, instance):
        try:
            qty = float(self.input.text)
            result = zakat_silver(qty)
            self.result.text = result
        except:
            self.result.text = "Invalid input"

    def calculate_cash(self, instance):
        try:
            qty = float(self.input.text)
            result = zakat_cash(qty)
            self.result.text = result
        except:
            self.result.text = "Invalid input"


# Kivy App
class ZakatApp(App):
    def build(self):
        return ZakatCalculator()


if __name__ == '__main__':
    ZakatApp().run()
