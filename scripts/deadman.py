#!/usr/bin/env python3
"""Dead man's switch — the human's acknowledgement age as an arousal ceiling.

Every other stop condition in the loop is keyed to the agent or to the world.
This one is keyed to the human who is meant to be reading. A file holds the
timestamp of the last *human act*; at the top of each tick the loop reads its
age and caps what it may do:

  ack age        ceiling       exit
  < 1 day        full          0     act; outbound still needs the human's word
  1 – 7 days     read-only     1     sense, draft, write memory; nothing outbound
  7 – 30 days    memory-only   2     consolidate; no new drafts
  > 30 days      deep-sleep    3     no timer; wake only on the human
  unknown        deep-sleep    3     missing / unreadable / future = fails closed

Rules the script enforces:
  - An ack is an act, not a receipt. Only a human input channel may write it.
    In hook mode, only a UserPromptSubmit event records an ack. The `ack`
    command refuses to run inside an agent context (CLAUDECODE set) unless the
    call is that hook — otherwise the loop would acknowledge itself.
  - Unknown fails closed: no file, bad timestamp, or a timestamp in the future
    all read as the deepest level, with the reason printed.
  - Degrade, don't halt: the script never blocks a hook (hook mode exits 0);
    it reports the ceiling and leaves the tick to honour it.

Ack file: $DEADMAN_ACK, else ~/.deadman-ack  (one line: ts_utc<TAB>source)
Thresholds: $DEADMAN_DAYS="1,7,30" (days for read-only / memory-only / deep-sleep)

    deadman.py                       # hook mode, reads Claude Code hook JSON on stdin:
                                     #   UserPromptSubmit -> records an ack
                                     #   SessionStart     -> prints the ceiling line
    deadman.py ack --source <s>      # record a human act from a non-hook channel
    deadman.py ceiling [--json]      # print the ceiling; exit code = level (0..3)
"""
import sys, os, json, datetime

ACK = os.path.expanduser(os.environ.get('DEADMAN_ACK', '~/.deadman-ack'))
FMT = '%Y-%m-%dT%H:%M:%SZ'
LEVELS = ['full', 'read-only', 'memory-only', 'deep-sleep']
FUTURE_TOLERANCE = datetime.timedelta(minutes=5)


def thresholds():
    raw = os.environ.get('DEADMAN_DAYS', '1,7,30')
    try:
        d = [float(x) for x in raw.split(',')]
        if len(d) != 3 or d != sorted(d) or d[0] <= 0:
            raise ValueError
        return d
    except ValueError:
        return [1.0, 7.0, 30.0]


def now():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)


def write_ack(source):
    os.makedirs(os.path.dirname(ACK) or '.', exist_ok=True)
    tmp = ACK + '.tmp'
    with open(tmp, 'w') as f:
        f.write(f"{now().strftime(FMT)}\t{source}\n")
    os.replace(tmp, ACK)


def read_ack():
    """Return (ts, source) or (None, reason). Never raises."""
    try:
        with open(ACK) as f:
            line = f.readline().strip()
    except FileNotFoundError:
        return None, 'no ack file'
    except OSError as e:
        return None, f'ack file unreadable ({e.__class__.__name__})'
    if not line:
        return None, 'ack file empty'
    ts_s, _, source = line.partition('\t')
    try:
        ts = datetime.datetime.strptime(ts_s, FMT).replace(tzinfo=datetime.timezone.utc)
    except ValueError:
        return None, f'ack timestamp unparsable: {ts_s!r}'
    if ts > now() + FUTURE_TOLERANCE:
        return None, f'ack timestamp in the future: {ts_s}'
    return ts, source or 'unknown'


def human_age(delta):
    s = int(delta.total_seconds())
    if s < 60:
        return f'{s}s'
    if s < 3600:
        return f'{s // 60}m'
    if s < 86400:
        return f'{s // 3600}h{(s % 3600) // 60:02d}'
    return f'{s // 86400}d{(s % 86400) // 3600:02d}h'


def ceiling():
    """Return dict: level (0..3), name, age_seconds or None, reason, source."""
    ts, info = read_ack()
    if ts is None:
        return {'level': 3, 'name': LEVELS[3], 'age_seconds': None,
                'reason': f'fails closed: {info}', 'source': None}
    age = now() - ts
    days = age.total_seconds() / 86400
    t = thresholds()
    level = 0 if days < t[0] else 1 if days < t[1] else 2 if days < t[2] else 3
    return {'level': level, 'name': LEVELS[level], 'age_seconds': int(age.total_seconds()),
            'reason': f'last human ack {human_age(age)} ago', 'source': info}


def ceiling_line(c):
    src = f' via {c["source"]}' if c.get('source') else ''
    return f'deadman: {c["name"]} — {c["reason"]}{src}'


def cmd_ceiling(args):
    c = ceiling()
    if '--json' in args:
        print(json.dumps(c))
    else:
        print(ceiling_line(c))
    return c['level']


def cmd_ack(args):
    source = None
    if '--source' in args:
        i = args.index('--source')
        source = args[i + 1] if i + 1 < len(args) else None
    if not source:
        print('deadman: ack needs --source <human channel>', file=sys.stderr)
        return 2
    if os.environ.get('CLAUDECODE'):
        print('deadman: refused — an ack must come from the human channel, '
              'not from inside the agent (CLAUDECODE is set). Bind the '
              'UserPromptSubmit hook instead.', file=sys.stderr)
        return 2
    write_ack(source)
    print(ceiling_line(ceiling()))
    return 0


def hook_mode():
    """Claude Code hook: stdin JSON. Never blocks; always exits 0."""
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    event = payload.get('hook_event_name', '')
    try:
        if event == 'UserPromptSubmit':
            write_ack('prompt')
        elif event == 'SessionStart':
            print(ceiling_line(ceiling()))
    except Exception:
        pass
    return 0


def main(argv):
    if not argv:
        return hook_mode()
    cmd, args = argv[0], argv[1:]
    if cmd == 'ceiling':
        return cmd_ceiling(args)
    if cmd == 'ack':
        return cmd_ack(args)
    if cmd in ('-h', '--help', 'help'):
        print(__doc__)
        return 0
    print(f'deadman: unknown command {cmd!r}; see --help', file=sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
