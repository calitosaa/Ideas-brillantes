#!/usr/bin/env python3
"""
Maia Settings - Configuración del Sistema Material 3 Expressive
Aplicación nativa de Maia OS construida con GTK4 y Libadwaita
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib, Gdk
import subprocess
import os

class MaiaSettings(Adw.Application):
    def __init__(self):
        super().__init__(application_id='org.maiaos.settings',
                        flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = SettingsWindow(application=self)
        win.present()

class SettingsWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.set_default_size(1000, 700)
        self.set_title("Configuración")
        
        # Header Bar
        header = Adw.HeaderBar()
        header.set_show_end_title_buttons(True)
        
        # Search entry
        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text("Buscar configuración...")
        self.search_entry.set_width_chars(30)
        self.search_entry.connect("changed", self.on_search)
        header.set_title_widget(self.search_entry)
        
        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.append(header)
        
        # Content with navigation sidebar
        content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        content_box.set_spacing(0)
        
        # Navigation sidebar
        nav_view = Adw.NavigationSplitView()
        nav_view.set_sidebar_width_fraction(0.25)
        nav_view.set_min_sidebar_width(200)
        nav_view.set_max_sidebar_width(300)
        
        # Sidebar list
        sidebar_list = Adw.PreferencesGroup()
        sidebar_list.add_css_class("navigation-sidebar")
        
        categories = [
            ("🎨 Apariencia", "appearance"),
            ("📱 Pantalla", "display"),
            ("🔊 Sonido", "sound"),
            ("🌐 Red e Internet", "network"),
            ("🔔 Notificaciones", "notifications"),
            ("⚡ Energía", "power"),
            ("🔒 Privacidad", "privacy"),
            ("👤 Usuarios", "users"),
            ("📦 Aplicaciones", "applications"),
            ("🔄 Actualizaciones", "updates"),
            ("ℹ️ Acerca de", "about"),
        ]
        
        for i, (name, id_) in enumerate(categories):
            row = Adw.ActionRow(title=name)
            row.set_activatable(True)
            row.add_css_class("nav-row")
            if i == 0:
                row.add_css_class("selected")
            row.connect("activated", self.on_category_selected, id_)
            sidebar_list.add(row)
        
        sidebar_scroll = Gtk.ScrolledWindow()
        sidebar_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sidebar_scroll.set_child(sidebar_list)
        
        # Main content area
        self.content_stack = Gtk.Stack()
        self.content_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.content_stack.set_transition_duration(300)
        
        # Create pages
        self.create_appearance_page()
        self.create_display_page()
        self.create_sound_page()
        self.create_network_page()
        self.create_notifications_page()
        self.create_power_page()
        self.create_privacy_page()
        self.create_users_page()
        self.create_applications_page()
        self.create_updates_page()
        self.create_about_page()
        
        content_box.append(sidebar_scroll)
        content_box.append(self.content_stack)
        
        main_box.append(content_box)
        self.set_content(main_box)
        
        # Show first page by default
        self.content_stack.set_visible_child_name("appearance")
    
    def on_category_selected(self, row, category_id):
        # Remove selected class from all rows
        group = row.get_parent()
        for child in group:
            if isinstance(child, Adw.ActionRow):
                child.remove_css_class("selected")
        
        # Add selected class to current row
        row.add_css_class("selected")
        
        # Switch to corresponding page
        self.content_stack.set_visible_child_name(category_id)
    
    def on_search(self, entry):
        search_text = entry.get_text().lower()
        # Implement search functionality
        print(f"Searching for: {search_text}")
    
    def create_appearance_page(self):
        """Página de Apariencia con tema Material 3"""
        page = Adw.ToolbarView()
        
        content = Adw.Clamp()
        content.set_maximum_size(800)
        
        prefs_group = Adw.PreferencesGroup()
        prefs_group.set_title("Tema")
        prefs_group.set_description("Personaliza la apariencia de Maia OS")
        
        # Dark/Light mode switch
        theme_row = Adw.ComboRow()
        theme_row.set_title("Modo oscuro")
        theme_row.set_subtitle("Elige entre modo claro, oscuro o automático")
        theme_model = Gtk.StringList()
        theme_model.append("Claro")
        theme_model.append("Oscuro")
        theme_model.append("Automático")
        theme_row.set_model(theme_model)
        theme_row.set_selected(2)  # Auto by default
        prefs_group.add(theme_row)
        
        # Accent color picker
        accent_row = Adw.ComboRow()
        accent_row.set_title("Color de acento")
        accent_row.set_subtitle("Color principal para botones y elementos destacados")
        accent_model = Gtk.StringList()
        colors = ["Violeta", "Azul", "Verde", "Ámbar", "Rojo", "Rosa"]
        for color in colors:
            accent_model.append(color)
        accent_row.set_model(accent_model)
        accent_row.set_selected(0)
        prefs_group.add(accent_row)
        
        # Wallpaper row
        wallpaper_row = Adw.ActionRow()
        wallpaper_row.set_title("Fondo de pantalla")
        wallpaper_row.set_subtitle("Cambiar fondo de escritorio")
        
        change_btn = Gtk.Button(label="Cambiar")
        change_btn.add_css_class("suggested-action")
        change_btn.connect("clicked", self.on_change_wallpaper)
        wallpaper_row.add_suffix(change_btn)
        wallpaper_row.set_activatable_widget(change_btn)
        prefs_group.add(wallpaper_row)
        
        # Icon theme
        icon_row = Adw.ComboRow()
        icon_row.set_title("Tema de iconos")
        icon_row.set_subtitle("Estilo de iconos del sistema")
        icon_model = Gtk.StringList()
        icons = ["Material You", "Classic", "Minimal", "Colorful"]
        for icon in icons:
            icon_model.append(icon)
        icon_row.set_model(icon_model)
        icon_row.set_selected(0)
        prefs_group.add(icon_row)
        
        content.set_child(prefs_group)
        page.set_content(content)
        self.content_stack.add_named(page, "appearance")
    
    def on_change_wallpaper(self, button):
        dialog = Gtk.FileDialog()
        dialog.set_title("Seleccionar fondo de pantalla")
        dialog.set_filters([Gtk.FileFilter.new()])
        dialog.get_filters()[0].add_pattern("*.jpg")
        dialog.get_filters()[0].add_pattern("*.png")
        dialog.get_filters()[0].add_pattern("*.jpeg")
        dialog.open(self, None, self.on_wallpaper_selected)
    
    def on_wallpaper_selected(self, dialog, result):
        try:
            file = dialog.open_finish(result)
            path = file.get_path()
            # Set wallpaper logic here
            print(f"Wallpaper changed to: {path}")
        except Exception as e:
            print(f"Error: {e}")
    
    def create_display_page(self):
        page = Adw.ToolbarView()
        content = Adw.Clamp()
        content.set_maximum_size(800)
        
        prefs_group = Adw.PreferencesGroup()
        prefs_group.set_title("Pantalla")
        
        # Resolution
        res_row = Adw.ComboRow()
        res_row.set_title("Resolución")
        res_model = Gtk.StringList()
        resolutions = ["1920×1080", "2560×1440", "3840×2160", "Nativa"]
        for res in resolutions:
            res_model.append(res)
        res_row.set_model(res_model)
        res_row.set_selected(3)
        prefs_group.add(res_row)
        
        # Scale
        scale_row = Adw.ComboRow()
        scale_row.set_title("Escala")
        scale_model = Gtk.StringList()
        scales = ["100%", "125%", "150%", "175%", "200%"]
        for scale in scales:
            scale_model.append(scale)
        scale_row.set_model(scale_model)
        scale_row.set_selected(0)
        prefs_group.add(scale_row)
        
        # Refresh rate
        refresh_row = Adw.ComboRow()
        refresh_row.set_title("Tasa de refresco")
        refresh_model = Gtk.StringList()
        rates = ["60Hz", "75Hz", "90Hz", "120Hz", "144Hz"]
        for rate in rates:
            refresh_model.append(rate)
        refresh_row.set_model(refresh_model)
        refresh_row.set_selected(0)
        prefs_group.add(refresh_row)
        
        # Night light
        night_light = Adw.SwitchRow()
        night_light.set_title("Luz nocturna")
        night_light.set_subtitle("Reducir luz azul por la noche")
        prefs_group.add(night_light)
        
        content.set_child(prefs_group)
        page.set_content(content)
        self.content_stack.add_named(page, "display")
    
    def create_sound_page(self):
        page = Adw.ToolbarView()
        content = Adw.Clamp()
        content.set_maximum_size(800)
        
        prefs_group = Adw.PreferencesGroup()
        prefs_group.set_title("Sonido")
        
        # Output volume
        output_vol = Adw.PreferencesRow()
        output_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        output_box.set_margin_start(12)
        output_box.set_margin_end(12)
        output_box.set_margin_top(12)
        output_box.set_margin_bottom(12)
        
        vol_label = Gtk.Label(label="Volumen de salida")
        vol_label.set_hexpand(True)
        vol_label.set_xalign(0)
        
        vol_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 5)
        vol_scale.set_value(75)
        vol_scale.set_size_request(200, -1)
        
        output_box.append(vol_label)
        output_box.append(vol_scale)
        output_vol.set_child(output_box)
        prefs_group.add(output_vol)
        
        # Input volume
        input_vol = Adw.PreferencesRow()
        input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        input_box.set_margin_start(12)
        input_box.set_margin_end(12)
        input_box.set_margin_top(12)
        input_box.set_margin_bottom(12)
        
        input_label = Gtk.Label(label="Volumen de entrada")
        input_label.set_hexpand(True)
        input_label.set_xalign(0)
        
        input_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 5)
        input_scale.set_value(50)
        input_scale.set_size_request(200, -1)
        
        input_box.append(input_label)
        input_box.append(input_scale)
        input_vol.set_child(input_box)
        prefs_group.add(input_vol)
        
        # Sound theme
        sound_theme = Adw.ComboRow()
        sound_theme.set_title("Tema de sonido")
        sound_model = Gtk.StringList()
        themes = ["Material", "Default", "Minimal", "Retro"]
        for theme in themes:
            sound_model.append(theme)
        sound_theme.set_model(sound_model)
        sound_theme.set_selected(0)
        prefs_group.add(sound_theme)
        
        content.set_child(prefs_group)
        page.set_content(content)
        self.content_stack.add_named(page, "sound")
    
    def create_network_page(self):
        page = Adw.ToolbarView()
        content = Adw.Clamp()
        content.set_maximum_size(800)
        
        prefs_group = Adw.PreferencesGroup()
        prefs_group.set_title("Red e Internet")
        
        # WiFi toggle
        wifi_row = Adw.SwitchRow()
        wifi_row.set_title("Wi-Fi")
        wifi_row.set_active(True)
        prefs_group.add(wifi_row)
        
        # Bluetooth toggle
        bt_row = Adw.SwitchRow()
        bt_row.set_title("Bluetooth")
        bt_row.set_active(True)
        prefs_group.add(bt_row)
        
        # Airplane mode
        airplane_row = Adw.SwitchRow()
        airplane_row.set_title("Modo avión")
        airplane_row.set_subtitle("Desactivar todas las conexiones inalámbricas")
        prefs_group.add(airplane_row)
        
        content.set_child(prefs_group)
        page.set_content(content)
        self.content_stack.add_named(page, "network")
    
    def create_notifications_page(self):
        page = Adw.ToolbarView()
        content = Adw.Clamp()
        content.set_maximum_size(800)
        
        prefs_group = Adw.PreferencesGroup()
        prefs_group.set_title("Notificaciones")
        
        # Notifications toggle
        notif_row = Adw.SwitchRow()
        notif_row.set_title("Notificaciones")
        notif_row.set_active(True)
        prefs_group.add(notif_row)
        
        # Do not disturb
        dnd_row = Adw.SwitchRow()
        dnd_row.set_title("No molestar")
        dnd_row.set_subtitle("Silenciar todas las notificaciones")
        prefs_group.add(dnd_row)
        
        # Lock screen notifications
        lock_row = Adw.SwitchRow()
        lock_row.set_title("Notificaciones en pantalla de bloqueo")
        lock_row.set_active(True)
        prefs_group.add(lock_row)
        
        content.set_child(prefs_group)
        page.set_content(content)
        self.content_stack.add_named(page, "notifications")
    
    def create_power_page(self):
        page = Adw.ToolbarView()
        content = Adw.Clamp()
        content.set_maximum_size(800)
        
        prefs_group = Adw.PreferencesGroup()
        prefs_group.set_title("Energía")
        
        # Power mode
        power_mode = Adw.ComboRow()
        power_mode.set_title("Modo de energía")
        power_model = Gtk.StringList()
        modes = ["Ahorro de energía", "Equilibrado", "Rendimiento"]
        for mode in modes:
            power_model.append(mode)
        power_mode.set_model(power_model)
        power_mode.set_selected(1)
        prefs_group.add(power_mode)
        
        # Battery percentage
        battery_row = Adw.SwitchRow()
        battery_row.set_title("Mostrar porcentaje de batería")
        battery_row.set_active(True)
        prefs_group.add(battery_row)
        
        # Auto suspend
        suspend_row = Adw.SwitchRow()
        suspend_row.set_title("Suspender automáticamente")
        suspend_row.set_subtitle("Suspender después de 15 minutos de inactividad")
        suspend_row.set_active(True)
        prefs_group.add(suspend_row)
        
        content.set_child(prefs_group)
        page.set_content(content)
        self.content_stack.add_named(page, "power")
    
    def create_privacy_page(self):
        page = Adw.ToolbarView()
        content = Adw.Clamp()
        content.set_maximum_size(800)
        
        prefs_group = Adw.PreferencesGroup()
        prefs_group.set_title("Privacidad")
        
        # Location
        location_row = Adw.SwitchRow()
        location_row.set_title("Servicios de ubicación")
        prefs_group.add(location_row)
        
        # Usage stats
        usage_row = Adw.SwitchRow()
        usage_row.set_title("Enviar estadísticas de uso")
        usage_row.set_active(False)
        prefs_group.add(usage_row)
        
        # App permissions
        perms_row = Adw.ActionRow()
        perms_row.set_title("Permisos de aplicaciones")
        perms_row.set_subtitle("Gestionar permisos de cámara, micrófono, etc.")
        perms_row.set_activatable(True)
        prefs_group.add(perms_row)
        
        content.set_child(prefs_group)
        page.set_content(content)
        self.content_stack.add_named(page, "privacy")
    
    def create_users_page(self):
        page = Adw.ToolbarView()
        content = Adw.Clamp()
        content.set_maximum_size(800)
        
        prefs_group = Adw.PreferencesGroup()
        prefs_group.set_title("Usuarios")
        
        # Current user
        user_row = Adw.ActionRow()
        user_row.set_title("Usuario Actual")
        user_row.set_subtitle("usuario@maia-os")
        
        avatar = Gtk.Image.new_from_icon_name("avatar-default-symbolic")
        avatar.set_pixel_size(48)
        avatar.add_css_class("circular")
        user_row.add_prefix(avatar)
        
        change_btn = Gtk.Button(label="Cambiar")
        change_btn.add_css_class("suggested-action")
        user_row.add_suffix(change_btn)
        user_row.set_activatable_widget(change_btn)
        prefs_group.add(user_row)
        
        content.set_child(prefs_group)
        page.set_content(content)
        self.content_stack.add_named(page, "users")
    
    def create_applications_page(self):
        page = Adw.ToolbarView()
        content = Adw.Clamp()
        content.set_maximum_size(800)
        
        prefs_group = Adw.PreferencesGroup()
        prefs_group.set_title("Aplicaciones")
        
        # Default apps
        browser_row = Adw.ComboRow()
        browser_row.set_title("Navegador web")
        browser_model = Gtk.StringList()
        browsers = ["Maia Browser", "Firefox", "Chrome", "Brave"]
        for browser in browsers:
            browser_model.append(browser)
        browser_row.set_model(browser_model)
        browser_row.set_selected(0)
        prefs_group.add(browser_row)
        
        content.set_child(prefs_group)
        page.set_content(content)
        self.content_stack.add_named(page, "applications")
    
    def create_updates_page(self):
        page = Adw.ToolbarView()
        content = Adw.Clamp()
        content.set_maximum_size(800)
        
        prefs_group = Adw.PreferencesGroup()
        prefs_group.set_title("Actualizaciones")
        
        # Check for updates button
        check_row = Adw.ActionRow()
        check_row.set_title("Buscar actualizaciones")
        check_row.set_subtitle("Última comprobación: Hoy")
        
        check_btn = Gtk.Button(label="Comprobar ahora")
        check_btn.add_css_class("suggested-action")
        check_btn.connect("clicked", self.on_check_updates)
        check_row.add_suffix(check_btn)
        check_row.set_activatable_widget(check_btn)
        prefs_group.add(check_row)
        
        # Auto update
        auto_update = Adw.SwitchRow()
        auto_update.set_title("Actualizar automáticamente")
        auto_update.set_subtitle("Descargar e instalar actualizaciones en segundo plano")
        auto_update.set_active(True)
        prefs_group.add(auto_update)
        
        content.set_child(prefs_group)
        page.set_content(content)
        self.content_stack.add_named(page, "updates")
    
    def on_check_updates(self, button):
        button.set_label("Comprobando...")
        button.set_sensitive(False)
        # Simulate update check
        GLib.timeout_add(2000, lambda: button.set_label("Comprobar ahora") or button.set_sensitive(True))
    
    def create_about_page(self):
        page = Adw.ToolbarView()
        content = Adw.Clamp()
        content.set_maximum_size(800)
        
        prefs_group = Adw.PreferencesGroup()
        prefs_group.set_title("Acerca de Maia OS")
        
        # Logo
        logo_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        logo_box.set_margin_start(20)
        logo_box.set_margin_end(20)
        logo_box.set_margin_top(30)
        logo_box.set_margin_bottom(30)
        
        logo = Gtk.Image.new_from_icon_name("org.maiaos.logo")
        logo.set_pixel_size(128)
        logo_box.append(logo)
        
        title = Gtk.Label(label="Maia OS")
        title.add_css_class("title-1")
        logo_box.append(title)
        
        version = Gtk.Label(label="Versión 1.0 Stable")
        version.add_css_class("body")
        version.set_opacity(0.7)
        logo_box.append(version)
        
        prefs_group.add(logo_box)
        
        # Info rows
        info_rows = [
            ("Basado en", "Debian 12 Bookworm"),
            ("Entorno", "GNOME 45+ Material 3"),
            ("Kernel", "Linux 6.8+"),
            ("Arquitectura", "x86_64"),
        ]
        
        for title, value in info_rows:
            row = Adw.ActionRow()
            row.set_title(title)
            subtitle = Gtk.Label(label=value)
            subtitle.set_opacity(0.7)
            row.add_suffix(subtitle)
            prefs_group.add(row)
        
        # Credits
        credits_row = Adw.ActionRow()
        credits_row.set_title("Créditos")
        credits_row.set_subtitle("Diseñado con Material 3 Expressive")
        prefs_group.add(credits_row)
        
        content.set_child(prefs_group)
        page.set_content(content)
        self.content_stack.add_named(page, "about")

def main():
    app = MaiaSettings()
    app.run(None)

if __name__ == "__main__":
    main()
