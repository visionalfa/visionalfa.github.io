-- Mail de cada profesional para avisarle de sus reservas. Privado: sin políticas, solo lo leen las funciones.
create table if not exists public.agenda_contactos (
  agenda text primary key,
  email  text not null
);
alter table public.agenda_contactos enable row level security;
