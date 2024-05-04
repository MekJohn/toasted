
"""
Windows Toast Notification.
See at: https: //learn.microsoft.com/en-us/windows/apps/design/
        shell/tiles-and-notifications/adaptive-interactive-toasts?tabs=appsdk
"""


# general
import os as os
import datetime as dt
import platform as pt
import enum as en

# xml document packages
from xml.etree import ElementTree as xe
import winsdk.windows.data.xml.dom as wx

# specific
import winsdk as wk
import winsdk.windows.foundation as wf
import winsdk.windows.ui.notifications as wn




class Element(xe.Element):

    def __init__(self, tag: str, text="", **attributes):
        super().__init__(tag, **attributes)
        self.text = text

    @classmethod
    def from_Wxml(cls, element: wx.XmlElement):
        """
        Create a new xml element (first level object)
        """
        tag: str = element.tag_name
        text: str = element.inner_text
        attributes = element.attributes
        return cls(tag, text=text, **attributes)


    @classmethod
    def from_str(cls, xml: str):
        document = xe.ElementTree.parse(xml)
        return document

    @property
    def indented(self):
        # get xml string and send it to the parser
        str_tree = str(self)
        temp_element = xe.XML(str_tree)
        # indent it and cast in string
        xe.indent(temp_element)
        indented_xml = xe.tostring(temp_element, encoding="unicode")
        return indented_xml

    def __str__(self):
        # get indented string xml
        xml_string = xe.tostring(self, encoding="unicode")
        return xml_string

    def __repr__(self):
        return self.indented


class Tree(xe.ElementTree):

    def __init__(self, source = None):
        winXml = wx.XmlElement, wx.XmlDocument
        if isinstance(source, Element):
            super().__init__(source)
        elif isinstance(source, winXml):
            tree = winXml.get_xml()
            super().__init__(tree)
        elif isinstance(source, str):
            is_xml = os.path.splitext(source)[1] in (".xml", ".txt")
            if os.path.isfile(source) and is_xml:
                super().parse(source)
            else:
                # if is a string try to load by string parser
                # otherwise init an empty root tag element
                try:
                    tree = xe.XML(source)
                    super().__init__(tree)
                except xe.ParseError:
                    default_tag = Element(source[:10])
                    super().__init__(default_tag)
        else:
            # if is None or whatever init
            # a default tag empty element
            root = Element("root")
            super().__init__(root)

    @property
    def indented(self):
        # get xml string and send it to the parser
        str_tree = str(self)
        temp_element_tree = xe.XML(str_tree)
        # indent it and cast in string
        xe.indent(temp_element_tree)
        indented_xml = xe.tostring(temp_element_tree, encoding="unicode")
        return indented_xml

    @property
    def root(self):
        """
        Get the entire root element
        """
        return self.getroot()

    def set(self, node: str, key: str, value: str):
        """
        Set attributes to the first node tag or to the specified node path
        """
        root = self.root
        node = root if node == root.tag else self.find(node)
        node = self.root if node is None else node
        node.set(key, value)
        return node

    def move(self, from_path: str, to_path: str):
        """
        Move element
        """
        # TODO da finire
        parent, element = from_path.rsplit("/", 1)
        copied = parent.copy()
        parent.remove(from_path)




    def __str__(self):
        # get indented string xml
        root_element: Element = self.getroot()
        xml_string = xe.tostring(root_element, encoding="unicode")
        return xml_string

    def __repr__(self):
        return self.indented


class Event(list):

    def __init__(self, notification, handler):
        super().__init__()
        event = notification, handler
        self.append(event)


    @property
    def active(toast):
        toast.add

    @property
    def is_ignored(self):
        pass

    @property
    def is_failed(self):
        pass

    @staticmethod
    def Activated(event):
        return wn.ToastActivatedEventArgs._from(event)

    @staticmethod
    def Dismissed(event):
        return wn.ToastDismissedEventArgs._from(event)

    @staticmethod
    def Failed(event):
        return wn.ToastFailedEventArgs._from(event)


    @classmethod
    def Dismiss():
        pass

    @classmethod
    def Fault():
        pass




class Audio(str):

    ROOT = "ms-winsoundevent:"

    RPATH = "Notification."
    SAMPLES_1 = "Default", "IM", "Mail", "Reminder", "SMS"

    LPATH = "Notification.Looping."
    SAMPLES_2 = "Alarm", *(f"Alarm{i}" for i in range(2, 11))
    SAMPLES_3 = "Call", *(f"Call{i}" for i in range(2, 11))

    SAMPLES = *SAMPLES_1, *SAMPLES_2, *SAMPLES_3

    def __new__(cls, path: str = ""):
        path = cls.abspath(path)
        return None if path is None else str.__new__(cls, path)

    @property
    def send():
        return True

    @staticmethod
    def listaudio():
        for i,s in enumerate(Audio.SAMPLES):
            audiotype = Audio.RPATH if i <= 4 else Audio.LPATH
            audio = Audio.ROOT + audiotype + s
            yield audio


    @staticmethod
    def abspath(path: str):
        abs_audiopath = None
        # get abs file path if is a file
        if os.path.isfile(path):
            abs_audiopath = os.path.abspath(path)
        else:
            # otherwise search for default win audios
            path = path.split(".")[-1].lower()
            for default_path in Audio.listaudio():
                default_name = default_path.split(".")[-1].lower()
                if path == default_name:
                    abs_audiopath = default_path
                    break
        return abs_audiopath


    @classmethod
    def ring(cls, number: int = 1):
        root = cls.ROOT + cls.RPATH
        number = min(abs(number), 5)
        path = root + cls.SAMPLES_1[0] if number in (0, 1) else root + cls.SAMPLES_1[number - 1]
        return cls(path)

    @classmethod
    def loop(cls, number: int = 1):
        root = cls.ROOT + cls.LPATH
        number = min(abs(number), 10)
        path = root + cls.SAMPLES_3[0] if number in (0, 1) else root + cls.SAMPLES_3[number - 1]
        return cls(path)

    @classmethod
    def Default(cls):
        return cls.ring(0)

    @classmethod
    def IM(cls):
        return cls.ring(1)

    @classmethod
    def Mail(cls):
        return cls.ring(2)

    @classmethod
    def Reminder(cls):
        return cls.ring(3)

    @classmethod
    def Sms(cls):
        return cls.ring(4)

    @classmethod
    def Alarm(cls, number: int = 1):
        return cls.ring(number)

    @classmethod
    def Call(cls, number: int = 1):
        return cls.loop(number)





class Toast:

    """
    Intro:  www.learn.microsoft.com/en-us/windows/apps/design/shell/
            tiles-and-notifications/toast-notifications-overview

    The term 'toast notification' is being replaced with 'app notification'.
    These terms both refer to the same feature of Windows,
    but over time we will phase out the use of "toast notification" also in the documentation.
    """

    DEFAULT_APPID: str = "Python"
    ROOT: str = "toast"

    PRIORITY_LOW: int = 0
    PRIORITY_HIGH: int = 1

    DURATION_SHORT: str = "short" # 7 seconds
    DURATION_LONG: str = "long" # permanent




    def __init__(self, document = None, app_id: str = "Python"):
        # init the main document content
        # TODO init should be manage simple empty tree
        # TODO init shold be manage the correct order of nodes:
        #       - all input should be placed before all action
        self.xml = document if isinstance(document, Tree) else Tree("toast")

        # default toast settings functionality
        self.xml.set(self.ROOT, "launch", "http:")
        self.xml.set(self.ROOT, "activationType", "protocol")
        self.timestamp()

        self.xml.set(self.ROOT, "useButtonStyle", "true")
        # self.xml.set("scenario", "incomingCall") # fa una breve musichetta tipo suoneria

        self.id = 0             # id number is needed when you want to group similar toasts
        self.group = ""         # unique identification toast group name string
        self.tag = ""           # unique identification toast tag family within a group
        self.data = dict()      # keys and values that could be updated in binding type toast
        self.seq_number = 0     # progressive number used to determine whether the notification data is out-of-date


        self.event_args = None
        self.event_input = None


        self.priority = Toast.PRIORITY_LOW
        self.exipire_on_reboot = False
        self.exipire_on_time = 1200
        self.manager = wn.ToastNotificationManager
        self.app_id: str = "Python" if app_id is None else app_id


    @property
    def visual(self):
        """
        Get visual element
        """
        return self.xml.find("./visual")

    @property
    def binding(self):
        """
        Get binding element
        """
        return self.xml.find("./visual/binding")


    @property
    def actions(self):
        """
        Get actions element
        """
        return self.xml.find("./actions")


    @property
    def Wxml(self):
        """
        Get Windows SDK XmlDocument class object
        """
        xml_string = str(self.xml)
        win_doc = wx.XmlDocument()
        win_doc.load_xml(xml_string)
        return win_doc


    @property
    def notification(self) -> wn.ToastNotification:
        # create native notification from xml document
        notification = wn.ToastNotification(self.Wxml)
        # add activator type event
        subscription = self.subscription
        subs_number = notification.add_activated(subscription)
        print(subs_number.value)
        return notification


    def subscription(self, notification, user_response):
        """
        Handler function that subscribe the app to user events.
        When event happend, this function will be called in order
        to update Toast's event attributes
        """
        # init the event function
        listener = wn.ToastActivatedEventArgs._from
        # and a cast factory function for win Object
        to_string = lambda val: wf.IPropertyValue._from(val).get_string()
        # get event contents
        user_args = listener(user_response).arguments
        user_inputs = listener(user_response).user_input
        # set the event attributes
        # for the arguments
        if user_args != "":
            self.event_args = user_args
        else:
            self.event_args = None
        # and for the inputs
        if user_inputs.size > 0:
            self.event_input = {k: to_string(v) for k,v in user_inputs.items()}
        else:
            self.event_input = None
        # return raw contents
        return notification, user_args, user_inputs

    @staticmethod
    def Section(tag: str, **attributes) -> Element:
        section = Element(tag, **attributes)
        return section

    @staticmethod
    def Visual(**attributes) -> Element:
        visual = Toast.Section("visual", **attributes)
        return visual

    @staticmethod
    def Binding(*elements: Element, **attributes) -> Element:
        binding = Toast.Section("binding", **attributes)
        binding.set("template", "ToastGeneric")
        binding.extend(elements)
        return binding

    @staticmethod
    def Actions(*elements: Element, **attributes) -> Element:
        actions = Toast.Section("actions", **attributes)
        actions.extend(elements)
        return actions

    @staticmethod
    def Audio(source: str, loop: bool = False, silent: bool = False) -> Element:
        """
        Create the xml Audio element for the toast.

        Parameters
        ----------

        source : str
            The media file to play in place of the default sound.
            On Windows, this attribute can have one of the default string values.
            See the class Audio.

        loop : bool, optional
            Set to true if the sound should repeat as long as the toast is shown; false to play only once.
            If this attribute is set to true, the duration attribute in the toast element must also be set.
            There are specific sounds provided to be used when looping.
            Selecting loop to True windows stop all other sounds.
            The default is False.

        silent : bool, optional
            True to mute all toast sound; false to allow the toast notification sound to play.
            The default is False.

        Returns
        -------
        audio : Element
            Element object to be used to compose the xml tree for the toast.

        """
        # init the element
        audio = Element("audio")
        # set default attributes
        sample = Audio(source)
        if sample is not None:
            audio.set("src", sample)
        # set specific attributes
        if loop is True:
            audio.set("loop", "true")
        if silent is True:
            audio.set("silent", "true")
        return audio



    @staticmethod
    def Event(event: object):
        # TODO deve gestire gli eventi
        # notification prò essere attivato, dismesso ecc mediante apposito suoi metodi
        # ToastActivatedEventArgs._from(...) inizializza la classe omonima e setta i metodi
        # 'arguments' che contiene la sorgente e 'user_input' che contiene i valori
        # che contengono i dati, mentre
        # la lambda restituisce una wf.EventRegistrationToken (?)
        # questi metodi
        return


    def header(self, id_number: int = 0, title = ""):
        """
        Used to group notifications under headers within Notification Center.
        """
        idn = f"{id_number:0>4}"
        self.xml.set("id", idn)
        self.xml.set("title", title)
        self.xml.set("arguments", f"action=openConversation&amp;id={idn}")
        return True

    @staticmethod
    def is_toast_compatible():
        """
        Determine wheter or not the system is capable to send toast notification
        """
        # compatibility
        MIN_WIN_BUILD = 10240
        # check to platform info
        platform = pt.system()
        build = pt.version()
        check = False
        # determine the capability
        if platform == "Windows":
            build_number = int(build.split(".")[2])
            check = True if build_number >= MIN_WIN_BUILD else False
        return check



    def timestamp(self, datetime: str = "", timezone: str = "+00:00") -> dt.datetime:
        """
        Set the timestamp of the toast.
        Keep and set time in UTC, Win will takes care to convert in local time.

        Format:     YYYY-MM-DD HH:MM:SS
        Example:    2024-06-25 11:02:54
        """
        time = dt.datetime.now() if datetime == "" else dt.datetime.fromisoformat(datetime)
        stamp = time.strftime("%Y-%m-%dT%H:%M:%S") + timezone
        self.xml.set(self.ROOT, "displayTimestamp", stamp)
        return time


    @staticmethod
    def SubGroup(*elements: Element) -> Element:
        """
        Specifies vertical columns that can contain text and images.
        """
        column = Element("subgroup")
        column.extend(elements)
        return column

    @staticmethod
    def Group(*subgroups: Element) -> Element:
        """
        Semantically identifies that the content in the group must either be
        displayed as a whole, or not displayed if it cannot fit.
        Groups also allow creating multiple columns.
        """
        group = Element("group")
        group.extend(subgroups)
        return group

    @staticmethod
    def Text(text: str, rich: bool = True,
             align: str = "default", style: str = "default", minline: int = 1, maxline: int = 2,
             attribution: bool = False, **attributes):
        """
        An adaptive text element.
        If placed in the top level ToastBindingGeneric.Children, only HintMaxLines
        will be applied. But if this is placed as a child of a group/subgroup,
        full text styling is supported.

        If you need to reference the source of your content, you can use ATTRIBUTION text.
        This text is always displayed below any text elements, but above inline images.
        The text uses a slightly smaller size than standard text elements to help to
        distinguish from regular text elements. On older versions of Windows that don't
        support attribution text, the text will simply be displayed as another text
        element (assuming you don't already have the maximum of three text elements).

        align:                  Only with 'rich' set to True
            default:            Default value. Alignment is automatically determined by the renderer.
            auto:               Alignment determined by the current language and culture.
            left:               To the left
            center:             In the middle
            left:               To the left

        style:                  Only with 'rich' set to True
            default:            Default value. Style is determined by the renderer.
            caption:            Smaller than paragraph font size.
            captionSubtle:      Same as Caption but with subtle opacity.
            body:               Paragraph font size.
            bodySubtle:         Same as Body but with subtle opacity.
            base:               Paragraph font size, bold weight. Essentially the bold version of Body.
            baseSubtle:         Same as Base but with subtle opacity.
            subtitle:           H4 font size.
            subtitleSubtle:     Same as Subtitle but with subtle opacity.
            title:              H3 font size.
            titleSubtle:        Same as Title but with subtle opacity.
            titleNumeral:       Same as Title but with top/bottom padding removed.
            subheader:          H2 font size.
            subheaderSubtle:    Same as Subheader but with subtle opacity.
            subheaderNumeral	Same as Subheader but with top/bottom padding removed.
            header:             H1 font size.
            headerSubtle:       Same as Header but with subtle opacity.
            headerNumeral:      Same as Header but with top/bottom padding removed.

        -- attributes --
        placement:
            - attribution       (bottom text that could indicate the source of notification)

        More on:    learn.microsoft.com/en-us/windows/apps/design/
                    shell/tiles-and-notifications/toast-schema#adaptivetext
        """
        text = Element("text", text=text, **attributes)
        # attribution text type
        if attribution is True:
            text.set("placement", "attribution")
        if rich is True:
            text.set("hint-align", align)
            text.set("hint-style", style)
            text.set("hint-minLines", str(minline))
        return text



    @staticmethod
    def Button(label: str, color: str = None, icon: str = None, tip: str = None, inputbox: str = None) -> Element:
        """
        Button
        """
        # TODO sembra che tutto si incentrato in una sorta di registrazione app in windows
        # struttata per avviare e comunicare con l app.
        button = Element("action")
        button.set("activationType", "protocol")
        button.set("content", label)
        button.set("arguments", f"http:{label}")
        # add icon on button (max 16x16 no padding)
        if icon is not None and os.path.isfile(icon):
            button.set("imageUri", rf"file:///{icon}" )
        # apply help tip when overing
        if tip is not None:
            button.set("hint-toolTip", tip)
        # apply button color
        COLORS = ("green", "g", "red", "r")
        color = color.lower() if isinstance(color, str) else None
        if color in COLORS:
            color_tag = "Success" if color.startswith("g") else "Critical"
            button.set("hint-buttonStyle", color_tag)
        # set the button on the right side of the inputbox specified
        if inputbox is not None:
            button.set("hint-inputId", inputbox)
        return button

    @staticmethod
    def ButtonPospone(*button_arg, duration: str | Element = None, **button_kargs) -> Element:
        """
        System Pospone Button.
        """
        pospone = Toast.Button("Snooze", *button_arg, **button_kargs)
        pospone.set("content", "")
        pospone.set("activationType", "system")
        pospone.set("arguments", "snooze")
        if duration is not None:
            time = duration.get("id") if isinstance(duration, Element) else None
            pospone.set("hint-inputId", time)
        return pospone

    @staticmethod
    def ButtonDismiss(*button_arg, **button_kargs) -> Element:
        """
        System Dismiss Button.
        """
        dismiss = Toast.Button("Dismiss", *button_arg, **button_kargs)
        dismiss.set("content", "")
        dismiss.set("activationType", "system")
        dismiss.set("arguments", "dismiss")
        return dismiss



    @staticmethod
    def Link(tag, attribute):
        hint = "hint-" + f"{tag.lower()}{attribute.title()}"
        return hint




    @staticmethod
    def Context(command: str) -> Element:
        # init the element
        menu = Element("action")
        # set default attributes
        menu.set("activationType", "protocol")
        menu.set("arguments", f"http:{command}")
        menu.set("placement", "contextMenu")
        # set specific attributes
        menu.set("content", command)
        return menu

    @staticmethod
    def Image(source: str, position: str = None, rounded: bool = None) -> Element:
        """

        By default, images are displayed inline, after any text elements, filling the full
        width of the visual area.

        - logo:
            Specifying a placement value of "appLogoOverride" will cause the image to be displayed
            in a square on the left side of the visual area. The name of this property reflects
            the behavior in previous versions of Windows, where the image would replace the default
            app logo image. In Windows 11, the app logo is displayed in the attribution area, so it
            is not overridden by the appLogoOverride image placement.

            Image dimensions are 48x48 pixels at 100% scaling. We generally recommend providing a
            version each icon asset for each scale factor: 100%, 125%, 150%, 200%, and 400%.

        - rounded:
            Microsoft style guidelines recommend representing profile pictures with
            a circular image to provide a consistent representation of people across apps
            and the shell. Set the HintCrop property to Circle to render the image with a
            circular crop.

        - hero:
            New in Anniversary Update: App notifications can display a hero image, which
            is a featured ToastGenericHeroImage displayed prominently within the toast banner
            and while inside Notification Center. Image dimensions are 364x180 pixels at
            100% scaling.

        Image size restrictions.
        The images you use in your toast notification can be sourced from:

            - http://
            - ms-appx:///
            - ms-appdata:///

        For http and https remote web images, there are limits on the file size of each
        individual image. In the Fall Creators Update (16299), we increased the limit to be
        3 MB on normal connections and 1 MB on metered connections. Before that, images were
        always limited to 200 KB.

            - Normal connection               3 MB
            - Metered connection              1 MB
            - Before Fall Creators Update     220 KB

        If an image exceeds the file size, or fails to download, or times out, the image
        will be dropped and the rest of the notification will be displayed.

        """

        # create element and set default attributes
        image = Element("image")
        image.set("src", source)
        # set image type
        if position == "hero":
            image.set("placement", "hero")
        elif position in ("logo", "appLogoOverride"):
            image.set("placement", "appLogoOverride")
            if rounded is True:
                image.set("hint-crop", "circle")
        return image


    @staticmethod
    def InputBox(tag: str, placeholder: str = "...") -> Element:
        # init the element
        inputbox = Element("input")
        inputbox.set("type", "text")
        # set default attributes
        inputbox.set("id", tag)
        inputbox.set("activationType", "protocol")
        inputbox.set("arguments", f"http:{tag}")
        # set specific attributes
        inputbox.set("placeHolderContent", placeholder)
        return inputbox

    @staticmethod
    def Selection(key: str, value: str) -> Element:
        """
        Create selection option to be append in a Toast.SelectionBox.
        Need a pair key, value.
        """
        selection = Element("selection")
        selection.set("id", key)
        selection.set("content", value)
        return selection

    @staticmethod
    def SelectionBox(*selections: str | tuple, name: str = "SelectionBox",
                     label: str = "", default: int = 0) -> Element:
        # init the element
        selectbox = Element("input")
        selectbox.set("type", "selection")
        # set default attributes
        selectbox.set("id", name)
        selectbox.set("activationType", "protocol")
        selectbox.set("arguments", f"http:{name}")
        # set specific attributes
        selectbox.set("title", label)
        # set selections as k,v pair
        if isinstance(selections[0], str):
            selections = list(enumerate(selections))
        # generate and append options
        for idn, label in selections:
            option = Toast.Selection(str(idn), label)
            selectbox.append(option)
        # set the default
        selectbox.set("defaultInput", str(selections[default][0]))
        return selectbox


    @classmethod
    def Reminder(cls, title: str = "Reminder", text = "Don't forget about it."):
        """
        In the reminder scenario, the notification will stay on screen until the
        user dismisses it or takes action. A reminder sound will be played.
        You must provide at least one button on your app notification.
        Otherwise, the notification will be treated as a normal notification.
        """
        toast = Element("toast")
        # visual section
        visual = Toast.Visual()
        # binging section
        binding = Toast.Binding()
        title = Toast.Text(title, **{"hint-align": "center"})
        place = Toast.Text(text, **{"hint-align": "center"})
        subgroup = Toast.SubGroup(title, place)
        group = Toast.Group(subgroup)
        binding.append(group)
        visual.append(binding)
        # actions section
        actions = Toast.Actions()
        # set the options. The Id should be number in minutes.
        selections = [("1", "1 minute"), ("15", "15 minutes"), ("60", "1 hour"),
                      ("240", "4 hours"), ("1440", "24 hour")]
        selectionbox = Toast.SelectionBox(*selections, name = "snoozeTime", label="postpone in:", default = 0)

        snooze = Toast.ButtonPospone(duration=selectionbox)
        dismiss = Toast.ButtonDismiss()

        actions.extend([selectionbox, snooze, dismiss])
        toast.extend([visual, actions])

        tree = Tree(toast)
        return cls(tree)


    @classmethod
    def IncomingCall(cls):
        # TODO non funziona benissimo come nel sito
        toast = Element("toast", scenario="incomingCall")
        path = r"C:\Users\gaudi\Desktop\projects\refinery\src\gui\image_png.png"
        # visual section
        visual = Element("visual")
        # binging section
        binding = Element("binding", template="ToastGeneric")
        text_name = Element("text", text="Andrew Bares", **{"hint-callScenarioCenterAlign": "true"})
        text_info = Element("text", text="incoming call - mobile", **{"hint-callScenarioCenterAlign": "true"})
        image = Toast.Image(path, rounded=True)
        binding.extend([text_name, text_info, image])
        visual.append(binding)
        # action section
        actions = Element("actions")
        reply = Toast.Button('Reply')
        reminder = Toast.Button('Reminder')
        answer = Toast.Button('Ignore')
        actions.extend([reply, reminder, answer])

        toast.extend([visual, actions])
        tree = Tree(toast)
        return cls(tree)



    @classmethod
    def Template(cls, number: int = 0):
        """
        Windows toast templates.

            No, Name:    0, TOAST_IMAGE_AND_TEXT01
            Descr:  A large image and a single string wrapped across three lines of text

            ...

            No, Name:    7, TOAST_TEXT04
            Descr:  -

        """
        TEMPLATE_NUMBER: int = number
        content: wx.XmlDocument = wn.ToastNotificationManager.get_template_content(TEMPLATE_NUMBER)
        template: str = content.get_xml()
        tree = Tree(template)
        return cls(tree)


    @classmethod
    def os_history(cls, app_id: str = "Python", toast_tag: str = None, user: str = None):
        manager = wn.ToastNotificationManager if user is None else wn.ToastNotificationManagerForUser(user)
        history = manager.history.get_history(app_id)
        history_list = [cls.from_win(toast) for toast in history]
        return history_list

    @staticmethod
    def os_clear(app_id: str = "Python", toast_group: str = None, toast_tag: str = None, user: str = None):
        # check call namespace preference
        manager = wn.ToastNotificationManager if user is None else wn.ToastNotificationManagerForUser(user)
        # get history
        history_manager = manager.history
        # removing
        if toast_group is not None and toast_tag is None:
            # clear all group notification of app
            history_manager.remove_group(toast_group, app_id)
        elif toast_group is not None and toast_tag is not None:
            # clear all specific tag group notification of app
            history_manager.remove(toast_tag, toast_group, app_id)
        else:
            # clear all app history
            history_manager.clear(app_id)
        return True


    def __str__(self):
        # get indented string xml
        string = xe.tostring(self.xml, encoding="unicode")
        return string

    def __repr__(self):
        # get xml string and send it to the parser
        string = str(self.xml)
        temp_element = xe.XML(string)
        # indent it and cast in string
        xe.indent(temp_element)
        string_indented = xe.tostring(temp_element, encoding="unicode")
        return string_indented



    def create_notification(self):
        app_tag: str = self.app_id if self.app_id not in (None, "") else Toast.DEFAULT_APPID
        notification = self.manager.create_toast_notifier(app_tag)
        return notification

    def send(self):
        notification = self.notification
        toast = self.manager.create_toast_notifier(self.app_id)
        toast.show(notification)
        return True

    def clear_history():
        pass

    def replace():
        pass

    def update(self, data, tag, group):
        """
        See:    learn.microsoft.com/en-us/windows/apps/design/shell/
                tiles-and-notifications/toast-progress-bar?tabs=xml
        """
        self.manager.create_toast_notifier().update(data, tag, group)
        return True





toast = Element("toast")
visual = Toast.Visual()
binding = Toast.Binding()

text1 = Toast.Text("Conf Room 2001 / Building 135")
text2 = Toast.Text("10:00 AM - 10:30 AM")

source = r"C:\Users\gaudi\Desktop\projects\tosted\img.png"
image = Toast.Image(source, position="appLogoOverride", rounded=True)

actions = Toast.Actions()
inp = Toast.InputBox("textBox")
menu = Toast.Context("Premi per uscire")
butt = Toast.Button("Ok", tip="clicca", inputbox="ins2")
butt2 = Toast.Button("Send", tip="send", color="g")
butt3 = Toast.Button("Cancel", tip="clicca", color="r")

sel = Toast.SelectionBox("uno", "due")
audio = Toast.Audio("alarm3")

binding.extend([text1, text2, image])
visual.append(binding)
toast.append(audio)
toast.append(visual)
actions.append(inp)
actions.append(menu)


#actions.append(sel)
actions.append(butt)
actions.append(butt2)
actions.append(butt3)


toast.append(actions)

xml = Tree(toast)

t = Toast(xml)
t.send()
a = Toast.IncomingCall()
b = Toast.Reminder()
# TODO b esce testo non richiesto

