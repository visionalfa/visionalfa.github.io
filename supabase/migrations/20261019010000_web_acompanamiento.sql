-- "Tu web automatizada" pasa a ser un acompañamiento: un solo pago de $500.000,
-- todas las reuniones que hagan falta y acceso ilimitado a todos los ebooks.
alter table public.servicios add column if not exists reuniones_incluidas boolean not null default false;

update public.servicios set
  nombre = 'Tu web automatizada: acompañamiento completo',
  descripcion = 'Te acompaño a hacer una web como esta, con ventas, cobros, agenda y mails automáticos. Pagás una sola vez y tenés todas las reuniones que hagan falta hasta que tu web quede funcionando, más acceso ilimitado a todos los ebooks.',
  precio = 500000,
  incluye_ebook = 'vitalicio',
  reuniones_incluidas = true
where id = 'web-automatizada';
