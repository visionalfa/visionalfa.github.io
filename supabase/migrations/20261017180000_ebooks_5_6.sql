-- Ebooks N.º 5 y 6 de la colección.
insert into public.productos (id, nombre, tipo, precio, archivo, orden) values
  ('vender-por-whatsapp-e-instagram', 'Vender por WhatsApp e Instagram', 'ebook', 25000, 'vender-por-whatsapp-e-instagram.html', 5),
  ('como-venderle-a-comercios',       'Cómo venderle a comercios',       'ebook', 25000, 'como-venderle-a-comercios.html', 6)
on conflict (id) do nothing;
