from __future__ import print_function

import sys

import psutil


if not (psutil.LINUX or psutil.MACOS or psutil.WINDOWS):
    sys.exit("platform not supported")


def convert_bytes(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


def main():
    ad_pids = []
    procs = []
    for p in psutil.process_iter():
        with p.oneshot():
            try:
                mem = p.memory_full_info()
                info = p.as_dict(["cmdline", "username"])
            except psutil.AccessDenied:
                ad_pids.append(p.pid)
            except psutil.NoSuchProcess:
                pass
            else:
                p._uss = mem.uss
                p._rss = mem.rss
                if not p._uss:
                    continue
                p._pss = getattr(mem, "pss", "")
                p._swap = getattr(mem, "swap", "")
                p._info = info
                procs.append(p)

    templ = "%-7s %-7s %7s %7s %7s %7s %-25s %7s"
    print(templ % ("PID", "User", "USS", "PSS", "Swap", "RSS", "NAME", "Cmdline"))
    print("=" * 100)

    total = [0, 0, 0, 0]
    process_map = {}
    for p in procs:
        name = p.name()
        if name in process_map:
            process_map[name][0] += p._uss
            process_map[name][1] += p._rss
        else:
            process_map[name] = [p._uss, p._rss, p]

        total[0] += p._uss
        total[1] += p._pss if p._pss else 0
        total[2] += p._swap if p._swap else 0
        total[3] += p._rss

    process_map = dict(
        sorted(process_map.items(), key=lambda x: x[1][0], reverse=True))
    for k, v in process_map.items():
        uss, rss, p = v
        cmd = " ".join(p._info["cmdline"])[:80] if p._info["cmdline"] else ""
        line = templ % (
            p.pid,
            p._info["username"][:7] if p._info["username"] else "",
            convert_bytes(uss),
            convert_bytes(p._pss) if p._pss != "" else "",
            convert_bytes(p._swap) if p._swap != "" else "",
            convert_bytes(rss),
            k,
            cmd,
        )
        print(line)
    print(templ % ("", "",
                   convert_bytes(total[0]),
                   convert_bytes(total[1]),
                   convert_bytes(total[2]),
                   convert_bytes(total[3]),
                   "", ""))

    if ad_pids:
        print("warning: access denied for %s pids" % (len(ad_pids)),
              file=sys.stderr)


if __name__ == '__main__':
    sys.exit(main())
