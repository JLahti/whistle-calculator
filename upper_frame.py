import tkinter
import sys
from tkinter import messagebox
from tkinter import ttk

from data_store import DataStore
#from configuration import Configuration
from utility import Logger, debugger, raise_event, register_event
import utility

class UpperFrame(tkinter.Frame):
    '''
    This class manages the upper frame of the display.
    '''
    def __init__(self, master):
        self.logger = Logger(self, Logger.INFO)
        self.logger.debug("constructor")
        self.master = master
        self.data_store = DataStore.get_instance()
        register_event("UPDATE_UPPER_EVENT", self.set_state)

    @debugger
    def create_frame(self):
        # build the screen

        # Fill in the upper frame
        tkinter.Label(self.master, text="Title").grid(row=0, column=0, sticky=tkinter.E)
        self.titleEntry = tkinter.Entry(self.master, width=40, validate="focusout", validatecommand=self.setTitleCommand)
        self.titleEntry.bind('<Return>', self.setTitleCommand)
        self.titleEntry.bind('<Tab>', self.setTitleCommand)
        self.titleEntry.grid(row=0, column=1, columnspan=3, padx=9, pady=4)

        tkinter.Label(self.master, text="Inside Diameter").grid(row=1, column=0, sticky=tkinter.E, pady=4)
        self.insideDiaEntry = tkinter.Entry(self.master, validate="focusout", validatecommand=self.insideDiaCommand)
        self.insideDiaEntry.bind('<Return>', self.insideDiaCommand)
        self.insideDiaEntry.bind('<Tab>', self.insideDiaCommand)
        self.insideDiaEntry.grid(row=1, column=1, pady=4)

        tkinter.Label(self.master, text="Wall Thickness").grid(row=1, column=2, sticky=tkinter.E, pady=4)
        self.wallThicknessEntry = tkinter.Entry(self.master, validate="focusout", validatecommand=self.wallThicknessCommand)
        self.wallThicknessEntry.bind('<Return>', self.wallThicknessCommand)
        self.wallThicknessEntry.bind('<Tab>', self.wallThicknessCommand)
        self.wallThicknessEntry.grid(row=1, column=3, pady=4)

        tkinter.Label(self.master, text="Number of Holes").grid(row=2, column=0, sticky=tkinter.E, pady=4)
        self.numHolesEntry = tkinter.Entry(self.master, validate="focusout", validatecommand=self.numHolesCommand)
        self.numHolesEntry.bind('<Return>', self.numHolesCommand)
        self.numHolesEntry.bind('<Tab>', self.numHolesCommand)
        self.numHolesEntry.grid(row=2, column=1, pady=4)

        tkinter.Label(self.master, text="Select Bell Note").grid(row=2, column=2, sticky=tkinter.E, pady=4)
        self.bellNoteCombo = ttk.Combobox(self.master, state="readonly", values=self.data_store.bellNoteArray)
        self.bellNoteCombo.config(width=17)
        self.bellNoteCombo.grid(row=2, column=3, pady=4)
        self.bellNoteCombo.bind("<<ComboboxSelected>>", self.bellSelectCallback)

        tkinter.Label(self.master, text="Embouchure Area").grid(row=4, column=0, sticky=tkinter.E, pady=4)
        self.embouchureAreaEntry = tkinter.Entry(self.master)
        self.embouchureAreaEntry.grid(row=4, column=1, pady=4)

        tkinter.Label(self.master, text="Units of Measure").grid(row=3, column=0, sticky=tkinter.E, pady=4)
        self.measureUnitsOpt = ttk.Combobox(self.master, state="readonly", values=["inch", "mm"])
        self.measureUnitsOpt.config(width=17)
        self.measureUnitsOpt.grid(row=3, column=1, pady=4)
        self.measureUnitsOpt.bind("<<ComboboxSelected>>", self.measureUnitsCallback)

        tkinter.Label(self.master, text="Display Format").grid(row=3, column=2, sticky=tkinter.E, pady=4)
        self.displayFormatOpt = ttk.Combobox(self.master, state="readonly", values=["decimal", "fraction"])
        self.displayFormatOpt.current(1)
        self.displayFormatOpt.config(width=17)
        self.displayFormatOpt.grid(row=3, column=3, pady=4)
        self.displayFormatOpt.bind("<<ComboboxSelected>>", self.displayFormatCallback)

        tkinter.Label(self.master, text="Length").grid(row=4, column=2, sticky=tkinter.E, pady=4)
        self.lengthEntry = tkinter.Entry(self.master)
        self.lengthEntry.grid(row=4, column=3, pady=4)

        if self.measureUnitsOpt.get() == 'mm':
            self.displayFormatOpt.config(state="readonly")

        self.refreshButton = tkinter.Button(
            self.master, text="Refresh", width=14, command=self.refreshButtonCommand)
        self.refreshButton.grid(row=5, column=0, columnspan=4, pady=4)

        self.set_state() # write what's in the data_store to the GUI

    @debugger
    def get_state(self):
        '''
        Return the state of the controls in the upper half into the data store.
        '''

        if self.displayFormatOpt.current() == 0:
            self.data_store.set_disp_frac(False)
        else:
            self.data_store.set_disp_frac(True)

        if self.measureUnitsOpt.current() == 0:
            self.data_store.set_units(False)
        else:
            self.data_store.set_units(True)

        self.data_store.set_title(self.titleEntry.get())
        self.data_store.set_inside_dia(float(self.insideDiaEntry.get()))
        self.data_store.set_wall_thickness(float(self.wallThicknessEntry.get()))
        self.data_store.set_number_holes(int(self.numHolesEntry.get()))
        self.data_store.set_bell_note_select(self.bellNoteCombo.current())
        #self.data_store.set_embouchure_area(float(self.embouchureAreaEntry.get()))
        self.data_store.set_bell_freq(
            self.data_store.note_table[self.data_store.get_bell_note_select()]['frequency'])


    @debugger
    def set_state(self):
        '''
        Take the state from the data store and put in the GUI.
        '''
        self.titleEntry.delete(0, tkinter.END)
        self.titleEntry.insert(0, self.data_store.get_title())

        self.bellNoteCombo.current(self.data_store.get_bell_note_select())
        self.measureUnitsOpt.current(int(self.data_store.get_units())) # it's a bool in the data_store
        self.displayFormatOpt.current(int(self.data_store.get_disp_frac())) # it's a bool in the data_store

        self.insideDiaEntry.delete(0, tkinter.END)
        self.insideDiaEntry.insert(0, str(self.data_store.get_inside_dia()))

        self.wallThicknessEntry.delete(0, tkinter.END)
        self.wallThicknessEntry.insert(0, str(self.data_store.get_wall_thickness()))

        self.numHolesEntry.delete(0, tkinter.END)
        self.numHolesEntry.insert(0, str(self.data_store.get_number_holes()))

        self.embouchureAreaEntry.config(state=tkinter.NORMAL)
        self.embouchureAreaEntry.delete(0, tkinter.END)
        self.embouchureAreaEntry.insert(0, "%0.4f"%(self.data_store.get_embouchure_area()))
        self.embouchureAreaEntry.config(state="readonly")

        self.lengthEntry.config(state=tkinter.NORMAL)
        self.lengthEntry.delete(0, tkinter.END)
        self.lengthEntry.insert(0, "%0.4f"%(self.data_store.get_length()))
        self.lengthEntry.config(state="readonly")

    @debugger
    def insideDiaCommand(self, event=None):
        try:
            v = self.insideDiaEntry.get()
            n = float(v)
            if self.data_store.get_inside_dia() != n:
                self.logger.debug("change wall from %f to %f"%(self.data_store.get_inside_dia(), n))
                self.data_store.set_inside_dia(n)
                self.insideDiaEntry.delete(0, tkinter.END)
                self.insideDiaEntry.insert(0, str(n))
                raise_event("CALCULATE_EVENT")
                self.data_store.set_change_flag()
            else:
                self.logger.debug("ignore")
            return True
        except ValueError as e:
            self.logger.error(str(e))
            messagebox.showerror("Error", "Could not convert inside diameter to a floating point number.\nRead value was \"%s\"." % (v))
            self.insideDiaEntry.delete(0, tkinter.END)
            self.insideDiaEntry.insert(0, str(self.data_store.get_inside_dia()))
            return False
        except IndexError:
            self.logger.error(str(e))
            self.wallThicknessEntry.delete(0, tkinter.END)
            self.wallThicknessEntry.insert(0, str(self.data_store.get_wall_thickness()))
        except Exception as e:
            self.logger.error(str(e))
            messagebox.showerror("Unknown Error", "Unknown exception trying to convert inside diameter to a floating point number.\nRead value was \"%s\".\nException: %s" % (v, str(e)))
            self.wallThicknessEntry.delete(0, tkinter.END)
            self.wallThicknessEntry.insert(0, str(self.data_store.get_wall_thickness()))


    @debugger
    def wallThicknessCommand(self, event=None):
        try:
            v = self.wallThicknessEntry.get()
            n = float(v)
            if n != self.data_store.get_wall_thickness():
                self.logger.debug("change wall from %f to %f"%(self.data_store.get_wall_thickness(), n))
                self.data_store.set_wall_thickness(n)
                self.wallThicknessEntry.delete(0, tkinter.END)
                self.wallThicknessEntry.insert(0, str(n))
                raise_event("CALCULATE_EVENT")
                self.data_store.set_change_flag()
            else:
                self.logger.debug("ignore")
            return True
        except ValueError as e:
            self.logger.error(str(e))
            messagebox.showerror("Error", "Could not convert wall thickness to a floating point number.\nRead value was \"%s\"." % (v))
            self.wallThicknessEntry.delete(0, tkinter.END)
            self.wallThicknessEntry.insert(0, str(self.data_store.get_wall_thickness()))
            return False
        except IndexError:
            self.logger.error(str(e))
            self.wallThicknessEntry.delete(0, tkinter.END)
            self.wallThicknessEntry.insert(0, str(self.data_store.get_wall_thickness()))
        except Exception as e:
            self.logger.error(str(e))
            messagebox.showerror("Unknown Error", "Unknown exception trying convert wall thickness to a floating point number.\nRead value was \"%s\".\nException %s" % (v, str(e)))
            self.wallThicknessEntry.delete(0, tkinter.END)
            self.wallThicknessEntry.insert(0, str(self.data_store.get_wall_thickness()))


    @debugger
    def numHolesCommand(self, event=None):
        n = 0
        try:
            v = self.numHolesEntry.get()
            n = int(v)
            if n >= 1 and n <= 12:
                # only raise the event if the number of holes is different from
                # what is in the data_store
                if n != self.data_store.get_number_holes():
                    self.logger.debug("change number of holes from %d to %d"%(self.data_store.get_number_holes(), n))
                    self.data_store.set_number_holes(n)
                    raise_event('UPDATE_LOWER_FRAME_EVENT')
                    self.data_store.set_change_flag()
                else:
                    self.logger.debug("ignore")
                return True
            else:
                self.logger.error("range error on number of holes: %s"%(str(n)))
                messagebox.showerror("Error", message="Number of holes must be an integer between 1 and 12.\nRead value was \"%s\"." % (v))
                self.numHolesEntry.delete(0, tkinter.END)
                self.numHolesEntry.insert(0, str(self.data_store.get_number_holes()))
                return False
        except ValueError as e:
            self.logger.error(str(e))
            messagebox.showerror("Error", message="Could not convert number of holes to an integer.\nRead value was \"%s\"." % (v))
            self.numHolesEntry.delete(0, tkinter.END)
            self.numHolesEntry.insert(0, str(self.data_store.get_number_holes()))
            return False
        except IndexError as e:
            self.logger.error(str(e))
            self.numHolesEntry.delete(0, tkinter.END)
            self.numHolesEntry.insert(0, str(self.data_store.get_number_holes()))
        except Exception as e:
            self.logger.error(str(e))
            messagebox.showerror("Unknown Error", message="Unknown exception trying to convert number of holes to an integer.\nRead value was \"%s\".\nException: %s" % (v, str(e)))
            self.wallThicknessEntry.delete(0, tkinter.END)
            self.wallThicknessEntry.insert(0, str(self.data_store.get_wall_thickness()))


    @debugger
    def displayFormatCallback(self, event):
        if self.displayFormatOpt.current() == 0:
            val = False
        else:
            val = True

        if val != self.data_store.get_disp_frac():
            self.data_store.set_disp_frac(val)
            raise_event("UPDATE_HOLE_EVENT")
            self.logger.debug("current format set to: %s"%(str(self.data_store.get_disp_frac())))
            self.data_store.set_change_flag()
        else:
            self.logger.debug("ignore")


    @debugger
    def measureUnitsCallback(self, event):
        if self.measureUnitsOpt.current() == 0:
            val = False
        else:
            val = True

        if self.data_store.get_units() != val:
            if self.measureUnitsOpt.current() == 1:
                self.displayFormatOpt.config(state=tkinter.DISABLED)
            else:
                self.displayFormatOpt.config(state="readonly")

            self.data_store.set_units(val)
            self.change_units()
            self.logger.debug("current units set to: %s"%(str(self.data_store.get_units())))
            self.data_store.set_change_flag()
        else:
            self.logger.debug("ignore")


    @debugger
    def bellSelectCallback(self, event):
        '''
        Change the data_store to match the new bell selection
        '''
        val = self.bellNoteCombo.current()
        if val != self.data_store.get_bell_note_select():
            self.data_store.set_bell_note_select(val)
            self.data_store.set_bell_freq(self.data_store.note_table[val]['frequency'])
            self.logger.debug("current bell selection set to: %d: %f"%(self.data_store.get_bell_note_select(), self.data_store.get_bell_freq()))
            raise_event("UPDATE_NOTES_EVENT")
            self.data_store.set_change_flag()
        else:
            self.logger.debug("ignore")
        self.set_state()

    @debugger
    def refreshButtonCommand(self):
        self.refreshButton.focus_set()
        self.get_state()
        #raise_event('UPDATE_LINES_EVENT')
        raise_event('UPDATE_LOWER_FRAME_EVENT')
        self.set_state()

    @debugger
    def change_units(self):
        '''
        When this is called, the assumption is that the GUI and the
        data_store have the wrong units. This function takes what ever
        is in the data_sore and converts if to the units that it finds
        there.  Then it updates the GUI.
        '''
        if self.data_store.get_units(): # true of units are mm
            self.data_store.set_inside_dia(utility.in_to_mm(self.data_store.get_inside_dia()))
            self.data_store.set_wall_thickness(utility.in_to_mm(self.data_store.get_wall_thickness()))
        else:
            self.data_store.set_inside_dia(utility.mm_to_in(self.data_store.get_inside_dia()))
            self.data_store.set_wall_thickness(utility.mm_to_in(self.data_store.get_wall_thickness()))

        self.set_state()
        # Cause the other frames to update
        raise_event("CHANGE_UNITS_EVENT")
        raise_event('CALCULATE_EVENT')
        self.data_store.set_change_flag()

    @debugger
    def setTitleCommand(self, event=None):
        try:
            title = self.titleEntry.get()
            old_title = self.data_store.get_title()
            if title != old_title:
                self.data_store.set_title(title)
                self.logger.debug("title set to: \"%s\""%(str(self.data_store.get_title())))
                self.data_store.set_change_flag()
            else:
                self.logger.debug("ignore")
        except IndexError:
            pass # always ignore
