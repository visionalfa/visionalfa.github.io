-- Medición anónima de visitas: sin cookies, sin datos personales.
create table if not exists public.visitas (
  id          bigint generated always as identity primary key,
  creada      timestamptz not null default now(),
  evento      text not null default 'vista',   -- vista | clic
  pagina      text,
  origen      text,                            -- instagram, google, whatsapp, directo, etc.
  dispositivo text,                            -- celular | compu
  sesion      text,                            -- id al azar por pestaña (no identifica a nadie)
  detalle     text
);
create index if not exists visitas_creada on public.visitas (creada);
alter table public.visitas enable row level security;
