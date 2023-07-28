from tkinter import END
from typing import TYPE_CHECKING

if TYPE_CHECKING: from page.source import source

from source import unselect

# EDIT
def editMenu(self: "source"):

    self.addOrEditSourceToplevel.title(self.langs.t('UI.EDIT_MENU_SOURCE.title_edit'))

    self.addOrEditBtn.config(text=self.langs.t('UI.EDIT_MENU_SOURCE.button_apply'), command=lambda: edit(self))

    self.nameSourceEntry.delete(0, END)
    self.pathFolderSourceEntry.delete(0, END)

    try:
        selected: list[str] = self.listSource.getItemSelectedRow()["values"]

        # output to entry boxes
        self.nameSourceEntry.insert(0, selected[0])
        self.pathFolderSourceEntry.insert(0, selected[1])
        

        self.addOrEditSourceToplevel.show()

    except:
        self.log.debug("Not select", "editMenu")

def edit(self: "source"):

    try:

        iid = self.listSource.getSelectedRow()[0]


        self.listSource.editItem(iid, values=[self.nameSourceEntry.get(), self.pathFolderSourceEntry.get()])
        self.addOrEditSourceToplevel.hide()
    except ValueError as e:
        self.log.debug("error : "+e)

# ADD
def addMenu(self: "source"):
    
    self.addOrEditSourceToplevel.title(self.langs.t('UI.EDIT_MENU_SOURCE.title_add'))

    self.addOrEditBtn.config(text=self.langs.t('UI.EDIT_MENU_SOURCE.button_add'), command=lambda: add(self))

    self.nameSourceEntry.delete(0, END)
    self.pathFolderSourceEntry.delete(0, END)

    self.addOrEditSourceToplevel.show()

def add(self: "source"):
    nameSource = self.nameSourceEntry.get()
    folderSource = self.pathFolderSourceEntry.get()

    if nameSource!="" and folderSource!="":
        try:
            self.listSource.addItem(iid=nameSource, values=(nameSource, folderSource), tags=('evenrow',))
            unselect(self)
            self.addOrEditSourceToplevel.hide()
            self.log.debug("ok")

        except ValueError as e:
            self.log.debug("error : "+e)

    else:
        self.log.debug("nameSource And folderSource is required")