-- Silvana Cuevas se suma al equipo: recursos humanos. Lunes, miércoles y viernes de 13 a 17.
insert into public.servicios (id, agenda, profesional, nombre, descripcion, precio, duracion, hora_desde, hora_hasta, dias, modalidad, incluye_ebook, orden) values
  ('recursos-humanos', 'silvana', 'Silvana Cuevas', 'Asesoría en recursos humanos',
   'Para ordenar lo que tiene que ver con tu gente: cómo buscar y elegir a quién sumar, cómo organizar tareas y cómo acompañar al equipo.', 60000, 1, 13, 17, '{1,3,5}', 'Videollamada individual', null, 8)
on conflict (id) do nothing;
