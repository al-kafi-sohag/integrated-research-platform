import customtkinter as ctk
from tkinter import filedialog
import os
import threading
from ..scraper.scholar_scraper import ScholarScraper
from ..utils.file_handler import FileHandler

class ScholarScraperApp:
    def __init__(self):
        self.scraper = ScholarScraper()
        self.file_handler = FileHandler()
        self.setup_window()
        self.setup_ui()

    def setup_window(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.window = ctk.CTk()
        self.window.title("Google Scholar Scraper")
        self.window.geometry("800x800")
        self.window.resizable(False, False)

    def setup_ui(self):
        self.setup_main_frame()
        self.setup_header()
        self.setup_input_frame()
        self.setup_buttons()
        self.setup_progress()
        self.setup_team_info()

    def setup_main_frame(self):
        self.main_frame = ctk.CTkFrame(self.window, fg_color="#1A1A1A")
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    def setup_header(self):
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="#2B2B2B")
        header_frame.pack(fill="x", padx=20, pady=(0, 20))

        title_label = ctk.CTkLabel(
            header_frame, 
            text="Google Scholar Scraper",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=(10, 5))

        university_label = ctk.CTkLabel(
            header_frame,
            text="Department of Electronics and Communication Engineering\nHajee Mohammad Danesh Science and Technology University\nDinajpur, Bangladesh",
            font=ctk.CTkFont(size=16),
            text_color="#3B8ED0"
        )
        university_label.pack(pady=(0, 10))

    def setup_input_frame(self):
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color="#2B2B2B")
        self.input_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Query input
        query_label = ctk.CTkLabel(
            self.input_frame,
            text="Article Title or Keyword:",
            font=ctk.CTkFont(size=14),
            text_color="#CCCCCC"
        )
        query_label.pack(anchor="w", padx=20, pady=(15, 0))

        self.entry_query = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Enter search terms...",
            height=35,
            width=700,
            fg_color="#232323",
            border_color="#3B8ED0",
            text_color="white"
        )
        self.entry_query.pack(padx=20, pady=(5, 15))

        # Pages input
        pages_label = ctk.CTkLabel(
            self.input_frame,
            text="Number of Pages:",
            font=ctk.CTkFont(size=14),
            text_color="#CCCCCC"
        )
        pages_label.pack(anchor="w", padx=20)

        self.entry_pages = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Enter number of pages to scrape...",
            height=35,
            width=700,
            fg_color="#232323",
            border_color="#3B8ED0",
            text_color="white"
        )
        self.entry_pages.pack(padx=20, pady=(5, 15))

        # Folder selection
        folder_label = ctk.CTkLabel(
            self.input_frame,
            text="Output Folder (optional, default: ./data/):",
            font=ctk.CTkFont(size=14),
            text_color="#CCCCCC"
        )
        folder_label.pack(anchor="w", padx=20)

        folder_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        folder_frame.pack(fill="x", padx=20, pady=(5, 20))

        self.entry_folder = ctk.CTkEntry(
            folder_frame,
            placeholder_text="Select output folder... (default: ./data/)",
            height=35,
            width=580,
            fg_color="#232323",
            border_color="#3B8ED0",
            text_color="white"
        )
        self.entry_folder.pack(side="left")

        browse_button = ctk.CTkButton(
            folder_frame,
            text="Browse",
            width=100,
            height=35,
            fg_color="#3B8ED0",
            hover_color="#2B6F9F",
            command=self.browse_folder
        )
        browse_button.pack(side="right", padx=(20, 0))

    def setup_buttons(self):
        self.buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.buttons_frame.pack(pady=(0, 20))

        self.start_button = ctk.CTkButton(
            self.buttons_frame,
            text="Start Scraping",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=200,
            height=45,
            fg_color="#3B8ED0",
            hover_color="#2B6F9F",
            command=self.scrape_articles
        )
        self.start_button.pack(side="left", padx=10)

        self.open_file_button = ctk.CTkButton(
            self.buttons_frame,
            text="Open File",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=200,
            height=45,
            fg_color="#28A745",
            hover_color="#218838",
            command=self.open_excel_file
        )
        self.open_file_button.pack_forget()

    def setup_progress(self):
        self.progress_bar = ctk.CTkProgressBar(self.main_frame)
        self.progress_bar.set(0)
        self.progress_bar.configure(
            mode="determinate",
            width=700,
            height=15,
            fg_color="#232323",
            progress_color="#3B8ED0"
        )
        self.progress_bar.pack_forget()

        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Ready to scrape",
            font=ctk.CTkFont(size=14),
            text_color="#CCCCCC"
        )
        self.status_label.pack(pady=(0, 20))

    def setup_team_info(self):
        team_frame = ctk.CTkFrame(self.main_frame, fg_color="#2B2B2B")
        team_frame.pack(fill="x", padx=20, pady=(0, 10))

        team_label = ctk.CTkLabel(
            team_frame,
            text="Development Team",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#3B8ED0"
        )
        team_label.pack(pady=(10, 15))

        team_members = [
            ("Al Kafi Sohag", "2002116"),
            ("Md. Humaun Kabir", "2002174"),
            ("Sheikh Md Rezanur Hasan", "2002169")
        ]

        for name, student_id in team_members:
            member_frame = ctk.CTkFrame(team_frame, fg_color="transparent")
            member_frame.pack(fill="x", pady=2)
            
            member_label = ctk.CTkLabel(
                member_frame,
                text=f"{name}",
                font=ctk.CTkFont(size=14),
                text_color="#CCCCCC"
            )
            member_label.pack(side="left", padx=(20, 0))
            
            id_label = ctk.CTkLabel(
                member_frame,
                text=f"Student ID: {student_id}",
                font=ctk.CTkFont(size=14),
                text_color="#999999"
            )
            id_label.pack(side="right", padx=(0, 20))

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.entry_folder.delete(0, ctk.END)
            self.entry_folder.insert(0, folder_path)

    def update_progress(self, progress, message):
        if progress >= 0:
            self.progress_bar.set(progress)
            if progress == 1:
                self.progress_bar.configure(progress_color="#00FF00")
            elif progress == -1:
                self.progress_bar.configure(progress_color="#FF0000")
            else:
                self.progress_bar.configure(progress_color="#3B8ED0")
        self.status_label.configure(text=message)
        self.window.update()

    def scrape_in_thread(self, query, num_pages, folder_path, filename):
        try:
            articles = self.scraper.scrape_articles(query, num_pages, self.update_progress)
            full_path = os.path.join(folder_path, filename)
            saved_file = self.file_handler.save_to_excel(articles, full_path)
            self.window.current_file = saved_file
            
            self.window.after(0, lambda: self.status_label.configure(
                text=f"Extraction complete! Data saved to: {filename}",
                text_color="green"
            ))
            self.window.after(0, lambda: self.progress_bar.configure(progress_color="#00FF00"))
            self.window.after(0, lambda: self.start_button.configure(state="normal"))
            self.window.after(0, lambda: self.open_file_button.pack(side="left", padx=10))
            
        except Exception as e:
            error_message = f"Error during scraping: {str(e)}"
            self.window.after(0, lambda: self.status_label.configure(text=error_message, text_color="red"))
            self.window.after(0, lambda: self.progress_bar.configure(progress_color="#FF0000"))
            self.window.after(0, lambda: self.start_button.configure(state="normal"))
            self.window.after(0, lambda: self.open_file_button.pack_forget())

    def scrape_articles(self):
        query = self.entry_query.get()
        try:
            num_pages = int(self.entry_pages.get())
        except ValueError:
            self.status_label.configure(text="Please enter a valid number of pages", text_color="red")
            return

        if not query:
            self.status_label.configure(text="Please enter a search query", text_color="red")
            return

        self.start_button.configure(state="disabled")
        self.progress_bar.configure(progress_color="#3B8ED0")
        self.progress_bar.set(0)
        self.progress_bar.pack(padx=20, pady=(0, 20))
        
        self.status_label.configure(text="Initializing scraping...", text_color="white")
        self.window.update()
        
        filename = self.file_handler.generate_filename(query)
        folder_path = self.file_handler.ensure_data_directory(self.entry_folder.get())

        thread = threading.Thread(
            target=self.scrape_in_thread,
            args=(query, num_pages, folder_path, filename),
            daemon=True
        )
        thread.start()

    def open_excel_file(self):
        try:
            if hasattr(self.window, 'current_file') and os.path.exists(self.window.current_file):
                os.startfile(self.window.current_file)
            else:
                self.status_label.configure(text="No file available to open", text_color="red")
        except Exception as e:
            self.status_label.configure(text=f"Error opening file: {str(e)}", text_color="red")

    def run(self):
        self.window.mainloop()
