"""Green Greenhouses Calendar Application."""
import tkinter as tk
from tkinter import messagebox
from ..backend.DBHandler import DBHandler
from .eventViewer import EventViewer
import string
from .userHandling import Register, Login


class Application(tk.Tk):
    """Main Application class inheriting from tkinter.Tk."""

    def __init__(self):
        """Initialise Application class."""
        super().__init__()

        self.resizable(False, False)
        self.geometry("500x500")

        self.dbh = DBHandler()

        self.pages = {}

        self.create_pages()

        self.tk_setPalette(background="#F0F0F0", foreground="#000000")
        self.dark_mode = False
        self.bind("q", self.switch)

    def switch(self, event):
        """Switch the application between light and dark mode."""
        if self.dark_mode:
            self.tk_setPalette(background="#F0F0F0", foreground="#000000")

        else:
            self.tk_setPalette(background="#292D32", foreground="#2e3237")

        self.dark_mode = not self.dark_mode

    def create_pages(self):
        """
        Create the applications pages.

        Arguments:
            N/A
        Returns:
            N/A
        """
        self.pages[LoginPage] = LoginPage(self)
        self.pages[HomePage] = HomePage(self)
        self.pages[AddEventPage] = AddEventPage(self)
        self.pages[CalendarPage] = CalendarPage(self)

        self.change_page(HomePage)

    def change_page(self, new_page):
        """
        Change the currently displayed page.

        Arguments:
            new_page - The page to change to
        Returns:
            N/A
        """
        for page in self.grid_slaves():
            page.grid_remove()
        if new_page is EventViewer:
            self.parent.pages[CalendarPage].create_widgets()
        self.pages[new_page].grid(column=0, row=0)


class LoginPage(tk.Frame):
    """Landing page for application."""

    def __init__(self, parent):
        """Initialise Home Page class."""
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1000)

        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        """
        Create the pages widgets.

        Arguments:
            N/A
        Returns:
            N/A
        """
        self.title = tk.Label(
            self, text="Welcome to Green Greenhouses\nEvent Manager",
            font=("Helvetica", 24, "bold")
        )
        self.title.grid(row=0, column=0, sticky="ew", pady=(10, 0))

        self.registerButton = tk.Button(
            self, text="REGISTER", width=10,
            font=("Arial", 20, "italic"),
            command=self.register
        )
        self.registerButton.grid(row=5, column=0, pady=100)

        self.loginButton = tk.Button(
            self, text="LOGIN", width=10,
            font=("Arial", 20, "italic"),
            command=self.login
        )
        self.loginButton.grid(row=10, column=0)

    def register(self):
        Register(self.parent.dbh)

    def login(self):
        loginWindow = Login(self.parent.dbh)
        self.wait_window(loginWindow.window)
        if loginWindow.loggedIn:
            print(f"Logged In User {self.parent.dbh.logged_in_user}")
            self.parent.change_page(HomePage)
        else:
            print("Not Logged In")


class HomePage(tk.Frame):
    """Landing page for application."""

    def __init__(self, parent):
        """Initialise Home Page class."""
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1000)

        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        """
        Create the pages widgets.

        Arguments:
            N/A
        Returns:
            N/A
        """
        self.title = tk.Label(
            self, text="Main Menu",
            font=("Helvetica", 24, "bold")
        )
        self.title.grid(row=0, column=3, pady=(10, 0))

        self.register = tk.Button(
            self, text="VIEW EVENTS", width=12,
            font=("Arial", 20, "italic"),
            command=lambda: self.parent.change_page(EventViewer)
        )
        self.register.grid(row=5, column=3, pady=100)

        self.login = tk.Button(
            self, text="MAKE EVENT", width=12,
            font=("Arial", 20, "italic"),
            command=lambda: self.parent.change_page(AddEventPage)
        )
        self.login.grid(row=10, column=3)


class AddEventPage(tk.Frame):
    """Page where you can add events to the calendar."""

    def __init__(self, parent):
        """
        Initialise the Add Event page.

        Arguments:
            None
        Returns:
            None
        """
        super().__init__()

        self.parent = parent
        self.create_widgets()
        self.months = {
            "1": 31,
            "2": 28,
            "3": 31,
            "4": 30,
            "5": 31,
            "6": 30,
            "7": 31,
            "8": 31,
            "9": 30,
            "10": 31,
            "11": 30,
            "12": 31}

    def create_widgets(self):
        """
        Create the pages widgets.

        Arguments:
            N/A
        Returns:
            N/A
        """
        self.title = tk.Label(
            self,
            text="Add an event", font=(30))
        self.title.grid(column=1)
        # Name
        self.name = tk.Label(
            self,
            text="Name ",
            font=(24))
        self.name.grid(row=1, sticky="E")
        self.nameEntry = tk.Text(
            self,
            height=2, width=49)
        self.nameEntry.grid(row=1, column=1)
        # Location
        self.location = tk.Label(
            self,
            text="Location ",
            font=(24),)
        self.location.grid(row=2, sticky="E")
        self.locationEntry = tk.Text(
            self,
            height=2, width=49)
        self.locationEntry.grid(row=2, column=1)
        # Date
        self.date = tk.Label(
            self,
            text="Date ",
            font=(24))
        self.date.grid(row=3, sticky="E")
        self.dateSpinBoxs = tk.Frame(self)
        self.timeEntryD = tk.Spinbox(self.dateSpinBoxs,
                                     width=14,
                                     from_=1,
                                     to=31)

        self.timeEntryM = tk.Spinbox(self.dateSpinBoxs,
                                     width=15,
                                     from_=1,
                                     to=12)

        self.timeEntryY = tk.Spinbox(self.dateSpinBoxs,
                                     width=14,
                                     from_=2019,
                                     to=3000)

        self.timeEntryD.grid(row=3, column=1)
        self.timeEntryM.grid(row=3, column=2)
        self.timeEntryY.grid(row=3, column=3)
        self.dateSpinBoxs.grid(row=3, column=1)
        # Description
        self.description = tk.Label(
            self,
            text="Description ",
            font=(24))
        self.description.grid(row=4, sticky="N")
        self.descriptionEntry = tk.Text(
            self, height=20,
            width=49)
        self.descriptionEntry.grid(row=4, column=1)

        # Submit Button
        self.submitBack = tk.Frame(self)
        self.submitBtn = tk.Button(
            self.submitBack,
            text="Submit ✔",
            command=lambda: self.inputCheck())
        self.submitBtn.grid(row=1, sticky="W")
        # back button
        self.back = tk.Button(
            self.submitBack,
            text="Back",
            command=lambda:
            self.parent.change_page(HomePage))
        self.back.grid(row=1, column=1, sticky="W")
        self.submitBack.grid(column=1)

    def IsDaysCorrect(self, list):
        """"""
        if self.months[str(int(list[1]))] >= int(list[0]):
            return True
        return False

    def inputCheck(self):
        """
        the Function that checks to see if all date boxs
        have been filled out correctly.

        Argumnets:
            None
        Returns:
            None
        """

        dateList = [
            self.timeEntryD.get(),
            self.timeEntryM.get(),
            self.timeEntryY.get()]

        if (
                any(
                    letter for letter in self.descriptionEntry.get(
                        "1.0",
                        tk.END)
                    if letter.lower() in string.ascii_lowercase) and
                any(
                    letter for letter in self.locationEntry.get(
                        "1.0",
                        tk.END)
                    if letter.lower() in string.ascii_lowercase) and
                self.IsDaysCorrect(dateList) and
                any(
                    letter for letter in self.nameEntry.get(
                        "1.0",
                        tk.END)
                    if letter.lower() in string.ascii_lowercase)):
            self.parent.dbh.addEvent(
                self.nameEntry.get("1.0", tk.END),
                self.locationEntry.get("1.0", tk.END),
                ".".join(dateList),
                self.descriptionEntry.get("1.0", tk.END))

        else:
            messagebox.showinfo(
                "Missing arguments",
                "It seems you didnt fill out all the info boxs \n" +
                "Or you didnt fill the date correctly\n" +
                "please fill them all correctly and try again.")
        self.parent.pages[CalendarPage].create_widgets()
        self.parent.change_page(HomePage)


class CalendarPage(tk.Frame):
    """Example page for Application."""

    eventLabels = {
        0: "ID",
        1: "Name",
        2: "Location",
        3: "Date",
        4: "Description"
    }

    def __init__(self, parent):
        """
        Initialise the Example page.

        Arguments:
            None
        Returns:
            None
        """
        super().__init__()

        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        """
        Create the pages widgets.

        Arguments:
            None
        Returns:
            None
        """
        self.back = tk.Button(
            self,
            text="Back",
            command=lambda:
            self.parent.change_page(HomePage))

        self.back.grid(sticky="W")
        self.grid_columnconfigure(0, weight=1)
        # Fetch all events

        events = self.parent.dbh.fetchEvents()
        # Event format:
        # (ID, name, location, Date, description)--

        self.event_viewer = EventViewer(self)
        self.event_viewer.grid(row=10, column=0)
        for event in events:
            self.event_viewer.add_event(event)
