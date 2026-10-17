-- La reserva se confirma recién cuando Mercado Pago aprueba el pago.
-- pendiente: el horario queda guardado unos minutos mientras la persona paga.
-- pagada_sin_turno: el pago llegó tarde y alguien más tomó el horario (hay que reprogramar o devolver).
alter table public.reservas drop constraint if exists reservas_estado_check;
alter table public.reservas add constraint reservas_estado_check
  check (estado in ('pendiente', 'confirmada', 'cancelada', 'vencida', 'pagada_sin_turno'));
alter table public.reservas alter column estado set default 'pendiente';
alter table public.reservas add column if not exists vence   timestamptz;
alter table public.reservas add column if not exists pago_id text;
alter table public.reservas add column if not exists monto   numeric(12, 2);

drop index if exists public.reservas_turno_unico;
create unique index reservas_turno_unico on public.reservas (inicio) where estado in ('pendiente', 'confirmada');
