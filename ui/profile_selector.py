import tkinter as tk
from tkinter import simpledialog, messagebox

class ProfileSelector(tk.Frame):
    def __init__(self, master, profile_manager, on_profile_change, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.profile_manager = profile_manager
        self.on_profile_change = on_profile_change
        self.var = tk.StringVar()
        self.dropdown = tk.OptionMenu(self, self.var, *self.profile_manager.list_profiles(), command=self._on_select)
        self.dropdown.pack(side="left", padx=4)
        tk.Button(self, text="New", command=self.create_profile).pack(side="left", padx=2)
        tk.Button(self, text="Delete", command=self.delete_profile).pack(side="left", padx=2)
        tk.Button(self, text="Reset", command=self.reset_profile).pack(side="left", padx=2)
        self.refresh()

    def refresh(self):
        profiles = self.profile_manager.list_profiles()
        menu = self.dropdown['menu']
        menu.delete(0, 'end')
        for p in profiles:
            menu.add_command(label=p, command=lambda v=p: self.var.set(v))
        if profiles:
            self.var.set(self.profile_manager.current_profile or profiles[0])
        else:
            self.var.set('')

    def _on_select(self, value):
        try:
            self.profile_manager.load_profile(value)
            self.on_profile_change()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        self.refresh()

    def create_profile(self):
        name = simpledialog.askstring("New Profile", "Enter profile name:")
        if name:
            try:
                self.profile_manager.create_profile(name)
                self.profile_manager.load_profile(name)
                self.on_profile_change()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        self.refresh()

    def delete_profile(self):
        name = self.var.get()
        if not name:
            return
        if messagebox.askyesno("Delete Profile", f"Delete profile '{name}'?"):
            self.profile_manager.delete_profile(name)
            profiles = self.profile_manager.list_profiles()
            if profiles:
                self.profile_manager.load_profile(profiles[0])
            else:
                self.profile_manager.create_profile('default')
                self.profile_manager.load_profile('default')
            self.on_profile_change()
        self.refresh()

    def reset_profile(self):
        name = self.var.get()
        if not name:
            return
        if messagebox.askyesno("Reset Profile", f"Reset all stats for '{name}'?"):
            self.profile_manager.reset_profile(name)
            self.profile_manager.load_profile(name)
            self.on_profile_change()
        self.refresh()
