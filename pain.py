#test
import tkinter as tk
import paramiko
import threading

class SSHGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SSH Command Runner")

        # IP Address Entry
        self.ip_label = tk.Label(root, text="IP Address:")
        self.ip_label.pack()
        self.ip_entry = tk.Entry(root)
        self.ip_entry.pack()

        # Commands Entry
        self.cmd_label = tk.Label(root, text="Commands (use {i} as a variable):")
        self.cmd_label.pack()
        self.cmd_entry = tk.Entry(root)
        self.cmd_entry.pack()

        # Iterations Entry
        self.iter_label = tk.Label(root, text="Iterations:")
        self.iter_label.pack()
        self.iter_entry = tk.Entry(root)
        self.iter_entry.pack()

        # Log Textbox
        self.log_label = tk.Label(root, text="Log:")
        self.log_label.pack()
        self.log_textbox = tk.Text(root, height=10, width=50)
        self.log_textbox.pack()

        # Run Button
        self.run_button = tk.Button(root, text="Run", command=self.run_ssh_commands)
        self.run_button.pack()

    def run_ssh_commands(self):
        # Retrieve user inputs
        ip_address = self.ip_entry.get()
        commands = self.cmd_entry.get().split('\n')
        iterations = int(self.iter_entry.get())

        # Clear log textbox
        self.log_textbox.delete(1.0, tk.END)

        # Create SSH client
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Connect to the remote server
            self.log_textbox.insert(tk.END, f"Connecting to {ip_address}...\n")
            client.connect(ip_address)

            # Execute commands
            for i in range(iterations):
                self.log_textbox.insert(tk.END, f"\nIteration {i+1}:\n")

                for command in commands:
                    # Replace {i} variable with current iteration value
                    command = command.replace('{i}', str(i+1))
                    self.log_textbox.insert(tk.END, f"Executing command: {command}\n")

                    # Execute the command
                    stdin, stdout, stderr = client.exec_command(command)

                    # Log the output
                    output = stdout.read().decode('utf-8')
                    self.log_textbox.insert(tk.END, f"Output:\n{output}\n")

        except Exception as e:
            self.log_textbox.insert(tk.END, f"Error: {str(e)}\n")

        finally:
            # Close the SSH connection
            client.close()

# Create the root window
root = tk.Tk()

# Create the SSHGUI object
ssh_gui = SSHGUI(root)

# Run the GUI
root.mainloop()
