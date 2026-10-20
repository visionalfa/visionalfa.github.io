-- El acompañamiento incluye 8 horas de reuniones en total (4 reuniones de 2 horas).
alter table public.servicios add column if not exists horas_incluidas int;
update public.servicios set
  horas_incluidas = 8,
  nombre = 'Tu web automatizada: acompañamiento de 8 horas',
  descripcion = 'Esta web la armé con inteligencia artificial en unas 8 horas. Te acompaño a hacer la tuya de la misma forma, con ventas, cobros, agenda y mails automáticos, resolviendo juntos cada paso con IA. Pagás una sola vez e incluye 8 horas de reuniones (4 encuentros de 2 horas) y acceso ilimitado a todos los ebooks.'
where id = 'web-automatizada';
