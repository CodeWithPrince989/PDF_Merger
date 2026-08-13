import os
from pypdf import PdfWriter
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Set the overall look and feel
ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

class PDFMergerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window Configuration
        self.title("Modern PDF Merger")
        self.geometry("600x450")
        self.resizable(False, False)
        
        # Internal State tracking selected files
        self.pdf_files = []
        
        self.create_widgets()

    def create_widgets(self):
        # 1. Main Title
        self.title_label = ctk.CTkLabel(
            self, text="Python PDF Merger", font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=20)

        # 2. File Selection Buttons Frame
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=10)

        self.select_btn = ctk.CTkButton(
            self.btn_frame, text="Select PDF Files", command=self.select_files, width=150
        )
        self.select_btn.grid(row=0, column=0, padx=10)

        self.clear_btn = ctk.CTkButton(
            self.btn_frame, text="Clear List", command=self.clear_list, fg_color="#C0392B", hover_color="#922B21", width=150
        )
        self.clear_btn.grid(row=0, column=1, padx=10)

        # 3. List Box / Status Text Area to show selected files
        self.text_box = ctk.CTkTextbox(self, width=520, height=200, state="disabled")
        self.text_box.pack(pady=10)
        self.update_text_box("No files selected yet. Click 'Select PDF Files' to start.")

        # 4. Action Button (Merge)
        self.merge_btn = ctk.CTkButton(
            self, text="⚡ Merge PDFs", command=self.merge_files, font=ctk.CTkFont(size=16, weight="bold"), height=40, width=200
        )
        self.merge_btn.pack(pady=20)

    def update_text_box(self, initial_message=None):
        """Helper function to cleanly refresh the UI text display."""
        self.text_box.configure(state="normal")
        self.text_box.delete("1.0", ctk.END)
        
        if initial_message:
            self.text_box.insert(ctk.END, initial_message)
        else:
            for idx, file in enumerate(self.pdf_files, 1):
                self.text_box.insert(ctk.END, f"{idx}. {os.path.basename(file)}\n")
                
        self.text_box.configure(state="disabled")

    def select_files(self):
        """Opens a file dialog allowing multiple PDF selections."""
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if files:
            # Append new files to our existing list
            self.pdf_files.extend(files)
            self.update_text_box()

    def clear_list(self):
        """Clears the current selection."""
        self.pdf_files = []
        self.update_text_box("No files selected yet. Click 'Select PDF Files' to start.")

    def merge_files(self):
        """Validates, merges the selected PDFs, and saves the output."""
        if len(self.pdf_files) < 2:
            messagebox.showwarning("Warning", "Please select at least 2 PDF files to merge!")
            return

        # Prompt user where to save the output file
        save_path = filedialog.asksaveasfilename(
            title="Save Merged PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )

        if not save_path:
            return # User cancelled the save dialog

        try:
            merger = PdfWriter()
            for pdf in self.pdf_files:
                merger.append(pdf)
                
            with open(save_path, "wb") as output_file:
                merger.write(output_file)
            
            merger.close()
            messagebox.showinfo("Success", f"PDFs successfully merged and saved to:\n{save_path}")
            self.clear_list()
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during merging:\n{str(e)}")

if __name__ == "__main__":
    app = PDFMergerApp()
    app.mainloop()
