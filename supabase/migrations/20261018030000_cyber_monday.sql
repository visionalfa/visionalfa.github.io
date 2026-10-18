-- Precios de oferta con fecha: el checkout los aplica solo dentro de la ventana.
alter table public.productos add column if not exists precio_oferta numeric(12, 2);
alter table public.productos add column if not exists oferta_desde  timestamptz;
alter table public.productos add column if not exists oferta_hasta  timestamptz;

-- Cyber Monday 2026: lunes 2 al miércoles 4 de noviembre (hora de Argentina).
update public.productos
   set precio_oferta = 17500, oferta_desde = '2026-11-02 00:00:00-03', oferta_hasta = '2026-11-04 23:59:59-03'
 where tipo = 'ebook' and id not like 'prueba%';
update public.productos
   set precio_oferta = 60000, oferta_desde = '2026-11-02 00:00:00-03', oferta_hasta = '2026-11-04 23:59:59-03'
 where id = 'vitalicio';
