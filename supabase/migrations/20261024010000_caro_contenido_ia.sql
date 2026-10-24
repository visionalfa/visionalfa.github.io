-- Caro se suma al equipo: diseño y contenido para redes con IA. Agenda propia, lunes a viernes de 17 a 20.
insert into public.servicios (id, agenda, profesional, nombre, descripcion, precio, duracion, hora_desde, hora_hasta, modalidad, incluye_ebook, orden) values
  ('contenido-ia', 'caro', 'Caro', 'Asesoría: tu contenido con IA',
   'Te enseña a crear los estáticos y videos de tus redes con Claude, Midjourney y Magnific. Te llevás tu flujo de trabajo y tus prompts listos para usar.', 60000, 1, 17, 20, 'Videollamada individual', null, 6),
  ('contenido-mensual', 'caro', 'Caro', 'Contenido mensual listo para publicar',
   'Calendario del mes y 8 piezas a convenir. Se paga por mes: reservás una reunión de 1 hora para definir el calendario y las piezas, y cada mes reservás la del mes siguiente.', 250000, 1, 17, 20, 'Videollamada individual', null, 7)
on conflict (id) do nothing;
