-- Ebook N.º 7 de la colección.
insert into public.productos (id, nombre, tipo, precio, archivo, orden) values
  ('tu-web-de-ventas-con-ia', 'Tu web de ventas con IA', 'ebook', 25000, 'tu-web-de-ventas-con-ia.html', 7)
on conflict (id) do nothing;
