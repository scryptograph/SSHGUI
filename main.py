import tkinter as tk
from tkinter import messagebox
import paramiko
import matplotlib.pyplot as plt
import threading

class SSHClient:
    def __init__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connected = False

    def connect(self, host, port, username, password):
        try:
            self.ssh.connect(host, port=port, username=username, password=password)
            self.connected = True
            messagebox.showinfo("Connection", "Connected to the system.")
        except paramiko.AuthenticationException:
            messagebox.showerror("Connection", "Authentication failed.")
        except paramiko.SSHException as ssh_exception:
            messagebox.showerror("Connection", f"SSH connection failed: {ssh_exception}")
        except Exception as e:
            messagebox.showerror("Connection", f"An error occurred: {e}")

    def disconnect(self):
        self.ssh.close()
        self.connected = False

    def execute_command(self, command):
        if self.connected:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            return stdout.read().decode().strip()
        else:
            messagebox.showwarning("Command Execution", "Not connected to the system.")

class ShmooPlotter:
    def __init__(self):
        self.variables = []
        self.commands = []
        self.results = []

    def add_variable(self, variable_name):
        self.variables.append(variable_name)

    def add_command(self, command):
        self.commands.append(command)

    def update_shmoo(self, variable_index, result):
        self.results.append((variable_index, float(result)))

        # Plot the shmoo
        plt.figure()
        for var_index in range(len(self.variables)):
            x = []
            y = []
            for res in self.results:
                if res[0] == var_index:
                    x.append(res[1])
                    y.append(var_index)
            plt.plot(x, y, marker='o', linestyle='-', label=self.variables[var_index])
        plt.xlabel('Result')
        plt.ylabel('Variable')
        plt.legend()
        plt.title('Shmoo Plot')
        plt.show()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SSH Test Commands")
        self.geometry("400x400")

        self.ssh_client = SSHClient()
        self.shmoo_plotter = ShmooPlotter()

        self.host_entry = tk.Entry(self)
        self.host_entry.insert(0, "SSH Host")
        self.host_entry.pack()

        self.port_entry = tk.Entry(self)
        self.port_entry.insert(0, "SSH Port")
        self.port_entry.pack()

        self.username_entry = tk.Entry(self)
        self.username_entry.insert(0, "Username")
        self.username_entry.pack()

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.insert(0, "Password")
        self.password_entry.pack()

        self.connect_button = tk.Button(self, text="Connect", command=self.connect_ssh)
        self.connect_button.pack()

        self.disconnect_button = tk.Button(self, text="Disconnect", command=self.disconnect_ssh, state=tk.DISABLED)
        self.disconnect_button.pack()

        self.command_entry = tk.Entry(self)
        self.command_entry.insert(0, "Test Command")
        self.command_entry.pack()

        self.execute_button = tk.Button(self, text="Execute", command=self.execute_command)
        self.execute_button.pack()

        self.variable_entry = tk.Entry(self)
        self.variable_entry.insert(0, "Variable Name")
        self.variable_entry.pack()

        self.add_variable_button = tk.Button(self, text="Add Variable", command=self.add_variable)
        self.add_variable_button.pack()

        self.shmoo_variable_entry = tk.Entry(self)
        self.shmoo_variable_entry.insert(0, "Variable Index (0-based)")
        self.shmoo_variable_entry.pack()

        self.shmoo_result_entry = tk.Entry(self)
        self.shmoo_result_entry.insert(0, "Result")
        self.shmoo_result_entry.pack()

        self.update_shmoo_button = tk.Button(self, text="Update Shmoo", command=self.update_shmoo)
        self.update_shmoo_button.pack()

        self.setting_button = tk.Button(self, text="Settings", command=self.show_settings)
        self.setting_button.pack()

    def connect_ssh(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.ssh_client.connect(host, port, username, password)

        if self.ssh_client.connected:
            self.connect_button.config(state=tk.DISABLED)
            self.disconnect_button.config(state=tk.NORMAL)

    def disconnect_ssh(self):
        self.ssh_client.disconnect()

        self.connect_button.config(state=tk.NORMAL)
        self.disconnect_button.config(state=tk.DISABLED)

    def execute_command(self):
        command = self.command_entry.get()
        result = self.ssh_client.execute_command(command)
        messagebox.showinfo("Command Execution Result", f"Result:\n{result}")

    def add_variable(self):
        variable_name = self.variable_entry.get()
        self.shmoo_plotter.add_variable(variable_name)

    def update_shmoo(self):
        variable_index = int(self.shmoo_variable_entry.get())
        result = self.shmoo_result_entry.get()
        self.shmoo_plotter.update_shmoo(variable_index, result)

    def show_settings(self):
        settings_window = tk.Toplevel(self)
        settings_window.title("Settings")
        settings_window.geometry("400x300")

        host_label = tk.Label(settings_window, text="SSH Host:")
        host_label.pack()
        host_entry = tk.Entry(settings_window)
        host_entry.insert(0, self.host_entry.get())
        host_entry.pack()

        port_label = tk.Label(settings_window, text="SSH Port:")
        port_label.pack()
        port_entry = tk.Entry(settings_window)
        port_entry.insert(0, self.port_entry.get())
        port_entry.pack()

        username_label = tk.Label(settings_window, text="Username:")
        username_label.pack()
        username_entry = tk.Entry(settings_window)
        username_entry.insert(0, self.username_entry.get())
        username_entry.pack()

        password_label = tk.Label(settings_window, text="Password:")
        password_label.pack()
        password_entry = tk.Entry(settings_window, show="*")
        password_entry.insert(0, self.password_entry.get())
        password_entry.pack()

        save_button = tk.Button(settings_window, text="Save", command=lambda: self.save_settings(settings_window, host_entry, port_entry, username_entry, password_entry))
        save_button.pack()

    def save_settings(self, settings_window, host_entry, port_entry, username_entry, password_entry):
        self.host_entry.delete(0, tk.END)
        self.host_entry.insert(0, host_entry.get())

        self.port_entry.delete(0, tk.END)
        self.port_entry.insert(0, port_entry.get())

        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, username_entry.get())

        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password_entry.get())

        settings_window.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
