from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.transition import MDFadeSlideTransition
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivymd.uix.spinner import MDSpinner
import requests
from Home import Home_Screen

Window.size = [360,540]
Builder.load_file("main.kv")

store = JsonStore('app.json')

class Login_Screen(MDScreen):

    name = "login_screen"
    def __init__(self,**kwargs):
        super(Login_Screen,self).__init__(**kwargs)
        # self.background = "assests/images/background/auth-bg.png"

    def __str__(self):
        return "Login Screen"

    def password_validate(self,pass_instance):
        if(len(pass_instance.text) < 8 or len(pass_instance.text)>15):
            pass_instance.error = True
            pass_instance.helper_text = "invalid password"
            pass_instance.helper_text_mode = "on_error"
            return False
        else:
            pass_instance.error = False
            pass_instance.helper_text = ""
            pass_instance.color_mode = "custom"
            pass_instance.line_color_focus = "#28a745"

            pass_instance.helper_text_mode = "on_focus"
            return True

    def username_validate(self,user_instance):
        if(len(user_instance.text) == 0):
            user_instance.error = True
            user_instance.helper_text = "invalid username"
            user_instance.helper_text_mode = "on_error"
            return False
        else:
            user_instance.error = False
            user_instance.helper_text = ""
            user_instance.helper_text_mode = "on_focus"
            user_instance.color_mode = "custom"
            user_instance.line_color_focus = "#28a745"
            return True

    def show_error(self,instance,msg):
        instance.error = True
        instance.helper_text = msg
        instance.helper_text_error = "on_error"

    def enable_disable_spinner(self):
        self.ids.loading.active = False if self.ids.loading.active else True
        self.ids.login_button.text = "Login" if self.ids.login_button.text == "" else ""



    def authenticate(self):
        pass_instance = self.ids.password
        user_instance = self.ids.username
        if self.username_validate(user_instance) and self.password_validate(pass_instance):
            try:
                self.enable_disable_spinner()
                response = requests.post(url="http://127.0.0.1:8000/api/api-auth-token/",data={'username':user_instance.text,'password':pass_instance.text})

                try:
                    self.remove_widget(self.ids.error_1)
                    self.remove_widget(self.ids.error_2)
                except:
                    pass

                if response.status_code == 200:
                    token = response.json().get('token')
                    store.put('token',value = token)
                    store.put('user',username=user_instance.text)
                    #put token in a file
                    self.parent.add_widget(Pre_Enter_Screen())
                    self.manager.transition = MDFadeSlideTransition()
                    self.manager.current = "pre_enter_screen"

                elif response.status_code == 400:
                    self.show_error(pass_instance,"password may not valid")
                    self.show_error(user_instance,"username may not be valid")


                else:
                    self.add_widget(
                        MDLabel(
                        id = "error_1",
                        halign = "center",
                        pos_hint = {'center_x':.5,'center_y':.56},
                        text =  "Some error occurred try again later",
                        theme_text_color = "error",
                        font_size = "13sp"
                        ))

                self.enable_disable_spinner()

            except Exception as ex:
                print(ex)
                self.add_widget(
                    MDLabel(
                        id = "error_2",
                        halign = "center",
                        pos_hint={'center_x': .5, 'center_y': .56},
                        text="Connection error check your internet",
                        theme_text_color="Error",
                        font_size="13sp"
                    )
                )
                self.enable_disable_spinner()


class Register_Screen(MDScreen):
    name= "register_screen"
    def __init__(self,**kwargs):
        super(Register_Screen,self).__init__(**kwargs)

    def __str__(self):
        return "Register Screen"




class Pre_Enter_Screen(MDScreen):
    name = "pre_enter_screen"
    def __init__(self,**kwargs):
        super(Pre_Enter_Screen, self).__init__(**kwargs)
        self.token = store.get('token')['value']
        self.get_post()

    def __str__(self):
        return "Pre Enter Screen"

    def change_screen(self,dt):
        self.parent.add_widget(Home_Screen())
        self.manager.current = "home_screen"

    def get_post(self):
        try:
            username = store.get('user')['username']
            post_response = requests.get(url ="http://127.0.0.1:8000/api/post-list/",headers={'Authorization':f'Token {self.token}'})
            profile_response = requests.get(url=f"http://127.0.0.1:8000/api/profile/{username}",headers={'Authorization':f'Token {self.token}'})

            if post_response.status_code == 200:
                store.put('posts',data= post_response.json())

            if profile_response.status_code == 200:
                store.put('profile',data=profile_response.json())
                print(profile_response.json())

            Clock.schedule_once(
                    self.change_screen,4
                )


        except Exception as ex:
            print(ex)



class App_Screen(MDScreenManager):
    def __init__(self,**kwargs):
        super(App_Screen,self).__init__(**kwargs)

    def __str__(self):
        return "App Screen"


class App_Runner(MDApp):
    def build(self):
        self.title = "Angalo"
        self.theme_cls.primary_palette = "Blue"
        self.icon = "assets/images/logo-24x24.png"
        return App_Screen()



        return self.scm
if __name__ =="__main__":
    App_Runner().run()