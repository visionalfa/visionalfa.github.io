-- Servicios del equipo: cada uno con su agenda, horario, duración y precio.
create extension if not exists btree_gist;

create table if not exists public.servicios (
  id            text primary key,
  agenda        text not null,              -- de quién es la agenda (los turnos no se pisan dentro de una misma agenda)
  profesional   text not null,
  nombre        text not null,
  descripcion   text,
  precio        numeric(12, 2) not null,
  duracion      int  not null default 1,    -- horas
  hora_desde    int  not null,              -- hora de Argentina en que arranca la franja
  hora_hasta    int  not null,              -- hora en que termina la franja
  dias          int[] not null default '{1,2,3,4,5}', -- 0 domingo … 6 sábado
  modalidad     text not null default 'Videollamada individual',
  incluye_ebook text,                       -- id de producto que se habilita al pagar
  activo        boolean not null default true,
  orden         int not null default 0
);
alter table public.servicios enable row level security;
drop policy if exists "servicios visibles" on public.servicios;
create policy "servicios visibles" on public.servicios for select using (activo);

insert into public.servicios (id, agenda, profesional, nombre, descripcion, precio, duracion, hora_desde, hora_hasta, modalidad, incluye_ebook, orden) values
  ('asesoria', 'florentina', 'Florentina Cecchini', 'Asesoría para tu emprendimiento',
   'Revisamos juntos tu emprendimiento y armamos los próximos pasos: ventas, precios, redes e IA.', 60000, 1, 17, 20, 'Videollamada individual', null, 1),
  ('web-automatizada', 'florentina', 'Florentina Cecchini', 'Tu web automatizada: 2 horas + ebook',
   'Te enseño a hacer una web como esta, con ventas, cobros y mails automáticos. Incluye el ebook "Tu web de ventas con IA".', 150000, 2, 17, 20, 'Videollamada individual', 'tu-web-de-ventas-con-ia', 2),
  ('orientacion-vocacional', 'carla', 'Carla Tanzi', 'Orientación vocacional',
   'Sesión semanal de 1 hora. El proceso completo es de 6 a 8 sesiones.', 60000, 1, 9, 12, 'Videollamada individual', null, 3),
  ('coaching-equipos', 'marcelo', 'Marcelo De los Santos', 'Coaching ontológico para equipos',
   'Sesión grupal para equipos de trabajo: comunicación, liderazgo y conversaciones que destraban resultados.', 60000, 1, 9, 12, 'Videollamada grupal', null, 4),
  ('asuntos-publicos', 'juliana', 'Juliana Cecchini', 'Asuntos públicos e inversión social',
   'Relación con comunidades, gobiernos y la industria del oil & gas; diseño de programas de inversión social.', 60000, 1, 9, 12, 'Videollamada', null, 5)
on conflict (id) do nothing;

-- Reservas: a qué servicio y agenda corresponden, y cuándo terminan.
alter table public.reservas add column if not exists servicio_id text references public.servicios (id);
alter table public.reservas add column if not exists agenda text;
alter table public.reservas add column if not exists fin timestamptz;
update public.reservas set servicio_id = 'asesoria' where servicio_id is null;
update public.reservas set agenda = 'florentina' where agenda is null;
update public.reservas set fin = inicio + interval '1 hour' where fin is null;
alter table public.reservas alter column servicio_id set not null;
alter table public.reservas alter column agenda set not null;
alter table public.reservas alter column fin set not null;

-- Dentro de una misma agenda dos turnos activos no se pueden superponer.
drop index if exists public.reservas_turno_unico;
alter table public.reservas drop constraint if exists reservas_sin_superposicion;
alter table public.reservas add constraint reservas_sin_superposicion
  exclude using gist (agenda with =, tstzrange(inicio, fin) with &&)
  where (estado in ('pendiente', 'confirmada'));

-- Días bloqueados por agenda (agenda vacía = todas).
alter table public.dias_bloqueados add column if not exists agenda text not null default '';
alter table public.dias_bloqueados drop constraint if exists dias_bloqueados_pkey;
alter table public.dias_bloqueados add primary key (fecha, agenda);
