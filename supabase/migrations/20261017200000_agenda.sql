-- Agenda de asesorías: turnos de 1 hora, lunes a viernes de 17 a 20 (hora de Argentina).
create table if not exists public.reservas (
  id        uuid primary key default gen_random_uuid(),
  inicio    timestamptz not null,
  nombre    text not null,
  email     text not null,
  whatsapp  text,
  tema      text,
  estado    text not null default 'confirmada' check (estado in ('confirmada', 'cancelada')),
  token     uuid not null default gen_random_uuid(),
  creada    timestamptz not null default now()
);
-- Un solo turno confirmado por horario.
create unique index if not exists reservas_turno_unico on public.reservas (inicio) where estado = 'confirmada';
create index if not exists reservas_email on public.reservas (email);
alter table public.reservas enable row level security;

-- Días sin atención (feriados, vacaciones).
create table if not exists public.dias_bloqueados (
  fecha  date primary key,
  motivo text
);
alter table public.dias_bloqueados enable row level security;
-- Sin políticas: solo las funciones del servidor leen y escriben estas tablas.
