import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import os

class EnvManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('VEnv Manager')
        self.geometry('250x600')

        # environment management section
        self.frame_env = tk.LabelFrame(self, text="Environment Management", padx=5, pady=5)
        self.frame_env.pack(fill="x", padx=10, pady=5)

        self.label_env_name = tk.Label(self.frame_env, text="Environment Name:")
        self.label_env_name.pack(side="top", fill="x")
        
        self.entry_env_name = tk.Entry(self.frame_env)
        self.entry_env_name.pack(side="top", fill="x")

        self.btn_create_env = tk.Button(self.frame_env, text="Create Environment", command=self.create_env, bg="green", fg="black")
        self.btn_create_env.pack(side="top", fill="x")

        self.btn_delete_env = tk.Button(self.frame_env, text="Delete Environment", command=self.delete_env, bg="red", fg="black")
        self.btn_delete_env.pack(side="top", fill="x")

        self.btn_list_envs = tk.Button(self.frame_env, text="All Environments List", command=self.list_envs)
        self.btn_list_envs.pack(side="top", fill="x")

        self.listbox_envs = tk.Listbox(self.frame_env)
        self.listbox_envs.pack(side="top", fill="both", expand=True)

        # package management section
        self.frame_packages = tk.LabelFrame(self, text="Package Management", padx=5, pady=5)
        self.frame_packages.pack(fill="both", padx=10, pady=5, expand=True)

        self.label_package_name = tk.Label(self.frame_packages, text="Package Name:")
        self.label_package_name.pack(side="top", fill="x")
        
        self.entry_package_name = tk.Entry(self.frame_packages)
        self.entry_package_name.pack(side="top", fill="x")

        self.btn_install_package = tk.Button(self.frame_packages, text="Install Package",bg="green", command=self.install_package)
        self.btn_install_package.pack(side="top", fill="x")

        self.btn_delete_package = tk.Button(self.frame_packages, text="Delete Package",  bg="red", command=self.delete_package)
        self.btn_delete_package.pack(side="top", fill="x")

        self.btn_install_requirements = tk.Button(self.frame_packages, text="Install requirements.txt", command=self.install_requirements, bg="blue", fg="black")
        self.btn_install_requirements.pack(side="top", fill="x")

        self.btn_install_terminal = tk.Button(self.frame_packages, text="Install using Terminal", command=self.install_using_terminal, bg="orange", fg="black")
        self.btn_install_terminal.pack(side="top", fill="x")

        self.btn_export_packages = tk.Button(self.frame_packages, text="Export Packages List", command=self.export_packages)
        self.btn_export_packages.pack(side="top", fill="x")

        self.btn_import_packages = tk.Button(self.frame_packages, text="Import Packages List", command=self.import_packages)
        self.btn_import_packages.pack(side="top", fill="x")

        self.btn_view_installed_packages = tk.Button(self.frame_packages, text="Manage Installed Packages",  bg="purple", command=self.view_installed_packages)
        self.btn_view_installed_packages.pack(side="top", fill="x")

    def view_installed_packages(self):
        env_name = self.entry_env_name.get()
        if env_name and os.path.exists(env_name):
            installed_packages = subprocess.run([f"{env_name}\\Scripts\\pip", "list"], capture_output=True, text=True).stdout.split("\n")
            installed_packages = [pkg.split() for pkg in installed_packages[2:-1]]
            installed_packages_window = tk.Toplevel(self)
            installed_packages_window.title("Installed Packages")
            self.show_packages_table(installed_packages_window, installed_packages)
        else:
            messagebox.showerror("Error", "Environment does not exist or name not entered.")

    def show_packages_table(self, window, packages):
        frame = tk.Frame(window)
        frame.pack(fill="both", expand=True)

        header = ["Package", "Version", "Delete","Update"]
        for col, header_text in enumerate(header):
            label = tk.Label(frame, text=header_text, relief=tk.RIDGE, width=20)
            label.grid(row=0, column=col)

        for row, package in enumerate(packages, start=1):
            for col, value in enumerate(package[:2]):
                label = tk.Label(frame, text=value, relief=tk.RIDGE)
                label.grid(row=row, column=col)

            delete_button = tk.Button(frame, text="Delete", command=lambda pkg=package[0]: self.delete_installed_package(pkg))
            delete_button.grid(row=row, column=2)

            update_button = tk.Button(frame, text="Update", command=lambda pkg=package[0]: self.update_installed_package(pkg))
            update_button.grid(row=row, column=3)

    def delete_installed_package(self, package_name):
        env_name = self.entry_env_name.get()
        if env_name:
            command = f"{env_name}\\Scripts\\pip uninstall -y {package_name}"
            result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                messagebox.showinfo("Success", f"Package '{package_name}' deleted successfully from '{env_name}'.")
                self.view_installed_packages()
            else:
                messagebox.showerror("Error", f"An error occurred while deleting package '{package_name}': {result.stderr}")
        else:
            messagebox.showerror("Error", "Please enter a valid environment name.")

    def update_installed_package(self, package_name):
        env_name = self.entry_env_name.get()
        if env_name:
            command = f"{env_name}\\Scripts\\pip install --upgrade {package_name}"
            result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                messagebox.showinfo("Success", f"Package '{package_name}' updated successfully in '{env_name}'.")
                self.view_installed_packages()
            else:
                messagebox.showerror("Error", f"An error occurred while updating package '{package_name}': {result.stderr}")
        else:
            messagebox.showerror("Error", "Please enter a valid environment name.")

    def create_env(self):
        env_name = self.entry_env_name.get()
        if env_name:
            subprocess.run(f"python -m venv {env_name}", shell=True)
            messagebox.showinfo("Success", f"Environment '{env_name}' created successfully.")
            self.entry_env_name.delete(0, tk.END)
            self.list_envs()
        else:
            messagebox.showerror("Error", "Please enter a valid environment name.")

    def delete_env(self):
        env_name = self.entry_env_name.get()
        if env_name:
            subprocess.run(f"rmdir /s /q {env_name}", shell=True)
            messagebox.showinfo("Success", f"Environment '{env_name}' deleted successfully.")
            self.entry_env_name.delete(0, tk.END)
            self.list_envs()
        else:
            messagebox.showerror("Error", "Please enter a valid environment name.")
    
    def list_envs(self):
        envs = os.listdir('.')
        self.listbox_envs.delete(0, tk.END)
        for env in envs:
            if os.path.isdir(env) and os.path.exists(os.path.join(env, 'pyvenv.cfg')):
                self.listbox_envs.insert(tk.END, env)

    def install_package(self):
        env_name = self.entry_env_name.get()
        package_name = self.entry_package_name.get()
        if env_name and package_name:
            command = f"{env_name}\\Scripts\\pip install {package_name}"
            result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                messagebox.showinfo("Success", f"Package '{package_name}' installed successfully in '{env_name}'.")
            else:
                messagebox.showerror("Error", f"An error occurred while installing package '{package_name}': {result.stderr}")
        else:
            messagebox.showerror("Error", "Please enter a valid environment name and package name.")

    def delete_package(self):
        env_name = self.entry_env_name.get()
        package_name = self.entry_package_name.get()
        if env_name and package_name:
            command = f"{env_name}\\Scripts\\pip uninstall -y {package_name}"
            result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                messagebox.showinfo("Success", f"Package '{package_name}' deleted successfully from '{env_name}'.")
            else:
                messagebox.showerror("Error", f"An error occurred while deleting package '{package_name}': {result.stderr}")
        else:
            messagebox.showerror("Error", "Please enter a valid environment name and package name.")

    def install_requirements(self):
        env_name = self.entry_env_name.get()
        if env_name and os.path.exists(env_name):
            requirements_file = filedialog.askopenfilename(title="Select requirements.txt file", filetypes=[("Text files", "*.txt")])
            if requirements_file:
                command = f"{env_name}\\Scripts\\pip install -r {requirements_file}"
                result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode == 0:
                    messagebox.showinfo("Success", "Requirements installed successfully.")
                else:
                    messagebox.showerror("Error", f"An error occurred while installing requirements: {result.stderr}")
        else:
            messagebox.showerror("Error", "Environment does not exist or name not entered.")

    def export_packages(self):
        env_name = self.entry_env_name.get()
        if env_name:
            filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], initialfile="packages_list.txt")
            if filename:
                command = f"{env_name}\\Scripts\\pip freeze > {filename}"
                result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode == 0:
                    messagebox.showinfo("Success", "Package list exported successfully.")
                else:
                    messagebox.showerror("Error", f"An error occurred while exporting package list: {result.stderr}")
        else:
            messagebox.showerror("Error", "Please enter a valid environment name.")

    def import_packages(self):
        env_name = self.entry_env_name.get()
        if env_name:
            filename = filedialog.askopenfilename(title="Select package list file", filetypes=[("Text files", "*.txt")])
            if filename:
                command = f"{env_name}\\Scripts\\pip install -r {filename}"
                result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode == 0:
                    messagebox.showinfo("Success", "Package list imported successfully.")
                else:
                    messagebox.showerror("Error", f"An error occurred while importing package list: {result.stderr}")
        else:
            messagebox.showerror("Error", "Please enter a valid environment name.")

    def install_using_terminal(self):
        command = f'cmd /c start cmd /k "cd {os.getcwd()}"'
        subprocess.run(command, shell=True)


if __name__ == "__main__":
    app = EnvManagerApp()
    app.mainloop()
