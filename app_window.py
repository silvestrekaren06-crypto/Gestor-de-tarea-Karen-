import tkinter as tk
from tkinter import ttk, messagebox
from service.task_service import TaskService


class AppWindow(tk.Tk):

    def __init__(self, task_service: TaskService) -> None:
        super().__init__()
        self._task_service = task_service

        self.title("Gestión de Tareas")
        self.geometry("890x500")
        self.resizable(False, False)
        self.configure(bg="#0f172a")

        self.create_widgets()
        self.show_table()

    def create_widgets(self) -> None:
        title_label = tk.Label(
            self,
            text="📋 Gestión de Tareas",
            font=("Helvetica", 16, "bold"),
            bg="#0f172a",
            fg="#e2e8f0",
        )
        title_label.pack(pady=(15, 5))

        form_frame = tk.LabelFrame(
            self,
            text="Nueva Tarea",
            font=("Helvetica", 10, "bold"),
            bg="#1e293b",
            fg="#e2e8f0",
            padx=10,
            pady=8,
        )
        form_frame.pack(fill="x", padx=20, pady=(5, 10))

        tk.Label(form_frame, text="Título:", bg="#1e293b", fg="#94a3b8").grid(
            row=0, column=0, sticky="w", padx=(0, 5), pady=4
        )

        self.entry_title = tk.Entry(
            form_frame,
            width=30,
            font=("Helvetica", 10),
            bg="#0f172a",
            fg="#e2e8f0",
            insertbackground="white"
        )
        self.entry_title.grid(row=0, column=1, padx=(0, 20), pady=4)

        tk.Label(form_frame, text="Descripción:", bg="#1e293b", fg="#94a3b8").grid(
            row=0, column=2, sticky="w", padx=(0, 5), pady=4
        )

        self.entry_description = tk.Entry(
            form_frame,
            width=35,
            font=("Helvetica", 10),
            bg="#0f172a",
            fg="#e2e8f0",
            insertbackground="white"
        )
        self.entry_description.grid(row=0, column=3, padx=(0, 15), pady=4)

        btn_add = tk.Button(
            form_frame,
            text="➕ Registrar",
            command=self.create_task,
            bg="#22c55e",
            fg="white",
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            activebackground="#4ade80",
        )
        btn_add.grid(row=0, column=4, padx=(0, 5), pady=4)

        table_frame = tk.LabelFrame(
            self,
            text="Lista de Tareas",
            font=("Helvetica", 10, "bold"),
            bg="#1e293b",
            fg="#e2e8f0",
            padx=10,
            pady=8,
        )
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#1e293b",
            foreground="#e2e8f0",
            rowheight=28,
            fieldbackground="#1e293b",
            font=("Helvetica", 10),
        )

        style.configure(
            "Treeview.Heading",
            background="#22c55e",
            foreground="white",
            font=("Helvetica", 10, "bold"),
        )

        style.map(
            "Treeview",
            background=[("selected", "#4ade80")]
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=("id", "title", "description", "status"),
            show="headings",
            yscrollcommand=scrollbar.set,
        )
        scrollbar.config(command=self.tree.yview)

        self.tree.heading("id", text="ID (corto)")
        self.tree.heading("title", text="Título")
        self.tree.heading("description", text="Descripción")
        self.tree.heading("status", text="Estado")

        self.tree.column("id", width=100, anchor="center")
        self.tree.column("title", width=170, anchor="w")
        self.tree.column("description", width=290, anchor="w")
        self.tree.column("status", width=80, anchor="center")

        self.tree.pack(fill="both", expand=True)

    def create_task(self) -> None:
        title: str = self.entry_title.get().strip()
        description: str = self.entry_description.get().strip()

        if not title or not description:
            messagebox.showwarning("Campos vacíos", "Por favor completa el título y la descripción.")
            return

        self._task_service.create_one_task(title, description)
        self.show_table()
        self.clear_inputs()

    def show_table(self) -> None:
        self.clear_table()

        tasks = self._task_service.get_all_task()
        for task in tasks:
            short_id = str(task.uuid)[:8] + "…"
            status = "✅" if task.complete else "⏳"
            self.tree.insert(
                "",
                "end",
                values=(short_id, task.title, task.description, status),
            )

    def clear_table(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

    def clear_inputs(self) -> None:
        self.entry_title.delete(0, "end")
        self.entry_description.delete(0, "end")