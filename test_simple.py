"""
Test simplifié de l'éditeur de cartes avec formatage de texte
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os

# Ajouter le dossier lib au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from database_simple import CardRepo, Card
from text_formatting_editor import TextFormattingEditor
from lua_export_enhanced import LuaExporter

class SimpleCardEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🃏 Éditeur de Cartes Love2D - Simple")
        self.root.geometry("800x600")
        
        # Initialize database
        self.repo = CardRepo("cartes.db")
        self.current_card = None
        self.setup_ui()
        self.refresh_card_list()

    def setup_ui(self):
        """Setup the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel - Card list
        left_frame = ttk.LabelFrame(main_frame, text="📋 Liste des Cartes", padding=10)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Card list
        self.card_listbox = tk.Listbox(left_frame)
        self.card_listbox.pack(fill='both', expand=True)
        self.card_listbox.bind('<<ListboxSelect>>', self.on_card_select)
        
        # List buttons
        list_button_frame = ttk.Frame(left_frame)
        list_button_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(list_button_frame, text="➕ Nouvelle", command=self.new_card).pack(side='left', padx=(0, 5))
        ttk.Button(list_button_frame, text="🗑️ Supprimer", command=self.delete_card).pack(side='left', padx=(0, 5))
        ttk.Button(list_button_frame, text="🔄 Actualiser", command=self.refresh_card_list).pack(side='left')
        
        # Right panel - Card editor
        right_frame = ttk.LabelFrame(main_frame, text="✏️ Éditeur de Carte", padding=10)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Card form
        form_frame = ttk.Frame(right_frame)
        form_frame.pack(fill='x')
        
        # Name
        ttk.Label(form_frame, text="Nom:").grid(row=0, column=0, sticky='w', padx=(0, 5))
        self.nom_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.nom_var, width=30).grid(row=0, column=1, sticky='ew')
        
        # Type
        ttk.Label(form_frame, text="Type:").grid(row=1, column=0, sticky='w', padx=(0, 5), pady=(5, 0))
        self.type_var = tk.StringVar()
        type_combo = ttk.Combobox(form_frame, textvariable=self.type_var, 
                                  values=['Sort', 'Créature', 'Artefact', 'Enchantement'])
        type_combo.grid(row=1, column=1, sticky='ew', pady=(5, 0))
        
        # Rarity
        ttk.Label(form_frame, text="Rareté:").grid(row=2, column=0, sticky='w', padx=(0, 5), pady=(5, 0))
        self.rarete_var = tk.StringVar()
        rarete_combo = ttk.Combobox(form_frame, textvariable=self.rarete_var,
                                    values=['Commun', 'Inhabituel', 'Rare', 'Épique', 'Légendaire'])
        rarete_combo.grid(row=2, column=1, sticky='ew', pady=(5, 0))
        
        # Cost
        ttk.Label(form_frame, text="Coût:").grid(row=3, column=0, sticky='w', padx=(0, 5), pady=(5, 0))
        self.cout_var = tk.IntVar()
        ttk.Spinbox(form_frame, from_=0, to=20, textvariable=self.cout_var, width=30).grid(row=3, column=1, sticky='ew', pady=(5, 0))
        
        # Description
        ttk.Label(form_frame, text="Description:").grid(row=4, column=0, sticky='nw', padx=(0, 5), pady=(5, 0))
        self.description_text = tk.Text(form_frame, height=4, width=30)
        self.description_text.grid(row=4, column=1, sticky='ew', pady=(5, 0))
        
        # Image path
        ttk.Label(form_frame, text="Image:").grid(row=5, column=0, sticky='w', padx=(0, 5), pady=(5, 0))
        image_frame = ttk.Frame(form_frame)
        image_frame.grid(row=5, column=1, sticky='ew', pady=(5, 0))
        self.image_var = tk.StringVar()
        ttk.Entry(image_frame, textvariable=self.image_var).pack(side='left', fill='x', expand=True)
        ttk.Button(image_frame, text="📁", command=self.browse_image, width=3).pack(side='right', padx=(5, 0))
        
        form_frame.columnconfigure(1, weight=1)
        
        # Action buttons
        action_frame = ttk.Frame(right_frame)
        action_frame.pack(fill='x', pady=(20, 0))
        
        ttk.Button(action_frame, text="💾 Sauvegarder", command=self.save_card).pack(side='left', padx=(0, 5))
        ttk.Button(action_frame, text="📝 Formatage", command=self.open_text_formatter).pack(side='left', padx=(0, 5))
        ttk.Button(action_frame, text="📤 Exporter Lua", command=self.export_lua).pack(side='left')
        
        # Status bar
        self.status_var = tk.StringVar(value="Prêt")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief='sunken', anchor='w')
        status_bar.pack(side='bottom', fill='x')

    def refresh_card_list(self):
        """Refresh the card list."""
        self.card_listbox.delete(0, tk.END)
        cards = self.repo.list_cards()
        for card in cards:
            self.card_listbox.insert(tk.END, f"{card.nom} ({card.type})")
        self.status_var.set(f"Cartes chargées: {len(cards)}")

    def on_card_select(self, event):
        """Handle card selection."""
        selection = self.card_listbox.curselection()
        if selection:
            cards = self.repo.list_cards()
            if selection[0] < len(cards):
                self.current_card = cards[selection[0]]
                self.load_card_data()

    def load_card_data(self):
        """Load selected card data into form."""
        if not self.current_card:
            return
        
        self.nom_var.set(self.current_card.nom)
        self.type_var.set(self.current_card.type)
        self.rarete_var.set(self.current_card.rarete)
        self.cout_var.set(self.current_card.cout)
        self.description_text.delete('1.0', tk.END)
        self.description_text.insert('1.0', self.current_card.description)
        self.image_var.set(self.current_card.image_path)
        
        self.status_var.set(f"Carte chargée: {self.current_card.nom}")

    def new_card(self):
        """Create a new card."""
        self.current_card = Card()
        self.load_card_data()
        self.card_listbox.selection_clear(0, tk.END)
        self.status_var.set("Nouvelle carte créée")

    def save_card(self):
        """Save the current card."""
        if not self.current_card:
            self.new_card()
        
        # Update card data from form
        self.current_card.nom = self.nom_var.get()
        self.current_card.type = self.type_var.get()
        self.current_card.rarete = self.rarete_var.get()
        self.current_card.cout = self.cout_var.get()
        self.current_card.description = self.description_text.get('1.0', tk.END).strip()
        self.current_card.image_path = self.image_var.get()
        
        if not self.current_card.nom:
            messagebox.showerror("Erreur", "Le nom de la carte est requis!")
            return
        
        try:
            card_id = self.repo.save_card(self.current_card)
            self.current_card.id = card_id
            self.refresh_card_list()
            self.status_var.set(f"Carte sauvegardée: {self.current_card.nom}")
            messagebox.showinfo("Succès", "Carte sauvegardée avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {e}")

    def delete_card(self):
        """Delete the selected card."""
        if not self.current_card or not self.current_card.id:
            messagebox.showerror("Erreur", "Aucune carte sélectionnée!")
            return
        
        if messagebox.askyesno("Confirmation", f"Supprimer la carte '{self.current_card.nom}' ?"):
            try:
                self.repo.delete_card(self.current_card.id)
                self.refresh_card_list()
                self.new_card()
                self.status_var.set("Carte supprimée")
                messagebox.showinfo("Succès", "Carte supprimée avec succès!")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}")

    def browse_image(self):
        """Browse for image file."""
        filename = filedialog.askopenfilename(
            title="Sélectionner une image",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif"), ("Tous", "*.*")]
        )
        if filename:
            self.image_var.set(filename)

    def open_text_formatter(self):
        """Open the text formatting editor."""
        if not self.current_card:
            messagebox.showerror("Erreur", "Aucune carte sélectionnée!")
            return
        
        try:
            formatter = TextFormattingEditor(self.root, self.current_card, self.repo)
            self.root.wait_window(formatter.window)
            # Recharge la carte après formatage
            if self.current_card.id:
                self.current_card = self.repo.get_card(self.current_card.id)
                self.status_var.set("Formatage de texte mis à jour")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ouverture du formatage: {e}")

    def export_lua(self):
        """Export cards to Lua format."""
        try:
            exporter = LuaExporter(self.repo)
            lua_content = exporter.export_all_cards()
            
            filename = filedialog.asksaveasfilename(
                title="Exporter en Lua",
                defaultextension=".lua",
                filetypes=[("Fichiers Lua", "*.lua"), ("Tous", "*.*")]
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(lua_content)
                self.status_var.set(f"Export Lua sauvegardé: {filename}")
                messagebox.showinfo("Succès", f"Export Lua sauvegardé:\n{filename}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export: {e}")

    def run(self):
        """Run the application."""
        self.root.mainloop()

if __name__ == "__main__":
    app = SimpleCardEditor()
    app.run()
