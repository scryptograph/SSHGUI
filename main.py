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
       
