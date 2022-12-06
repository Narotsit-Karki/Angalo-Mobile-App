from kivy.storage.jsonstore import JsonStore
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel
from kivy.uix.image import AsyncImage
from kivymd.uix.boxlayout import BoxLayout,MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import ImageLeftWidget
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard, MDSeparator
from kivy.lang import Builder
from kivymd.uix.behaviors import CommonElevationBehavior
Builder.load_file('Home.kv')


store = JsonStore('app.json')





class PostCard(MDCard,CommonElevationBehavior):
    pass

class SideNavigationContent(MDBoxLayout):
    pass
# class Profile_Grid():
#     def __init__(self,**kwargs):
#         super(Profile_Grid, self).__init__(**kwargs)
#         for i in range(30):
#             self.add_widget(
#                 self
#             )
#             self.text = "item " + i
class Async_Angalo_Image(AsyncImage):
    pass

class Side_Profile_Pic(ImageLeftWidget,AsyncImage):
    pass



class Home_Screen_Tab(ScrollView):
    def __init__(self,**kwargs):
        super(Home_Screen_Tab, self).__init__(**kwargs)
        # self.add_widget(Profile_Grid()

class Home_Screen(MDScreen):
    name = "home_screen"
    def __init__(self,**kwargs):
        super(Home_Screen,self).__init__(**kwargs)
        self.profile = store.get('profile')['data']
        self.ids.side_profile.text = self.profile['username']
        self.ids.side_profile_pic.source = "http://127.0.0.1:8000"+self.profile['profile_pic']
