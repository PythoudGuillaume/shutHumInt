from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import NumericProperty
import kivy

from pulsectl import Pulse, PulseVolumeInfo
import pulsectl


class Container(BoxLayout):

    slider_val = NumericProperty(0)


    def __init__(self, *args, **kwargs):
        super(Container, self).__init__(*args, **kwargs)
        self.orientation = 'vertical'

        self.speakers = []
        self.pulse = pulsectl.Pulse()
        sinks = self.pulse.sink_list()
        for s in sinks:
            if s.name != 'combined':
                self.speakers.append(s)

        self.sink = sinks[0]
        self.speakers_order = [(0,0),(0,1),(1,0),(1,1)]


        self.slide = Slider(min=-1, max=1, value=0)
        self.slide.fbind('value', self.on_slider_val)

        but_reset = Button(text='RESET_BAL')
        but_reset.bind(on_press=self.slide_to_z)

        self.label = Label(text=str(self.slider_val))

        self.speaker_inf = Label()
        self.update_speak_info()

        self.add_widget(self.slide)
        self.add_widget(self.label)
        self.add_widget(self.speaker_inf)
        self.add_widget(but_reset)

    def on_slider_val(self, instance, val):
        self.label.text = str(val)
        vol = self.sink.volume.values
        l,r = vol
        m = (l + r)/2
        l = m - val*m
        r = m + val*m
        vol = PulseVolumeInfo([l,r])
        print(vol)
        try:
            self.pulse.volume_set(self.sink, vol)
        except:
            print("lol volume change error")

        self.update_speak_info()


    def slide_to_z(self, instance):
        self.slide.value = 0

        self.update_speak_info()

    def update_speak_info(self):
        speak_vol = ""
        for t in self.speakers_order:
            s,c = t
            speak_vol += (str(self.speakers[s].index) + " " + str(self.speakers[s].volume.values[c]) + "\n")
        self.speaker_inf.text = speak_vol

class app(App):

    def build(self):
        return Container()


app().run()
