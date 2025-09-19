import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class ImageToPDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convertidor de Imágenes a PDF")
        self.image_paths = []

        title_frame = tk.Frame(root)
        title_frame.pack(pady=10)
        title_label = tk.Label(title_frame, text="Convertidor de Imágenes a PDF", font=("Arial", 16, "bold"))
        title_label.pack()

        main_frame = tk.Frame(root)
        main_frame.pack(padx=25)

        self.listbox = tk.Listbox(main_frame, width=50, selectmode=tk.SINGLE)
        self.listbox.grid(row=0, column=0, padx=(0,20), sticky="n")
        self.listbox.bind("<<ListboxSelect>>", self.show_preview)

        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=0, column=1, sticky="n")

        self.add_btn = tk.Button(btn_frame, text="Agregar", command=self.add_images, width=12)
        self.add_btn.pack(pady=(6, 2))
        self.up_btn = tk.Button(btn_frame, text="Subir", command=self.move_up, width=12)
        self.up_btn.pack(pady=2)
        self.down_btn = tk.Button(btn_frame, text="Bajar", command=self.move_down, width=12)
        self.down_btn.pack(pady=2)
        self.remove_btn = tk.Button(btn_frame, text="Eliminar", command=self.remove_image, width=12)
        self.remove_btn.pack(pady=2)
        self.save_btn = tk.Button(btn_frame, text="Guardar", command=self.save_pdf, width=12)
        self.save_btn.pack(pady=2)

        self.preview_width = 400
        self.preview_height = 300
        self.preview_canvas = tk.Canvas(root, width=self.preview_width, height=self.preview_height, bg="gray90", relief=tk.SUNKEN)
        self.preview_canvas.pack(padx=10, pady=10)
        self.preview_img = None

    def show_preview(self, event=None):
        idx = self.listbox.curselection()
        self.preview_canvas.delete("all")
        if not idx:
            self.preview_canvas.create_text(
                self.preview_width//2, self.preview_height//2,
                text="Previsualización", fill="gray"
            )
            return
        img_path = self.image_paths[idx[0]]
        try:
            img = Image.open(img_path)
            img_ratio = img.width / img.height
            canvas_ratio = self.preview_width / self.preview_height

            if img_ratio > canvas_ratio:
                new_width = self.preview_width
                new_height = int(self.preview_width / img_ratio)
            else:
                new_height = self.preview_height
                new_width = int(self.preview_height * img_ratio)

            img = img.resize((new_width, new_height), Image.LANCZOS)
            self.preview_img = ImageTk.PhotoImage(img)
            x = (self.preview_width - new_width) // 2
            y = (self.preview_height - new_height) // 2
            self.preview_canvas.create_image(x, y, anchor=tk.NW, image=self.preview_img)
        except Exception:
            self.preview_canvas.create_text(
                self.preview_width//2, self.preview_height//2,
                text="No se pudo cargar la imagen", fill="red"
            )

    def add_images(self):
        files = filedialog.askopenfilenames(
            title="Selecciona imágenes",
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff")]
        )
        for f in files:
            if f not in self.image_paths:
                self.image_paths.append(f)
                self.listbox.insert(tk.END, os.path.basename(f))
        if self.image_paths and self.listbox.size() == len(self.image_paths):
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(tk.END)
            self.show_preview()

    def move_up(self):
        idx = self.listbox.curselection()
        if not idx or idx[0] == 0:
            return
        i = idx[0]
        self.image_paths[i-1], self.image_paths[i] = self.image_paths[i], self.image_paths[i-1]
        txt = self.listbox.get(i)
        self.listbox.delete(i)
        self.listbox.insert(i-1, txt)
        self.listbox.selection_set(i-1)
        self.show_preview()

    def move_down(self):
        idx = self.listbox.curselection()
        if not idx or idx[0] == len(self.image_paths)-1:
            return
        i = idx[0]
        self.image_paths[i+1], self.image_paths[i] = self.image_paths[i], self.image_paths[i+1]
        txt = self.listbox.get(i)
        self.listbox.delete(i)
        self.listbox.insert(i+1, txt)
        self.listbox.selection_set(i+1)
        self.show_preview()

    def remove_image(self):
        idx = self.listbox.curselection()
        if not idx:
            return
        i = idx[0]
        self.listbox.delete(i)
        del self.image_paths[i]
        self.show_preview()

    def save_pdf(self):
        if not self.image_paths:
            messagebox.showwarning("Advertencia", "No hay imágenes para guardar.")
            return
        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Guardar PDF como"
        )
        if not save_path:
            return
        images = []
        for img_path in self.image_paths:
            img = Image.open(img_path)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            images.append(img)
        try:
            images[0].save(save_path, save_all=True, append_images=images[1:])
            messagebox.showinfo("Éxito", f"PDF guardado en:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el PDF:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    root.update()
    app = ImageToPDFApp(root)
    root.mainloop()
