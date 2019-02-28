"""Green Greenhouses Calendar Application."""
import tkinter as tk
from tkinter import messagebox

from ..backend.DBHandler import DBHandler

from .eventViewer import EventViewer


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

    def create_pages(self):
        """
        Create the applications pages.

        Arguments:
            N/A
        Returns:
            N/A
        """
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

        self.pages[new_page].grid(column=0, row=0)


class HomePage(tk.Frame):
    """Landing page for application."""

    def __init__(self, parent):
        """Initialise Home Page class."""
        super().__init__(parent)

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
        self.title = tk.Label(self, text="Hello World")
        self.title.grid(row=0, column=0)

        self.button = tk.Button(self, text="Go to add event",
                                command=lambda:
                                    self.parent.change_page(CalendarPage))
        self.button.grid(row=1, column=0)


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
            "12": 31
        }

    def create_widgets(self):
        """
        Create the pages widgets.

        Arguments:
            N/A
        Returns:
            N/A
        """
        self.title = tk.Label(self, text="Add an event", font=(30))
        self.title.grid(column=1)
        # Name
        self.name = tk.Label(self, text="Name", font=(24))
        self.name.grid(row=1, sticky="E")
        self.nameEntry = tk.Entry(self)
        self.nameEntry.grid(row=1, column=1)
        # Location
        self.location = tk.Label(self, text="Location", font=(24))
        self.location.grid(row=2, sticky="E")
        self.locationEntry = tk.Entry(self)
        self.locationEntry.grid(row=2, column=1)
        # Date
        self.date = tk.Label(self, text="Date", font=(24))
        self.date.grid(row=3, sticky="E")
        self.dateSpinBoxs = tk.Frame(self)
        self.timeEntryD = tk.Spinbox(self.dateSpinBoxs,
                                     width=4,
                                     from_=1,
                                     to=31)

        self.timeEntryM = tk.Spinbox(self.dateSpinBoxs,
                                     width=5,
                                     from_=1,
                                     to=12)

        self.timeEntryY = tk.Spinbox(
                                     self.dateSpinBoxs,
                                     width=5,
                                     from_=2019,
                                     to=3000)
        self.timeEntryD.grid(row=3, column=1)
        self.timeEntryM.grid(row=3, column=2)
        self.timeEntryY.grid(row=3, column=3)
        self.dateSpinBoxs.grid(row=3, column=1)
        # Description
        self.description = tk.Label(self, text="Description", font=(24))
        self.description.grid(row=4, sticky="E")
        self.descriptionEntry = tk.Entry(self)
        self.descriptionEntry.grid(row=4, column=1)

        # Submit Button

        self.submitBtn = tk.Button(
            self,
            text="Submit ✔",
            command=lambda: self.inputCheck())
        self.submitBtn.grid()
        # back button
        self.back = tk.Button(
                              self,
                              text="Back",
                              command=lambda:
                              self.parent.change_page(CalendarPage))
        self.back.grid(row=5, column=1, sticky="w")

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
        print(self.IsDaysCorrect(dateList))

        if (
                self.nameEntry.get() and
                self.locationEntry.get() and
                self.IsDaysCorrect(dateList) and
                self.descriptionEntry.get()):
            self.parent.dbh.addEvent(
                                     self.nameEntry.get(),
                                     self.locationEntry.get(),
                                     ".".join(dateList),
                                     self.descriptionEntry.get())
        else:
            messagebox.showinfo(
                "Missing arguments",
                "It seems you didnt fill out all the info boxs \n" +
                "Or you didnt fill the date correctly\n" +
                "please fill them all correctly and try again.")
        self.parent.change_page(CalendarPage)


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
        # Create an add event button
        self.addEventBtn = tk.Button(self,
                                     text="[+] Add event",
                                     command=lambda: self.parent.change_page(
                                         AddEventPage))
        self.addEventBtn.grid()
        # Fetch all events
        events = self.parent.dbh.fetchEvents()
        # Event format:
        # (ID, name, location, Date, description)--
        self.grid_columnconfigure(0, weight=1)

        self.event_viewer = EventViewer(self)
        self.event_viewer.grid(row=10, column=0)
        for event in events:
            self.event_viewer.add_event(event)
