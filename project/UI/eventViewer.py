"""Event viewer specific class."""
import tkinter as tk


class EventViewer(tk.Frame):
    """Shows all event information in a single frame."""

    eventLabels = {
        0: "ID",
        1: "Name",
        2: "Location",
        3: "Date",
        4: "Description"
    }

    def __init__(self, parent):
        """Initialise the Event Viewer class."""
        super().__init__(parent)

        self.canvas = tk.Canvas(self)
        self.display_frame = tk.Frame(self.canvas)
        self.scrollbar = tk.Scrollbar(self, orient="vertical",
                                      command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", padx=10)
        self.canvas.create_window((0, 0), window=self.display_frame, anchor="nw")

        self.display_frame.bind("<Configure>", self.scrollMove)
        self.events = {}

    def scrollMove(self, event):
        """Update canvas information from scrollbar movement."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),
                              width=300, height=500)

    def add_event(self, event):
        """Add a new event to the viewer."""
        self.widgets = {}

        event_frame = tk.Frame(self.display_frame, height=200, width=300,
                               relief=tk.GROOVE, borderwidth=3)
        event_frame.pack(fill="both", expand=True)

        self.events.update({event: event_frame})

        for key, name in self.eventLabels.items():
            widget = tk.Label(event_frame, text=name+" - "+str(event[key]))
            widget.pack()