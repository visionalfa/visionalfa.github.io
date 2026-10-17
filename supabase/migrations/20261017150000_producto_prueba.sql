-- Producto temporal para probar el circuito de pago con dinero real (se desactiva después de la prueba).
insert into public.productos (id, nombre, tipo, precio, archivo, orden, activo)
values ('prueba-e09ef813', 'Prueba de compra Visión Alfa', 'vitalicio', 100, null, 99, true)
on conflict (id) do nothing;
