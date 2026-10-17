-- Ebooks N.º 2, 3 y 4 de la colección.
insert into public.productos (id, nombre, tipo, precio, archivo, orden) values
  ('emprender-desde-cero',       'Emprender desde cero',       'ebook', 25000, 'emprender-desde-cero.html', 2),
  ('excel-para-emprendedores',   'Excel para emprendedores',   'ebook', 25000, 'excel-para-emprendedores.html', 3),
  ('precios-que-dejan-ganancia', 'Precios que dejan ganancia', 'ebook', 25000, 'precios-que-dejan-ganancia.html', 4)
on conflict (id) do nothing;
