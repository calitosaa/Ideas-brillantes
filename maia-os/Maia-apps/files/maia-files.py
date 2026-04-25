#!/usr/bin/env python3
"""
Maia Files - Gestor de Archivos Material 3 Expressive
Aplicación nativa de Maia OS construida con GTK4 y Libadwaita
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib, Gdk, Pango
import os
from pathlib import Path

class MaiaFiles(Adw.Application):
    def __init__(self):
        super().__init__(application_id='org.maiaos.files',
                        flags=Gio.ApplicationFlags.FLAGS_NONE)
        
        self.current_path = Path.home()
        self.history = []
        self.history_index = -1
        
    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = MaiaWindow(application=self)
        win.present()

class MaiaWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.set_default_size(1200, 800)
        self.set_title("Maia Files")
        
        # Header Bar
        header = Adw.HeaderBar()
        header.set_show_end_title_buttons(True)
        
        # Title widget
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        title_label = Gtk.Label(label="📁 Maia Files")
        title_label.add_css_class("title")
        title_box.append(title_label)
        header.set_title_widget(title_box)
        
        # Navigation buttons
        self.back_btn = Gtk.Button(icon_name="go-previous-symbolic")
        self.back_btn.connect("clicked", self.on_back)
        header.pack_start(self.back_btn)
        
        self.forward_btn = Gtk.Button(icon_name="go-next-symbolic")
        self.forward_btn.connect("clicked", self.on_forward)
        header.pack_start(self.forward_btn)
        
        # Search button
        search_btn = Gtk.Button(icon_name="system-search-symbolic")
        search_btn.connect("clicked", self.on_search)
        header.pack_end(search_btn)
        
        # Menu button
        menu_btn = Gtk.MenuButton(icon_name="open-menu-symbolic")
        menu = Gio.Menu()
        menu.append("Preferencias", "app.preferences")
        menu.append("Acerca de", "app.about")
        menu_btn.set_menu_model(menu)
        header.pack_end(menu_btn)
        
        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.append(header)
        
        # Content area with sidebar
        content_paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        content_paned.set_position(250)
        content_paned.set_wide_handle(True)
        
        # Sidebar
        sidebar = self.create_sidebar()
        content_paned.set_start_child(sidebar)
        
        # Main view
        main_view = self.create_main_view()
        content_paned.set_end_child(main_view)
        
        main_box.append(content_paned)
        
        # Status bar
        status_bar = Gtk.Label(label="0 elementos")
        status_bar.add_css_class("statusbar")
        status_bar.set_margin_top(6)
        status_bar.set_margin_bottom(6)
        main_box.append(status_bar)
        
        self.set_content(main_box)
        
        # Load initial directory
        self.navigate_to(Path.home())
    
    def create_sidebar(self):
        """Crear barra lateral con accesos rápidos"""
        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar.set_size_request(250, -1)
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        listbox = Gtk.ListBox()
        listbox.add_css_class("navigation-sidebar")
        
        # Quick accesses
        items = [
            ("🏠 Inicio", str(Path.home())),
            ("🖥️ Escritorio", str(Path.home() / "Desktop")),
            ("📄 Documentos", str(Path.home() / "Documents")),
            ("⬇️ Descargas", str(Path.home() / "Downloads")),
            ("🎵 Música", str(Path.home() / "Music")),
            ("🖼️ Imágenes", str(Path.home() / "Pictures")),
            ("🎬 Videos", str(Path.home() / "Videos")),
            ("🗑️ Papelera", "trash://"),
        ]
        
        for name, path in items:
            row = Adw.ActionRow(title=name)
            row.set_activatable(True)
            row.connect("activated", self.on_sidebar_item_clicked, path)
            listbox.append(row)
        
        scroll.set_child(listbox)
        sidebar.append(scroll)
        
        return sidebar
    
    def create_main_view(self):
        """Crear vista principal con grid de archivos"""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # Flow box for file grid
        self.flow_box = Gtk.FlowBox()
        self.flow_box.set_homogeneous(True)
        self.flow_box.set_min_children_per_line(4)
        self.flow_box.set_max_children_per_line(8)
        self.flow_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.set_child(self.flow_box)
        
        main_box.append(scroll)
        
        return main_box
    
    def navigate_to(self, path):
        """Navegar a un directorio"""
        try:
            if str(path) == "trash://":
                # Implementar papelera
                return
            
            path = Path(path)
            if not path.exists():
                return
            
            self.current_path = path
            self.update_flowbox()
            self.update_history(path)
            
            # Update window title
            self.set_title(f"Maia Files - {path}")
            
        except Exception as e:
            print(f"Error navigating: {e}")
    
    def update_flowbox(self):
        """Actualizar grid de archivos"""
        # Clear existing items
        child = self.flow_box.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.flow_box.remove(child)
            child = next_child
        
        try:
            items = list(self.current_path.iterdir())
        except PermissionError:
            return
        
        # Sort: directories first, then files
        items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
        
        for item in items:
            card = self.create_file_card(item)
            self.flow_box.append(card)
        
        # Update status bar
        status_label = f"{len(items)} elementos"
        # Find and update status bar (simplified)
    
    def create_file_card(self, path):
        """Crear tarjeta de archivo/carpetas con Material 3"""
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        card.set_margin_start(8)
        card.set_margin_end(8)
        card.set_margin_top(8)
        card.set_margin_bottom(8)
        
        # Icon based on type
        icon_label = Gtk.Label()
        if path.is_dir():
            icon_label.set_label("📁")
        else:
            ext = path.suffix.lower()
            icons = {
                '.pdf': '📄', '.doc': '📝', '.docx': '📝',
                '.xls': '📊', '.xlsx': '📊',
                '.jpg': '🖼️', '.png': '🖼️', '.gif': '🖼️',
                '.mp3': '🎵', '.wav': '🎵',
                '.mp4': '🎬', '.avi': '🎬',
                '.py': '🐍', '.js': '📜', '.html': '🌐',
            }
            icon_label.set_label(icons.get(ext, '📄'))
        icon_label.set_scale(3)
        
        # Name label
        name_label = Gtk.Label(label=path.name)
        name_label.set_ellipsize(Pango.EllipsizeMode.END)
        name_label.set_max_width_chars(15)
        name_label.set_xalign(0.5)
        name_label.set_margin_top(8)
        
        card.append(icon_label)
        card.append(name_label)
        
        # Make clickable
        gesture = Gtk.GestureClick()
        gesture.connect("pressed", self.on_file_clicked, path)
        card.add_controller(gesture)
        
        return card
    
    def on_file_clicked(self, gesture, n_press, x, y, path):
        """Manejar click en archivo/carpeta"""
        if path.is_dir():
            self.navigate_to(path)
        else:
            # Open file with default application
            Gtk.show_uri(None, path.as_uri(), Gdk.CURRENT_TIME)
    
    def on_sidebar_item_clicked(self, row, path):
        """Manejar click en item de sidebar"""
        self.navigate_to(path)
    
    def update_history(self, path):
        """Actualizar historial de navegación"""
        # Trim forward history
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        
        self.history.append(str(path))
        self.history_index = len(self.history) - 1
        
        # Update button sensitivity
        self.back_btn.set_sensitive(self.history_index > 0)
        self.forward_btn.set_sensitive(self.history_index < len(self.history) - 1)
    
    def on_back(self, btn):
        """Navegar atrás"""
        if self.history_index > 0:
            self.history_index -= 1
            self.navigate_to(Path(self.history[self.history_index]))
    
    def on_forward(self, btn):
        """Navegar adelante"""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.navigate_to(Path(self.history[self.history_index]))
    
    def on_search(self, btn):
        """Mostrar búsqueda"""
        # Implement search dialog
        pass

def main():
    app = MaiaFiles()
    app.run(None)

if __name__ == '__main__':
    main()
