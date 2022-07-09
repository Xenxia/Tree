from threading import Thread
from tkinter import END, W, E, N, S, Entry
from tk_up.widgets import Frame_up
from tk_up.managerWidgets import ManagerWidgets_up
from tk_up.widgets import SCROLL_ALL, Button_up, Frame_up, Label_up, Toggle_Button_up, Treeview_up, Toplevel_up, Entry_up

from func.langages import Lang_app
from func.logger import Logger
from func.conf import ConfigTree
from func.function import sendMessage

class menu_edit_settings(Frame_up):

    # DONT REMOVE THIS
    parameters_list: list
    parameters_dict: dict
    manager_class: ManagerWidgets_up

    def __init__(self, parameters_list: list, parameters_dict: dict, manager_class: ManagerWidgets_up, master, kw={"width":0, "height":0}):
        self.parameters_list = parameters_list.copy()
        self.parameters_dict = parameters_dict.copy()
        self.manager_class = manager_class

        self.langs: Lang_app = parameters_list[0]
        self.config: ConfigTree = parameters_list[1]
        self.log: Logger = parameters_list[2]

        # Use 'self' in your widget
        Frame_up.__init__(self, master=master, width=kw["width"], height=kw["height"])
        self.gridPosSize(row=0, column=0, sticky=(E, W, S, N)).grid_propagate(False)

        self.frameButton = Frame_up(self)
        self.frameButton.gridPosSize(row=1, column=0, sticky=(E, W, S, N)).show()

        self.frameBox = Frame_up(self, width=700)
        self.frameBox.gridPosSize(row=2, column=0, sticky=(E, W, S, N)).show()
        # self.frameBox.propagate(False)
        
        self.treeView = Treeview_up(self, scroll=SCROLL_ALL, iid=True, child=True, show="tree headings", width=700, height=400)
        self.treeView.bind("<ButtonRelease-1>", self.selected)
        self.treeView.gridPosSize(row=0, column=0, sticky=(E, W, S, N)).show()
        self.treeView.setColumns([
                self.langs.lang['UI']['EDIT_MENU']['col_name_profil'],
                self.langs.lang['UI']['EDIT_MENU']['col_folder'],
                self.langs.lang['UI']['EDIT_MENU']['col_extention']
            ], 
            [150, 150, 300]
        )
        self.treeView.setTags((
            {
            "name": "disable",
            "bg": "#FF0000",
            },
        ))

        self.unselect_button = Button_up(self.frameButton, text=self.langs.lang['UI']['EDIT_MENU']['button_unselect'], width=10, command=self.unselect)
        self.unselect_button.gridPosSize(column=5, row=0, padx=5).show().disable()

        self.move_up = Button_up(self.frameButton, text="⬆", command=self.treeView.moveUpSelectedElement, width=3)
        self.move_up.gridPosSize(column=4, row=0).show().disable()

        self.move_down = Button_up(self.frameButton, text="⬇", command=self.treeView.moveDownSelectedElement, width=3)
        self.move_down.gridPosSize(column=3, row=0).show().disable()

        self.remove = Button_up(self.frameButton, text=self.langs.lang['UI']['EDIT_MENU']['button_delete'], width=10, command=self.delete)
        self.remove.gridPosSize(column=2, row=0, padx=5).show().disable()

        self.edit_button = Button_up(self.frameButton, text=self.langs.lang['UI']['EDIT_MENU']['button_edit'], width=10, command=self.editMenu)
        self.edit_button.gridPosSize(column=1, row=0, padx=(5, 0)).show().disable()

        add_button = Button_up(self.frameButton, text=self.langs.lang['UI']['EDIT_MENU']['button_add'], width=10, command=self.addMenu)
        add_button.gridPosSize(column=0, row=0).show()

        self.doNotSort_box = Entry(self.frameBox, width=71, bg="#555555", fg="#FFFFFF")
        self.doNotSort_box.grid(row=0, column=1, sticky=W, pady=(13, 0))

        d1 = Label_up(self.frameBox, text=self.langs.lang['UI']['EDIT_MENU']['label_not_sort'])
        d1.gridPosSize(row=0, column=0, pady=(20, 10), padx=(5, 5)).show()

        self.toggle_b = Toggle_Button_up(self.frameBox, width=3)
        self.toggle_b.custom_toggle(("✔", "✖"))
        self.toggle_b.gridPosSize(column=1, row=1, sticky=W).show()

        u1 = Label_up(self.frameBox, text=self.langs.lang['UI']['EDIT_MENU']['label_unsorted'])
        u1.gridPosSize(row=1, column=0, padx=(5, 5)).show()

        self.back = Button_up(self.frameBox, text="back", width=10, command=lambda: self.manager_class.showWidget("menu_option"))
        self.back.gridPosSize(column=0, row=2, padx=(5, 0), pady=(50, 0)).show()

        self.button_saveAndReturn = Button_up(self.frameBox, text=self.langs.lang['UI']['EDIT_MENU']['button_return_save'], command=self.saveDataInTree)
        self.button_saveAndReturn.gridPosSize(column=0, row=2, padx=(5, 0), pady=(50, 0)).show()

        self.button_return = Button_up(self.frameBox, text=self.langs.lang['UI']['EDIT_MENU']['button_return'], command=lambda: self.manager_class.showWidget("menu_option"))
        self.button_return.gridPosSize(column=1, row=2, padx=(0, 0), pady=(50, 0)).show()

        self.label_error_edit = Label_up(self.frameBox, text="test")
        self.label_error_edit.gridPosSize(column=0, row=3, padx=(5, 0), pady=(50, 0)).show()

        # TopLevel

        self.addEditWindow = Toplevel_up(master)
        self.addEditWindow.geometry("600x95")
        self.addEditWindow.iconbitmap(f"{self.parameters_dict['exe_path']}/img/tree.ico")
        self.addEditWindow.config(background='#202020')
        self.addEditWindow.resizable(0, 0)
        self.addEditWindow.hide()

        #Labels
        nl = Label_up(self.addEditWindow, text=self.langs.lang['UI']['EDIT_MENU']['col_name_profil'])
        nl.gridPosSize(row=0, column=0, sticky=W).show()

        il = Label_up(self.addEditWindow, text=self.langs.lang['UI']['EDIT_MENU']['col_folder'])
        il.gridPosSize(row=1, column=0, sticky=W).show()

        tl = Label_up(self.addEditWindow, text=self.langs.lang['UI']['EDIT_MENU']['col_extention'])
        tl.gridPosSize(row=2, column=0, sticky=W).show()

        #Entry boxes
        self.profile_box = Entry_up(self.addEditWindow, width=71)
        self.profile_box.gridPosSize(row=0, column=1, sticky=W).show()

        self.folder_box = Entry_up(self.addEditWindow, width=71)
        self.folder_box.gridPosSize(row=1, column=1, sticky=W).show()

        self.rule_box = Entry_up(self.addEditWindow, width=71)
        self.rule_box.gridPosSize(row=2, column=1, sticky=W).show()

        buttonF = Frame_up(self.addEditWindow)

        self.addOrEdit = Button_up(buttonF)
        self.addOrEdit.gridPosSize(row=0, column=0).show()

        self.cancel = Button_up(buttonF, text=self.langs.lang['UI']['EDIT_MENU']['button_cancel'], command=self.addEditWindow.hide)
        self.cancel.gridPosSize(row=0, column=1).show()

        buttonF.gridPosSize(row=3, column=1, sticky=W).show()

        self.label_error_addEditWindow = Label_up(self.addEditWindow, text="")
        self.label_error_addEditWindow.placePosSize(x=200, y=63, width=300, height=32)

    def editUi(self):

        for i in self.treeView.tree.get_children():
            self.treeView.tree.delete(i)

        for key in self.config.CONFIG['config_sort']:
            folder: str = self.config.CONFIG['config_sort'][key]['folder']
            rule: list = self.config.CONFIG['config_sort'][key]['ext']
            parent: str | None = self.config.CONFIG['config_sort'][key]['parent']

            parent = parent if parent is not None else ''

            # self.treeView.tree.insert(parent=parent, index=END, iid=key, text="", values=(key, folder, '|'.join(rule)))
            self.treeView.addElement(parent=parent, iid=key, text="", values=[key, folder, '|'.join(rule)])

        self.toggle_b.set_default_status(self.config.CONFIG["unsorted"])
        doNotSort = "|".join(self.config.CONFIG["doNotSort"])
        if not doNotSort == "":
            self.doNotSort_box.delete(0, END)
            self.doNotSort_box.insert(0, doNotSort)

        # self.show()

    def delete(self):
        self.treeView.removeSelectedElement()
        self.unselect()

    def unselect(self):
        try:
            self.edit_button.disable()
            self.remove.disable()
            self.unselect_button.disable()
            self.move_up.disable()
            self.move_down.disable()
            self.treeView.tree.selection_remove(self.treeView.tree.selection()[0])
        except:
            print("not select")

#Toplevel menu ------------------------------------------------------------------------
    def editMenu(self):

        self.addEditWindow.title(self.langs.lang['UI']['EDIT_MENU']['title_edit'])

        self.addOrEdit.config(text=self.langs.lang['UI']['EDIT_MENU']['button_apply'])

        self.profile_box.delete(0, END)
        self.folder_box.delete(0, END)
        self.rule_box.delete(0, END)

        self.addOrEdit.config(command=self.edit)

        try:
            selected = self.treeView.getItemSelectedElemnt()
            # values = self.treeView.tree.item(selected, 'values')

            # output to entry boxes
            self.profile_box.insert(0, selected[0])
            self.folder_box.insert(0, selected[1])
            self.rule_box.insert(0, selected[2])
            

            self.addEditWindow.show()

        except:
            print("not select")

    def edit(self):
        try:
            selected = self.treeView.tree.selection()[0]
            self.treeView.tree.item(selected, text=self.profile_box.get(), values=(self.folder_box.get(), self.rule_box.get()))
            self.addEditWindow.hide()
        except:
            Thread(target=lambda: sendMessage(self.label_error_edit, "#ff3030", f"no items selected")).start()

    def addMenu(self):
        self.addEditWindow.title(self.langs.lang['UI']['EDIT_MENU']['title_add'])

        self.addOrEdit.config(text=self.langs.lang['UI']['EDIT_MENU']['button_add'])

        self.profile_box.delete(0, END)
        self.folder_box.delete(0, END)
        self.rule_box.delete(0, END)

        self.addOrEdit.config(command=self.add)

        self.addEditWindow.show()

    def add(self):
        profile_name = self.profile_box.get()
        folder = self.folder_box.get()
        rule = self.rule_box.get()

        sellect = ""

        try:
            sellect = self.treeView.tree.selection()[0]
        except:
            self.log.debug("No select")

        if profile_name!="" and folder!="":
            try:
                self.treeView.tree.insert(parent=sellect, index=END, iid=profile_name, text=profile_name, values=(folder, rule), tags=('evenrow',))
                self.unselect()
                self.addEditWindow.hide()
            except:
                Thread(target=lambda: sendMessage(self.label_error_addEditWindow, "#ff3030", f"The profile {profile_name} already exists")).start()

        else:
            Thread(target=lambda: sendMessage(self.label_error_addEditWindow, "#ff3030", f"Profile name and Folder is required")).start()
            self.log.debug("Profile name and Folder is required")
#------------------------------------------------------------------------

    def selected(self, event):
        if self.treeView.getSelectedElement():
            self.edit_button.enable()
            self.remove.enable()
            self.unselect_button.enable()
            self.move_up.enable()
            self.move_down.enable()

    def saveDataInTree(self):

        self.config.CONFIG['config_sort'] = {}

        for iid in self.treeView.getAllChildren().items():
            key = ""
            fullPath = ""
            pathStatic = False

            self.config.CONFIG['config_sort'][iid[0]] = {}
            key = iid[0]

            value = iid[1]['values']
            tags = iid[1]['tags']

            self.config.CONFIG['config_sort'][key]['disable'] = False

            if 'disable' in tags:
                self.config.CONFIG['config_sort'][key]['disable'] = True

        
            self.config.CONFIG['config_sort'][key]['parent'] = iid[1]['parent']
            self.config.CONFIG['config_sort'][key]['folder'] = value[0]
            for index, parent in enumerate(self.treeView.getAllParentItem(key)[::-1]):

                folder = self.treeView.getItem(parent)["values"][0]
                
                if index != 0:
                    fullPath += f"/{folder}"
                else:
                    if folder[0] != "/" and folder[1] != ":":
                        fullPath += f"{folder}"
                    else:
                        fullPath += f"{folder}"
                        pathStatic = True

            self.config.CONFIG['config_sort'][key]['fullPath'] = fullPath
            self.config.CONFIG['config_sort'][key]['rule'] = value[1].split("|")
            self.config.CONFIG['config_sort'][key]['pathStatic'] = pathStatic

        self.config.CONFIG["unsorted"] = self.toggle_b.get_status()
        doNotSort2 = self.doNotSort_box.get()
        if not doNotSort2 == "":
            self.config.CONFIG["doNotSort"] = doNotSort2.split("|")
        else:
            self.config.CONFIG["doNotSort"] = []

        self.config.saveConfig()

        self.manager_class.showWidget("menu_option")

    def addDataToTree(self):
        for i in self.treeView.tree.get_children():
            self.treeView.tree.delete(i)

        for key in self.config.CONFIG['config_sort']:
            folder: str = self.config.CONFIG['config_sort'][key]['folder']
            rule: list = self.config.CONFIG['config_sort'][key]['rule']
            parent: str | None = self.config.CONFIG['config_sort'][key]['parent']

            tag = ""

            if self.config.CONFIG['config_sort'][key]['disable']:
                tag = "disable"

            parent = parent if parent is not None else ''

            # self.treeView.tree.insert(parent=parent, index=END, iid=key, text="", values=(key, folder, '|'.join(rule)))
            self.treeView.addElement(parent=parent, iid=key, text="", values=[key, folder, '|'.join(rule)], tags=tag)

        self.toggle_b.set_default_status(self.config.CONFIG["unsorted"])
        doNotSort = "|".join(self.config.CONFIG["doNotSort"])
        if not doNotSort == "":
            self.doNotSort_box.delete(0, END)
            self.doNotSort_box.insert(0, doNotSort)

    # this function is call if you hide widget
    def disable(self):
        pass

     # this function is call if you show class
    def enable(self):
        self.grid_propagate(False)
        self.addDataToTree()
        # pass