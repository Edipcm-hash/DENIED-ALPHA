import tkinter as tk
from tkinter import scrolledtext, font, ttk
import random
import time
import threading
import os
from datetime import datetime
import sys

class CyberTerminalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CYBER TERMINAL v3.0 - DarkNet Infiltration")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0a0a0a')
        
        # Tam ekran modu için
        self.fullscreen = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
        
        # Oyun durumu
        self.game = HackerGameState()
        
        # Fontlar
        self.terminal_font = font.Font(family="Consolas", size=12)
        self.header_font = font.Font(family="Courier New", size=14, weight="bold")
        
        # Renkler
        self.colors = {
            'bg': '#0a0a0a',
            'fg': '#00ff00',
            'header': '#00ffff',
            'warning': '#ff0000',
            'success': '#00ff00',
            'info': '#ffff00',
            'prompt': '#ff00ff'
        }
        
        self.setup_ui()
        self.start_boot_sequence()
    
    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
        return "break"
    
    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.root.attributes("-fullscreen", False)
        return "break"
    
    def setup_ui(self):
        # Ana frame
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Üst bilgi paneli
        self.create_header(main_frame)
        
        # Sol panel - Sistem durumu
        self.create_left_panel(main_frame)
        
        # Orta panel - Terminal
        self.create_terminal_panel(main_frame)
        
        # Sağ panel - Hızlı komutlar
        self.create_right_panel(main_frame)
        
        # Alt panel - İstatistikler
        self.create_bottom_panel(main_frame)
        
        # Giriş alanı
        self.create_input_area(main_frame)
    
    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg='#001a00', height=60)
        header_frame.pack(fill=tk.X, pady=(0, 2))
        header_frame.pack_propagate(False)
        
        # ASCII Art Başlık
        ascii_title = """
 ██████╗██╗   ██╗██████╗ ███████╗██████╗     ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗     
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║     
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝       ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║     
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗       ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║     
╚██████╗   ██║   ██████╔╝███████╗██║  ██║       ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝       ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝
        """
        
        title_label = tk.Label(header_frame, text=ascii_title, 
                              font=self.header_font, fg=self.colors['header'], 
                              bg='#001a00', justify=tk.LEFT)
        title_label.pack(side=tk.LEFT, padx=10)
        
        # Saat ve tarih
        time_frame = tk.Frame(header_frame, bg='#001a00')
        time_frame.pack(side=tk.RIGHT, padx=10)
        
        self.time_label = tk.Label(time_frame, font=self.terminal_font, 
                                  fg=self.colors['info'], bg='#001a00')
        self.time_label.pack()
        
        self.date_label = tk.Label(time_frame, font=self.terminal_font, 
                                   fg=self.colors['info'], bg='#001a00')
        self.date_label.pack()
        
        self.update_clock()
    
    def create_left_panel(self, parent):
        left_frame = tk.Frame(parent, bg='#001111', width=250)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 2))
        left_frame.pack_propagate(False)
        
        # Sistem durumu başlığı
        status_header = tk.Label(left_frame, text="SYSTEM STATUS", 
                                font=self.header_font, fg=self.colors['header'], 
                                bg='#002222', pady=10)
        status_header.pack(fill=tk.X)
        
        # Durum göstergeleri
        indicators_frame = tk.Frame(left_frame, bg='#001111')
        indicators_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_indicator(indicators_frame, "CONNECTION", "secure", "#00ff00")
        self.create_indicator(indicators_frame, "ENCRYPTION", "active", "#00ff00")
        self.create_indicator(indicators_frame, "STEALTH", "high", "#ffff00")
        self.create_indicator(indicators_frame, "ALERT LEVEL", "low", "#00ff00")
        
        # İlerleme barları
        progress_frame = tk.Frame(left_frame, bg='#001111')
        progress_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(progress_frame, text="MISSION PROGRESS", 
                font=self.terminal_font, fg=self.colors['info'], 
                bg='#001111').pack(anchor=tk.W)
        
        self.mission_progress = ttk.Progressbar(progress_frame, length=200, 
                                               mode='determinate', style="green.Horizontal.TProgressbar")
        self.mission_progress.pack(pady=5)
        
        tk.Label(progress_frame, text="NETWORK ACCESS", 
                font=self.terminal_font, fg=self.colors['info'], 
                bg='#001111').pack(anchor=tk.W, pady=(10, 0))
        
        self.network_progress = ttk.Progressbar(progress_frame, length=200, 
                                               mode='determinate', style="cyan.Horizontal.TProgressbar")
        self.network_progress.pack(pady=5)
        
        # Hızlı istatistikler
        stats_frame = tk.Frame(left_frame, bg='#001111')
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.stats_labels = {}
        stats = [
            ("Files Decrypted", "0/50"),
            ("Hints Collected", "0"),
            ("Security Level", "1/10"),
            ("Hosts Found", "0"),
            ("Tools Available", "5")
        ]
        
        for stat, value in stats:
            frame = tk.Frame(stats_frame, bg='#001111')
            frame.pack(fill=tk.X, pady=2)
            
            label = tk.Label(frame, text=stat + ":", font=self.terminal_font, 
                            fg=self.colors['fg'], bg='#001111', width=15, anchor=tk.W)
            label.pack(side=tk.LEFT)
            
            value_label = tk.Label(frame, text=value, font=self.terminal_font, 
                                  fg=self.colors['success'], bg='#001111', anchor=tk.W)
            value_label.pack(side=tk.RIGHT)
            self.stats_labels[stat] = value_label
    
    def create_terminal_panel(self, parent):
        terminal_frame = tk.Frame(parent, bg=self.colors['bg'])
        terminal_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
        
        # Terminal başlığı
        term_header = tk.Frame(terminal_frame, bg='#002a00', height=30)
        term_header.pack(fill=tk.X)
        term_header.pack_propagate(False)
        
        tk.Label(term_header, text="DARKNET TERMINAL v3.0", 
                font=self.terminal_font, fg=self.colors['success'], 
                bg='#002a00').pack(side=tk.LEFT, padx=10)
        
        # Terminal çıktısı alanı
        self.terminal_output = scrolledtext.ScrolledText(
            terminal_frame, 
            bg=self.colors['bg'], 
            fg=self.colors['fg'],
            font=self.terminal_font,
            insertbackground=self.colors['fg'],
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=0,
            state='disabled'
        )
        self.terminal_output.pack(fill=tk.BOTH, expand=True)
        
        # Sağ tıklama menüsü
        self.create_context_menu()
    
    def create_right_panel(self, parent):
        right_frame = tk.Frame(parent, bg='#110011', width=250)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(2, 0))
        right_frame.pack_propagate(False)
        
        # Hızlı komutlar başlığı
        tk.Label(right_frame, text="QUICK COMMANDS", 
                font=self.header_font, fg=self.colors['header'], 
                bg='#220022', pady=10).pack(fill=tk.X)
        
        # Komut butonları
        commands_frame = tk.Frame(right_frame, bg='#110011')
        commands_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        commands = [
            ("SCAN NETWORK", self.cmd_scan),
            ("TEST FIREWALL", self.cmd_firewall),
            ("CRACK PASSWORDS", self.cmd_crack),
            ("FIND FILES", self.cmd_find),
            ("SHOW MISSIONS", self.cmd_missions),
            ("SYSTEM STATUS", self.cmd_status),
            ("CONNECT TARGET", self.cmd_connect),
            ("DECRYPT FILES", self.cmd_decrypt)
        ]
        
        for cmd_text, cmd_func in commands:
            btn = tk.Button(commands_frame, text=cmd_text, 
                          font=self.terminal_font,
                          bg='#330033',
                          fg=self.colors['fg'],
                          activebackground='#440044',
                          activeforeground=self.colors['success'],
                          relief=tk.RAISED,
                          borderwidth=2,
                          command=cmd_func)
            btn.pack(fill=tk.X, pady=5, ipady=5)
        
        # Araçlar listesi
        tools_frame = tk.Frame(right_frame, bg='#110011')
        tools_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(tools_frame, text="AVAILABLE TOOLS", 
                font=self.terminal_font, fg=self.colors['info'], 
                bg='#110011').pack(anchor=tk.W)
        
        self.tools_listbox = tk.Listbox(tools_frame, 
                                       bg='#220022',
                                       fg=self.colors['success'],
                                       font=self.terminal_font,
                                       height=6,
                                       relief=tk.FLAT,
                                       borderwidth=1)
        self.tools_listbox.pack(fill=tk.X, pady=5)
        
        for tool in self.game.available_tools:
            self.tools_listbox.insert(tk.END, f"▶ {tool}")
    
    def create_bottom_panel(self, parent):
        bottom_frame = tk.Frame(parent, bg='#001122', height=100)
        bottom_frame.pack(fill=tk.X, pady=(2, 0))
        bottom_frame.pack_propagate(False)
        
        # Ağ durumu
        net_frame = tk.Frame(bottom_frame, bg='#001122')
        net_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(net_frame, text="NETWORK ACTIVITY", 
                font=self.terminal_font, fg=self.colors['header'], 
                bg='#001122').pack(anchor=tk.W)
        
        self.network_display = tk.Label(net_frame, text="", 
                                       font=self.terminal_font, 
                                       fg=self.colors['success'], 
                                       bg='#001122', justify=tk.LEFT)
        self.network_display.pack(anchor=tk.W)
        
        # Son olaylar
        log_frame = tk.Frame(bottom_frame, bg='#001122')
        log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(log_frame, text="RECENT ACTIVITY", 
                font=self.terminal_font, fg=self.colors['header'], 
                bg='#001122').pack(anchor=tk.W)
        
        self.activity_display = tk.Label(log_frame, text="", 
                                        font=self.terminal_font, 
                                        fg=self.colors['info'], 
                                        bg='#001122', justify=tk.LEFT)
        self.activity_display.pack(anchor=tk.W)
    
    def create_input_area(self, parent):
        input_frame = tk.Frame(parent, bg='#002200', height=40)
        input_frame.pack(fill=tk.X, pady=(2, 0))
        input_frame.pack_propagate(False)
        
        # Prompt
        self.prompt_label = tk.Label(input_frame, 
                                    text=f"{self.game.username}@darknet:~$ ",
                                    font=self.terminal_font,
                                    fg=self.colors['prompt'],
                                    bg='#002200')
        self.prompt_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Komut girişi
        self.command_entry = tk.Entry(input_frame,
                                     bg='#003300',
                                     fg=self.colors['fg'],
                                     font=self.terminal_font,
                                     insertbackground=self.colors['fg'],
                                     relief=tk.FLAT,
                                     borderwidth=0)
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, ipady=5)
        self.command_entry.bind("<Return>", self.execute_command)
        self.command_entry.focus_set()
        
        # Gönder butonu
        send_btn = tk.Button(input_frame, text="⏎",
                           font=self.terminal_font,
                           bg='#004400',
                           fg=self.colors['success'],
                           relief=tk.RAISED,
                           borderwidth=1,
                           command=lambda: self.execute_command())
        send_btn.pack(side=tk.RIGHT, padx=(0, 10), ipadx=10)
    
    def create_context_menu(self):
        self.context_menu = tk.Menu(self.terminal_output, tearoff=0, 
                                   bg='#003300', fg=self.colors['fg'],
                                   font=self.terminal_font)
        self.context_menu.add_command(label="Copy", command=self.copy_text)
        self.context_menu.add_command(label="Clear Terminal", command=self.clear_terminal)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Save Log", command=self.save_log)
        
        self.terminal_output.bind("<Button-3>", self.show_context_menu)
    
    def create_indicator(self, parent, text, status, color):
        frame = tk.Frame(parent, bg='#001111')
        frame.pack(fill=tk.X, pady=5)
        
        label = tk.Label(frame, text=text, font=self.terminal_font, 
                        fg=self.colors['fg'], bg='#001111', width=12, anchor=tk.W)
        label.pack(side=tk.LEFT)
        
        # LED göstergesi
        led_canvas = tk.Canvas(frame, width=20, height=20, bg='#001111', 
                              highlightthickness=0)
        led_canvas.pack(side=tk.LEFT, padx=(10, 5))
        led_canvas.create_oval(2, 2, 18, 18, fill=color, outline=color)
        
        status_label = tk.Label(frame, text=status, font=self.terminal_font, 
                               fg=color, bg='#001111', anchor=tk.W)
        status_label.pack(side=tk.LEFT, padx=(5, 0))
    
    def update_clock(self):
        now = datetime.now()
        self.time_label.config(text=now.strftime("%H:%M:%S"))
        self.date_label.config(text=now.strftime("%Y-%m-%d"))
        self.root.after(1000, self.update_clock)
    
    def start_boot_sequence(self):
        boot_messages = [
            ("Initializing DarkNet OS...", "#00ff00"),
            ("Loading kernel modules...", "#00ff00"),
            ("Starting encryption services...", "#00ff00"),
            ("Establishing secure connection...", "#00ff00"),
            ("Launching terminal interface...", "#00ff00"),
            ("SYSTEM READY", "#00ffff")
        ]
        
        def boot_animation():
            for i, (msg, color) in enumerate(boot_messages):
                self.print_to_terminal(f"> {msg}", color)
                time.sleep(0.5 if i < len(boot_messages)-1 else 1)
            
            self.print_to_terminal("\n" + "="*60, "#00ffff")
            self.print_to_terminal("CYBER TERMINAL v3.0 - ONLINE", "#00ffff")
            self.print_to_terminal("Type 'help' for available commands", "#00ff00")
            self.print_to_terminal("="*60 + "\n", "#00ffff")
            
            # Oyunu başlat
            self.prompt_for_username()
        
        threading.Thread(target=boot_animation, daemon=True).start()
    
    def prompt_for_username(self):
        def get_username():
            self.print_to_terminal("Enter your codename: ", "#ffff00", end="")
            self.root.after(100, self.command_entry.focus_set)
            
        self.root.after(500, get_username)
    
    def execute_command(self, event=None):
        cmd = self.command_entry.get().strip()
        if not cmd:
            return
        
        # Komutu terminale yaz
        self.print_to_terminal(f"{self.game.username}@darknet:~$ {cmd}", self.colors['prompt'])
        
        # Komutu işle
        self.process_command(cmd)
        
        # Giriş alanını temizle
        self.command_entry.delete(0, tk.END)
        
        # Terminali otomatik kaydır
        self.terminal_output.see(tk.END)
    
    def process_command(self, cmd):
        parts = cmd.lower().split()
        if not parts:
            return
        
        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        if command == "help":
            self.show_help()
        elif command == "clear":
            self.clear_terminal()
        elif command == "scan":
            self.cmd_scan()
        elif command == "firewall":
            self.cmd_firewall()
        elif command == "crack":
            self.cmd_crack()
        elif command == "find":
            self.cmd_find()
        elif command == "missions":
            self.cmd_missions()
        elif command == "status":
            self.cmd_status()
        elif command == "connect":
            self.cmd_connect(args)
        elif command == "decrypt":
            self.cmd_decrypt()
        elif command == "exit":
            self.exit_game()
        elif command == "whoami":
            self.print_to_terminal(f"User: {self.game.username}", self.colors['info'])
            self.print_to_terminal(f"Access Level: ROOT", self.colors['success'])
        elif command == "ls":
            self.print_to_terminal("mission_brief.txt  network_map.log  tools/  target_list.csv", self.colors['fg'])
        elif command == "pwd":
            self.print_to_terminal(f"/home/{self.game.username}/darknet", self.colors['fg'])
        else:
            self.print_to_terminal(f"Command '{command}' not found. Type 'help' for available commands.", self.colors['warning'])
    
    def show_help(self):
        help_text = """
Available Commands:
  help                    Show this help message
  clear                   Clear terminal screen
  whoami                  Show current user
  pwd                     Show current directory
  ls                      List files
  
  scan                    Scan network for targets
  firewall                Test firewall security
  crack                   Password cracking attack
  find                    Search for files
  connect <ip>            Connect to target
  decrypt                 Decrypt captured files
  
  missions                Show available missions
  status                  Show system status
  exit                    Exit the terminal
"""
        self.print_to_terminal(help_text, self.colors['info'])
    
    def cmd_scan(self):
        def scan_thread():
            self.print_to_terminal("Starting network reconnaissance...", "#00ff00")
            time.sleep(1)
            
            result = self.game.scan_network()
            for line in result:
                self.print_to_terminal(line, "#00ff00" if "✓" in line else "#ffff00")
            
            self.update_stats()
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def cmd_firewall(self):
        def firewall_thread():
            self.print_to_terminal("Analyzing firewall configuration...", "#00ff00")
            time.sleep(1.5)
            
            result = self.game.test_firewall()
            for line in result:
                color = "#00ff00" if "✓" in line else "#ff0000" if "✗" in line else "#ffff00"
                self.print_to_terminal(line, color)
            
            self.update_stats()
        
        threading.Thread(target=firewall_thread, daemon=True).start()
    
    def cmd_crack(self):
        if not self.game.known_passwords:
            self.print_to_terminal("No password hashes available!", "#ff0000")
            return
        
        def crack_thread():
            self.print_to_terminal("Starting brute-force attack...", "#00ff00")
            
            # Animasyon
            for i in range(1, 101, random.randint(5, 15)):
                bar = "█" * (i//2) + "░" * (50 - i//2)
                self.print_to_terminal(f"\rProgress: [{i:3}%] {bar}", "#ffff00", update=True)
                time.sleep(0.1)
            
            self.print_to_terminal("", "#ffff00")  # Yeni satır
            
            result = self.game.crack_password()
            color = "#00ff00" if "✓" in result else "#ff0000"
            self.print_to_terminal(result, color)
            
            self.update_stats()
        
        threading.Thread(target=crack_thread, daemon=True).start()
    
    def cmd_find(self):
        def find_thread():
            self.print_to_terminal("Searching filesystem for valuable data...", "#00ff00")
            time.sleep(1)
            
            result = self.game.find_files()
            for line in result:
                color = "#00ff00" if "+" in line else "#ff00ff" if "hash:" in line else "#ffff00"
                self.print_to_terminal(line, color)
            
            self.update_stats()
        
        threading.Thread(target=find_thread, daemon=True).start()
    
    def cmd_missions(self):
        missions = self.game.get_missions()
        self.print_to_terminal("\nAVAILABLE MISSIONS:", "#00ffff")
        self.print_to_terminal("─" * 40, "#00ffff")
        
        for i, (name, desc, reward, risk) in enumerate(missions, 1):
            self.print_to_terminal(f"\n[{i}] {name}", "#ffff00")
            self.print_to_terminal(f"   {desc}", "#00ff00")
            self.print_to_terminal(f"   Reward: {reward} | Risk: {risk}", "#ff00ff")
        
        self.print_to_terminal("\nSelect with: connect mission <number>", "#00ffff")
    
    def cmd_status(self):
        status = self.game.get_status()
        self.print_to_terminal("\nSYSTEM STATUS REPORT:", "#00ffff")
        self.print_to_terminal("─" * 40, "#00ffff")
        
        for line in status:
            self.print_to_terminal(line, "#00ff00")
        
        self.update_stats()
    
    def cmd_connect(self, args):
        if not args:
            self.print_to_terminal("Usage: connect <ip_address> or connect mission <number>", "#ff0000")
            return
        
        if args[0] == "mission":
            if len(args) < 2:
                self.print_to_terminal("Usage: connect mission <number>", "#ff0000")
                return
            
            try:
                mission_num = int(args[1]) - 1
                self.execute_mission(mission_num)
            except ValueError:
                self.print_to_terminal("Invalid mission number!", "#ff0000")
        else:
            ip = args[0]
            self.print_to_terminal(f"Connecting to {ip}...", "#00ff00")
            
            def connect_thread():
                time.sleep(1.5)
                result = self.game.connect_to_target(ip)
                color = "#00ff00" if "✓" in result else "#ff0000"
                self.print_to_terminal(result, color)
                self.update_stats()
            
            threading.Thread(target=connect_thread, daemon=True).start()
    
    def cmd_decrypt(self):
        def decrypt_thread():
            self.print_to_terminal("Starting file decryption...", "#00ff00")
            
            result = self.game.decrypt_files()
            for line in result:
                color = "#00ff00" if "✓" in line else "#ffff00"
                self.print_to_terminal(line, color)
            
            self.update_stats()
            
            if self.game.encrypted_files >= 50:
                self.show_victory_screen()
        
        threading.Thread(target=decrypt_thread, daemon=True).start()
    
    def execute_mission(self, mission_num):
        def mission_thread():
            self.print_to_terminal("Executing mission...", "#00ff00")
            time.sleep(1)
            
            result = self.game.execute_mission(mission_num)
            for line in result:
                color = "#00ff00" if "✓" in line else "#ff0000"
                self.print_to_terminal(line, color)
            
            self.update_stats()
        
        threading.Thread(target=mission_thread, daemon=True).start()
    
    def update_stats(self):
        # İstatistikleri güncelle
        self.stats_labels["Files Decrypted"].config(
            text=f"{self.game.encrypted_files}/50"
        )
        self.stats_labels["Hints Collected"].config(
            text=str(self.game.hints_collected)
        )
        self.stats_labels["Security Level"].config(
            text=f"{self.game.security_level}/10"
        )
        self.stats_labels["Hosts Found"].config(
            text=str(len(self.game.discovered_ips))
        )
        self.stats_labels["Tools Available"].config(
            text=str(len(self.game.available_tools))
        )
        
        # İlerleme barlarını güncelle
        self.mission_progress['value'] = (self.game.encrypted_files / 50) * 100
        self.network_progress['value'] = min(self.game.security_level * 10, 100)
        
        # Araçları güncelle
        self.tools_listbox.delete(0, tk.END)
        for tool in self.game.available_tools:
            self.tools_listbox.insert(tk.END, f"▶ {tool}")
        
        # Network aktivitesini güncelle
        network_text = f"IP: {self.game.ip_address}\nTarget: {self.game.target_ip}"
        if self.game.discovered_ips:
            network_text += f"\nHosts: {len(self.game.discovered_ips)} found"
        self.network_display.config(text=network_text)
        
        # Son aktiviteyi güncelle
        activity = f"Files: {self.game.encrypted_files}/50\n"
        activity += f"Hints: {self.game.hints_collected}\n"
        activity += f"Security: Lvl {self.game.security_level}"
        self.activity_display.config(text=activity)
    
    def print_to_terminal(self, text, color="#00ff00", end="\n", update=False):
        self.terminal_output.config(state='normal')
        
        if update:
            # Son satırı güncelle
            self.terminal_output.delete("end-2l", "end-1c")
        
        self.terminal_output.insert(tk.END, text + end, color)
        self.terminal_output.tag_config(color, foreground=color)
        
        self.terminal_output.config(state='disabled')
        self.terminal_output.see(tk.END)
    
    def clear_terminal(self):
        self.terminal_output.config(state='normal')
        self.terminal_output.delete(1.0, tk.END)
        self.terminal_output.config(state='disabled')
    
    def copy_text(self):
        try:
            selected = self.terminal_output.selection_get()
            self.root.clipboard_clear()
            self.root.clipboard_append(selected)
        except:
            pass
    
    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def save_log(self):
        # Basit log kaydetme (gerçek uygulamada dosya kaydetme dialogu kullanılır)
        self.print_to_terminal("Log saved to /var/log/darknet_session.log", "#00ff00")
    
    def show_victory_screen(self):
        victory_text = """
        ╔══════════════════════════════════════════╗
        ║                                          ║
        ║            MISSION ACCOMPLISHED!         ║
        ║                                          ║
        ║    All classified files decrypted!       ║
        ║    Military network infiltrated!         ║
        ║    Operation successful!                 ║
        ║                                          ║
        ╚══════════════════════════════════════════╝
        """
        
        self.print_to_terminal("\n" + "="*60, "#00ff00")
        self.print_to_terminal(victory_text, "#00ffff")
        self.print_to_terminal("="*60, "#00ff00")
    
    def exit_game(self):
        self.print_to_terminal("\nClosing connection...", "#00ff00")
        self.print_to_terminal("Cleaning traces...", "#00ff00")
        self.print_to_terminal("Shutting down DarkNet OS...", "#00ff00")
        
        self.root.after(2000, self.root.destroy)


class HackerGameState:
    def __init__(self):
        self.username = "anonymous"
        self.ip_address = "192.168.1.100"
        self.target_ip = "172.16.0.1"
        self.security_level = 1
        self.hints_collected = 0
        self.encrypted_files = 0
        self.discovered_ips = []
        self.available_tools = ["nmap", "ssh", "ftp", "sqlmap", "ping", "whois"]
        self.known_passwords = []
    
    def scan_network(self):
        result = []
        result.append(f"Scanning target: {self.target_ip}")
        result.append("PORT     STATE    SERVICE")
        result.append("22/tcp   open     ssh")
        result.append("80/tcp   open     http")
        result.append("443/tcp  filtered https")
        
        new_ips = random.randint(1, 3)
        for _ in range(new_ips):
            ip = f"172.16.0.{random.randint(10, 250)}"
            if ip not in self.discovered_ips:
                self.discovered_ips.append(ip)
        
        result.append(f"Discovered {new_ips} new hosts")
        
        if random.random() < 0.3:
            self.security_level = min(self.security_level + 1, 10)
            result.append("⚠️  Security alert! Trace detected!")
        
        return result
    
    def test_firewall(self):
        result = []
        firewall_types = ["Cisco ASA", "Fortinet", "Palo Alto", "iptables"]
        firewall = random.choice(firewall_types)
        
        result.append(f"Firewall Type: {firewall}")
        result.append(f"Security Level: {self.security_level}/10")
        
        success_chance = 0.7 - (self.security_level * 0.05)
        
        if random.random() < success_chance:
            hints = random.randint(1, 3)
            self.hints_collected += hints
            result.append("✓ Firewall bypass successful!")
            result.append(f"Gained {hints} hints")
            
            if random.random() < 0.3:
                new_tool = random.choice(["wireshark", "metasploit", "hydra"])
                if new_tool not in self.available_tools:
                    self.available_tools.append(new_tool)
                    result.append(f"New tool unlocked: {new_tool}")
        else:
            result.append("✗ Firewall blocked the attack!")
            self.security_level = min(self.security_level + 1, 10)
        
        return result
    
    def crack_password(self):
        if not self.known_passwords:
            return "No password hashes available!"
        
        if random.random() < 0.4:
            self.encrypted_files += random.randint(2, 6)
            return f"✓ Password cracked! Decrypted {self.encrypted_files}/50 files"
        else:
            self.security_level = min(self.security_level + 1, 10)
            if self.known_passwords:
                self.known_passwords.pop()
            return "✗ Password resistant to attack"
    
    def find_files(self):
        result = []
        files = [
            ("/var/log/auth.log", 2),
            ("/etc/shadow.bak", 3),
            ("/tmp/.hidden/keys.txt", 4),
            ("/var/www/html/config.php", 2)
        ]
        
        found = random.sample(files, random.randint(2, 4))
        
        for file, value in found:
            result.append(f"Found: {file}")
            
            if random.random() < 0.6:
                self.hints_collected += value
                result.append(f"  +{value} hints")
            
            if random.random() < 0.25:
                hash_val = self.generate_hash()
                self.known_passwords.append(hash_val)
                result.append(f"  Found hash: {hash_val}")
        
        return result
    
    def get_missions(self):
        return [
            ("EXFILTRATE DATA", "Steal classified documents", "5 hints", "high"),
            ("PLANT BACKDOOR", "Install persistent access", "8 hints", "critical"),
            ("CLEAR LOGS", "Remove evidence", "3 hints", "medium"),
            ("MAP NETWORK", "Discover all devices", "4 hints", "medium")
        ]
    
    def get_status(self):
        return [
            f"User: {self.username}",
            f"IP: {self.ip_address}",
            f"Target: {self.target_ip}",
            f"Hints: {self.hints_collected}",
            f"Files: {self.encrypted_files}/50",
            f"Security: {self.security_level}/10",
            f"Hosts: {len(self.discovered_ips)}",
            f"Tools: {len(self.available_tools)}"
        ]
    
    def connect_to_target(self, ip):
        if ip == self.target_ip:
            if self.hints_collected >= 10:
                files_found = random.randint(3, 8)
                self.encrypted_files += files_found
                return f"✓ Connected to primary target! Found {files_found} files."
            else:
                return "✗ Insufficient access rights! Collect more hints."
        else:
            self.hints_collected += random.randint(1, 3)
            return f"Connected to secondary system. Gained {self.hints_collected} hints."
    
    def decrypt_files(self):
        if self.encrypted_files >= 50:
            return ["✓ All files already decrypted!"]
        
        needed = self.hints_collected // 2
        if needed < 1:
            return ["✗ Not enough hints to decrypt files!"]
        
        to_decrypt = min(needed, 50 - self.encrypted_files)
        self.encrypted_files += to_decrypt
        self.hints_collected -= to_decrypt * 2
        
        return [
            f"✓ Successfully decrypted {to_decrypt} files!",
            f"Total: {self.encrypted_files}/50 files decrypted"
        ]
    
    def execute_mission(self, mission_num):
        missions = self.get_missions()
        if mission_num < 0 or mission_num >= len(missions):
            return ["✗ Invalid mission number!"]
        
        _, _, reward_str, risk = missions[mission_num]
        reward = int(reward_str.split()[0])
        
        success_chance = {"low": 0.9, "medium": 0.7, "high": 0.5, "critical": 0.3}[risk]
        
        if random.random() < success_chance:
            self.hints_collected += reward
            result = ["✓ Mission accomplished!"]
            result.append(f"Gained {reward} hints")
            
            if random.random() < 0.4:
                new_ip = f"10.0.{random.randint(0,255)}.{random.randint(1,254)}"
                self.discovered_ips.append(new_ip)
                result.append(f"Discovered new IP: {new_ip}")
        else:
            result = ["✗ Mission failed!"]
            self.security_level = min(self.security_level + 2, 10)
            result.append(f"Security increased to {self.security_level}")
        
        return result
    
    def generate_hash(self):
        hash_types = ["md5", "sha1", "sha256"]
        hash_type = random.choice(hash_types)
        chars = "abcdef0123456789"
        hash_val = ''.join(random.choice(chars) for _ in range(32))
        return f"{hash_type}:{hash_val}"


def main():
    root = tk.Tk()
    
    # Tkinter stilini ayarla
    style = ttk.Style()
    style.theme_use('clam')
    
    # Özel progressbar stilleri
    style.configure("green.Horizontal.TProgressbar", 
                   background='#00ff00',
                   troughcolor='#003300',
                   bordercolor='#00aa00',
                   lightcolor='#00ff00',
                   darkcolor='#00aa00')
    
    style.configure("cyan.Horizontal.TProgressbar", 
                   background='#00ffff',
                   troughcolor='#003333',
                   bordercolor='#00aaaa',
                   lightcolor='#00ffff',
                   darkcolor='#00aaaa')
    
    app = CyberTerminalGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()